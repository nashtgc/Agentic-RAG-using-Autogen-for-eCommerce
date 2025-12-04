"""Tests for order data models."""

import pytest
from datetime import datetime

from src.data.orders import Order, OrderItem, OrderStatus, SAMPLE_ORDERS


class TestOrderItem:
    """Test cases for OrderItem model."""

    def test_order_item_creation(self):
        """Test creating an order item."""
        item = OrderItem(
            product_id="prod-001",
            product_name="Test Product",
            quantity=2,
            unit_price=49.99,
        )
        assert item.product_id == "prod-001"
        assert item.quantity == 2
        assert item.unit_price == 49.99

    def test_order_item_total_price(self):
        """Test order item total price calculation."""
        item = OrderItem(
            product_id="prod-001",
            product_name="Test Product",
            quantity=3,
            unit_price=10.00,
        )
        assert item.total_price == 30.00


class TestOrder:
    """Test cases for Order model."""

    def test_order_creation(self):
        """Test creating an order."""
        order = Order(
            id="ORD-TEST",
            customer_id="CUST-001",
            customer_name="Test Customer",
            items=[
                OrderItem(
                    product_id="prod-001",
                    product_name="Product 1",
                    quantity=1,
                    unit_price=100.00,
                )
            ],
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            shipping_address="123 Test St",
        )
        assert order.id == "ORD-TEST"
        assert order.status == OrderStatus.PENDING
        assert order.total_amount == 100.00

    def test_order_total_amount(self):
        """Test order total amount calculation."""
        order = Order(
            id="ORD-TEST",
            customer_id="CUST-001",
            customer_name="Test Customer",
            items=[
                OrderItem(
                    product_id="prod-001",
                    product_name="Product 1",
                    quantity=2,
                    unit_price=50.00,
                ),
                OrderItem(
                    product_id="prod-002",
                    product_name="Product 2",
                    quantity=1,
                    unit_price=25.00,
                ),
            ],
            status=OrderStatus.CONFIRMED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            shipping_address="456 Test Ave",
        )
        assert order.total_amount == 125.00

    def test_order_summary(self):
        """Test order summary generation."""
        order = Order(
            id="ORD-TEST",
            customer_id="CUST-001",
            customer_name="Test Customer",
            items=[
                OrderItem(
                    product_id="prod-001",
                    product_name="Test Product",
                    quantity=1,
                    unit_price=99.99,
                )
            ],
            status=OrderStatus.SHIPPED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            shipping_address="789 Test Blvd",
            tracking_number="TRK12345",
        )
        summary = order.to_summary()
        assert "ORD-TEST" in summary
        assert "Test Product" in summary
        assert "shipped" in summary
        assert "TRK12345" in summary

    def test_sample_orders_exist(self):
        """Test that sample orders are available."""
        assert len(SAMPLE_ORDERS) > 0
        assert all(isinstance(o, Order) for o in SAMPLE_ORDERS)

    def test_order_status_values(self):
        """Test all order status values."""
        statuses = [s.value for s in OrderStatus]
        expected = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]
        assert set(statuses) == set(expected)
