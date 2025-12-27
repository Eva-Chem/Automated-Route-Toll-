import os
from dotenv import load_dotenv

load_dotenv()


class MpesaConfig:
    """M-Pesa API Configuration"""
    
    # App Credentials
    CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY", "")
    CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "")
    
    # Shortcodes
    STK_SHORTCODE = os.getenv("MPESA_STK_SHORTCODE", "174379")
    C2B_SHORTCODE = os.getenv("MPESA_C2B_SHORTCODE", "600383")
    
    # Passkey
    PASSKEY = os.getenv("MPESA_PASSKEY", "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919")
    
    # Callback Base URL (from ngrok)
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000/payments/").rstrip("/") + "/"
    
    # M-Pesa API URLs (Sandbox)
    OAUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    C2B_REGISTER_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v2/registerurl"
    C2B_SIMULATE_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = [
            (cls.CONSUMER_KEY, "MPESA_CONSUMER_KEY"),
            (cls.CONSUMER_SECRET, "MPESA_CONSUMER_SECRET"),
            (cls.PASSKEY, "MPESA_PASSKEY"),
        ]
        
        missing = [name for value, name in required if not value]
        
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
        
        print(f"✅ M-Pesa Config: {cls.STK_SHORTCODE} | {cls.BASE_URL}")
        return True