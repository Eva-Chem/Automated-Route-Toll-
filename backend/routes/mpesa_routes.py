from flask import Blueprint, request, jsonify
import requests
import base64
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
@mpesa_bp.route("/stk-push", methods=["POST"])
def stk_push():
    data = request.json
    phone = data.get("phone")
    amount = data.get("amount")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = (
        MpesaConfig.STK_SHORTCODE +
        MpesaConfig.PASSKEY +
        timestamp
    )

    encoded_password = base64.b64encode(password.encode()).decode()

    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "BusinessShortCode": MpesaConfig.STK_SHORTCODE,
        "Password": encoded_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": MpesaConfig.STK_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": MpesaConfig.BASE_URL + "stk/callback",
        "AccountReference": "RouteToll",
        "TransactionDesc": "Route Toll Payment"
    }

    res = requests.post(
        MpesaConfig.STK_PUSH_URL,
        json=payload,
        headers=headers
    )

    return jsonify(res.json())


# ---------------- CALLBACKS ----------------
@mpesa_bp.route("/stk/callback", methods=["POST"])
def stk_callback():
    data = request.get_json()
    print("📥 STK CALLBACK:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


@mpesa_bp.route("/c2b/validate", methods=["POST"])
def c2b_validate():
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


@mpesa_bp.route("/c2b/confirm", methods=["POST"])
def c2b_confirm():
    data = request.get_json()
    print("💰 PAYMENT CONFIRMED:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
