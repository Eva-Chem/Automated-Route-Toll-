import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
from .config import MpesaConfig


class MpesaService:
    """Service for M-Pesa API interactions"""
    
    @staticmethod
    def get_access_token():
        """
        Get OAuth access token from M-Pesa API
        
        Returns:
            str: Access token
        
        Raises:
            Exception: If token retrieval fails
        """
        if not MpesaConfig.CONSUMER_KEY or not MpesaConfig.CONSUMER_SECRET:
            raise Exception("M-Pesa credentials not configured")
        
        try:
            response = requests.get(
                MpesaConfig.OAUTH_URL,
                auth=HTTPBasicAuth(
                    MpesaConfig.CONSUMER_KEY.strip(),
                    MpesaConfig.CONSUMER_SECRET.strip()
                ),
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()["access_token"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get access token: {str(e)}")
    
    
    @staticmethod
    def stk_push(phone_number, amount, account_reference="TollPayment"):
        """
        Initiate STK Push payment
        
        Args:
            phone_number: Customer phone number (254XXXXXXXXX)
            amount: Amount to charge
            account_reference: Reference for the transaction
        
        Returns:
            dict: M-Pesa API response
        """
        access_token = MpesaService.get_access_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        shortcode = str(MpesaConfig.STK_SHORTCODE)
        # Generate password
        password_str = f"{MpesaConfig.STK_SHORTCODE}{MpesaConfig.PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()
        
        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": f"{MpesaConfig.BASE_URL}stk/callback",
            "AccountReference": account_reference,
            "TransactionDesc": f"Payment for {account_reference}"
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
    
    
    @staticmethod
    def simulate_c2b_payment(amount, phone_number, reference="Payment"):
        """
        Simulate C2B payment (Sandbox only)
        
        Args:
            amount: Amount to pay
            phone_number: Customer phone number
            reference: Bill reference number
        
        Returns:
            dict: M-Pesa API response
        """
        access_token = MpesaService.get_access_token()
        
        payload = {
            "ShortCode": MpesaConfig.C2B_SHORTCODE,
            "CommandID": "CustomerPayBillOnline",
            "Amount": int(amount),
            "Msisdn": phone_number,
            "BillRefNumber": reference
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            MpesaConfig.C2B_SIMULATE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()