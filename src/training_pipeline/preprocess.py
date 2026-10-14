import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# 1. Load the training dataset
csv_path = "data/UNSW_NB15_training-set.csv"
print(f"Loading dataset from {csv_path}...")
df = pd.read_csv(csv_path)

# 2. Define the exact features we are capturing from Suricata
numerical_features = ['dur', 'sbytes', 'dbytes', 'spkts', 'dpkts']
categorical_features = ['proto', 'service', 'state']
target_column = 'label'  # 0 for normal, 1 for attack

# Keep only necessary columns + target
features_to_clear = numerical_features + categorical_features + [target_column]
df = df[features_to_clear]

# Split features (X) and target label (y)
X = df.drop(columns=[target_column])
y = df[target_column]

print(f"Dataset shape: {X.shape}")

# 3. Set up Preprocessing Pipeline (Scaling + One-Hot Encoding)
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ]
)

# Fit and transform the training features
print("Applying preprocessing (scaling and encoding)...")
X_processed = preprocessor.fit_transform(X)

# 4. Split into Train and Validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X_processed, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set shape: {X_train.shape}")
print(f"Validation set shape: {X_val.shape}")

# 5. Save the preprocessor object for your live Suricata script later
joblib.dump(preprocessor, "suricata_preprocessor.pkl")
print("Saved preprocessor to 'suricata_preprocessor.pkl'")

# 6. Save processed arrays so we can train our classifier next
np.savez("processed_train_data.npz", X_train=X_train, y_train=y_train, X_val=X_val, y_val=y_val)
print("Saved processed arrays to 'processed_train_data.npz'")