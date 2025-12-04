"""Tests for vector store and retriever."""

import pytest

from src.rag.vector_store import ProductVectorStore
from src.rag.retriever import ProductRetriever
from src.data.products import Product, SAMPLE_PRODUCTS


class TestProductVectorStore:
    """Test cases for ProductVectorStore."""

    @pytest.fixture
    def vector_store(self):
        """Create a fresh vector store for each test."""
        store = ProductVectorStore(collection_name="test_products")
        return store

    @pytest.fixture
    def loaded_vector_store(self, vector_store):
        """Create a vector store with sample data loaded."""
        vector_store.load_sample_data()
        return vector_store

    def test_vector_store_creation(self, vector_store):
        """Test creating a vector store."""
        assert vector_store.count() == 0

    def test_add_products(self, vector_store):
        """Test adding products to the store."""
        products = SAMPLE_PRODUCTS[:3]
        vector_store.add_products(products)
        assert vector_store.count() == 3

    def test_load_sample_data(self, vector_store):
        """Test loading sample data."""
        vector_store.load_sample_data()
        assert vector_store.count() == len(SAMPLE_PRODUCTS)

    def test_search_products(self, loaded_vector_store):
        """Test searching for products."""
        results = loaded_vector_store.search("wireless headphones", n_results=3)
        assert len(results) > 0
        assert len(results) <= 3

    def test_search_with_category_filter(self, loaded_vector_store):
        """Test searching with category filter."""
        results = loaded_vector_store.search("electronics", n_results=10, category_filter="Electronics")
        for result in results:
            assert result["metadata"]["category"] == "Electronics"

    def test_get_product_by_id(self, loaded_vector_store):
        """Test getting product by ID."""
        product = loaded_vector_store.get_product_by_id("prod-001")
        assert product is not None
        assert product.id == "prod-001"

    def test_get_nonexistent_product(self, loaded_vector_store):
        """Test getting a product that doesn't exist."""
        product = loaded_vector_store.get_product_by_id("nonexistent")
        assert product is None

    def test_get_all_categories(self, loaded_vector_store):
        """Test getting all categories."""
        categories = loaded_vector_store.get_all_categories()
        assert len(categories) > 0
        assert "Electronics" in categories


class TestProductRetriever:
    """Test cases for ProductRetriever."""

    @pytest.fixture
    def retriever(self):
        """Create a retriever with sample data."""
        store = ProductVectorStore(collection_name="test_retriever")
        store.load_sample_data()
        return ProductRetriever(store)

    def test_retrieve_products(self, retriever):
        """Test retrieving products."""
        results = retriever.retrieve("running shoes", top_k=3)
        assert len(results) > 0
        assert len(results) <= 3

    def test_retrieve_with_category(self, retriever):
        """Test retrieving with category filter."""
        results = retriever.retrieve("items", top_k=5, category="Electronics")
        for result in results:
            assert result["category"] == "Electronics"

    def test_get_product_details(self, retriever):
        """Test getting product details."""
        details = retriever.get_product_details("prod-002")
        assert details is not None
        assert details["id"] == "prod-002"
        assert "name" in details
        assert "price" in details
        assert "in_stock" in details

    def test_get_categories(self, retriever):
        """Test getting categories."""
        categories = retriever.get_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0

    def test_format_results_empty(self, retriever):
        """Test formatting empty results."""
        formatted = retriever.format_results_for_agent([])
        assert "No products found" in formatted

    def test_format_results_with_products(self, retriever):
        """Test formatting results with products."""
        results = retriever.retrieve("headphones", top_k=2)
        formatted = retriever.format_results_for_agent(results)
        assert "Found the following products" in formatted
