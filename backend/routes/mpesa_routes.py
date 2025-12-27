from flask import Blueprint, request, jsonify
import json
from services.mpesa_service import MpesaService
from services.config import MpesaConfig

mpesa_bp = Blueprint("mpesa", __name__, url_prefix="/payments")


# ============= PAYMENT ENDPOINTS =============

@mpesa_bp.route('/stk-push', methods=['POST'])
def stk_push():
    """
    Initiate STK Push payment (Lipa Na M-Pesa)
    Request: {"phone": "254712345678", "amount": 100}
    """
    try:
        data = request.get_json()
        phone = data.get("phone")
        amount = data.get("amount")

        if not phone or not amount:
            return jsonify({
                "success": False,
                "error": "phone and amount are required"
            }), 400

        response = MpesaService.stk_push(
            phone_number=phone,
            amount=amount
        )

        return jsonify({
            "success": True,
            "response": response
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@mpesa_bp.route('/c2b/simulate', methods=['POST'])
def simulate_c2b():
    """
    Simulate C2B payment (Sandbox only)
    Request: {"phone": "254712345678", "amount": 100, "reference": "INV001"}
    """
    try:
        data = request.get_json()
        amount = data.get("amount")
        phone = data.get("phone")
        reference = data.get("reference", "Payment")

        if not amount or not phone:
            return jsonify({
                "success": False,
                "error": "amount and phone are required"
            }), 400

        response = MpesaService.simulate_c2b_payment(
            amount=amount,
            phone_number=phone,
            reference=reference
        )

        return jsonify({
            "success": True,
            "response": response
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============= CALLBACK ENDPOINTS =============

@mpesa_bp.route("/stk/callback", methods=["POST"])
def stk_callback():
    """Handle STK Push callback from M-Pesa"""
    try:
        data = request.get_json(force=True)
        
        # Log callback
        print("\n" + "="*60)
        print("💰 STK PUSH CALLBACK RECEIVED")
        print(json.dumps(data, indent=2))
        print("="*60 + "\n")

        # Extract payment details
        callback_data = data.get("Body", {}).get("stkCallback", {})
        result_code = callback_data.get("ResultCode")
        
        if result_code == 0:
            # Payment successful
            metadata = callback_data.get("CallbackMetadata", {}).get("Item", [])
            
            # TODO: Save to database
            # amount = next((item["Value"] for item in metadata if item["Name"] == "Amount"), None)
            # receipt = next((item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber"), None)
            # phone = next((item["Value"] for item in metadata if item["Name"] == "PhoneNumber"), None)
            
            print("✅ Payment successful!")
        else:
            print(f"❌ Payment failed: {callback_data.get('ResultDesc')}")

        # Save to file for debugging
        with open('stk_callbacks.json', 'a') as f:
            f.write(json.dumps(data, indent=2) + '\n\n')

        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

    except Exception as e:
        print(f"Error processing STK callback: {str(e)}")
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


@mpesa_bp.route("/c2b/validate", methods=["POST"])
def c2b_validate():
    """Validate C2B payment before processing"""
    try:
        data = request.get_json()
        print(f"\n🔍 C2B Validation: {json.dumps(data, indent=2)}\n")
        
        # Add validation logic here if needed
        # Return ResultCode: 0 to accept, 1 to reject
        
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return jsonify({"ResultCode": 1, "ResultDesc": "Rejected"})


@mpesa_bp.route("/c2b/confirm", methods=["POST"])
def c2b_confirm():
    """Confirm C2B payment"""
    try:
        data = request.get_json(force=True)
        
        # Log confirmation
        print("\n" + "="*60)
        print("💰 C2B PAYMENT CONFIRMED")
        print(json.dumps(data, indent=2))
        print("="*60 + "\n")

        # TODO: Save to database
        # transaction_id = data.get("TransID")
        # amount = data.get("TransAmount")
        # phone = data.get("MSISDN")
        # reference = data.get("BillRefNumber")

        # Save to file for debugging
        with open('c2b_confirmations.json', 'a') as f:
            f.write(json.dumps(data, indent=2) + '\n\n')

        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

    except Exception as e:
        print(f"Error processing C2B confirmation: {str(e)}")
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


# ============= UTILITY ENDPOINTS =============

@mpesa_bp.route("/register-c2b", methods=["POST"])
def register_c2b():
    """Register C2B validation and confirmation URLs"""
    try:
        access_token = MpesaService.get_access_token()
        
        import requests
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "ShortCode": MpesaConfig.C2B_SHORTCODE,
            "ResponseType": "Completed",
            "ConfirmationURL": f"{MpesaConfig.BASE_URL}c2b/confirm",
            "ValidationURL": f"{MpesaConfig.BASE_URL}c2b/validate"
        }

        response = requests.post(
            MpesaConfig.C2B_REGISTER_URL,
            json=payload,
            headers=headers
        )

        return jsonify({
            "success": True,
            "response": response.json()
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500