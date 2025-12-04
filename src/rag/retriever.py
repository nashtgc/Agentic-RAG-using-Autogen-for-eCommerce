"""Product retriever for RAG-based product search."""

from typing import Optional

from .vector_store import ProductVectorStore
from ..data.products import Product


class ProductRetriever:
    """Retriever for finding relevant products using RAG."""

    def __init__(self, vector_store: ProductVectorStore):
        """Initialize the retriever.

        Args:
            vector_store: The vector store containing product embeddings.
        """
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
    ) -> list[dict]:
        """Retrieve relevant products for a query.

        Args:
            query: The search query.
            top_k: Number of results to return.
            category: Optional category filter.

        Returns:
            List of relevant product information.
        """
        results = self.vector_store.search(
            query=query,
            n_results=top_k,
            category_filter=category,
        )

        # Format results for the agent
        formatted_results = []
        for result in results:
            metadata = result.get("metadata", {})
            formatted_results.append({
                "id": result["id"],
                "name": metadata.get("name", "Unknown"),
                "category": metadata.get("category", "Unknown"),
                "price": metadata.get("price", 0),
                "brand": metadata.get("brand", ""),
                "description": result.get("document", ""),
                "relevance_score": 1 - result.get("distance", 0),  # Convert distance to score
            })

        return formatted_results

    def get_product_details(self, product_id: str) -> Optional[dict]:
        """Get detailed information about a specific product.

        Args:
            product_id: The product ID.

        Returns:
            Product details or None if not found.
        """
        product = self.vector_store.get_product_by_id(product_id)
        if product:
            return {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "currency": product.currency,
                "stock_quantity": product.stock_quantity,
                "brand": product.brand,
                "attributes": product.attributes,
                "in_stock": product.stock_quantity > 0,
            }
        return None

    def get_categories(self) -> list[str]:
        """Get all available product categories."""
        return self.vector_store.get_all_categories()

    def format_results_for_agent(self, results: list[dict]) -> str:
        """Format search results as a string for the agent.

        Args:
            results: List of product search results.

        Returns:
            Formatted string of results.
        """
        if not results:
            return "No products found matching your query."

        output = "Found the following products:\n\n"
        for i, product in enumerate(results, 1):
            output += f"{i}. **{product['name']}**\n"
            output += f"   - ID: {product['id']}\n"
            output += f"   - Category: {product['category']}\n"
            output += f"   - Price: ${product['price']:.2f}\n"
            if product.get('brand'):
                output += f"   - Brand: {product['brand']}\n"
            output += f"   - Relevance: {product.get('relevance_score', 0):.2%}\n\n"

        return output
