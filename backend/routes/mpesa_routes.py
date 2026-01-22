# backend/routes/mpesa_routes.py
from flask import Blueprint, request, jsonify
import json
import uuid
from datetime import datetime
from services.mpesa_service import MpesaService
from services.config import MpesaConfig
from db import db, TollPaid, TollZone
from sqlalchemy import func

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
        
        payment = TollPaid.query.filter_by(
            checkout_request_id=checkout_request_id
        ).first()
        
        if result_code == 0:
            print("✅ PAYMENT SUCCESSFUL")
            
            callback_metadata = callback_data.get("CallbackMetadata", {})
            items = callback_metadata.get("Item", [])
            
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
            
            if payment:
                payment.status = "COMPLETED"
                payment.mpesa_receipt_number = mpesa_receipt
                payment.phone_number = phone_number
                print(f"✅ Updated payment record: {checkout_request_id}")
                print(f"   Receipt: {mpesa_receipt}")
                print(f"   Phone: {phone_number}")
                print(f"   Amount: {amount}")
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
                print(f"✅ Created new payment record: {checkout_request_id}")
                print(f"   Receipt: {mpesa_receipt}")
            
            db.session.commit()
            print("✅ Database changes committed successfully")
            
        else:
            print(f"❌ PAYMENT FAILED: {result_desc}")
            
            if payment:
                payment.status = "FAILED"
                db.session.commit()
                print(f"✅ Updated payment status to FAILED: {checkout_request_id}")
        
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200
    
    except Exception as e:
        print(f"❌ Error processing STK callback: {str(e)}")
        import traceback
        print(traceback.format_exc())
        db.session.rollback()
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200


@mpesa_bp.route("/status/<string:checkout_request_id>", methods=["GET"])
def get_payment_status(checkout_request_id):
    """
    Frontend polls this endpoint to know the STK payment status
    DEBUGGED VERSION with extensive logging
    """
    try:
        # Clean the input
        original_id = checkout_request_id
        checkout_request_id = checkout_request_id.strip()
        
        print(f"\n{'='*60}")
        print(f"🔍 PAYMENT STATUS CHECK")
        print(f"{'='*60}")
        print(f"Original ID: '{original_id}'")
        print(f"Cleaned ID:  '{checkout_request_id}'")
        print(f"ID Length:   {len(checkout_request_id)}")
        print(f"{'='*60}\n")
        
        # Try exact match first
        payment = TollPaid.query.filter(
            TollPaid.checkout_request_id == checkout_request_id
        ).first()
        
        if payment:
            print(f"✅ FOUND (exact match)")
            print(f"   Payment ID: {payment.id}")
            print(f"   Status: {payment.status}")
            print(f"   Amount: {payment.amount}")
            print(f"   Receipt: {payment.mpesa_receipt_number}")
        else:
            print(f"❌ NOT FOUND (exact match)")
            
            # Try case-insensitive search
            print(f"\n🔄 Trying case-insensitive search...")
            payment = TollPaid.query.filter(
                func.lower(TollPaid.checkout_request_id) == checkout_request_id.lower()
            ).first()
            
            if payment:
                print(f"✅ FOUND (case-insensitive)")
                print(f"   Actual ID in DB: '{payment.checkout_request_id}'")
            else:
                print(f"❌ NOT FOUND (case-insensitive)")
                
                # Show all similar IDs
                print(f"\n📋 Searching for similar checkout IDs...")
                similar_payments = TollPaid.query.filter(
                    TollPaid.checkout_request_id.contains(checkout_request_id[-10:])
                ).limit(5).all()
                
                if similar_payments:
                    print(f"Found {len(similar_payments)} similar IDs:")
                    for p in similar_payments:
                        print(f"   - '{p.checkout_request_id}' (status: {p.status})")
                else:
                    print(f"No similar IDs found")
                
                # Show last 10 payments
                print(f"\n📊 Last 10 payments in database:")
                recent_payments = TollPaid.query.order_by(
                    TollPaid.created_at.desc()
                ).limit(10).all()
                
                for p in recent_payments:
                    print(f"   ID: '{p.checkout_request_id}'")
                    print(f"      Status: {p.status}, Amount: {p.amount}, Created: {p.created_at}")
        
        print(f"\n{'='*60}\n")

        if not payment:
            return jsonify({
                "success": False,
                "error": "Payment not found",
                "searched_id": checkout_request_id,
                "id_length": len(checkout_request_id)
            }), 404

        # Return status based on payment.status
        response_data = {
            "success": True,
            "status": payment.status.lower()
        }
        
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
        print(f"❌ ERROR in get_payment_status: {str(e)}")
        import traceback
        traceback.print_exc()
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