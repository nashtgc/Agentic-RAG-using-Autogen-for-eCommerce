"""Vector store for product embeddings using ChromaDB."""

import hashlib
from typing import Optional
import chromadb
from chromadb.config import Settings
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

from ..data.products import Product, SAMPLE_PRODUCTS


class SimpleEmbeddingFunction(EmbeddingFunction):
    """Simple hash-based embedding function for offline use.

    This provides basic embedding functionality without requiring
    external services or model downloads. For production, consider
    using OpenAI embeddings or sentence-transformers.
    """

    def __init__(self, dimension: int = 384):
        """Initialize the embedding function.

        Args:
            dimension: Dimension of the embedding vectors.
        """
        self._dimension = dimension
        self._name = "simple_hash_embedding"

    def name(self) -> str:
        """Return the name of this embedding function."""
        return self._name

    def __call__(self, input: Documents) -> Embeddings:
        """Generate embeddings for input texts.

        Args:
            input: List of texts to embed.

        Returns:
            List of embedding vectors.
        """
        return self.embed_documents(input)

    def embed_documents(self, input: Documents) -> Embeddings:
        """Embed documents for storage.

        Args:
            input: List of documents to embed.

        Returns:
            List of embedding vectors.
        """
        embeddings = []
        for text in input:
            embedding = self._text_to_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def embed_query(self, input: Documents) -> Embeddings:
        """Embed a query for retrieval.

        Args:
            input: List of query texts.

        Returns:
            List of embedding vectors.
        """
        return self.embed_documents(input)

    def _text_to_embedding(self, text: str) -> list[float]:
        """Convert text to a deterministic embedding vector.

        Uses a simple hash-based approach that creates consistent
        embeddings for the same text. Not suitable for semantic
        similarity but works for demonstration purposes.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector.
        """
        # Normalize text
        text = text.lower().strip()

        # Create multiple hashes for diversity
        embedding = []
        for i in range(self._dimension):
            # Create hash with different seeds
            hash_input = f"{text}_{i}"
            hash_bytes = hashlib.sha256(hash_input.encode()).digest()
            # Convert to float between -1 and 1
            value = (int.from_bytes(hash_bytes[:4], "big") / (2**32)) * 2 - 1
            embedding.append(value)

        return embedding


class ProductVectorStore:
    """Vector store for storing and retrieving product embeddings."""

    def __init__(
        self,
        collection_name: str = "products",
        persist_directory: Optional[str] = None,
        use_simple_embeddings: bool = True,
    ):
        """Initialize the vector store.

        Args:
            collection_name: Name of the ChromaDB collection.
            persist_directory: Directory to persist the database. If None, uses in-memory storage.
            use_simple_embeddings: Use simple hash-based embeddings (no internet required).
        """
        if persist_directory:
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(anonymized_telemetry=False),
            )
        else:
            self.client = chromadb.Client(
                settings=Settings(anonymized_telemetry=False),
            )

        # Use simple embeddings by default to avoid network calls
        embedding_function = SimpleEmbeddingFunction() if use_simple_embeddings else None

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "eCommerce product embeddings"},
            embedding_function=embedding_function,
        )
        self._products_cache: dict[str, Product] = {}

    def add_products(self, products: list[Product]) -> None:
        """Add products to the vector store.

        Args:
            products: List of products to add.
        """
        documents = []
        metadatas = []
        ids = []

        for product in products:
            documents.append(product.to_text())
            metadatas.append({
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "price": product.price,
                "brand": product.brand or "",
                "stock_quantity": product.stock_quantity,
            })
            ids.append(product.id)
            self._products_cache[product.id] = product

        # Upsert to handle duplicates
        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )

    def search(
        self,
        query: str,
        n_results: int = 5,
        category_filter: Optional[str] = None,
    ) -> list[dict]:
        """Search for products matching the query.

        Args:
            query: Search query text.
            n_results: Number of results to return.
            category_filter: Optional category to filter results.

        Returns:
            List of matching products with scores.
        """
        where_filter = None
        if category_filter:
            where_filter = {"category": category_filter}

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        products = []
        if results["ids"] and results["ids"][0]:
            for i, product_id in enumerate(results["ids"][0]):
                product_data = {
                    "id": product_id,
                    "document": results["documents"][0][i] if results["documents"] else "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                }
                products.append(product_data)

        return products

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get a product by its ID.

        Args:
            product_id: The product ID to look up.

        Returns:
            The Product if found, None otherwise.
        """
        return self._products_cache.get(product_id)

    def load_sample_data(self) -> None:
        """Load sample product data into the vector store."""
        self.add_products(SAMPLE_PRODUCTS)

    def get_all_categories(self) -> list[str]:
        """Get all unique product categories."""
        categories = set()
        for product in self._products_cache.values():
            categories.add(product.category)
        return sorted(list(categories))

    def count(self) -> int:
        """Get the number of products in the store."""
        return self.collection.count()
