import streamlit as st
import pandas as pd
from urllib.parse import urlencode

st.set_page_config(layout="wide")

def load_data():
    df = pd.read_excel("claims_data_for_streamlit.xlsx")
    df["Claim Date"] = pd.to_datetime(df["Claim Date"], errors='coerce')
    df["Date Received"] = pd.to_datetime(df["Date Received"], errors='coerce')
    return df

df = load_data()

# Get selected CM Number from URL query params
query_params = st.query_params
selected_cm = query_params.get("cm", [None])[0]

if selected_cm:
    # ------------------ Claim Detail View ------------------
    st.title(f"Claim Detail: {selected_cm}")
    claim = df[df["CM Number"] == selected_cm].iloc[0]

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
    st.text_area("Notes / Complaint", value="[Placeholder for complaint text]", height=150)

    st.button("Mark as Processed (placeholder)")
    st.button("Send Email Response (placeholder)")
    st.button("Analyze with GPT (disabled)")

    st.markdown("[Back to All Claims](./)")

else:
    # ------------------ Open Claims List ------------------
    st.title("Warranty Claims Dashboard - Demo")

    # Metrics Summary
    total_claims = len(df)
    processed_claims = len(df[df['Status'].astype(str).str.lower() == 'processed'])
    unprocessed_claims = total_claims - processed_claims
    oldest_claim = df['Date Received'].min()
    over_90_days = len(df[(pd.Timestamp.today() - df['Date Received']).dt.days > 90])

    st.markdown("### 📊 Summary Metrics")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Total Claims", total_claims)
    metric_cols[1].metric("Processed Claims", processed_claims)
    metric_cols[2].metric("> 90 Days Old", over_90_days)
    metric_cols[3].metric("Oldest Claim", oldest_claim.date() if pd.notnull(oldest_claim) else "N/A")

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
    if len(date_range) == 2 and all(date_range):
        filtered_df = filtered_df[(filtered_df["Date Received"] >= pd.to_datetime(date_range[0])) &
                                   (filtered_df["Date Received"] <= pd.to_datetime(date_range[1]))]

    st.write(f"Loaded {len(df)} total claims.")
    st.write(f"Displaying {len(filtered_df)} claims after filters.")

    st.subheader("Open Claims")

    def make_clickable(cm):
        url = f"?{urlencode({'cm': cm})}"
        return f'<a href="{url}">{cm}</a>'

    display_df = filtered_df.copy()
    display_df["CM Number"] = display_df["CM Number"].apply(make_clickable)

    # Render scrollable HTML table with clickable links
    st.markdown("""
        <style>
        .scrollable-table-wrapper {
            height: 800px;
            overflow-y: scroll;
            overflow-x: auto;
            border: 1px solid #ccc;
            padding: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 6px 12px;
            border: 1px solid #ccc;
            text-align: left;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="scrollable-table-wrapper">' + display_df.to_html(escape=False, index=False) + '</div>', unsafe_allow_html=True)
