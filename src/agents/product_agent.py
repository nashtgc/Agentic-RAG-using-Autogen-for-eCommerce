"""Product Search Agent using Autogen with RAG capabilities."""

from typing import Annotated, Optional
import autogen

from ..rag.retriever import ProductRetriever


class ProductSearchAgent:
    """Agent for searching and retrieving product information using RAG."""

    def __init__(
        self,
        retriever: ProductRetriever,
        llm_config: Optional[dict] = None,
    ):
        """Initialize the Product Search Agent.

        Args:
            retriever: Product retriever for RAG-based search.
            llm_config: Configuration for the LLM.
        """
        self.retriever = retriever
        self.llm_config = llm_config or self._default_llm_config()

        # Create the assistant agent
        self.agent = autogen.AssistantAgent(
            name="ProductSearchAgent",
            system_message=self._get_system_message(),
            llm_config=self.llm_config,
        )

        # Register the search functions
        self._register_functions()

    def _default_llm_config(self) -> dict:
        """Get default LLM configuration."""
        return {
            "config_list": [
                {
                    "model": "gpt-4",
                    "api_key": "YOUR_API_KEY",  # Should be set via environment
                }
            ],
            "temperature": 0.7,
        }

    def _get_system_message(self) -> str:
        """Get the system message for the agent."""
        return """You are a helpful Product Search Agent for an eCommerce platform.
Your role is to help customers find products based on their queries.

You have access to the following tools:
1. search_products: Search for products by query, with optional category filter
2. get_product_details: Get detailed information about a specific product
3. get_categories: List all available product categories

When helping customers:
- Understand their needs and preferences
- Use the search_products function to find relevant items
- Provide clear and helpful product recommendations
- Include prices and key features in your responses
- Ask clarifying questions if the query is too vague

Always be friendly, professional, and helpful."""

    def _register_functions(self) -> None:
        """Register callable functions for the agent."""

        @self.agent.register_for_llm(description="Search for products matching a query")
        def search_products(
            query: Annotated[str, "The search query to find products"],
            category: Annotated[Optional[str], "Optional category to filter results"] = None,
            top_k: Annotated[int, "Number of results to return"] = 5,
        ) -> str:
            """Search for products in the catalog."""
            results = self.retriever.retrieve(query=query, top_k=top_k, category=category)
            return self.retriever.format_results_for_agent(results)

        @self.agent.register_for_llm(description="Get detailed information about a product")
        def get_product_details(
            product_id: Annotated[str, "The product ID to look up"],
        ) -> str:
            """Get details for a specific product."""
            details = self.retriever.get_product_details(product_id)
            if details:
                output = f"**{details['name']}**\n\n"
                output += f"- **ID**: {details['id']}\n"
                output += f"- **Description**: {details['description']}\n"
                output += f"- **Category**: {details['category']}\n"
                output += f"- **Price**: ${details['price']:.2f} {details['currency']}\n"
                output += f"- **Brand**: {details['brand'] or 'N/A'}\n"
                output += f"- **In Stock**: {'Yes' if details['in_stock'] else 'No'}\n"
                output += f"- **Stock Quantity**: {details['stock_quantity']}\n"
                if details['attributes']:
                    output += "- **Attributes**:\n"
                    for key, value in details['attributes'].items():
                        output += f"  - {key}: {value}\n"
                return output
            return f"Product with ID '{product_id}' not found."

        @self.agent.register_for_llm(description="Get all available product categories")
        def get_categories() -> str:
            """Get all product categories."""
            categories = self.retriever.get_categories()
            if categories:
                return "Available categories:\n" + "\n".join(f"- {cat}" for cat in categories)
            return "No categories available."

    def get_agent(self) -> autogen.AssistantAgent:
        """Get the underlying Autogen agent."""
        return self.agent
