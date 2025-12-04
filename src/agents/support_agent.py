"""Customer Support Agent using Autogen."""

from typing import Annotated, Optional
import autogen


class CustomerSupportAgent:
    """Agent for handling customer support queries."""

    def __init__(
        self,
        llm_config: Optional[dict] = None,
    ):
        """Initialize the Customer Support Agent.

        Args:
            llm_config: Configuration for the LLM.
        """
        self.llm_config = llm_config or self._default_llm_config()

        # FAQ database for common questions
        self.faq_database = self._get_faq_database()

        # Create the assistant agent
        self.agent = autogen.AssistantAgent(
            name="CustomerSupportAgent",
            system_message=self._get_system_message(),
            llm_config=self.llm_config,
        )

        # Register support functions
        self._register_functions()

    def _default_llm_config(self) -> dict:
        """Get default LLM configuration."""
        return {
            "config_list": [
                {
                    "model": "gpt-4",
                    "api_key": "YOUR_API_KEY",
                }
            ],
            "temperature": 0.7,
        }

    def _get_system_message(self) -> str:
        """Get the system message for the agent."""
        return """You are a friendly and helpful Customer Support Agent for an eCommerce platform.
Your role is to assist customers with their questions and concerns.

You have access to the following tools:
1. get_faq_answer: Look up answers to frequently asked questions
2. get_return_policy: Get information about the return policy
3. get_shipping_info: Get shipping information
4. create_support_ticket: Create a support ticket for issues that need escalation

When helping customers:
- Be empathetic and understanding
- Provide clear and accurate information
- If you can't answer a question, escalate by creating a support ticket
- Always thank customers for their patience

Common topics you handle:
- Shipping and delivery questions
- Return and refund policies
- Payment issues
- Account-related questions
- General product inquiries"""

    def _get_faq_database(self) -> dict:
        """Get the FAQ database."""
        return {
            "payment_methods": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, Apple Pay, and Google Pay.",
            "shipping_time": "Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days. Same-day delivery is available in select areas.",
            "return_period": "You can return most items within 30 days of delivery for a full refund. Items must be unused and in original packaging.",
            "track_order": "You can track your order by logging into your account and viewing your order history, or by using the tracking number sent to your email.",
            "cancel_order": "Orders can be cancelled within 1 hour of placement. After that, you may need to wait for delivery and then initiate a return.",
            "warranty": "Most electronics come with a 1-year manufacturer warranty. Extended warranty options are available at checkout.",
            "gift_wrapping": "Gift wrapping is available for $5.99 per item. You can select this option during checkout.",
            "international_shipping": "We ship to over 50 countries worldwide. International shipping rates and delivery times vary by destination.",
        }

    def _register_functions(self) -> None:
        """Register callable functions for the agent."""

        @self.agent.register_for_llm(description="Look up answer to a frequently asked question")
        def get_faq_answer(
            topic: Annotated[str, "The FAQ topic to look up"],
        ) -> str:
            """Get answer from FAQ database."""
            # Find matching FAQ
            topic_lower = topic.lower()
            for key, answer in self.faq_database.items():
                if key in topic_lower or any(word in topic_lower for word in key.split("_")):
                    return answer

            return "I couldn't find a specific FAQ for that topic. Let me help you with more details or create a support ticket if needed."

        @self.agent.register_for_llm(description="Get the store's return policy information")
        def get_return_policy() -> str:
            """Get return policy information."""
            return """**Return Policy**

Our return policy includes the following:

1. **30-Day Returns**: Most items can be returned within 30 days of delivery
2. **Condition**: Items must be unused and in original packaging
3. **Refund Method**: Refunds are processed to the original payment method
4. **Processing Time**: Refunds are processed within 5-7 business days after we receive the return
5. **Exceptions**: 
   - Final sale items cannot be returned
   - Personalized items cannot be returned
   - Intimate apparel must have tags attached

**How to Return**:
1. Log into your account
2. Go to Order History
3. Select the item to return
4. Print the prepaid shipping label
5. Drop off at any authorized shipping location

For questions about specific items, please contact our support team."""

        @self.agent.register_for_llm(description="Get shipping information and options")
        def get_shipping_info() -> str:
            """Get shipping information."""
            return """**Shipping Options**

We offer the following shipping options:

1. **Standard Shipping** (5-7 business days)
   - Free for orders over $50
   - $4.99 for orders under $50

2. **Express Shipping** (2-3 business days)
   - $12.99 flat rate
   - Free for orders over $100

3. **Same-Day Delivery** (select areas)
   - $19.99
   - Order by 12 PM local time
   - Available in major metropolitan areas

4. **International Shipping**
   - Rates vary by destination
   - Delivery in 7-21 business days
   - Customs fees may apply

**Order Tracking**:
- Tracking number sent via email once shipped
- Track online through your account or carrier website

**Note**: Delivery times are estimates and may vary during peak seasons."""

        @self.agent.register_for_llm(description="Create a support ticket for escalation")
        def create_support_ticket(
            subject: Annotated[str, "Brief subject of the issue"],
            description: Annotated[str, "Detailed description of the issue"],
            priority: Annotated[str, "Priority level: low, medium, or high"] = "medium",
        ) -> str:
            """Create a support ticket."""
            import random
            ticket_id = f"TKT-{random.randint(100000, 999999)}"  # noqa: S311

            return f"""**Support Ticket Created**

- **Ticket ID**: {ticket_id}
- **Subject**: {subject}
- **Priority**: {priority.capitalize()}
- **Status**: Open

Your ticket has been submitted and assigned to our support team.
Expected response time:
- High priority: 4-8 hours
- Medium priority: 24-48 hours
- Low priority: 2-3 business days

You will receive updates at your registered email address.
Please reference ticket ID {ticket_id} for any follow-up inquiries."""

    def get_agent(self) -> autogen.AssistantAgent:
        """Get the underlying Autogen agent."""
        return self.agent
