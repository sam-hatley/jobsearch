from dotenv import load_dotenv
import os


# Get ProtonVPN username and password from .env file
load_dotenv()
PV_UN = os.environ.get('PVPN_UN')
PV_PASS = os.environ.get('PVPN_PASS')
