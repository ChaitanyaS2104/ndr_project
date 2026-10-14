import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# 1. Load the processed arrays we saved earlier
print("Loading processed training and validation data...")
data = np.load("processed_train_data.npz")

X_train = data["X_train"]
y_train = data["y_train"]
X_val = data["X_val"]
y_val = data["y_val"]

print(f"Loaded X_train shape: {X_train.shape}")
print(f"Loaded X_val shape: {X_val.shape}")

# 2. Initialize the Random Forest Classifier
# (n_estimators=100 means 100 decision trees in the forest)
print("Training Random Forest Classifier...")
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

# 3. Fit the model on the training data
clf.fit(X_train, y_train)
print("Training completed successfully!")

# 4. Evaluate the model on the validation set
print("\nEvaluating model on validation set...")
y_pred = clf.predict(X_val)

accuracy = accuracy_score(y_val, y_pred)
print(f"Validation Accuracy: {accuracy * 100:.2f}%\n")

print("Classification Report:")
print(classification_report(y_val, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_val, y_pred))

# 5. Save the trained model artifact for live Suricata inference later
model_filename = "suricata_nids_model.pkl"
joblib.dump(clf, model_filename)
print(f"\nSaved trained model to '{model_filename}'")