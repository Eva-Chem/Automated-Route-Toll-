from flask import Blueprint, request, jsonify
import requests
import base64, json
from datetime import datetime
from services.config import MpesaConfig
from services.mpesa_service import MpesaService
import logging

logger = logging.getLogger(__name__)


mpesa_bp = Blueprint("mpesa", __name__, url_prefix="/payments")


def get_access_token():
    response = requests.get(
        MpesaConfig.OAUTH_URL,
        auth=(MpesaConfig.CONSUMER_KEY, MpesaConfig.CONSUMER_SECRET)
    )
    response.raise_for_status()
    return response.json()["access_token"]


# ---------------- C2B REGISTER ----------------
@mpesa_bp.route("/register-c2b", methods=["GET"])
def register_c2b():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "ShortCode": MpesaConfig.C2B_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": MpesaConfig.BASE_URL + "c2b/confirm",
        "ValidationURL": MpesaConfig.BASE_URL + "c2b/validate"
    }

    res = requests.post(
        MpesaConfig.C2B_REGISTER_URL,
        json=payload,
        headers=headers
    )

    return jsonify(res.json())

@mpesa_bp.route('/c2b/simulate', methods=['POST'])
def simulate_c2b():
    """
    Simulate a C2B payment (Sandbox only)
    """
    try:
        data = request.get_json()

        amount = data.get("amount")
        phone = data.get("phone")
        reference = data.get("reference", "TestPay")

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
        logger.error(f"C2B Simulation Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500




# ---------------- STK PUSH ----------------
@mpesa_bp.route('/stk-push', methods=['POST'])
def stk_push():
    try:
        data = request.get_json()

        phone = data.get("phone")
        amount = data.get("amount")

        if not phone or not amount:
            return jsonify({
                "success": False,
                "error": "phone and amount required"
            }), 400

        response = MpesaService.stk_push(
            phone_number=phone,
            amount=amount
        )

        return jsonify({
            "success": True,
            "response": response
        })

    except Exception as e:
        logger.error(f"STK Push Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ---------------- CALLBACKS ----------------
@mpesa_bp.route('/stk/callback', methods=['POST'])
def stk_callback():
    data = request.get_json()

    logger.info("📥 STK Callback Received")
    logger.info(json.dumps(data, indent=2))

    with open("stk_callback.json", "a") as f:
        f.write(json.dumps(data) + "\n")

    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})



@mpesa_bp.route("/c2b/validate", methods=["POST"])
def c2b_validate():
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


@mpesa_bp.route("/c2b/confirm", methods=["POST"])
def c2b_confirm():
    data = request.get_json()
    print("💰 PAYMENT CONFIRMED:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
