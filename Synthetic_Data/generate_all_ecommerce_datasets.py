from __future__ import annotations

from pathlib import Path

import numpy as np

from augment_ecommerce_with_ai import main as run_augmentation
from generate_ecommerce_ai_full import make_ai_complete_ecommerce
from generate_synthetic_datasets import make_ecommerce_dataset


OUTPUT_DIR = Path(__file__).resolve().parent


def main() -> None:
    # 1) Existing Python-script synthetic generation.
    python_script_df = make_ecommerce_dataset(int(np.random.randint(6200, 9100)))
    python_script_path = OUTPUT_DIR / "ecommerce_python_script.csv"
    python_script_df.to_csv(python_script_path, index=False)

    # 2) Fully synthetic AI-complete dataset.
    ai_complete_df = make_ai_complete_ecommerce(n_rows=9000)
    ai_complete_path = OUTPUT_DIR / "ecommerce_ai_complete.csv"
    ai_complete_df.to_csv(ai_complete_path, index=False)

    # 3) Augment a real open-source e-commerce dataset with synthetic rows.
    run_augmentation()

    print(f"Saved {python_script_path.name} with {len(python_script_df)} rows")
    print(f"Saved {ai_complete_path.name} with {len(ai_complete_df)} rows")
    print("Saved ecommerce_open_source_augmented.csv via UCI open-source base data")


if __name__ == "__main__":
    main()
