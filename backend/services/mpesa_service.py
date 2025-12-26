import requests
from requests.auth import HTTPBasicAuth
import logging
from .config import MpesaConfig
import base64
from datetime import datetime


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
            
            # Validate credentials exist
            if not MpesaConfig.CONSUMER_KEY or not MpesaConfig.CONSUMER_SECRET:
                raise Exception("M-Pesa credentials not configured. Check your .env file.")
            
            consumer_key = MpesaConfig.CONSUMER_KEY.strip()
            consumer_secret = MpesaConfig.CONSUMER_SECRET.strip()
            
            
            # Make request
            url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            
            
            response = requests.get(
                url,
                auth=HTTPBasicAuth(consumer_key, consumer_secret),
                headers={
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
           
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                access_token = data.get('access_token')
                
                if access_token:
                    
                    return access_token
                else:
                    raise Exception("No access token in response")
                    
            elif response.status_code == 400:
                
                try:
                    error_data = response.json()
                    error_message = error_data.get('error_description', 'Invalid credentials')
                    raise Exception(f"Invalid M-Pesa credentials: {error_message}")
                except:
                    raise Exception("Invalid M-Pesa credentials. Please check your Consumer Key and Consumer Secret.")
                    
            elif response.status_code == 401:
                
                raise Exception("Unauthorized: Invalid M-Pesa credentials")
                
            else:
                error_msg = f"Status {response.status_code}: {response.text}"
                
                raise Exception(f"M-Pesa API error: {error_msg}")
            
        except requests.exceptions.Timeout:
           
            raise Exception("Request timeout. M-Pesa API is not responding.")
            
        except requests.exceptions.ConnectionError:
           
            raise Exception("Unable to connect to M-Pesa API. Check your internet connection.")
            
        except requests.exceptions.RequestException as e:
            
            raise Exception(f"Request failed: {str(e)}")
            
        except Exception as e:
            
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

        
        return response.json()