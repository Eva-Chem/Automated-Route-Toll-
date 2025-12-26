import os
from dotenv import load_dotenv

load_dotenv()

class MpesaConfig:
    # App credentials
    CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")

    # Shortcodes
    STK_SHORTCODE = os.getenv("MPESA_STK_SHORTCODE")   # 174379
    C2B_SHORTCODE = os.getenv("MPESA_C2B_SHORTCODE")   # 600383

    PASSKEY = os.getenv("MPESA_PASSKEY")

    BASE_URL = os.getenv("BASE_URL").rstrip("/") + "/"

    # API URLs
    OAUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    C2B_REGISTER_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    C2B_SIMULATE_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"

    @classmethod
    def validate(cls):
        required = [
            cls.CONSUMER_KEY,
            cls.CONSUMER_SECRET,
            cls.STK_SHORTCODE,
            cls.PASSKEY,
            cls.BASE_URL
        ]
        if not all(required):
            raise ValueError("❌ Missing M-Pesa environment variables")

        print("✅ M-Pesa configuration loaded successfully")
