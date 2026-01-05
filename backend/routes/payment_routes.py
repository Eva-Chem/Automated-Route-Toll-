from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.toll_zone import TollPayment, TollZone, db
from middlewares.auth import admin_required, operator_required
from datetime import datetime

payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/payments", methods=["GET"])
@jwt_required()
@operator_required
def get_all_payments():
    """Get all toll payments - accessible by admin and operator"""
    try:
        payments = TollPayment.query.order_by(TollPayment.created_at.desc()).all()
        
        return jsonify({
            "success": True,
            "data": [payment.to_dict() for payment in payments],
            "count": len(payments)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@payment_bp.route("/payments/<string:payment_id>", methods=["GET"])
@jwt_required()
@operator_required
def get_payment(payment_id):
    """Get specific payment by ID - accessible by admin and operator"""
    try:
        payment = TollPayment.query.filter_by(id=payment_id).first()
        
        if not payment:
            return jsonify({
                "success": False,
                "error": "Payment not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": payment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@payment_bp.route("/payments", methods=["POST"])
@jwt_required()
def create_payment():
    """Create a new toll payment"""
    data = request.get_json()
    
    if not data or "zone_id" not in data or "amount" not in data:
        return jsonify({
            "success": False,
            "error": "Missing required fields: zone_id, amount"
        }), 400
    
    try:
        # Verify zone exists
        zone = TollZone.query.filter_by(zone_id=data['zone_id']).first()
        if not zone:
            return jsonify({
                "success": False,
                "error": "Toll zone not found"
            }), 404
        
        # Generate unique checkout_request_id
        import uuid
        checkout_request_id = data.get('checkout_request_id', str(uuid.uuid4()))
        
        new_payment = TollPayment(
            zone_id=data['zone_id'],
            amount=int(data['amount']),
            checkout_request_id=checkout_request_id,
            status=data.get('status', 'Pending')
        )
        
        db.session.add(new_payment)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "msg": "Payment recorded successfully",
            "payment": new_payment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@payment_bp.route("/payments/<string:payment_id>", methods=["PUT"])
@jwt_required()
@operator_required
def update_payment(payment_id):
    """Update payment status - accessible by admin and operator"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided"
        }), 400
    
    payment = TollPayment.query.filter_by(id=payment_id).first()
    
    if not payment:
        return jsonify({
            "success": False,
            "error": "Payment not found"
        }), 404
    
    try:
        if "status" in data:
            valid_statuses = ['Pending', 'Completed', 'Failed']
            if data["status"] not in valid_statuses:
                return jsonify({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {valid_statuses}"
                }), 400
            payment.status = data["status"]
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "msg": "Payment updated successfully",
            "payment": payment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@payment_bp.route("/payments/<string:payment_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_payment(payment_id):
    """Delete payment - admin only"""
    payment = TollPayment.query.filter_by(id=payment_id).first()
    
    if not payment:
        return jsonify({
            "success": False,
            "error": "Payment not found"
        }), 404
    
    try:
        db.session.delete(payment)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "msg": "Payment deleted successfully",
            "id": payment_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@payment_bp.route("/payments/zone/<string:zone_id>", methods=["GET"])
@jwt_required()
@operator_required
def get_payments_by_zone(zone_id):
    """Get all payments for a specific zone - accessible by admin and operator"""
    try:
        zone = TollZone.query.filter_by(zone_id=zone_id).first()
        if not zone:
            return jsonify({
                "success": False,
                "error": "Toll zone not found"
            }), 404
        
        payments = TollPayment.query.filter_by(zone_id=zone_id).order_by(TollPayment.created_at.desc()).all()
        
        total_amount = sum(p.amount for p in payments if p.status == 'Completed')
        
        return jsonify({
            "success": True,
            "zone_name": zone.name,
            "data": [payment.to_dict() for payment in payments],
            "count": len(payments),
            "total_completed_amount": total_amount
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

