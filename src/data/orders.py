"""Order data models and sample orders."""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class OrderStatus(str, Enum):
    """Order status enumeration."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    """Individual item in an order."""

    product_id: str
    product_name: str
    quantity: int
    unit_price: float

    @property
    def total_price(self) -> float:
        """Calculate total price for this item."""
        return self.quantity * self.unit_price


class Order(BaseModel):
    """Order model for eCommerce system."""

    id: str
    customer_id: str
    customer_name: str
    items: list[OrderItem]
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    shipping_address: str
    tracking_number: Optional[str] = None

    @property
    def total_amount(self) -> float:
        """Calculate total order amount."""
        return sum(item.total_price for item in self.items)

    def to_summary(self) -> str:
        """Generate order summary text."""
        items_text = ", ".join(
            f"{item.product_name} x{item.quantity}" for item in self.items
        )
        return (
            f"Order {self.id}: {items_text}. "
            f"Total: ${self.total_amount:.2f}. "
            f"Status: {self.status.value}. "
            f"Tracking: {self.tracking_number or 'Not available yet'}."
        )


# Sample orders for demonstration
SAMPLE_ORDERS = [
    Order(
        id="ORD-10001",
        customer_id="CUST-001",
        customer_name="John Doe",
        items=[
            OrderItem(
                product_id="prod-001",
                product_name="Wireless Bluetooth Headphones",
                quantity=1,
                unit_price=149.99,
            ),
            OrderItem(
                product_id="prod-006",
                product_name="Wireless Phone Charger",
                quantity=2,
                unit_price=24.99,
            ),
        ],
        status=OrderStatus.SHIPPED,
        created_at=datetime(2024, 1, 15, 10, 30),
        updated_at=datetime(2024, 1, 17, 14, 20),
        shipping_address="123 Main St, New York, NY 10001",
        tracking_number="TRK123456789",
    ),
    Order(
        id="ORD-10002",
        customer_id="CUST-002",
        customer_name="Jane Smith",
        items=[
            OrderItem(
                product_id="prod-003",
                product_name="Organic Cotton T-Shirt",
                quantity=3,
                unit_price=29.99,
            ),
        ],
        status=OrderStatus.PROCESSING,
        created_at=datetime(2024, 1, 18, 9, 15),
        updated_at=datetime(2024, 1, 18, 9, 15),
        shipping_address="456 Oak Ave, Los Angeles, CA 90001",
    ),
    Order(
        id="ORD-10003",
        customer_id="CUST-003",
        customer_name="Bob Johnson",
        items=[
            OrderItem(
                product_id="prod-002",
                product_name="Smart Fitness Watch",
                quantity=1,
                unit_price=199.99,
            ),
            OrderItem(
                product_id="prod-007",
                product_name="Running Shoes",
                quantity=1,
                unit_price=119.99,
            ),
            OrderItem(
                product_id="prod-009",
                product_name="Yoga Mat",
                quantity=1,
                unit_price=39.99,
            ),
        ],
        status=OrderStatus.DELIVERED,
        created_at=datetime(2024, 1, 10, 16, 45),
        updated_at=datetime(2024, 1, 14, 11, 30),
        shipping_address="789 Pine Rd, Chicago, IL 60601",
        tracking_number="TRK987654321",
    ),
    Order(
        id="ORD-10004",
        customer_id="CUST-001",
        customer_name="John Doe",
        items=[
            OrderItem(
                product_id="prod-008",
                product_name="Coffee Maker",
                quantity=1,
                unit_price=89.99,
            ),
        ],
        status=OrderStatus.PENDING,
        created_at=datetime(2024, 1, 20, 8, 0),
        updated_at=datetime(2024, 1, 20, 8, 0),
        shipping_address="123 Main St, New York, NY 10001",
    ),
]
