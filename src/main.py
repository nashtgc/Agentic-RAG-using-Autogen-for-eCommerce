"""Main application for Agentic RAG eCommerce system using Autogen."""

from typing import Optional
import autogen

from .config import AppConfig, load_config, get_llm_config_for_autogen
from .agents import ProductSearchAgent, CustomerSupportAgent, OrderAssistantAgent
from .rag import ProductVectorStore, ProductRetriever
from .data import SAMPLE_PRODUCTS, SAMPLE_ORDERS


class ECommerceRAGSystem:
    """Multi-agent eCommerce RAG system using Autogen."""

    def __init__(self, config: Optional[AppConfig] = None):
        """Initialize the eCommerce RAG system.

        Args:
            config: Application configuration. If None, loads from environment.
        """
        self.config = config or load_config()
        self.llm_config = get_llm_config_for_autogen(self.config)

        # Initialize vector store and retriever
        self.vector_store = ProductVectorStore(
            collection_name=self.config.vector_store.collection_name,
            persist_directory=self.config.vector_store.persist_directory,
        )
        self.retriever = ProductRetriever(self.vector_store)

        # Load sample data
        self.vector_store.load_sample_data()

        # Initialize agents
        self._init_agents()

        # Create the group chat manager
        self._init_group_chat()

    def _init_agents(self) -> None:
        """Initialize all agents."""
        # Product search agent with RAG
        self.product_agent = ProductSearchAgent(
            retriever=self.retriever,
            llm_config=self.llm_config,
        )

        # Customer support agent
        self.support_agent = CustomerSupportAgent(
            llm_config=self.llm_config,
        )

        # Order assistant agent
        self.order_agent = OrderAssistantAgent(
            orders=SAMPLE_ORDERS,
            llm_config=self.llm_config,
        )

        # User proxy for human interaction
        self.user_proxy = autogen.UserProxyAgent(
            name="Customer",
            human_input_mode="ALWAYS",
            max_consecutive_auto_reply=10,
            code_execution_config=False,
            system_message="A customer interacting with the eCommerce support system.",
        )

    def _init_group_chat(self) -> None:
        """Initialize the group chat for multi-agent collaboration."""
        # Get all agents
        agents = [
            self.user_proxy,
            self.product_agent.get_agent(),
            self.support_agent.get_agent(),
            self.order_agent.get_agent(),
        ]

        # Create group chat
        self.group_chat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=20,
            speaker_selection_method="auto",
        )

        # Create manager
        self.manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.llm_config,
        )

    def chat(self, message: str) -> None:
        """Start a chat with the given message.

        Args:
            message: Initial message from the customer.
        """
        self.user_proxy.initiate_chat(
            self.manager,
            message=message,
        )

    def single_agent_chat(
        self,
        message: str,
        agent_type: str = "product",
    ) -> None:
        """Chat with a single agent instead of the group.

        Args:
            message: Message to send.
            agent_type: Type of agent to chat with (product, support, order).
        """
        agent_map = {
            "product": self.product_agent.get_agent(),
            "support": self.support_agent.get_agent(),
            "order": self.order_agent.get_agent(),
        }

        agent = agent_map.get(agent_type)
        if not agent:
            raise ValueError(f"Unknown agent type: {agent_type}")

        self.user_proxy.initiate_chat(
            agent,
            message=message,
        )


def create_demo_system() -> ECommerceRAGSystem:
    """Create a demo system with sample data.

    Returns:
        Configured ECommerceRAGSystem instance.
    """
    return ECommerceRAGSystem()


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("Welcome to the Agentic RAG eCommerce Support System")
    print("=" * 60)
    print("\nThis system uses multiple AI agents to help you with:")
    print("- Product search and recommendations")
    print("- Order tracking and management")
    print("- Customer support inquiries")
    print("\nType 'quit' or 'exit' to end the conversation.")
    print("=" * 60)

    try:
        system = create_demo_system()
        print("\n✓ System initialized successfully!")
        print(f"✓ Loaded {system.vector_store.count()} products into the catalog.")
        print("\nPlease enter your query:")

        # Start interactive session
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["quit", "exit"]:
                print("\nThank you for using our service. Goodbye!")
                break
            if user_input:
                system.chat(user_input)

    except KeyboardInterrupt:
        print("\n\nSession interrupted. Goodbye!")


if __name__ == "__main__":
    main()
