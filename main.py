
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Sample transaction dataset
data = {
    "Amount": [100, 200, 150, 5000, 80, 7000,
               120, 9000, 250, 6000, 300, 8000],
    "Transactions": [1, 2, 1, 10, 1, 12,
                     2, 15, 1, 11, 2, 14],
    "Fraud": [0, 0, 0, 1, 0, 1,
              0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

# Features and target
X = df[["Amount", "Transactions"]]
y = df["Fraud"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42,
    stratify=y
)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Check accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Credit Card Fraud Detection")
print("---------------------------")
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Test a transaction
amount = 8000
transactions = 12

new_transaction = pd.DataFrame(
    [[amount, transactions]],
    columns=["Amount", "Transactions"]
)

result = model.predict(new_transaction)

if result[0] == 1:
    print("Result: Possible Fraud Transaction")
else:
    print("Result: Normal Transaction")
