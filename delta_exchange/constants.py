"""
Delta Exchange API Constants

This module contains all the constants used throughout the Delta Exchange Python client,
including base URLs, API endpoints, timeouts, and other configuration values.
"""

# Base URLs
REST_BASE_URL = "https://api.india.delta.exchange"
WS_BASE_URL = "wss://socket.india.delta.exchange"

# API Version
API_VERSION = "v2"

# Timeout Configuration (seconds)
DEFAULT_TIMEOUT_CONNECT = 3
DEFAULT_TIMEOUT_READ = 27
DEFAULT_TIMEOUT = (DEFAULT_TIMEOUT_CONNECT, DEFAULT_TIMEOUT_READ)

# REST API Endpoints
# Orders
ORDERS_ENDPOINT = f"/{API_VERSION}/orders"
ORDERS_BY_ID_ENDPOINT = f"/{API_VERSION}/orders/{{order_id}}"
BATCH_ORDERS_ENDPOINT = f"/{API_VERSION}/orders/batch"
BATCH_EDIT_ORDERS_ENDPOINT = f"/{API_VERSION}/orders/batch"
BATCH_DELETE_ORDERS_ENDPOINT = f"/{API_VERSION}/orders/batch_delete"
ORDER_HISTORY_ENDPOINT = f"/{API_VERSION}/orders/history"
ORDER_LEVERAGE_ENDPOINT = f"/{API_VERSION}/orders/{{product_id}}"

# Positions
POSITIONS_ENDPOINT = f"/{API_VERSION}/positions"
CHANGE_MARGIN_ENDPOINT = f"/{API_VERSION}/positions/change_margin"
CLOSE_ALL_POSITIONS_ENDPOINT = f"/{API_VERSION}/positions/close_all"
AUTO_TOPUP_ENDPOINT = f"/{API_VERSION}/positions/auto_topup"

# Wallet
WALLET_BALANCES_ENDPOINT = f"/{API_VERSION}/wallet/balances"

# Products
PRODUCTS_ENDPOINT = f"/{API_VERSION}/products"
PRODUCT_BY_SYMBOL_ENDPOINT = f"/{API_VERSION}/products/{{symbol}}"

# Orderbook
L2_ORDERBOOK_ENDPOINT = "/l2orderbook/{{symbol}}"

# Trades
TRADES_ENDPOINT = "/trades/{{symbol}}"
USER_FILLS_ENDPOINT = f"/{API_VERSION}/fills"

# Heartbeat
HEARTBEAT_CREATE_ENDPOINT = f"/{API_VERSION}/heartbeat/create"
HEARTBEAT_ENDPOINT = f"/{API_VERSION}/heartbeat"

# WebSocket Channels
# Public Channels
WS_CHANNEL_TICKER = "v2/ticker"
WS_CHANNEL_ORDERBOOK = "l2_orderbook"
WS_CHANNEL_TRADES = "all_trades"
WS_CHANNEL_FUNDING_RATE = "funding_rate"
WS_CHANNEL_MARK_PRICE = "mark_price"

# Private Channels (require authentication)
WS_CHANNEL_ORDERS = "orders"
WS_CHANNEL_POSITIONS = "positions"
WS_CHANNEL_USER_TRADES = "user_trades"
WS_CHANNEL_MARGINS = "margins"

# WebSocket Message Types
WS_TYPE_SUBSCRIBE = "subscribe"
WS_TYPE_UNSUBSCRIBE = "unsubscribe"
WS_TYPE_AUTH = "auth"
WS_TYPE_PING = "ping"
WS_TYPE_PONG = "pong"

# Request Headers
HEADER_API_KEY = "api-key"
HEADER_SIGNATURE = "signature"
HEADER_TIMESTAMP = "timestamp"
HEADER_USER_AGENT = "User-Agent"
HEADER_CONTENT_TYPE = "Content-Type"

# Default Values
DEFAULT_USER_AGENT = "delta-exchange-python-client/0.1.0"
DEFAULT_CONTENT_TYPE = "application/json"

# Rate Limiting
# Note: Actual rate limits should be verified with Delta Exchange documentation
# These are conservative estimates
RATE_LIMIT_ORDERS_PER_SECOND = 10
RATE_LIMIT_REQUESTS_PER_SECOND = 20

# Signature Configuration
SIGNATURE_VALIDITY_SECONDS = 5
SIGNATURE_ALGORITHM = "sha256"

# WebSocket Configuration
WS_PING_INTERVAL = 30  # seconds
WS_RECONNECT_DELAY_INITIAL = 1  # seconds
WS_RECONNECT_DELAY_MAX = 60  # seconds
WS_RECONNECT_EXPONENTIAL_BASE = 2
WS_MAX_RECONNECT_ATTEMPTS = 10

# Pagination
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 500

