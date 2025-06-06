import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")  # ✅ Must be FIRST Streamlit command

def load_data():
    df = pd.read_excel("claims_data_for_streamlit.xlsx")
    df["Claim Date"] = pd.to_datetime(df["Claim Date"], errors='coerce')
    df["Date Received"] = pd.to_datetime(df["Date Received"], errors='coerce')
    return df

df = load_data()

st.title("Warranty Claims Dashboard - Demo")

# Sidebar Filters
st.sidebar.header("Filter Claims")
customer_filter = st.sidebar.text_input("Customer Number")
cm_filter = st.sidebar.text_input("CM Number")
date_range = st.sidebar.date_input("Date Received Range", [])

filtered_df = df.copy()
if customer_filter:
    filtered_df = filtered_df[filtered_df["Customer Number"].astype(str).str.contains(customer_filter)]
if cm_filter:
    filtered_df = filtered_df[filtered_df["CM Number"].astype(str).str.contains(cm_filter)]
if len(date_range) == 2:
    filtered_df = filtered_df[(filtered_df["Date Received"] >= pd.to_datetime(date_range[0])) &
                               (filtered_df["Date Received"] <= pd.to_datetime(date_range[1]))]

# Main Table View
st.subheader("Open Claims")
st.dataframe(filtered_df, use_container_width=True)

# Claim Detail View
st.subheader("Claim Detail Viewer")
selected_cm = st.selectbox("Select CM Number", filtered_df["CM Number"].dropna().unique())
claim = filtered_df[filtered_df["CM Number"] == selected_cm].iloc[0]

cols = st.columns(2)
with cols[0]:
    st.text(f"Customer #: {claim['Customer Number']}")
    st.text(f"Claim #: {claim['Claim Number']}")
    st.text(f"Date Received: {claim['Date Received']}")
    st.text(f"Status: {claim['Status']}")
with cols[1]:
    st.text(f"Part Value: {claim['Part Value']}")
    st.text(f"Quantity: {claim['Quantity']}")
    st.text(f"RGA #: {claim['RGA Number']}")
    st.text(f"Final Input: {claim['Final Input']}")

st.markdown("---")
st.text_area("Notes / Complaint", value="[Placeholder for complaint text]", height=100)

st.button("Mark as Processed (placeholder)")
st.button("Send Email Response (placeholder)")
st.button("Analyze with GPT (disabled)")
