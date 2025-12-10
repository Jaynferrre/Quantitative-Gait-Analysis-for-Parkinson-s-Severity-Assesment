import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.utils import resample

# --- CONFIGURATION ---
INPUT_FILE = 'demographics.csv'
OUTPUT_FILE = 'demographics_synthetic_300_ordered.csv'
TARGET_ROWS = 300
RANDOM_SEED = 42

# 1. Load Data
df = pd.read_csv(INPUT_FILE)

# 2. Preprocessing
# We include Study and Group in training to learn their distribution
train_cols = [
    'Study', 'Group', 'Gender', 'Age',
    'Height (meters)', 'Weight (kg)', 'HoehnYahr',
    'UPDRS', 'UPDRSM', 'TUAG', 'Speed_01 (m/sec)', 'Speed_10'
]

# Work on a copy
data = df[train_cols].copy()

# Encode Categorical Variables
cat_cols = ['Study', 'Group', 'Gender']
encoders = {}
for col in cat_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    encoders[col] = le

# Impute Missing Values (Required for GMM)
imputer = SimpleImputer(strategy='mean')
data_imputed = imputer.fit_transform(data)

# 3. Bootstrapping
# Resample to stabilize the statistical properties
bootstrapped_data = resample(
    data_imputed,
    replace=True,
    n_samples=len(data_imputed),
    random_state=RANDOM_SEED
)

# 4. Gaussian Mixture Model
# Fit the model to the bootstrapped data
gmm = GaussianMixture(
    n_components=2,
    covariance_type='full',
    random_state=RANDOM_SEED
)
gmm.fit(bootstrapped_data)

# 5. Generate Synthetic Data
# Sample 300 new rows
generated_data, _ = gmm.sample(n_samples=TARGET_ROWS)
df_new = pd.DataFrame(generated_data, columns=train_cols)

# 6. Decode Categorical Columns
for col in cat_cols:
    # Round to nearest integer to map back to category index
    df_new[col] = df_new[col].round().astype(int).clip(0, len(encoders[col].classes_) - 1)
    df_new[col] = encoders[col].inverse_transform(df_new[col])

# 7. ENFORCE ORIGINAL ROW ORDERING
# The original file structure is:
# 1st: All PD patients (Sub-sorted by Study: Ga -> Ju -> Si)
# 2nd: All CO patients (Sub-sorted by Study: Ga -> Ju -> Si)

# Create ranking columns to sort by
# Group: PD comes first (0), CO comes second (1)
df_new['Group_Rank'] = df_new['Group'].map({'PD': 0, 'CO': 1})

# Study: Ga (0) -> Ju (1) -> Si (2)
df_new['Study_Rank'] = df_new['Study'].map({'Ga': 0, 'Ju': 1, 'Si': 2})

# Sort the 300 rows based on this hierarchy
df_new = df_new.sort_values(by=['Group_Rank', 'Study_Rank'])

# 8. Clean Up & Rename Columns
rename_map = {
    'Height (meters)': 'Height_m',
    'Weight (kg)': 'Weight_kg',
    'TUAG': 'TUAG_sec',
    'Speed_01 (m/sec)': 'Speed_01_mps',
    'Speed_10': 'Speed_10_mps'
}
df_new.rename(columns=rename_map, inplace=True)

# 9. Value Constraints (Clean synthetic artifacts)
df_new['Age'] = df_new['Age'].clip(30, 95).round().astype(int)
df_new['Height_m'] = df_new['Height_m'].clip(1.4, 2.0).round(2)
df_new['Weight_kg'] = df_new['Weight_kg'].clip(40, 120).round(1)
df_new['HoehnYahr'] = df_new['HoehnYahr'].clip(0, 5).round(1)
df_new['UPDRS'] = df_new['UPDRS'].clip(0).round(0)
df_new['UPDRSM'] = df_new['UPDRSM'].clip(0).round(0)
df_new['TUAG_sec'] = df_new['TUAG_sec'].clip(0).round(2)
df_new['Speed_01_mps'] = df_new['Speed_01_mps'].clip(0).round(3)
df_new['Speed_10_mps'] = df_new['Speed_10_mps'].clip(0).round(3)

# 10. Calculate BMI
df_new['BMI'] = (df_new['Weight_kg'] / (df_new['Height_m'] ** 2)).round(2)

# 11. Assign IDs (PT001 to PT300)
# IDs are assigned *after* the sort, so PT001 is the first PD patient from 'Ga'
df_new['ID'] = [f'PT{i:03d}' for i in range(1, TARGET_ROWS + 1)]

# 12. Final Column Selection
final_order = [
    'ID', 'Study', 'Age', 'Gender', 'Height_m', 'Weight_kg',
    'BMI', 'TUAG_sec', 'Speed_01_mps', 'Speed_10_mps',
    'UPDRS', 'UPDRSM', 'HoehnYahr'
]
df_final = df_new[final_order]

# Save
df_final.to_csv(OUTPUT_FILE, index=False)
print(f"Generated {OUTPUT_FILE} with correct block ordering (PD->CO).")
print(df_final.head())
