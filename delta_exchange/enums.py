"""
Delta Exchange Enumerations

This module contains all enumeration classes used throughout the Delta Exchange
Python client library.
"""

from enum import Enum


class OrderSide(str, Enum):
    """
    Order side enumeration.
    
    Represents whether an order is a buy or sell order.
    """
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """
    Order type enumeration.
    
    Represents the different types of orders that can be placed.
    """
    LIMIT_ORDER = "limit_order"
    MARKET_ORDER = "market_order"
    STOP_LIMIT = "stop_limit"
    STOP_MARKET = "stop_market"


class StopOrderType(str, Enum):
    """
    Stop order type enumeration.
    
    Represents the type of stop order (stop loss or take profit).
    """
    STOP_LOSS_ORDER = "stop_loss_order"
    TAKE_PROFIT_ORDER = "take_profit_order"


class OrderState(str, Enum):
    """
    Order state enumeration.
    
    Represents the current state of an order.
    """
    OPEN = "open"
    PENDING = "pending"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class TimeInForce(str, Enum):
    """
    Time in force enumeration.
    
    Represents how long an order remains active before it is executed or expires.
    
    - GTC (Good Till Cancelled): Order remains active until filled or cancelled
    - IOC (Immediate or Cancel): Order must be filled immediately, unfilled portion is cancelled
    - FOK (Fill or Kill): Order must be filled entirely immediately or cancelled completely
    """
    GTC = "gtc"  # Good Till Cancelled
    IOC = "ioc"  # Immediate or Cancel
    FOK = "fok"  # Fill or Kill (if supported)


class StopTriggerMethod(str, Enum):
    """
    Stop trigger method enumeration.
    
    Represents the price type used to trigger stop orders.
    """
    MARK_PRICE = "mark_price"
    LAST_TRADED_PRICE = "last_traded_price"
    SPOT_PRICE = "spot_price"


class MMPLevel(str, Enum):
    """
    Market Maker Protection (MMP) level enumeration.
    
    Represents the MMP level for an order.
    """
    DISABLED = "disabled"
    MMP1 = "mmp1"
    MMP2 = "mmp2"
    MMP3 = "mmp3"
    MMP4 = "mmp4"
    MMP5 = "mmp5"


class ContractType(str, Enum):
    """
    Contract type enumeration.
    
    Represents the type of trading contract.
    """
    FUTURES = "futures"
    PERPETUAL_FUTURES = "perpetual_futures"
    CALL_OPTIONS = "call_options"
    PUT_OPTIONS = "put_options"


class FillType(str, Enum):
    """
    Fill type enumeration.
    
    Represents the type of fill (trade execution).
    """
    NORMAL = "normal"
    ADL = "adl"  # Auto-Deleveraging
    LIQUIDATION = "liquidation"
    SETTLEMENT = "settlement"
    OTC = "otc"  # Over-the-counter


class Role(str, Enum):
    """
    Trade role enumeration.
    
    Represents whether the user was a taker or maker in a trade.
    """
    TAKER = "taker"
    MAKER = "maker"


class TransactionType(str, Enum):
    """
    Transaction type enumeration.
    
    Represents different types of wallet transactions.
    """
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    COMMISSION = "commission"
    FUNDING = "funding"
    SETTLEMENT = "settlement"
    REALIZED_PNL = "realized_pnl"
    TRANSFER = "transfer"

