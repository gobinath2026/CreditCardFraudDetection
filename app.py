
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- MODEL ----------------
data = {
    "Amount": [100, 200, 150, 5000, 80, 7000,
               120, 9000, 250, 6000, 300, 8000],
    "Transactions": [1, 2, 1, 10, 1, 12,
                     2, 15, 1, 11, 2, 14],
    "Fraud": [0, 0, 0, 1, 0, 1,
              0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)
X = df[["Amount", "Transactions"]]
y = df["Fraud"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X, y)

# ---------------- SESSION HISTORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f, #0b192b 65%, #10243a);
    color: #edf5ff;
}
[data-testid="stSidebar"] {
    background: #091321;
    border-right: 1px solid #243850;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}
h1, h2, h3, p, label {
    color: #edf5ff;
}
.hero {
    background: linear-gradient(115deg, #102a43, #123c52);
    border: 1px solid #24536b;
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 22px;
}
.eyebrow {
    color: #53e0cb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
}
.hero-title {
    font-size: 34px;
    font-weight: 800;
    margin: 10px 0;
}
.hero-desc {
    color: #bbccdc;
    font-size: 15px;
}
.panel {
    background: #101f31;
    border: 1px solid #263c52;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 16px;
}
.small-label {
    color: #a8bdd0;
    font-size: 13px;
}
.big-number {
    color: #ffffff;
    font-size: 27px;
    font-weight: 750;
    margin-top: 8px;
}
div.stButton > button {
    background: linear-gradient(90deg, #15cdb5, #3aa7f5);
    color: #061522;
    border: 0;
    border-radius: 11px;
    min-height: 48px;
    font-weight: 800;
    width: 100%;
}
div.stButton > button:hover {
    border: 1px solid #ffffff;
    color: #061522;
}
div[data-testid="stMetric"] {
    background: #101f31;
    border: 1px solid #263c52;
    padding: 18px;
    border-radius: 15px;
}
hr {
    border-color: #263c52;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 🛡️ FraudShield")
    st.markdown("### AI SECURITY CENTER")
    st.caption("Machine Learning Demo")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Overview", "Transaction Scanner", "Transaction History"],
        index=0
    )

    st.divider()
    st.markdown("🟢 **System Status**")
    st.caption("Demo model loaded")
    st.caption("Version 1.0")
    st.divider()
    st.caption("Built with Python + Scikit-learn")

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">INTELLIGENT TRANSACTION MONITORING</div>
    <div class="hero-title">FraudShield AI 🛡️</div>
    <div class="hero-desc">
        Monitor transactions. Identify suspicious patterns.
        Explore a machine learning fraud-detection demo.
    </div>
</div>
""", unsafe_allow_html=True)

st.warning(
    "ACADEMIC DEMO ONLY — The model uses a tiny synthetic dataset. "
    "Predictions and metrics are not validated for real financial use."
)

# ---------------- OVERVIEW ----------------
if page == "Overview":
    total = len(st.session_state.history)
    flagged = sum(
        1 for item in st.session_state.history
        if item["Result"] == "Possible Fraud"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Transactions Checked", total)

    with c2:
        st.metric("Flagged in This Session", flagged)

    with c3:
        st.metric("Model Type", "Random Forest")

    st.markdown("## ⚡ Quick Actions")

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="panel">
            <div class="small-label">01 / SCAN</div>
            <h3>🔎 Transaction Scanner</h3>
            <p>Enter an amount and transaction count
            to test the demo model.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Transaction Scanner"):
            st.session_state.next_page = "Transaction Scanner"
            st.rerun()

    with b:
        st.markdown("""
        <div class="panel">
            <div class="small-label">02 / HISTORY</div>
            <h3>📊 Activity Log</h3>
            <p>Review predictions generated during
            your current website session.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Transaction History"):
            st.session_state.next_page = "Transaction History"
            st.rerun()

    st.markdown("## 🧠 How the system works")

    x1, x2, x3 = st.columns(3)
    x1.info("**01 — INPUT**\n\nEnter transaction details.")
    x2.info("**02 — ANALYZE**\n\nRandom Forest model checks the inputs.")
    x3.info("**03 — RESULT**\n\nView the predicted class.")

    st.markdown("### Model training data")
    st.caption(
        "The current model uses 12 invented training examples. "
        "Its results are not meaningful estimates of real-world accuracy."
    )

elif page == "Transaction Scanner":
    st.markdown("## 🔎 Transaction Scanner")
    st.write("Enter the sample transaction details below.")

    with st.form("transaction_form"):
        left, right = st.columns(2)

        with left:
            amount = st.number_input(
                "Transaction amount (₹)",
                min_value=1.0,
                max_value=1000000.0,
                value=8000.0,
                step=100.0
            )

        with right:
            transactions = st.number_input(
                "Transaction count",
                min_value=1,
                max_value=100,
                value=12,
                step=1
            )

        submitted = st.form_submit_button("🛡️ ANALYZE TRANSACTION")

    if submitted:
        sample = pd.DataFrame(
            [[amount, transactions]],
            columns=["Amount", "Transactions"]
        )

        prediction = int(model.predict(sample)[0])

        if prediction == 1:
            result = "Possible Fraud"
            st.error("⚠️ Model result: Possible Fraud Transaction")
        else:
            result = "Normal"
            st.success("✅ Model result: Normal Transaction")

        st.markdown("### Analysis summary")

        r1, r2 = st.columns(2)
        r1.metric("Amount Submitted", f"₹{amount:,.2f}")
        r2.metric("Transaction Count", int(transactions))

        st.session_state.history.insert(0, {
            "Time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "Amount (₹)": amount,
            "Transactions": int(transactions),
            "Result": result
        })

        st.caption(
            "This is a prediction from a tiny demo model, "
            "not a verified assessment of fraud risk."
        )

elif page == "Transaction History":
    st.markdown("## 📊 Transaction History")
    st.write("Predictions from this browser session.")

    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True)

        csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download History CSV",
            data=csv,
            file_name="fraudshield_history.csv",
            mime="text/csv"
        )

        if st.button("Clear Session History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info(
            "No transactions checked yet. "
            "Open Transaction Scanner and test a transaction."
        )

st.divider()
st.caption(
    "FraudShield AI • Student Mini Project • "
    "Synthetic data only • Not for real banking decisions"
)
