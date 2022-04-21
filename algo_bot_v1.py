import os
import statistics
import sys
import time
import asyncio
from enum import Enum
import pytz
from datetime import datetime, timedelta
from pytz import timezone
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from alpaca_trade_api.rest_async import gather_with_concurrency, AsyncRest
from alpaca_trade_api.entity_v2 import BarsV2
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Load .env enviroment variables
load_dotenv()

# Set Alpaca API key and secret
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Create Alpaca Trade API client
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, api_version='v2')

# Fetch Account
account = api.get_account()
print(account)

# Print Account Details
print(account.id, account.equity, account.status)