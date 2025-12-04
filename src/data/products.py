"""Product data models and sample eCommerce products."""

from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    """Product model for eCommerce catalog."""

    id: str
    name: str
    description: str
    category: str
    price: float
    currency: str = "USD"
    stock_quantity: int
    brand: Optional[str] = None
    attributes: dict = {}

    def to_text(self) -> str:
        """Convert product to text representation for embeddings."""
        attrs = ", ".join(f"{k}: {v}" for k, v in self.attributes.items())
        return (
            f"Product: {self.name}. "
            f"Brand: {self.brand or 'N/A'}. "
            f"Category: {self.category}. "
            f"Description: {self.description}. "
            f"Price: {self.price} {self.currency}. "
            f"In Stock: {'Yes' if self.stock_quantity > 0 else 'No'}. "
            f"Attributes: {attrs if attrs else 'None'}."
        )


# Sample eCommerce products for demonstration
SAMPLE_PRODUCTS = [
    Product(
        id="prod-001",
        name="Wireless Bluetooth Headphones",
        description="Premium noise-canceling wireless headphones with 30-hour battery life, comfortable over-ear design, and crystal-clear audio quality.",
        category="Electronics",
        price=149.99,
        stock_quantity=50,
        brand="SoundMax",
        attributes={"color": "Black", "connectivity": "Bluetooth 5.0", "battery_life": "30 hours"},
    ),
    Product(
        id="prod-002",
        name="Smart Fitness Watch",
        description="Advanced fitness tracker with heart rate monitoring, GPS, sleep tracking, and water resistance up to 50 meters.",
        category="Electronics",
        price=199.99,
        stock_quantity=30,
        brand="FitTech",
        attributes={"color": "Silver", "display": "AMOLED", "water_resistance": "50m"},
    ),
    Product(
        id="prod-003",
        name="Organic Cotton T-Shirt",
        description="Soft and sustainable organic cotton t-shirt with a classic fit. Available in multiple colors and sizes.",
        category="Clothing",
        price=29.99,
        stock_quantity=200,
        brand="EcoWear",
        attributes={"material": "100% Organic Cotton", "fit": "Classic", "sizes": "XS-XXL"},
    ),
    Product(
        id="prod-004",
        name="Stainless Steel Water Bottle",
        description="Double-wall insulated water bottle that keeps drinks cold for 24 hours or hot for 12 hours. BPA-free and eco-friendly.",
        category="Home & Kitchen",
        price=34.99,
        stock_quantity=100,
        brand="HydroLife",
        attributes={"capacity": "750ml", "material": "Stainless Steel", "insulation": "Double-wall"},
    ),
    Product(
        id="prod-005",
        name="Laptop Backpack",
        description="Durable and spacious laptop backpack with anti-theft design, USB charging port, and ergonomic padding. Fits laptops up to 15.6 inches.",
        category="Bags & Accessories",
        price=59.99,
        stock_quantity=75,
        brand="TravelPro",
        attributes={"laptop_size": "15.6 inches", "features": "USB port, Anti-theft", "material": "Water-resistant Polyester"},
    ),
    Product(
        id="prod-006",
        name="Wireless Phone Charger",
        description="Fast wireless charging pad compatible with all Qi-enabled devices. Sleek design with LED indicator and safety protection.",
        category="Electronics",
        price=24.99,
        stock_quantity=120,
        brand="ChargeFast",
        attributes={"power": "15W", "compatibility": "Qi-enabled devices", "features": "LED indicator, Overcharge protection"},
    ),
    Product(
        id="prod-007",
        name="Running Shoes",
        description="Lightweight and breathable running shoes with responsive cushioning and excellent grip. Perfect for daily training and marathons.",
        category="Footwear",
        price=119.99,
        stock_quantity=45,
        brand="SprintMax",
        attributes={"type": "Running", "cushioning": "Responsive foam", "sizes": "US 6-13"},
    ),
    Product(
        id="prod-008",
        name="Coffee Maker",
        description="Programmable drip coffee maker with 12-cup capacity, built-in grinder, and thermal carafe to keep coffee hot for hours.",
        category="Home & Kitchen",
        price=89.99,
        stock_quantity=25,
        brand="BrewMaster",
        attributes={"capacity": "12 cups", "features": "Built-in grinder, Programmable", "carafe": "Thermal"},
    ),
    Product(
        id="prod-009",
        name="Yoga Mat",
        description="Non-slip yoga mat with extra thickness for joint support. Eco-friendly TPE material with alignment markers.",
        category="Sports & Fitness",
        price=39.99,
        stock_quantity=80,
        brand="ZenFit",
        attributes={"thickness": "6mm", "material": "TPE", "features": "Non-slip, Alignment markers"},
    ),
    Product(
        id="prod-010",
        name="Bluetooth Speaker",
        description="Portable waterproof Bluetooth speaker with 360-degree sound, 20-hour battery life, and built-in microphone for calls.",
        category="Electronics",
        price=79.99,
        stock_quantity=60,
        brand="SoundMax",
        attributes={"waterproof": "IPX7", "battery_life": "20 hours", "features": "360 sound, Built-in mic"},
    ),
]
