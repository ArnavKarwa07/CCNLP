from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_FILE = Path(__file__).resolve().parent / "ecommerce_ai_complete.csv"


def _random_invoice_numbers(n_rows: int) -> list[str]:
    """Generate invoice numbers similar to public online retail transaction data."""
    base = np.random.randint(500000, 700000, size=n_rows)
    invoice_numbers: list[str] = []
    for value in base:
        # Prefix with C for a small share of cancellation-like rows.
        if np.random.rand() < 0.03:
            invoice_numbers.append(f"C{value}")
        else:
            invoice_numbers.append(str(value))
    return invoice_numbers


def _random_stock_codes(n_rows: int) -> list[str]:
    prefixes = ["A", "B", "C", "D", "E", "F", "G", "H", "J"]
    codes: list[str] = []
    for _ in range(n_rows):
        prefix = random.choice(prefixes)
        number = np.random.randint(10000, 99999)
        codes.append(f"{prefix}{number}")
    return codes


def _catalog() -> dict[str, tuple[str, tuple[float, float]]]:
    """Map product description to a category and price range."""
    return {
        "WHITE HANGING HEART T-LIGHT HOLDER": ("Home Decor", (2.5, 8.5)),
        "REGENCY CAKESTAND 3 TIER": ("Kitchen", (7.0, 22.0)),
        "JUMBO BAG RED RETROSPOT": ("Bags", (1.5, 5.0)),
        "LUNCH BAG BLACK SKULL": ("Bags", (1.4, 4.5)),
        "SET OF 3 CAKE TINS PANTRY DESIGN": ("Kitchen", (5.0, 18.0)),
        "PACK OF 72 RETROSPOT CAKE CASES": ("Kitchen", (0.6, 2.2)),
        "ASSORTED COLOUR BIRD ORNAMENT": ("Home Decor", (1.8, 6.0)),
        "PARTY BUNTING": ("Party", (2.0, 9.0)),
        "ALARM CLOCK BAKELIKE GREEN": ("Home Decor", (2.5, 10.5)),
        "WOODEN PICTURE FRAME WHITE FINISH": ("Home Decor", (2.4, 8.8)),
        "FELTCRAFT DOLL ROSIE": ("Kids", (2.2, 8.5)),
        "KNITTED UNION FLAG HOT WATER BOTTLE": ("Lifestyle", (3.0, 11.0)),
        "CHOCOLATE HOT WATER BOTTLE": ("Lifestyle", (2.8, 10.0)),
        "VINTAGE SNAP CARDS": ("Kids", (0.9, 3.3)),
        "BREAD BIN DINER STYLE RED": ("Kitchen", (12.0, 34.0)),
    }


def make_ai_complete_ecommerce(n_rows: int = 9000) -> pd.DataFrame:
    """Create a complete synthetic e-commerce dataset without external input."""
    catalog = _catalog()
    products = list(catalog.keys())

    countries = [
        "United Kingdom",
        "Germany",
        "France",
        "EIRE",
        "Spain",
        "Netherlands",
        "Belgium",
        "Switzerland",
        "Portugal",
        "Norway",
    ]
    country_probs = np.array([0.64, 0.08, 0.07, 0.06, 0.04, 0.03, 0.03, 0.02, 0.02, 0.01])
    country_probs = country_probs / country_probs.sum()

    invoice_numbers = _random_invoice_numbers(n_rows)
    stock_codes = _random_stock_codes(n_rows)

    product_choices = np.random.choice(products, size=n_rows)
    invoice_dates = pd.to_datetime("2023-01-01") + pd.to_timedelta(
        np.random.randint(0, 1170, size=n_rows), unit="D"
    ) + pd.to_timedelta(np.random.randint(0, 24 * 60, size=n_rows), unit="m")

    quantity = np.random.poisson(lam=8, size=n_rows)
    quantity = np.clip(quantity, 1, 120)

    # A small share of negative quantities mimics returned transactions.
    return_mask = np.random.rand(n_rows) < 0.025
    quantity[return_mask] *= -1

    unit_prices = []
    for product_name in product_choices:
        _category, price_range = catalog[product_name]
        low, high = price_range
        price = np.random.uniform(low, high)
        price += np.random.normal(0, 0.2)
        unit_prices.append(round(max(0.1, price), 2))

    customer_ids = np.random.randint(12350, 18300, size=n_rows)
    countries_sample = np.random.choice(countries, size=n_rows, p=country_probs)

    df = pd.DataFrame(
        {
            "InvoiceNo": invoice_numbers,
            "StockCode": stock_codes,
            "Description": product_choices,
            "Quantity": quantity,
            "InvoiceDate": invoice_dates,
            "UnitPrice": unit_prices,
            "CustomerID": customer_ids,
            "Country": countries_sample,
        }
    )

    # Inject small realistic missingness in non-critical columns.
    for col in ["Description", "CustomerID"]:
        mask = np.random.rand(n_rows) < np.random.uniform(0.01, 0.03)
        df.loc[mask, col] = np.nan

    return df.sample(frac=1, random_state=SEED + 1).reset_index(drop=True)


def main() -> None:
    df = make_ai_complete_ecommerce()
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {OUTPUT_FILE.name} with {len(df)} rows")


if __name__ == "__main__":
    main()
