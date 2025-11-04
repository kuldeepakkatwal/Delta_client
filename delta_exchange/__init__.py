"""
Delta Exchange Python Client

A professional Python client library for the Delta Exchange API.

Example:
    >>> from delta_exchange import DeltaRestClient
    >>> client = DeltaRestClient(api_key="your_key", api_secret="your_secret")
    >>> positions = client.get_positions()
"""

__version__ = "0.1.0"
__author__ = "Delta Exchange Python Client Contributors"
__license__ = "MIT"

# Import main classes
from .client import DeltaRestClient
from .websocket_client import DeltaWebSocketClient

# Import exceptions
from .exceptions import (
    DeltaExchangeException,
    AuthenticationError,
    OrderError,
    APIError,
    WebSocketError,
    RateLimitError,
    ValidationError,
    NetworkError,
)

# Import auth
from .auth import DeltaAuth

# Import models
from .models import (
    Order,
    Position,
    Balance,
    Product,
    Fill,
    OrderBook,
    OrderBookLevel,
    Trade,
)

# Import enums
from .enums import (
    OrderSide,
    OrderType,
    OrderState,
    StopOrderType,
    TimeInForce,
    StopTriggerMethod,
    MMPLevel,
    ContractType,
    FillType,
    Role,
    TransactionType,
)

# Import constants (optional, for advanced users)
from . import constants

# Define what's available when using "from delta_exchange import *"
__all__ = [
    # Version
    "__version__",
    # Main classes
    "DeltaRestClient",
    "DeltaWebSocketClient",
    # Auth
    "DeltaAuth",
    # Models
    "Order",
    "Position",
    "Balance",
    "Product",
    "Fill",
    "OrderBook",
    "OrderBookLevel",
    "Trade",
    # Enums
    "OrderSide",
    "OrderType",
    "OrderState",
    "StopOrderType",
    "TimeInForce",
    "StopTriggerMethod",
    "MMPLevel",
    "ContractType",
    "FillType",
    "Role",
    "TransactionType",
    # Exceptions
    "DeltaExchangeException",
    "AuthenticationError",
    "OrderError",
    "APIError",
    "WebSocketError",
    "RateLimitError",
    "ValidationError",
    "NetworkError",
    # Constants module
    "constants",
]

