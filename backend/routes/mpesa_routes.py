# backend/routes/mpesa_routes.py
from flask import Blueprint, request, jsonify
import json
import uuid
from datetime import datetime
from services.mpesa_service import MpesaService
from services.config import MpesaConfig
from db import db, TollPaid, TollZone

mpesa_bp = Blueprint("mpesa", __name__, url_prefix="/payments")


@mpesa_bp.route('/stk-push', methods=['POST'])
def stk_push():
    """Initiate STK Push payment"""
    try:
        data = request.get_json()
        phone = data.get("phone")
        amount = data.get("amount")
        zone_id = data.get("zone_id")  # Optional: pass zone_id from frontend

        if not phone or not amount:
            return jsonify({"success": False, "error": "phone and amount are required"}), 400

        # Initiate STK push
        response = MpesaService.stk_push(phone_number=phone, amount=amount)
        
        # If STK push initiated successfully, create a pending payment record
        if response.get("ResponseCode") == "0":
            checkout_request_id = response.get("CheckoutRequestID")
            
            # Create pending payment record
            toll_payment = TollPaid(
                id=uuid.uuid4(),
                zone_id=uuid.UUID(zone_id) if zone_id else None,
                amount=int(amount),
                checkout_request_id=checkout_request_id,
                status="PENDING",
                created_at=datetime.utcnow()
            )
            
            db.session.add(toll_payment)
            db.session.commit()
            
            print(f"✅ Created pending payment record: {checkout_request_id}")
        
        return jsonify({"success": True, "response": response}), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in STK push: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@mpesa_bp.route("/stk/callback", methods=["POST"])
def stk_callback():
    """Handle M-Pesa STK Push callback"""
    try:
        data = request.get_json(force=True)
        callback_data = data.get("Body", {}).get("stkCallback", {})
        
        result_code = callback_data.get("ResultCode")
        checkout_request_id = callback_data.get("CheckoutRequestID")
        result_desc = callback_data.get("ResultDesc")
        
        print("\n========== STK CALLBACK RECEIVED ==========")
        print(json.dumps(data, indent=2))
        print("==========================================")
        
        # Find the payment record by CheckoutRequestID
        payment = TollPaid.query.filter_by(
            checkout_request_id=checkout_request_id
        ).first()
        
        if result_code == 0:
            # Payment successful
            print("✅ PAYMENT SUCCESSFUL")
            
            # Extract payment details from callback
            callback_metadata = callback_data.get("CallbackMetadata", {})
            items = callback_metadata.get("Item", [])
            
            # Parse metadata
            mpesa_receipt = None
            phone_number = None
            transaction_date = None
            amount = None
            
            for item in items:
                name = item.get("Name")
                value = item.get("Value")
                
                if name == "MpesaReceiptNumber":
                    mpesa_receipt = value
                elif name == "PhoneNumber":
                    phone_number = str(value)
                elif name == "TransactionDate":
                    transaction_date = value
                elif name == "Amount":
                    amount = value
            
            # Update existing payment record or create new one
            if payment:
                payment.status = "COMPLETED"
                payment.mpesa_receipt_number = mpesa_receipt  # Store receipt number
                payment.phone_number = phone_number  # Store phone number
                print(f"✅ Updated payment record: {checkout_request_id}")
                print(f"   Receipt: {mpesa_receipt}")
                print(f"   Phone: {phone_number}")
                print(f"   Amount: {amount}")
            else:
                # Create new record if it doesn't exist
                payment = TollPaid(
                    id=uuid.uuid4(),
                    zone_id=None,
                    amount=int(amount) if amount else 0,
                    checkout_request_id=checkout_request_id,
                    mpesa_receipt_number=mpesa_receipt,  # Store receipt number
                    phone_number=phone_number,  # Store phone number
                    status="COMPLETED",
                    created_at=datetime.utcnow()
                )
                db.session.add(payment)
                print(f"✅ Created new payment record: {checkout_request_id}")
                print(f"   Receipt: {mpesa_receipt}")
            
            # IMPORTANT: Commit the changes
            db.session.commit()
            print("✅ Database changes committed successfully")
            
        else:
            # Payment failed or cancelled
            print(f"❌ PAYMENT FAILED: {result_desc}")
            
            if payment:
                payment.status = "FAILED"
                db.session.commit()
                print(f"✅ Updated payment status to FAILED: {checkout_request_id}")
        
        # Always return success to M-Pesa
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200
    
    except Exception as e:
        print(f"❌ Error processing STK callback: {str(e)}")
        import traceback
        print(traceback.format_exc())
        db.session.rollback()
        # Still return success to M-Pesa to avoid retries
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

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
        print("\n========== C2B PAYMENT CONFIRMED ==========")
        print(json.dumps(data, indent=2))
        print("==========================================")
                
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