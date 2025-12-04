"""Tests for product data models."""

import pytest

from src.data.products import Product, SAMPLE_PRODUCTS


class TestProduct:
    """Test cases for Product model."""

    def test_product_creation(self):
        """Test creating a product."""
        product = Product(
            id="test-001",
            name="Test Product",
            description="A test product",
            category="Test Category",
            price=99.99,
            stock_quantity=10,
        )
        assert product.id == "test-001"
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.currency == "USD"

    def test_product_to_text(self):
        """Test product text representation."""
        product = Product(
            id="test-001",
            name="Test Product",
            description="A test description",
            category="Electronics",
            price=49.99,
            stock_quantity=5,
            brand="TestBrand",
        )
        text = product.to_text()
        assert "Test Product" in text
        assert "TestBrand" in text
        assert "Electronics" in text
        assert "49.99" in text
        assert "Yes" in text  # In stock

    def test_product_out_of_stock(self):
        """Test out of stock product."""
        product = Product(
            id="test-002",
            name="Out of Stock Item",
            description="This item is out of stock",
            category="Test",
            price=29.99,
            stock_quantity=0,
        )
        text = product.to_text()
        assert "No" in text  # Not in stock

    def test_sample_products_exist(self):
        """Test that sample products are available."""
        assert len(SAMPLE_PRODUCTS) > 0
        assert all(isinstance(p, Product) for p in SAMPLE_PRODUCTS)

    def test_sample_products_have_required_fields(self):
        """Test that all sample products have required fields."""
        for product in SAMPLE_PRODUCTS:
            assert product.id
            assert product.name
            assert product.description
            assert product.category
            assert product.price > 0
            assert product.stock_quantity >= 0
