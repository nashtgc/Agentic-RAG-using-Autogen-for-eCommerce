"""Order Assistant Agent using Autogen."""

from typing import Annotated, Optional
import autogen

from ..data.orders import Order, OrderStatus, SAMPLE_ORDERS


class OrderAssistantAgent:
    """Agent for handling order-related queries."""

    def __init__(
        self,
        orders: Optional[list[Order]] = None,
        llm_config: Optional[dict] = None,
    ):
        """Initialize the Order Assistant Agent.

        Args:
            orders: List of orders to work with. Uses sample orders if not provided.
            llm_config: Configuration for the LLM.
        """
        self.orders = {order.id: order for order in (orders or SAMPLE_ORDERS)}
        self.customer_orders: dict[str, list[str]] = {}

        # Build customer orders index
        for order in self.orders.values():
            if order.customer_id not in self.customer_orders:
                self.customer_orders[order.customer_id] = []
            self.customer_orders[order.customer_id].append(order.id)

        self.llm_config = llm_config or self._default_llm_config()

        # Create the assistant agent
        self.agent = autogen.AssistantAgent(
            name="OrderAssistantAgent",
            system_message=self._get_system_message(),
            llm_config=self.llm_config,
        )

        # Register order functions
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
        return """You are an Order Assistant Agent for an eCommerce platform.
Your role is to help customers with their orders.

You have access to the following tools:
1. get_order_status: Get the current status of an order
2. get_order_details: Get full details of an order
3. get_customer_orders: List all orders for a customer
4. track_shipment: Get tracking information for an order

When helping customers:
- Always verify the order ID before providing information
- Be clear about order statuses and expected timelines
- Provide tracking information when available
- If there are issues, suggest contacting customer support

Order statuses explained:
- Pending: Order received, awaiting confirmation
- Confirmed: Payment confirmed, preparing to process
- Processing: Order is being prepared
- Shipped: Order has been shipped
- Delivered: Order has been delivered
- Cancelled: Order was cancelled"""

    def _register_functions(self) -> None:
        """Register callable functions for the agent."""

        @self.agent.register_for_llm(description="Get the current status of an order")
        def get_order_status(
            order_id: Annotated[str, "The order ID to check"],
        ) -> str:
            """Get order status."""
            order = self.orders.get(order_id)
            if order:
                status_info = {
                    OrderStatus.PENDING: "Your order is pending confirmation.",
                    OrderStatus.CONFIRMED: "Your order has been confirmed and will be processed soon.",
                    OrderStatus.PROCESSING: "Your order is currently being processed and prepared for shipping.",
                    OrderStatus.SHIPPED: f"Your order has been shipped! Tracking number: {order.tracking_number or 'Not available yet'}",
                    OrderStatus.DELIVERED: "Your order has been delivered!",
                    OrderStatus.CANCELLED: "This order has been cancelled.",
                }
                return f"**Order {order_id}**\n\nStatus: {order.status.value.title()}\n{status_info.get(order.status, '')}"
            return f"Order '{order_id}' not found. Please check the order ID and try again."

        @self.agent.register_for_llm(description="Get full details of an order")
        def get_order_details(
            order_id: Annotated[str, "The order ID to look up"],
        ) -> str:
            """Get full order details."""
            order = self.orders.get(order_id)
            if order:
                output = f"**Order Details: {order_id}**\n\n"
                output += f"- **Customer**: {order.customer_name}\n"
                output += f"- **Status**: {order.status.value.title()}\n"
                output += f"- **Order Date**: {order.created_at.strftime('%B %d, %Y at %I:%M %p')}\n"
                output += f"- **Last Updated**: {order.updated_at.strftime('%B %d, %Y at %I:%M %p')}\n\n"
                output += "**Items**:\n"
                for item in order.items:
                    output += f"  - {item.product_name} x{item.quantity} @ ${item.unit_price:.2f} = ${item.total_price:.2f}\n"
                output += f"\n**Total**: ${order.total_amount:.2f}\n"
                output += f"\n**Shipping Address**:\n{order.shipping_address}\n"
                if order.tracking_number:
                    output += f"\n**Tracking Number**: {order.tracking_number}"
                return output
            return f"Order '{order_id}' not found. Please check the order ID and try again."

        @self.agent.register_for_llm(description="List all orders for a customer")
        def get_customer_orders(
            customer_id: Annotated[str, "The customer ID to look up"],
        ) -> str:
            """Get all orders for a customer."""
            order_ids = self.customer_orders.get(customer_id, [])
            if order_ids:
                output = f"**Orders for Customer {customer_id}**\n\n"
                for order_id in order_ids:
                    order = self.orders[order_id]
                    output += f"- **{order_id}**: {order.status.value.title()} - ${order.total_amount:.2f}\n"
                    output += f"  Ordered: {order.created_at.strftime('%B %d, %Y')}\n\n"
                return output
            return f"No orders found for customer '{customer_id}'."

        @self.agent.register_for_llm(description="Get tracking information for a shipped order")
        def track_shipment(
            order_id: Annotated[str, "The order ID to track"],
        ) -> str:
            """Get shipment tracking information."""
            order = self.orders.get(order_id)
            if not order:
                return f"Order '{order_id}' not found."

            if order.status == OrderStatus.PENDING:
                return f"Order {order_id} is pending and has not been shipped yet."
            elif order.status == OrderStatus.CONFIRMED:
                return f"Order {order_id} is confirmed but not yet shipped. Estimated ship date: within 1-2 business days."
            elif order.status == OrderStatus.PROCESSING:
                return f"Order {order_id} is being processed. It should ship within 24 hours."
            elif order.status == OrderStatus.SHIPPED:
                return f"""**Shipment Tracking for Order {order_id}**

- **Tracking Number**: {order.tracking_number}
- **Status**: In Transit
- **Shipped From**: Main Warehouse
- **Destination**: {order.shipping_address}

**Tracking Link**: https://track.example.com/{order.tracking_number}

Please allow 24-48 hours for tracking updates to appear after shipment."""
            elif order.status == OrderStatus.DELIVERED:
                return f"""**Order {order_id} - Delivered**

- **Tracking Number**: {order.tracking_number}
- **Delivered To**: {order.shipping_address}
- **Delivery Date**: {order.updated_at.strftime('%B %d, %Y')}

If you did not receive your package, please contact customer support."""
            else:
                return f"Order {order_id} was cancelled and will not be shipped."

    def get_agent(self) -> autogen.AssistantAgent:
        """Get the underlying Autogen agent."""
        return self.agent
