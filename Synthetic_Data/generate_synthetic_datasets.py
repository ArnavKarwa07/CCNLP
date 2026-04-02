import random
import uuid
from datetime import timedelta

import numpy as np
import pandas as pd
from faker import Faker


# Keep seeds for reproducibility while preserving realistic randomness.
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker()
Faker.seed(SEED)


def random_dates_between(
    start: pd.Timestamp, end: pd.Timestamp, size: int
) -> pd.Series:
    """Generate random timestamps between two endpoints."""
    delta_seconds = int((end - start).total_seconds())
    offsets = np.random.randint(0, max(delta_seconds, 1), size=size)
    return pd.Series(pd.to_datetime(start) + pd.to_timedelta(offsets, unit="s"))


def apply_missing_values(
    df: pd.DataFrame, protected_columns: list[str]
) -> pd.DataFrame:
    """Inject 5-10% missing values per non-protected column."""
    for col in df.columns:
        if col in protected_columns:
            continue
        miss_rate = np.random.uniform(0.05, 0.10)
        mask = np.random.rand(len(df)) < miss_rate
        df.loc[mask, col] = np.nan
    return df


def noisy_customer_id(prefix: str) -> str:
    """Create randomized, non-sequential IDs with occasional formatting drift."""
    core = uuid.uuid4().hex[:10].upper()
    if np.random.rand() < 0.08:
        return f"{prefix}{core}"  # missing delimiter in a few rows
    if np.random.rand() < 0.08:
        return f"{prefix}-{core.lower()}"  # mixed casing in a few rows
    return f"{prefix}-{core}"


def pick_city_country() -> tuple[str, str]:
    """Sample realistic city-country pairs with mild imbalance."""
    pairs = [
        ("New York", "USA"),
        ("Los Angeles", "USA"),
        ("Chicago", "USA"),
        ("Toronto", "Canada"),
        ("Vancouver", "Canada"),
        ("London", "UK"),
        ("Manchester", "UK"),
        ("Berlin", "Germany"),
        ("Munich", "Germany"),
        ("Paris", "France"),
        ("Lyon", "France"),
        ("Mumbai", "India"),
        ("Bengaluru", "India"),
        ("Delhi", "India"),
        ("Sydney", "Australia"),
        ("Melbourne", "Australia"),
        ("Sao Paulo", "Brazil"),
        ("Mexico City", "Mexico"),
    ]
    weights = np.array(
        [
            0.12,
            0.09,
            0.06,
            0.05,
            0.04,
            0.08,
            0.03,
            0.05,
            0.03,
            0.05,
            0.02,
            0.08,
            0.06,
            0.05,
            0.03,
            0.03,
            0.02,
            0.04,
        ]
    )
    weights = weights / weights.sum()
    idx = np.random.choice(len(pairs), p=weights)
    return pairs[idx]


def make_ecommerce_dataset(n_rows: int) -> pd.DataFrame:
    """Create a messy, realistic synthetic e-commerce dataset."""
    genders = ["Female", "Male", "Non-binary", "Prefer not to say"]
    gender_probs = [0.52, 0.43, 0.03, 0.02]

    categories = [
        "electronics",
        "fashion",
        "groceries",
        "home",
        "beauty",
        "sports",
        "books",
    ]
    category_probs = [0.26, 0.21, 0.18, 0.12, 0.10, 0.08, 0.05]

    devices = ["mobile", "desktop", "tablet"]
    device_probs = [0.68, 0.26, 0.06]

    records = []
    now = pd.Timestamp("2026-03-31")
    signup_start = now - pd.Timedelta(days=3650)

    for _ in range(n_rows):
        customer_id = noisy_customer_id("CUST")
        customer_name = fake.name()

        # Skewed toward younger adults using beta distribution.
        age = int(np.round(18 + np.random.beta(2.2, 4.5) * 52))

        gender = np.random.choice(genders, p=gender_probs)
        city, country = pick_city_country()

        signup_date = random_dates_between(
            signup_start, now - pd.Timedelta(days=1), 1
        ).iloc[0]

        # More active users buy more recently; still keep broad variability.
        days_since_signup = max((now - signup_date).days, 1)
        recency_factor = np.random.beta(1.2, 3.2)
        days_after_signup = int(recency_factor * days_since_signup)
        last_purchase_date = signup_date + pd.Timedelta(days=days_after_signup)

        # Poisson-like order counts with mild age/category effects.
        base_orders = np.random.poisson(lam=3.4)
        age_boost = 1 if 28 <= age <= 45 and np.random.rand() < 0.35 else 0
        total_orders = max(base_orders + age_boost, 0)

        preferred_category = np.random.choice(categories, p=category_probs)
        device_used = np.random.choice(devices, p=device_probs)

        category_price_bias = {
            "electronics": 42,
            "fashion": 8,
            "groceries": -26,
            "home": 12,
            "beauty": -6,
            "sports": 10,
            "books": -18,
        }[preferred_category]

        device_noise = {"mobile": -2, "desktop": 6, "tablet": 1}[device_used]

        # Normal distribution with noise and correlation to category/device.
        avg_order_value = np.random.normal(
            loc=95 + category_price_bias + device_noise, scale=24
        )
        avg_order_value += np.random.normal(0, 7)
        avg_order_value = max(5, avg_order_value)

        # Returning behavior is intentionally imbalanced and weakly tied to order history.
        returning_prob = 0.32 + min(total_orders * 0.06, 0.45)
        is_returning_customer = "yes" if np.random.rand() < returning_prob else "no"

        # Derived metric with small accounting inconsistencies.
        total_spent = (total_orders * avg_order_value) + np.random.normal(0, 30)
        if np.random.rand() < 0.04:
            total_spent *= np.random.uniform(
                0.82, 1.18
            )  # occasional reconciliation issues

        # Realistic free text, with occasional typo-like artifacts.
        note = fake.sentence(nb_words=np.random.randint(6, 14))
        if np.random.rand() < 0.06:
            note = note.replace(" ", "  ", 1)  # random double-space artifact

        records.append(
            {
                "customer_id": customer_id,
                "customer_name": customer_name,
                "age": age,
                "gender": gender,
                "city": city,
                "country": country,
                "signup_date": signup_date,
                "last_purchase_date": last_purchase_date,
                "total_orders": total_orders,
                "avg_order_value": round(avg_order_value, 2),
                "total_spent": round(total_spent, 2),
                "preferred_category": preferred_category,
                "device_used": device_used,
                "is_returning_customer": is_returning_customer,
                "customer_note": note,
            }
        )

    df = pd.DataFrame(records)

    # Add outliers in spending-related columns.
    outlier_idx = np.random.choice(
        df.index, size=max(1, int(0.015 * len(df))), replace=False
    )
    df.loc[outlier_idx, "avg_order_value"] *= np.random.uniform(
        2.8, 5.2, size=len(outlier_idx)
    )
    df.loc[outlier_idx, "total_spent"] *= np.random.uniform(
        3.0, 6.0, size=len(outlier_idx)
    )

    # Inject a few temporal inconsistencies similar to real data quality issues.
    bad_date_idx = np.random.choice(
        df.index, size=max(1, int(0.008 * len(df))), replace=False
    )
    df.loc[bad_date_idx, "last_purchase_date"] = pd.to_datetime(
        df.loc[bad_date_idx, "signup_date"]
    ) - pd.to_timedelta(np.random.randint(1, 25, len(bad_date_idx)), unit="D")

    # Apply random missingness in 5-10% range for non-key columns.
    df = apply_missing_values(df, protected_columns=["customer_id"])

    # Slight category spelling inconsistencies.
    typo_idx = np.random.choice(
        df.index, size=max(1, int(0.01 * len(df))), replace=False
    )
    typo_map = {
        "electronics": "electrnics",
        "groceries": "grocery",
        "fashion": "fashon",
    }
    for idx in typo_idx:
        cat = df.at[idx, "preferred_category"]
        if pd.notna(cat) and cat in typo_map:
            df.at[idx, "preferred_category"] = typo_map[cat]

    # Shuffle rows to avoid any generated order signature.
    df = df.sample(frac=1, random_state=SEED + 1).reset_index(drop=True)

    return df


def make_healthcare_dataset(n_rows: int) -> pd.DataFrame:
    """Create a messy, realistic synthetic healthcare dataset."""
    genders = ["Female", "Male", "Other"]
    gender_probs = [0.50, 0.47, 0.03]

    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    blood_probs = [0.29, 0.05, 0.24, 0.04, 0.09, 0.01, 0.24, 0.04]

    diagnoses = [
        "Hypertension",
        "Diabetes",
        "Respiratory Infection",
        "Fracture",
        "Gastroenteritis",
        "Cardiac Disease",
        "Migraine",
        "Kidney Disorder",
    ]
    diagnosis_probs = [0.21, 0.18, 0.17, 0.12, 0.10, 0.08, 0.09, 0.05]

    hospital_types = ["private", "government"]
    hospital_probs = [0.64, 0.36]

    records = []
    now = pd.Timestamp("2026-03-31")
    adm_start = now - pd.Timedelta(days=8 * 365)

    for _ in range(n_rows):
        patient_id = noisy_customer_id("PAT")
        name = fake.name()

        # Age from mixed distributions to mimic pediatric/adult/elderly populations.
        age_mix = np.random.choice(["child", "adult", "senior"], p=[0.16, 0.63, 0.21])
        if age_mix == "child":
            age = int(np.clip(np.random.normal(8, 4), 0, 17))
        elif age_mix == "adult":
            age = int(np.clip(np.random.normal(42, 14), 18, 64))
        else:
            age = int(np.clip(np.random.normal(73, 8), 65, 90))

        gender = np.random.choice(genders, p=gender_probs)
        blood_group = np.random.choice(blood_groups, p=blood_probs)

        city, _country = pick_city_country()

        admission_date = random_dates_between(
            adm_start, now - pd.Timedelta(days=1), 1
        ).iloc[0]

        diagnosis = np.random.choice(diagnoses, p=diagnosis_probs)

        diagnosis_severity_bias = {
            "Hypertension": 1.0,
            "Diabetes": 1.2,
            "Respiratory Infection": 0.8,
            "Fracture": 1.4,
            "Gastroenteritis": 0.6,
            "Cardiac Disease": 2.2,
            "Migraine": 0.5,
            "Kidney Disorder": 1.8,
        }[diagnosis]

        # Severity centered by diagnosis with random noise.
        severity_score = np.random.normal(4.2 + diagnosis_severity_bias, 1.4)
        severity_score = float(np.clip(severity_score, 1, 10))

        # Length of stay grows with severity but remains noisy.
        expected_stay = max(
            1, int(np.round(np.random.poisson(lam=1.8 + severity_score * 0.7)))
        )
        discharge_date = admission_date + pd.Timedelta(days=expected_stay)

        insurance_covered = "yes" if np.random.rand() < 0.72 else "no"
        hospital_type = np.random.choice(hospital_types, p=hospital_probs)

        # Right-skewed costs with explicit correlation to severity and stay length.
        base_cost = np.random.lognormal(mean=8.6, sigma=0.45)
        treatment_cost = (
            base_cost
            + severity_score * np.random.uniform(350, 900)
            + expected_stay * np.random.uniform(120, 320)
        )

        # Insurance and hospital type influence final billed amount.
        if insurance_covered == "yes":
            treatment_cost *= np.random.uniform(0.72, 0.92)
        if hospital_type == "private":
            treatment_cost *= np.random.uniform(1.08, 1.35)

        clinical_note = fake.sentence(nb_words=np.random.randint(8, 18))
        if np.random.rand() < 0.05:
            clinical_note = clinical_note.replace(".", "")  # minor text inconsistency

        records.append(
            {
                "patient_id": patient_id,
                "name": name,
                "age": age,
                "gender": gender,
                "blood_group": blood_group,
                "city": city,
                "admission_date": admission_date,
                "discharge_date": discharge_date,
                "diagnosis": diagnosis,
                "severity_score": round(severity_score, 2),
                "treatment_cost": round(treatment_cost, 2),
                "insurance_covered": insurance_covered,
                "hospital_type": hospital_type,
                "clinical_note": clinical_note,
            }
        )

    df = pd.DataFrame(records)

    # Add outliers in severity and cost to mimic rare critical cases or billing errors.
    outlier_idx = np.random.choice(
        df.index, size=max(1, int(0.017 * len(df))), replace=False
    )
    df.loc[outlier_idx, "severity_score"] = np.clip(
        df.loc[outlier_idx, "severity_score"]
        + np.random.uniform(2.5, 5.0, len(outlier_idx)),
        1,
        10,
    )
    df.loc[outlier_idx, "treatment_cost"] *= np.random.uniform(
        2.4, 4.8, len(outlier_idx)
    )

    # Inject date inconsistencies: discharge before admission for a small fraction.
    inconsistent_idx = np.random.choice(
        df.index, size=max(1, int(0.009 * len(df))), replace=False
    )
    df.loc[inconsistent_idx, "discharge_date"] = pd.to_datetime(
        df.loc[inconsistent_idx, "admission_date"]
    ) - pd.to_timedelta(np.random.randint(1, 6, len(inconsistent_idx)), unit="D")

    # Add occasional diagnosis spelling drifts.
    typo_idx = np.random.choice(
        df.index, size=max(1, int(0.008 * len(df))), replace=False
    )
    diag_typo = {
        "Hypertension": "Hypertensn",
        "Diabetes": "Diabtes",
        "Migraine": "Migrane",
    }
    for idx in typo_idx:
        d = df.at[idx, "diagnosis"]
        if d in diag_typo:
            df.at[idx, "diagnosis"] = diag_typo[d]

    # Apply random missingness in 5-10% range.
    df = apply_missing_values(df, protected_columns=["patient_id"])

    # Shuffle rows to remove generation order.
    df = df.sample(frac=1, random_state=SEED + 2).reset_index(drop=True)

    return df


def main() -> None:
    # Keep both datasets between 5000 and 10000 rows.
    ecommerce_rows = int(np.random.randint(6200, 9100))
    healthcare_rows = int(np.random.randint(5700, 8800))

    ecommerce_df = make_ecommerce_dataset(ecommerce_rows)
    healthcare_df = make_healthcare_dataset(healthcare_rows)

    ecommerce_df.to_csv("ecommerce_synthetic.csv", index=False)
    healthcare_df.to_csv("healthcare_synthetic.csv", index=False)

    print(f"Saved ecommerce_synthetic.csv with {len(ecommerce_df)} rows")
    print(f"Saved healthcare_synthetic.csv with {len(healthcare_df)} rows")


if __name__ == "__main__":
    main()
