"""
Delta Exchange Custom Exceptions

This module defines all custom exception classes used throughout the Delta Exchange
Python client library. These exceptions provide clear, specific error information
for different types of failures.
"""


class DeltaExchangeException(Exception):
    """
    Base exception class for all Delta Exchange errors.
    
    All custom exceptions in this library inherit from this base class,
    allowing users to catch all Delta Exchange-related errors with a single
    except clause if desired.
    
    Attributes:
        message (str): Human-readable error message
        error_code (str, optional): API error code if available
        status_code (int, optional): HTTP status code if applicable
    """
    
    def __init__(self, message: str, error_code: str = None, status_code: int = None):
        """
        Initialize DeltaExchangeException.
        
        Args:
            message: Human-readable error message
            error_code: Optional API error code from Delta Exchange
            status_code: Optional HTTP status code
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)
    
    def __str__(self):
        """Return string representation of the exception."""
        error_parts = [self.message]
        if self.error_code:
            error_parts.append(f"Error Code: {self.error_code}")
        if self.status_code:
            error_parts.append(f"Status Code: {self.status_code}")
        return " | ".join(error_parts)


class AuthenticationError(DeltaExchangeException):
    """
    Raised when API authentication fails.
    
    This exception is raised when:
    - Invalid API key or secret is provided
    - Signature generation fails
    - Signature validation fails on the server
    - API credentials have expired or been revoked
    
    Example:
        >>> try:
        ...     client.place_order(...)
        ... except AuthenticationError as e:
        ...     print(f"Authentication failed: {e}")
    """
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, **kwargs)


class OrderError(DeltaExchangeException):
    """
    Raised when an order operation fails.
    
    This exception is raised when:
    - Order placement fails
    - Order cancellation fails
    - Order editing fails
    - Invalid order parameters are provided
    - Insufficient balance for order
    
    Example:
        >>> try:
        ...     client.place_order(symbol="BTCUSD", side="buy", size=1000000)
        ... except OrderError as e:
        ...     print(f"Order failed: {e}")
    """
    
    def __init__(self, message: str = "Order operation failed", **kwargs):
        super().__init__(message, **kwargs)


class APIError(DeltaExchangeException):
    """
    Raised when a general API error occurs.
    
    This exception is raised when:
    - API returns an error response
    - Invalid request parameters
    - Server-side errors (5xx)
    - Request validation fails
    
    Example:
        >>> try:
        ...     client.get_positions(product_id=-1)
        ... except APIError as e:
        ...     print(f"API error: {e}")
    """
    
    def __init__(self, message: str = "API request failed", **kwargs):
        super().__init__(message, **kwargs)


class WebSocketError(DeltaExchangeException):
    """
    Raised when a WebSocket operation fails.
    
    This exception is raised when:
    - WebSocket connection fails
    - WebSocket authentication fails
    - Subscription to channel fails
    - Message sending fails
    - Connection is unexpectedly closed
    
    Example:
        >>> try:
        ...     await ws_client.subscribe_ticker(["BTCUSD"])
        ... except WebSocketError as e:
        ...     print(f"WebSocket error: {e}")
    """
    
    def __init__(self, message: str = "WebSocket operation failed", **kwargs):
        super().__init__(message, **kwargs)


class RateLimitError(DeltaExchangeException):
    """
    Raised when API rate limits are exceeded.
    
    This exception is raised when:
    - Too many requests in a short time period
    - Rate limit headers indicate throttling
    - Server returns 429 (Too Many Requests)
    
    Attributes:
        retry_after (int, optional): Seconds to wait before retrying
    
    Example:
        >>> try:
        ...     for i in range(1000):
        ...         client.place_order(...)
        ... except RateLimitError as e:
        ...     print(f"Rate limited. Retry after {e.retry_after} seconds")
        ...     time.sleep(e.retry_after)
    """
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None, **kwargs):
        """
        Initialize RateLimitError.
        
        Args:
            message: Human-readable error message
            retry_after: Optional number of seconds to wait before retrying
            **kwargs: Additional arguments passed to base exception
        """
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
    
    def __str__(self):
        """Return string representation including retry_after if available."""
        base_str = super().__str__()
        if self.retry_after:
            return f"{base_str} | Retry After: {self.retry_after}s"
        return base_str


class ValidationError(DeltaExchangeException):
    """
    Raised when input validation fails.
    
    This exception is raised when:
    - Required parameters are missing
    - Parameter values are invalid
    - Parameter types are incorrect
    - Business logic validation fails
    
    Example:
        >>> try:
        ...     client.place_order(symbol="BTCUSD", side="invalid")
        ... except ValidationError as e:
        ...     print(f"Validation error: {e}")
    """
    
    def __init__(self, message: str = "Validation failed", **kwargs):
        super().__init__(message, **kwargs)


class NetworkError(DeltaExchangeException):
    """
    Raised when network-related errors occur.
    
    This exception is raised when:
    - Connection timeout
    - DNS resolution fails
    - Network is unreachable
    - SSL/TLS errors
    
    Example:
        >>> try:
        ...     client.get_positions()
        ... except NetworkError as e:
        ...     print(f"Network error: {e}")
    """
    
    def __init__(self, message: str = "Network error occurred", **kwargs):
        super().__init__(message, **kwargs)

