from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OPEN_SOURCE_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
)
OUTPUT_FILE = Path(__file__).resolve().parent / "ecommerce_open_source_augmented.csv"
SOURCE_NOTE_FILE = Path(__file__).resolve().parent / "open_source_dataset_source.txt"

REQUIRED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]


def load_open_source_ecommerce() -> pd.DataFrame:
    """Load the open-source UCI Online Retail dataset."""
    base_df = pd.read_excel(OPEN_SOURCE_URL)
    missing = [col for col in REQUIRED_COLUMNS if col not in base_df.columns]
    if missing:
        raise ValueError(f"Missing expected columns from open dataset: {missing}")

    base_df = base_df[REQUIRED_COLUMNS].copy()
    base_df["InvoiceNo"] = base_df["InvoiceNo"].astype(str)
    base_df["StockCode"] = base_df["StockCode"].astype(str)
    base_df["Description"] = base_df["Description"].astype("string")
    base_df["Country"] = base_df["Country"].astype("string")

    base_df["Quantity"] = pd.to_numeric(base_df["Quantity"], errors="coerce")
    base_df["UnitPrice"] = pd.to_numeric(base_df["UnitPrice"], errors="coerce")
    base_df["CustomerID"] = pd.to_numeric(base_df["CustomerID"], errors="coerce")
    base_df["InvoiceDate"] = pd.to_datetime(base_df["InvoiceDate"], errors="coerce")

    base_df = base_df.dropna(subset=["InvoiceNo", "StockCode", "InvoiceDate", "UnitPrice"])
    return base_df.reset_index(drop=True)


def _sample_with_fallback(series: pd.Series, n: int, fallback: list[str]) -> np.ndarray:
    valid = series.dropna().astype(str)
    if len(valid) == 0:
        return np.random.choice(fallback, size=n)
    return valid.sample(n=n, replace=True, random_state=SEED).to_numpy()


def generate_augmented_rows(base_df: pd.DataFrame, extra_rows: int = 2500) -> pd.DataFrame:
    """Generate synthetic rows aligned to the open dataset schema and distribution."""
    invoices_numeric = (
        base_df["InvoiceNo"]
        .astype(str)
        .str.replace("C", "", regex=False)
        .str.extract(r"(\d+)")[0]
    )
    max_invoice = pd.to_numeric(invoices_numeric, errors="coerce").max()
    if pd.isna(max_invoice):
        max_invoice = 700000

    invoice_numbers = (np.arange(1, extra_rows + 1) + int(max_invoice)).astype(str)

    descriptions = _sample_with_fallback(
        base_df["Description"], extra_rows, fallback=["GENERIC PRODUCT"]
    )
    stock_codes = _sample_with_fallback(base_df["StockCode"], extra_rows, fallback=["S0001"])
    countries = _sample_with_fallback(
        base_df["Country"], extra_rows, fallback=["United Kingdom"]
    )

    unit_price_ref = base_df.loc[base_df["UnitPrice"] > 0, "UnitPrice"]
    if len(unit_price_ref) > 10:
        sampled_prices = unit_price_ref.sample(n=extra_rows, replace=True, random_state=SEED)
        noise = np.random.normal(0, sampled_prices.std() * 0.05, size=extra_rows)
        unit_prices = np.maximum(0.1, sampled_prices.to_numpy() + noise)
    else:
        unit_prices = np.random.uniform(0.5, 35.0, size=extra_rows)

    qty_ref = base_df.loc[base_df["Quantity"] != 0, "Quantity"]
    if len(qty_ref) > 10:
        sampled_qty = qty_ref.sample(n=extra_rows, replace=True, random_state=SEED).to_numpy()
        quantity = np.where(sampled_qty == 0, 1, sampled_qty)
    else:
        quantity = np.random.poisson(lam=6, size=extra_rows)
        quantity = np.clip(quantity, 1, 80)

    # Keep some returns similar to online retail data.
    return_mask = np.random.rand(extra_rows) < 0.03
    quantity = np.abs(quantity)
    quantity[return_mask] *= -1

    date_min = base_df["InvoiceDate"].min()
    date_max = base_df["InvoiceDate"].max()
    if pd.isna(date_min) or pd.isna(date_max):
        date_min = pd.Timestamp("2023-01-01")
        date_max = pd.Timestamp("2026-03-31")

    seconds_span = max(int((date_max - date_min).total_seconds()), 1)
    offsets = np.random.randint(0, seconds_span, size=extra_rows)
    invoice_dates = date_min + pd.to_timedelta(offsets, unit="s")

    customer_ids = np.random.randint(10000, 20000, size=extra_rows)

    augmented_rows = pd.DataFrame(
        {
            "InvoiceNo": invoice_numbers,
            "StockCode": stock_codes,
            "Description": descriptions,
            "Quantity": quantity.astype(int),
            "InvoiceDate": invoice_dates,
            "UnitPrice": np.round(unit_prices, 2),
            "CustomerID": customer_ids,
            "Country": countries,
        }
    )

    return augmented_rows


def main() -> None:
    base_df = load_open_source_ecommerce()
    print(f"Original open-source dataset shape before augmentation: {base_df.shape}")

    synthetic_rows = generate_augmented_rows(base_df=base_df)

    base_df = base_df.copy()
    base_df["dataset_source"] = "open_source_original"

    synthetic_rows = synthetic_rows.copy()
    synthetic_rows["dataset_source"] = "ai_augmented_rows"

    combined = pd.concat([base_df, synthetic_rows], ignore_index=True)
    combined.to_csv(OUTPUT_FILE, index=False)

    SOURCE_NOTE_FILE.write_text(
        "Open-source dataset used for augmentation:\n"
        f"{OPEN_SOURCE_URL}\n"
        "Source: UCI Machine Learning Repository - Online Retail dataset.\n",
        encoding="utf-8",
    )

    print(f"Saved {OUTPUT_FILE.name} with {len(combined)} rows")
    print(f"Original open-source rows: {len(base_df)}")
    print(f"AI-augmented rows added: {len(synthetic_rows)}")


if __name__ == "__main__":
    main()
