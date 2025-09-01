import streamlit as st
import pandas as pd

# ---------------------------
# Must be the first Streamlit command
# ---------------------------
st.set_page_config(page_title="Flagged Users Dashboard", layout="wide")

# ---------------------------
# Load CSV
# ---------------------------
CSV_FILE = "visitors.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE)
    return df

df = load_data()

st.title("🚨 Flagged Users Dashboard")

# ---------------------------
# Filters
# ---------------------------
st.sidebar.header("Filters")
vpn_filter = st.sidebar.selectbox("VPN Suspected?", ["All", "Yes", "No"])
search_term = st.sidebar.text_input("Search Email / Phone")

filtered_df = df.copy()

# Filter by VPN
if vpn_filter == "Yes":
    filtered_df = filtered_df[filtered_df["vpn"] == True]
elif vpn_filter == "No":
    filtered_df = filtered_df[filtered_df["vpn"] == False]

# Filter by search term
if search_term:
    filtered_df = filtered_df[
        filtered_df["email"].str.contains(search_term, na=False, case=False) |
        filtered_df["phone"].astype(str).str.contains(search_term, na=False)
    ]

# ---------------------------
# Show the table normally
# ---------------------------
st.subheader(f"Total Records: {len(filtered_df)}")
st.dataframe(filtered_df, height=500)  # No highlight, normal table

# ---------------------------
# Show summary stats
# ---------------------------
st.sidebar.subheader("Summary")
st.sidebar.markdown(f"- Total Visitors: {len(df)}")
st.sidebar.markdown(f"- Total Flagged (email/phone filled): {len(df[(df['email']!='N/A') | (df['phone']!='N/A')])}")
st.sidebar.markdown(f"- Total VPN Suspected: {len(df[df['vpn'] == True])}")
