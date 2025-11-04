"""
Delta Exchange Data Models

This module contains all data models used for representing API responses
and requests in the Delta Exchange Python client library.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

from .enums import (
    OrderSide,
    OrderType,
    OrderState,
    StopOrderType,
    TimeInForce,
    StopTriggerMethod,
    MMPLevel,
    FillType,
    Role,
)


@dataclass
class Order:
    """
    Represents an order on Delta Exchange.
    
    Attributes:
        id: Unique order ID
        user_id: User ID who placed the order
        product_id: Product ID
        product_symbol: Product symbol (e.g., "BTCUSD")
        size: Order size
        unfilled_size: Remaining unfilled size
        side: Order side (buy/sell)
        order_type: Type of order (limit/market/stop)
        limit_price: Limit price for limit orders
        stop_order_type: Type of stop order
        stop_price: Stop trigger price
        trail_amount: Trailing stop amount
        paid_commission: Commission already paid
        commission: Total commission
        reduce_only: Whether order only reduces position
        client_order_id: Client-provided order ID
        state: Current state of the order
        created_at: Timestamp when order was created (microseconds)
        time_in_force: Time in force setting
        mmp: Market maker protection level
        post_only: Whether order is post-only
        stop_trigger_method: Method to trigger stop orders
        bracket_stop_loss_price: Bracket stop loss price
        bracket_stop_loss_limit_price: Bracket stop loss limit price
        bracket_take_profit_price: Bracket take profit price
        bracket_take_profit_limit_price: Bracket take profit limit price
        bracket_trail_amount: Bracket trailing amount
        cancel_orders_accepted: Whether cancel all was accepted
    """
    
    id: int
    user_id: int
    size: int
    side: OrderSide
    order_type: OrderType
    state: OrderState
    product_id: int
    product_symbol: str
    unfilled_size: Optional[int] = None
    limit_price: Optional[str] = None
    stop_order_type: Optional[StopOrderType] = None
    stop_price: Optional[str] = None
    trail_amount: Optional[str] = None
    paid_commission: Optional[str] = None
    commission: Optional[str] = None
    reduce_only: bool = False
    client_order_id: Optional[str] = None
    created_at: Optional[str] = None
    time_in_force: Optional[TimeInForce] = None
    mmp: Optional[MMPLevel] = None
    post_only: bool = False
    stop_trigger_method: Optional[StopTriggerMethod] = None
    bracket_stop_loss_price: Optional[str] = None
    bracket_stop_loss_limit_price: Optional[str] = None
    bracket_take_profit_price: Optional[str] = None
    bracket_take_profit_limit_price: Optional[str] = None
    bracket_trail_amount: Optional[str] = None
    bracket_stop_trigger_method: Optional[StopTriggerMethod] = None
    cancel_orders_accepted: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Order":
        """
        Create an Order instance from API response dictionary.
        
        Args:
            data: Dictionary from API response
            
        Returns:
            Order instance
        """
        # Convert string enums to enum instances
        kwargs = data.copy()
        
        if "side" in kwargs and kwargs["side"]:
            kwargs["side"] = OrderSide(kwargs["side"])
        
        if "order_type" in kwargs and kwargs["order_type"]:
            kwargs["order_type"] = OrderType(kwargs["order_type"])
        
        if "state" in kwargs and kwargs["state"]:
            kwargs["state"] = OrderState(kwargs["state"])
        
        if "stop_order_type" in kwargs and kwargs["stop_order_type"]:
            kwargs["stop_order_type"] = StopOrderType(kwargs["stop_order_type"])
        
        if "time_in_force" in kwargs and kwargs["time_in_force"]:
            kwargs["time_in_force"] = TimeInForce(kwargs["time_in_force"])
        
        if "mmp" in kwargs and kwargs["mmp"]:
            kwargs["mmp"] = MMPLevel(kwargs["mmp"])
        
        if "stop_trigger_method" in kwargs and kwargs["stop_trigger_method"]:
            kwargs["stop_trigger_method"] = StopTriggerMethod(kwargs["stop_trigger_method"])
        
        if "bracket_stop_trigger_method" in kwargs and kwargs["bracket_stop_trigger_method"]:
            kwargs["bracket_stop_trigger_method"] = StopTriggerMethod(kwargs["bracket_stop_trigger_method"])
        
        # Remove unknown fields
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        return cls(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Order instance to dictionary for API requests.
        
        Returns:
            Dictionary representation
        """
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Enum):
                    result[key] = value.value
                else:
                    result[key] = value
        return result


@dataclass
class Position:
    """
    Represents a trading position on Delta Exchange.
    
    Attributes:
        user_id: User ID
        product_id: Product ID
        product_symbol: Product symbol
        size: Position size (positive for long, negative for short)
        entry_price: Average entry price
        margin: Margin allocated to position
        liquidation_price: Liquidation price
        bankruptcy_price: Bankruptcy price
        adl_level: Auto-deleveraging level
        commission: Commission blocked in position
        realized_pnl: Realized PnL since position opened
        realized_funding: Realized funding since position opened
    """
    
    user_id: int
    product_id: int
    product_symbol: str
    size: int
    entry_price: Optional[str] = None
    margin: Optional[str] = None
    liquidation_price: Optional[str] = None
    bankruptcy_price: Optional[str] = None
    adl_level: Optional[int] = None
    commission: Optional[str] = None
    realized_pnl: Optional[str] = None
    realized_funding: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Position":
        """Create Position instance from API response dictionary."""
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        kwargs = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Position instance to dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class Balance:
    """
    Represents a wallet balance on Delta Exchange.
    
    Attributes:
        asset_id: Asset ID
        asset_symbol: Asset symbol (e.g., "USDT", "BTC")
        available_balance: Available balance for trading
        balance: Total balance
        order_margin: Margin blocked in orders
        position_margin: Margin blocked in positions
        commission: Commission balance
        pending_referral_bonus: Pending referral rewards
        pending_trading_fee_credit: Pending fee credits
    """
    
    asset_id: int
    asset_symbol: str
    balance: str
    available_balance: Optional[str] = None
    order_margin: Optional[str] = None
    position_margin: Optional[str] = None
    commission: Optional[str] = None
    pending_referral_bonus: Optional[str] = None
    pending_trading_fee_credit: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Balance":
        """Create Balance instance from API response dictionary."""
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        kwargs = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Balance instance to dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class Product:
    """
    Represents a trading product on Delta Exchange.
    
    Attributes:
        id: Product ID
        symbol: Product symbol
        description: Product description
        contract_type: Type of contract
        contract_value: Contract value
        tick_size: Minimum price increment
        maker_commission_rate: Maker fee rate
        taker_commission_rate: Taker fee rate
        settlement_time: Settlement time
        underlying_asset_id: Underlying asset ID
        underlying_asset_symbol: Underlying asset symbol
        quoting_asset_id: Quoting asset ID
        quoting_asset_symbol: Quoting asset symbol
        settling_asset_id: Settling asset ID
        settling_asset_symbol: Settling asset symbol
    """
    
    id: int
    symbol: str
    description: Optional[str] = None
    contract_type: Optional[str] = None
    contract_value: Optional[str] = None
    tick_size: Optional[str] = None
    maker_commission_rate: Optional[str] = None
    taker_commission_rate: Optional[str] = None
    settlement_time: Optional[str] = None
    underlying_asset_id: Optional[int] = None
    underlying_asset_symbol: Optional[str] = None
    quoting_asset_id: Optional[int] = None
    quoting_asset_symbol: Optional[str] = None
    settling_asset_id: Optional[int] = None
    settling_asset_symbol: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        """Create Product instance from API response dictionary."""
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        kwargs = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Product instance to dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class Fill:
    """
    Represents a trade fill on Delta Exchange.
    
    Attributes:
        id: Fill ID
        order_id: Associated order ID
        product_id: Product ID
        product_symbol: Product symbol
        side: Trade side (buy/sell)
        size: Fill size
        price: Fill price
        role: Trade role (maker/taker)
        commission: Commission paid
        fill_type: Type of fill
        created_at: Timestamp when fill occurred
        settling_asset_id: Settling asset ID
        settling_asset_symbol: Settling asset symbol
        meta_data: Additional metadata
    """
    
    id: str
    order_id: str
    product_id: int
    product_symbol: str
    side: OrderSide
    size: int
    price: str
    role: Role
    commission: str
    fill_type: FillType
    created_at: str
    settling_asset_id: Optional[int] = None
    settling_asset_symbol: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Fill":
        """Create Fill instance from API response dictionary."""
        kwargs = data.copy()
        
        if "side" in kwargs and kwargs["side"]:
            kwargs["side"] = OrderSide(kwargs["side"])
        
        if "role" in kwargs and kwargs["role"]:
            kwargs["role"] = Role(kwargs["role"])
        
        if "fill_type" in kwargs and kwargs["fill_type"]:
            kwargs["fill_type"] = FillType(kwargs["fill_type"])
        
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        return cls(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Fill instance to dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Enum):
                    result[key] = value.value
                else:
                    result[key] = value
        return result


@dataclass
class OrderBookLevel:
    """
    Represents a single level in the order book.
    
    Attributes:
        price: Price level
        size: Size at this level
        depth: Cumulative depth up to this level
    """
    
    price: str
    size: int
    depth: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderBookLevel":
        """Create OrderBookLevel instance from API response dictionary."""
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert OrderBookLevel instance to dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class OrderBook:
    """
    Represents an L2 order book on Delta Exchange.
    
    Attributes:
        symbol: Product symbol
        buy: List of buy levels
        sell: List of sell levels
        last_updated_at: Last update timestamp (microseconds)
    """
    
    symbol: str
    buy: List[OrderBookLevel]
    sell: List[OrderBookLevel]
    last_updated_at: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OrderBook":
        """Create OrderBook instance from API response dictionary."""
        kwargs = data.copy()
        
        if "buy" in kwargs:
            kwargs["buy"] = [OrderBookLevel.from_dict(level) for level in kwargs["buy"]]
        
        if "sell" in kwargs:
            kwargs["sell"] = [OrderBookLevel.from_dict(level) for level in kwargs["sell"]]
        
        return cls(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert OrderBook instance to dictionary."""
        return {
            "symbol": self.symbol,
            "buy": [level.to_dict() for level in self.buy],
            "sell": [level.to_dict() for level in self.sell],
            "last_updated_at": self.last_updated_at,
        }


@dataclass
class Trade:
    """
    Represents a public trade on Delta Exchange.
    
    Attributes:
        id: Trade ID
        symbol: Product symbol
        price: Trade price
        size: Trade size
        side: Trade side (buy/sell)
        timestamp: Trade timestamp
    """
    
    id: str
    symbol: str
    price: str
    size: int
    side: OrderSide
    timestamp: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trade":
        """Create Trade instance from API response dictionary."""
        kwargs = data.copy()
        
        if "side" in kwargs and kwargs["side"]:
            kwargs["side"] = OrderSide(kwargs["side"])
        
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        return cls(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Trade instance to dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, Enum):
                    result[key] = value.value
                else:
                    result[key] = value
        return result


# Fix missing import
from enum import Enum

