import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MpesaConfig:
    """M-Pesa API Configuration"""
    
    # API Credentials
    CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY', '').strip()
    CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET', '').strip()
    
    # Business Details
    SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379')
    PASSKEY = os.getenv('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')
    
    # Base URL for callbacks - CHANGED: now uses /payments/ instead of /mpesa/
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000/payments/').strip()
    # Ensure BASE_URL ends with /payments/
    if not BASE_URL.endswith('/payments/'):
        if BASE_URL.endswith('/'):
            BASE_URL = BASE_URL + 'payments/'
        else:
            BASE_URL = BASE_URL + '/payments/'
    
    # API URLs (Sandbox)
    OAUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    C2B_REGISTER_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v2/registerurl"
    STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    @classmethod
    def validate(cls):
        """Validate that required configurations are present"""
        if not cls.CONSUMER_KEY:
            raise ValueError("MPESA_CONSUMER_KEY is not set")
        if not cls.CONSUMER_SECRET:
            raise ValueError("MPESA_CONSUMER_SECRET is not set")
        
        print(f"✅ Consumer Key: {cls.CONSUMER_KEY[:20]}... (length: {len(cls.CONSUMER_KEY)})")
        print(f"✅ Consumer Secret: {cls.CONSUMER_SECRET[:20]}... (length: {len(cls.CONSUMER_SECRET)})")
        print(f"✅ Shortcode: {cls.SHORTCODE}")
        print(f"✅ Base URL: {cls.BASE_URL}")
        
        return True