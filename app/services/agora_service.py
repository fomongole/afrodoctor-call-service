import os
import time
import random
from agora_token_builder import RtcTokenBuilder
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("AGORA_APP_ID")
APP_CERTIFICATE = os.getenv("AGORA_APP_CERTIFICATE")

class AgoraService:
    @staticmethod
    def generate_rtc_token(channel_name: str, role: int = 1):
        # Generate a random UID between 1 and 232-1
        uid = random.randint(1, 2**32 - 1)
        
        # Token expires in 1 hour (3600 seconds)
        expiration_time_in_seconds = 3600
        current_timestamp = int(time.time())
        privilege_expired_ts = current_timestamp + expiration_time_in_seconds

        token = RtcTokenBuilder.buildTokenWithUid(
            APP_ID, 
            APP_CERTIFICATE, 
            channel_name, 
            uid, 
            role, 
            privilege_expired_ts
        )

        return {
            "token": token,
            "uid": uid,
            "appId": APP_ID
        }