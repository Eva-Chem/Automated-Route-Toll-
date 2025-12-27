from flask import Blueprint, request, jsonify
import json
from services.mpesa_service import MpesaService
from services.config import MpesaConfig

mpesa_bp = Blueprint("mpesa", __name__, url_prefix="/payments")


@mpesa_bp.route('/stk-push', methods=['POST'])
def stk_push():
    """Initiate STK Push payment"""
    try:
        data = request.get_json()
        phone = data.get("phone")
        amount = data.get("amount")

        if not phone or not amount:
            return jsonify({"success": False, "error": "phone and amount are required"}), 400

        response = MpesaService.stk_push(phone_number=phone, amount=amount)
        return jsonify({"success": True, "response": response}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@mpesa_bp.route('/c2b/simulate', methods=['POST'])
def simulate_c2b():
    """Simulate C2B payment (Sandbox only)"""
    try:
        data = request.get_json()
        amount = data.get("amount")
        phone = data.get("phone")
        reference = data.get("reference", "Payment")

        if not amount or not phone:
            return jsonify({"success": False, "error": "amount and phone are required"}), 400

        response = MpesaService.simulate_c2b_payment(
            amount=amount,
            phone_number=phone,
            reference=reference
        )
        return jsonify({"success": True, "response": response}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@mpesa_bp.route("/stk/callback", methods=["POST"])
def stk_callback():
    """Handle STK Push callback from M-Pesa"""
    try:
        data = request.get_json(force=True)
        callback_data = data.get("Body", {}).get("stkCallback", {})
        result_code = callback_data.get("ResultCode")
        
        print(f"\n{'='*60}\nSTK PUSH CALLBACK: {result_code}\n{json.dumps(data, indent=2)}\n{'='*60}\n")
        
        if result_code == 0:
            print("Payment successful")
        else:
            print(f"Payment failed: {callback_data.get('ResultDesc')}")

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
        print(f"\n C2B Validation: {json.dumps(data, indent=2)}\n")
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
        
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return jsonify({"ResultCode": 1, "ResultDesc": "Rejected"})


@mpesa_bp.route("/c2b/confirm", methods=["POST"])
def c2b_confirm():
    """Confirm C2B payment"""
    try:
        data = request.get_json(force=True)
        print(f"\n{'='*60}\n C2B PAYMENT CONFIRMED\n{json.dumps(data, indent=2)}\n{'='*60}\n")

        with open('c2b_confirmations.json', 'a') as f:
            f.write(json.dumps(data, indent=2) + '\n\n')

        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

    except Exception as e:
        print(f"Error processing C2B confirmation: {str(e)}")
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


@mpesa_bp.route("/register-c2b", methods=["POST"])
def register_c2b():
    """Register C2B validation and confirmation URLs"""
    try:
        import requests
        access_token = MpesaService.get_access_token()
        
        payload = {
            "ShortCode": MpesaConfig.C2B_SHORTCODE,
            "ResponseType": "Completed",
            "ConfirmationURL": f"{MpesaConfig.BASE_URL}c2b/confirm",
            "ValidationURL": f"{MpesaConfig.BASE_URL}c2b/validate"
        }

        response = requests.post(
            MpesaConfig.C2B_REGISTER_URL,
            json=payload,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        return jsonify({"success": True, "response": response.json()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500