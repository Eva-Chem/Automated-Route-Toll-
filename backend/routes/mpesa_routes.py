from flask import Blueprint, request, jsonify
import logging
import json
import requests
from services.mpesa_service import MpesaService
from services.config import MpesaConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CHANGED: url_prefix from '/mpesa' to '/payments'
mpesa_bp = Blueprint('mpesa', __name__, url_prefix='/payments')


@mpesa_bp.route('/access-token', methods=['GET'])
def get_access_token():
    """
    Get M-Pesa OAuth access token
    
    Returns:
        JSON with access token or error message
    """
    try:
        logger.info("📞 Access token endpoint called")
        
        # Get access token from M-Pesa
        access_token = MpesaService.get_access_token()
        
        return jsonify({
            "success": True,
            "access_token": access_token
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@mpesa_bp.route('/register-urls', methods=['POST'])
def register_urls():
    """
    Register C2B validation and confirmation URLs with M-Pesa
    
    Returns:
        JSON with registration response
    """
    try:
        logger.info("📝 Register URLs endpoint called")
        
        # Get access token
        access_token = MpesaService.get_access_token()
        
        # Prepare request
        endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v2/registerurl'
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "ShortCode": MpesaConfig.SHORTCODE,
            "ResponseType": "Completed",
            "ConfirmationURL": f"{MpesaConfig.BASE_URL}c2b/confirm",
            "ValidationURL": f"{MpesaConfig.BASE_URL}c2b/validate"
        }
        
        logger.info(f"Registering URLs with payload: {json.dumps(payload, indent=2)}")
        
        # Make request to M-Pesa
        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response: {response.text}")
        
        response_data = response.json()
        
        return jsonify({
            "success": True,
            "response": response_data
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@mpesa_bp.route('/c2b/validate', methods=['POST'])
def c2b_validate():
    """
    C2B validation callback - M-Pesa calls this to validate payments
    
    Returns:
        JSON response to M-Pesa
    """
    try:
        data = request.get_json()
        logger.info("✅ C2B Validation callback received")
        logger.info(f"Data: {json.dumps(data, indent=2)}")
        
        # Save to file for debugging
        with open('data_validation.json', 'a') as f:
            f.write(json.dumps(data, indent=2) + '\n')
            f.write('\n' + '='*50 + '\n')
        
        # Return success response to M-Pesa
        return jsonify({
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Validation error: {str(e)}")
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Rejected"
        }), 200


@mpesa_bp.route('/c2b/confirm', methods=['POST'])
def c2b_confirm():
    """
    C2B confirmation callback - M-Pesa calls this to confirm payments
    
    Returns:
        JSON response to M-Pesa
    """
    try:
        data = request.get_json()
        logger.info("✅ C2B Confirmation callback received")
        logger.info(f"Data: {json.dumps(data, indent=2)}")
        
        # Save to file for debugging
        with open('data_confirmation.json', 'a') as f:
            f.write(json.dumps(data, indent=2) + '\n')
            f.write('\n' + '='*50 + '\n')
        
        # Return success response to M-Pesa
        return jsonify({
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Confirmation error: {str(e)}")
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Rejected"
        }), 200