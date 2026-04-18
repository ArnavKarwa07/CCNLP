# Part B Data / Corpus Creation Report

## 1. Proposed Title to Data

**Synthetic Ecommerce and Healthcare Learning Corpus (SEHLC)**

## 2. Dataset Overview

- **Version:** 1.0
- **Authors/Contributors:** Arnav Karwa, Prof. Suja Sreejith Panickar
- **Department:** Department of Computer Engineering and Technology, School of Computer Science and Engineering
- **Affiliation/Organization:** Dr. Vishwanath Karad MIT World Peace University, Pune, Maharashtra, India

This submission presents a synthetic corpus prepared for academic analytics and NLP-oriented experimentation. The data was generated with controlled randomness and practical noise so that it behaves closer to real-world records during preprocessing, EDA, and model testing.

## 3. Motivation

In classroom and lab settings, one common problem is that clean toy datasets do not expose actual data quality issues. I created this corpus to make practice work more realistic without sharing sensitive personal records.

The goal was to produce structured data with useful variability: missing values, outliers, class imbalance, and minor text inconsistencies. This allows stronger testing of pipelines, especially where models can become overconfident on perfectly clean data.

## 3.1 Purpose

This dataset was created to support robust experimentation in data cleaning, exploratory analysis, feature engineering, and NLP preprocessing tasks using safe synthetic records.

## 3.2 Intended Use Cases

- Performance benchmarking of preprocessing and modeling workflows.
- Teaching and practice for NLP/data mining concepts using non-sensitive records.
- Comparative evaluation of algorithms under noisy and imbalanced conditions.

## 4. Novelty / Research Contribution

- Combines multiple synthetic generation strategies in one submission instead of relying on a single pipeline.
- Preserves realistic imperfections intentionally, rather than post-cleaning everything.
- Includes source-tracking in augmented data (`dataset_source`) to support provenance-aware analysis.

## 5. Relevance to NLP

Even though the datasets are tabular, they include text-heavy fields such as product descriptions, diagnosis labels, and short free-text notes. These fields are useful for tokenization checks, typo robustness, normalization, and text-feature extraction.

## 6. Intended Use and Target Audience

- **Target audience:** Students, instructors, and beginner researchers in data science/NLP.
- **Intended use:** Coursework practice, controlled experiments, reproducible demonstrations.
- **Not intended for:** Clinical decision support, financial decisions, or production deployment.

## 7. Source of Data

### 7.1 Data Sources Used

- Fully synthetic simulation from custom Python scripts.
- UCI Online Retail dataset (used only in the augmentation pipeline).

### 7.2 Data Ownership, Rights, and Safety Notes

- No copyrighted text, images, or confidential personal records were copied into the synthetic-only datasets.
- The submission is prepared for academic use and should not be publicly redistributed.
- Dataset files should remain confidential as per course instructions.

## 8. Data Collection / Creation Method

Three generation approaches were used.

### Method A: Python simulation (structured synthetic generation)

- **Ecommerce profile simulation:** Customer behavior fields were generated using mixed distributions.
- **Healthcare profile simulation:** Patient timelines, diagnosis patterns, and cost-related attributes were generated with dependency-aware logic.
- **Noise injection:** Missing values, outliers, small spelling drift, and occasional date inconsistencies were added to mimic field-level imperfections.

### Method B: Fully synthetic ecommerce transaction generation

- Created transaction-style records end-to-end without importing original customer data.
- Added behavior such as return-like entries, cancellation-like invoice patterns, and country imbalance.

### Method C: Open-source augmentation

- Used UCI Online Retail as base schema.
- Added synthetic rows sampled from source-like distributions.
- Appended provenance indicator (`dataset_source`) to separate original and synthetic portions.

### Names of Models / Tools Used for Generation

- Python (NumPy, pandas, random, datetime utilities)
- Rule-based generators and distribution-based sampling
- AI-assisted drafting support for code and language polishing (see Section 14)

## 9. Dataset Description

### 9.1 File-wise Summary

| Dataset                               | Number of Instances (rows) | Number of Features (columns) | Data Types                                   | File Format |
| ------------------------------------- | -------------------------: | ---------------------------: | -------------------------------------------- | ----------- |
| `ecommerce_synthetic.csv`             |                      7,060 |                           15 | Numerical, categorical, datetime, short text | CSV         |
| `healthcare_synthetic.csv`            |                      6,994 |                           14 | Numerical, categorical, datetime, short text | CSV         |
| `ecommerce_ai_complete.csv`           |                      9,000 |                            8 | Numerical, categorical, datetime, text       | CSV         |
| `ecommerce_open_source_augmented.csv` |                    544,409 |                            9 | Numerical, categorical, datetime, text       | CSV         |

### 9.2 Overall Count Snapshot

- **Total rows across all files:** 567,463
- **Minimum columns per file:** 8
- **Maximum columns per file:** 15

### 9.3 Approximate Size Note

- File sizes are in CSV format and suitable for local academic analysis workflows.
- The augmented ecommerce file is significantly larger and intended for scale-oriented experiments.

## 10. Supporting Theory Behind the Data

The generation logic follows basic statistical simulation principles:

- **Distribution-guided generation:** Different attributes are sampled from different distributions to avoid flat or unrealistic records.
- **Correlation-aware rules:** Related fields (for example, severity and treatment cost) are generated with dependency constraints.
- **Noise for robustness:** Controlled missingness and outliers are injected so preprocessing and model stability can be meaningfully tested.

This mirrors real data behavior more closely than perfectly clean random tables.

## 11. Annotation Process

The corpus is primarily structured synthetic data, so there is no manual sentence-level annotation phase. However, a lightweight labeling logic was applied through generation rules:

- Category/diagnosis labels were assigned using controlled vocabularies.
- Behavioral flags (for example, return-like patterns) were produced from rule conditions.
- Provenance tagging (`dataset_source`) was added in the augmented dataset.

After generation, schema checks were done to confirm column consistency and datatype alignment.

## 12. Limitations of Proposed Data

- Some datasets are below 10K rows individually, though the combined corpus is much larger.
- Synthetic noise is realistic but still simplified compared to full production-grade messiness.
- Healthcare records are artificial and should not be interpreted as clinical evidence.
- Domain drift may occur if models trained on this corpus are tested on unrelated real datasets.

## 13. Future Scope

- Expand the two smaller files to around 10K+ rows each for uniform scale across subsets.
- Add multilingual text fields for broader NLP experiments.
- Introduce temporal seasonality effects for richer forecasting tasks.
- Add documented benchmark splits for reproducible model comparison.

## 14. AI Tools Used (Transparency Section)

| Name of AI Tool Used          | Purpose                                                    |
| ----------------------------- | ---------------------------------------------------------- |
| GitHub Copilot / Copilot Chat | Assisted with code drafting and report language refinement |
| GPT-based LLM assistance      | Helped improve structure and wording clarity               |

## 15. References

1. UCI Machine Learning Repository - Online Retail Dataset: https://archive.ics.uci.edu/ml/datasets/online+retail
2. pandas documentation: https://pandas.pydata.org/docs/
3. NumPy documentation: https://numpy.org/doc/

## 16. Actual Data Files Submitted

1. `ecommerce_synthetic.csv`
2. `healthcare_synthetic.csv`
3. `ecommerce_ai_complete.csv`
4. `ecommerce_open_source_augmented.csv`

## 17. Compliance Notes for Submission

- Minimum column requirement is satisfied in all files (each has at least 8 columns).
- Minimum row requirement for interim checks is satisfied.
- Combined final corpus size is well above 10K rows.
- Data was generated/augmented for academic use while respecting confidentiality and rights constraints.
