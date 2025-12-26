import requests
from requests.auth import HTTPBasicAuth
import logging
from .config import MpesaConfig
import base64
from datetime import datetime


logger = logging.getLogger(__name__)

class MpesaService:
    
    @staticmethod
    def get_access_token():
        """
        Get OAuth access token from M-Pesa API
        
        Returns:
            str: Access token
            
        Raises:
            Exception: If token retrieval fails
        """
        try:
            logger.info("="*60)
            logger.info("🔐 Requesting M-Pesa Access Token")
            logger.info("="*60)
            
            # Validate credentials exist
            if not MpesaConfig.CONSUMER_KEY or not MpesaConfig.CONSUMER_SECRET:
                raise Exception("M-Pesa credentials not configured. Check your .env file.")
            
            consumer_key = MpesaConfig.CONSUMER_KEY.strip()
            consumer_secret = MpesaConfig.CONSUMER_SECRET.strip()
            
            logger.info(f"Consumer Key Length: {len(consumer_key)}")
            logger.info(f"Consumer Secret Length: {len(consumer_secret)}")
            logger.info(f"Consumer Key (first 10 chars): {consumer_key[:10]}...")
            logger.info(f"Consumer Secret (first 10 chars): {consumer_secret[:10]}...")
            
            # Make request
            url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            logger.info(f"URL: {url}")
            
            response = requests.get(
                url,
                auth=HTTPBasicAuth(consumer_key, consumer_secret),
                headers={
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response Body: {response.text}")
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                access_token = data.get('access_token')
                
                if access_token:
                    logger.info("✅ Access token retrieved successfully")
                    logger.info(f"Token (first 30 chars): {access_token[:30]}...")
                    return access_token
                else:
                    raise Exception("No access token in response")
                    
            elif response.status_code == 400:
                logger.error("❌ Status 400: Bad Request - Invalid credentials")
                try:
                    error_data = response.json()
                    error_message = error_data.get('error_description', 'Invalid credentials')
                    raise Exception(f"Invalid M-Pesa credentials: {error_message}")
                except:
                    raise Exception("Invalid M-Pesa credentials. Please check your Consumer Key and Consumer Secret.")
                    
            elif response.status_code == 401:
                logger.error("❌ Status 401: Unauthorized")
                raise Exception("Unauthorized: Invalid M-Pesa credentials")
                
            else:
                error_msg = f"Status {response.status_code}: {response.text}"
                logger.error(f"❌ M-Pesa API Error: {error_msg}")
                raise Exception(f"M-Pesa API error: {error_msg}")
            
        except requests.exceptions.Timeout:
            logger.error("⏱️ Request timeout")
            raise Exception("Request timeout. M-Pesa API is not responding.")
            
        except requests.exceptions.ConnectionError:
            logger.error("🔌 Connection error")
            raise Exception("Unable to connect to M-Pesa API. Check your internet connection.")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request failed: {str(e)}")
            raise Exception(f"Request failed: {str(e)}")
            
        except Exception as e:
            logger.error(f"❌ Unexpected error: {str(e)}")
            raise


    @staticmethod
    def simulate_c2b_payment(amount, phone_number, reference="TestPay"):
        """
        Simulate a C2B payment (SANDBOX ONLY)
        """
        access_token = MpesaService.get_access_token()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "ShortCode": MpesaConfig.C2B_SHORTCODE,
            "CommandID": "CustomerPayBillOnline",
            "Amount": amount,
            "Msisdn": phone_number,
            "BillRefNumber": reference
        }

        response = requests.post(
            MpesaConfig.C2B_SIMULATE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def stk_push(phone_number, amount, account_reference="TollPayment"):
        access_token = MpesaService.get_access_token()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        password_str = (
            MpesaConfig.STK_SHORTCODE +
            MpesaConfig.PASSKEY +
            timestamp
        )

        password = base64.b64encode(password_str.encode()).decode()

        payload = {
            "BusinessShortCode": MpesaConfig.STK_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": MpesaConfig.STK_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": f"{MpesaConfig.BASE_URL}stk/callback",
            "AccountReference": account_reference,
            "TransactionDesc": "Route Toll Payment"
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            MpesaConfig.STK_PUSH_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        logger.info(f"STK Push Response: {response.text}")
        return response.json()