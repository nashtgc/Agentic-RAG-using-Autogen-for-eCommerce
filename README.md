# Agentic RAG using Autogen for eCommerce

A multi-agent Retrieval-Augmented Generation (RAG) system built with [Autogen](https://github.com/microsoft/autogen) for eCommerce customer support. This system uses multiple specialized AI agents to handle product searches, order management, and customer support inquiries.

## Features

- **Product Search Agent**: RAG-powered product search using ChromaDB vector store
- **Customer Support Agent**: Handles FAQs, return policies, shipping information
- **Order Assistant Agent**: Manages order tracking, status updates, and order details
- **Multi-Agent Collaboration**: Agents work together via Autogen's GroupChat
- **Configurable LLM**: Supports OpenAI GPT models with customizable settings

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Customer Interface                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GroupChat Manager                         │
│              (Autogen Agent Orchestration)                   │
└─────────────────────────────────────────────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Product Search │ │ Customer Support│ │ Order Assistant │
│     Agent       │ │     Agent       │ │     Agent       │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ - RAG Search    │ │ - FAQ Database  │ │ - Order Status  │
│ - Product Info  │ │ - Return Policy │ │ - Order Details │
│ - Categories    │ │ - Shipping Info │ │ - Tracking      │
└─────────────────┘ └─────────────────┘ └─────────────────┘
         │
         ▼
┌─────────────────┐
│  ChromaDB       │
│  Vector Store   │
└─────────────────┘
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nashtgc/Agentic-RAG-using-Autogen-for-eCommerce.git
cd Agentic-RAG-using-Autogen-for-eCommerce
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Configuration

Create a `.env` file with the following settings:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# LLM Settings
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# ChromaDB Settings
CHROMA_COLLECTION=products
CHROMA_PERSIST_DIR=  # Leave empty for in-memory storage

# Debug Mode
DEBUG=false
```

## Usage

### Basic Usage

Run the main application:

```bash
python -m src.main
```

### Programmatic Usage

```python
from src.main import ECommerceRAGSystem

# Create the system
system = ECommerceRAGSystem()

# Start a conversation
system.chat("I'm looking for wireless headphones under $200")

# Or chat with a specific agent
system.single_agent_chat("What's my order status for ORD-10001?", agent_type="order")
```

### Available Agent Types

- `product`: Product search and recommendations using RAG
- `support`: Customer support, FAQs, policies
- `order`: Order tracking and management

## Project Structure

```
Agentic-RAG-using-Autogen-for-eCommerce/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── main.py             # Main application entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── product_agent.py    # RAG-powered product search
│   │   ├── support_agent.py    # Customer support
│   │   └── order_agent.py      # Order management
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── vector_store.py     # ChromaDB vector store
│   │   └── retriever.py        # Product retriever
│   └── data/
│       ├── __init__.py
│       ├── products.py         # Product data models
│       └── orders.py           # Order data models
├── tests/
│   ├── __init__.py
│   ├── test_products.py
│   ├── test_orders.py
│   ├── test_rag.py
│   └── test_config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_rag.py
```

## Sample Data

The system comes with sample eCommerce data including:

**Products** (10 items):
- Wireless Bluetooth Headphones
- Smart Fitness Watch
- Organic Cotton T-Shirt
- Stainless Steel Water Bottle
- Laptop Backpack
- Wireless Phone Charger
- Running Shoes
- Coffee Maker
- Yoga Mat
- Bluetooth Speaker

**Orders** (4 sample orders):
- Various statuses: Pending, Processing, Shipped, Delivered
- Multiple customers with order history

## Example Queries

### Product Search
- "I need wireless headphones with good battery life"
- "Show me fitness equipment under $50"
- "What electronics do you have?"

### Customer Support
- "What's your return policy?"
- "How long does shipping take?"
- "What payment methods do you accept?"

### Order Management
- "Where is my order ORD-10001?"
- "What orders does customer CUST-001 have?"
- "Track my shipment for order ORD-10003"

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
