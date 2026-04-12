# Synthetic Data Generation Report

## 1. Aim

This assignment develops realistic synthetic datasets for analytics practice in ecommerce and healthcare domains. The generation process is designed to preserve practical real-world properties such as missing values, outliers, class imbalance, and minor inconsistencies.

## 2. Methodology

### Method 1: Python-based synthetic simulation

This method programmatically creates structured records using seeded randomness and distribution-driven feature generation.

#### 2.1 Ecommerce simulation

- Generates customer-level profiles and transaction behavior.
- Uses mixed statistical behavior for realistic spread:
  - Beta distribution for age profile.
  - Poisson distribution for order frequency.
  - Normal distribution for monetary variation.
- Injects data imperfections:
  - Missing values in non-key fields.
  - Outliers in spending attributes.
  - Occasional temporal inconsistency between signup and purchase dates.
  - Minor category/text spelling noise.

Generated file:

- `ecommerce_synthetic.csv`

#### 2.2 Healthcare simulation

- Generates patient records with diagnosis, severity, treatment cost, and hospitalization timelines.
- Preserves meaningful correlations across diagnosis, severity, stay length, and cost.
- Injects practical noise:
  - Missing values.
  - Outliers in severity and treatment cost.
  - Occasional admission/discharge date inconsistency.
  - Minor diagnosis spelling drift.

Generated file:

- `healthcare_synthetic.csv`

### Method 2: Fully synthetic AI-complete ecommerce generation

- Produces transaction-level ecommerce records without using external source data.
- Includes invoice IDs, stock codes, item descriptions, quantity, invoice date, unit price, customer IDs, and country.
- Adds realistic transaction behavior:
  - Small cancellation-like invoice share.
  - Return-like negative quantity rows.
  - Country distribution imbalance.
  - Product-level price variability with noise.
  - Small missingness in selected fields.

Generated file:

- `ecommerce_ai_complete.csv`

### Method 3: Open-source dataset augmentation with synthetic rows

- Uses UCI Online Retail as base data.
- Aligns schema and data types before generation.
- Appends synthetic rows sampled from source-like distributions.
- Adds provenance tracking using a `dataset_source` column.

Generated file:

- `ecommerce_open_source_augmented.csv`

## 3. Output Datasets and Schema Summary

| Dataset                               | Features                                                                                                                                                                                                     | Feature Count |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------: |
| `ecommerce_synthetic.csv`             | `customer_id, customer_name, age, gender, city, country, signup_date, last_purchase_date, total_orders, avg_order_value, total_spent, preferred_category, device_used, is_returning_customer, customer_note` |            15 |
| `healthcare_synthetic.csv`            | `patient_id, name, age, gender, blood_group, city, admission_date, discharge_date, diagnosis, severity_score, treatment_cost, insurance_covered, hospital_type, clinical_note`                               |            14 |
| `ecommerce_ai_complete.csv`           | `InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country`                                                                                                                   |             8 |
| `ecommerce_open_source_augmented.csv` | `InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country, dataset_source`                                                                                                   |             9 |

## 4. Results

| Files                |    Rows | Column Count |
| ------------------------------------- | ------: | -----------: |
| `ecommerce_ai_complete.csv`           |   9,000 |            8 |
| `ecommerce_open_source_augmented.csv` | 544,409 |            9 |
| `ecommerce_synthetic.csv`             |   7,060 |           15 |
| `healthcare_synthetic.csv`            |   6,994 |           14 |

## 5. Conclusion

 Successfully implemented three synthetic data generation methods: direct Python simulation, full synthetic transaction generation, and open-source augmentation. The produced datasets are reproducible, structurally realistic, and intentionally imperfect, making them suitable for preprocessing, EDA, feature engineering, and robustness-focused modeling workflows.
