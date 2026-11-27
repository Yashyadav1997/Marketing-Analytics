"""A written tracking specification: the contract the audit checks events against.

Every event the business cares about is named here with its required parameters and their
types. A tracking plan that exists only in someone's head cannot be audited.
"""

CURRENCY = "INR"

SPEC = {
    "page_view":      {"page_location": str},
    "view_item":      {"item_id": str},
    "add_to_cart":    {"item_id": str, "value": float},
    "begin_checkout": {"value": float},
    "purchase":       {"transaction_id": str, "value": float, "currency": str},
}

# Which business question each KPI answers, and the events it depends on (used by Lesson 3).
KPI_DEPENDENCIES = {
    "conversion_rate":      ["page_view", "purchase"],
    "revenue":              ["purchase"],
    "average_order_value":  ["purchase"],
    "cart_abandonment":     ["add_to_cart", "purchase"],
    "checkout_dropoff":     ["begin_checkout", "purchase"],
    "product_view_to_cart": ["view_item", "add_to_cart"],
    "repeat_purchase_rate": ["purchase"],   # also needs a persistent customer identifier, see identity.py
}
