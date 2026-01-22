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
        zone_id = data.get("zone_id")

        if not phone or not amount:
            return jsonify({"success": False, "error": "phone and amount are required"}), 400

        response = MpesaService.stk_push(phone_number=phone, amount=amount)
        
        if response.get("ResponseCode") == "0":
            checkout_request_id = response.get("CheckoutRequestID")
            
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
        
        return jsonify({"success": True, "response": response}), 200

    except Exception as e:
        db.session.rollback()
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
        
        payment = TollPaid.query.filter_by(
            checkout_request_id=checkout_request_id
        ).first()
        
        if result_code == 0:
            callback_metadata = callback_data.get("CallbackMetadata", {})
            items = callback_metadata.get("Item", [])
            
            mpesa_receipt = None
            phone_number = None
            amount = None
            
            for item in items:
                name = item.get("Name")
                value = item.get("Value")
                
                if name == "MpesaReceiptNumber":
                    mpesa_receipt = value
                elif name == "PhoneNumber":
                    phone_number = str(value)
                elif name == "Amount":
                    amount = value
            
            if payment:
                payment.status = "COMPLETED"
                payment.mpesa_receipt_number = mpesa_receipt
                payment.phone_number = phone_number
            else:
                payment = TollPaid(
                    id=uuid.uuid4(),
                    zone_id=None,
                    amount=int(amount) if amount else 0,
                    checkout_request_id=checkout_request_id,
                    mpesa_receipt_number=mpesa_receipt,
                    phone_number=phone_number,
                    status="COMPLETED",
                    created_at=datetime.utcnow()
                )
                db.session.add(payment)
            
            db.session.commit()
            
        else:
            if payment:
                payment.status = "FAILED"
                db.session.commit()
        
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200


@mpesa_bp.route("/status/<string:checkout_request_id>", methods=["GET"])
def get_payment_status(checkout_request_id):
    """Get payment status by CheckoutRequestID"""
    try:
        checkout_request_id = checkout_request_id.strip()
        
        payment = TollPaid.query.filter_by(
            checkout_request_id=checkout_request_id
        ).first()

        if not payment:
            return jsonify({
                "success": False,
                "error": "Payment not found"
            }), 404

        response_data = {"success": True}
        
        if payment.status == "COMPLETED":
            response_data.update({
                "status": "paid",
                "receipt": payment.mpesa_receipt_number,
                "amount": payment.amount,
                "phone": payment.phone_number
            })
        elif payment.status == "FAILED":
            response_data.update({
                "status": "failed",
                "reason": "Payment failed or was cancelled"
            })
        elif payment.status == "PENDING":
            response_data.update({
                "status": "pending"
            })

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


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
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
        
    except Exception as e:
        return jsonify({"ResultCode": 1, "ResultDesc": "Rejected"})


@mpesa_bp.route("/c2b/confirm", methods=["POST"])
def c2b_confirm():
    """Confirm C2B payment"""
    try:
        data = request.get_json(force=True)
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

    except Exception as e:
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