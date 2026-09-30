import streamlit as st
import json
import os
import pandas as pd

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claims_data.json")

st.set_page_config(
    page_title="Guidewire Claims Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main .block-container {padding-top: 2rem; padding-bottom: 2rem;}
        .metric-card {
            background: #ffffff;
            border-radius: 10px;
            padding: 1rem 1.25rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.08);
            border: 1px solid #eee;
        }
        .status-badge {
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.80rem;
            font-weight: 600;
            color: white;
            display: inline-block;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
        }
        h1, h2, h3 {font-family: 'Segoe UI', sans-serif;}
    </style>
    """,
    unsafe_allow_html=True,
)

STATUS_COLORS = {
    "Open": "#2563eb",
    "InReview": "#d97706",
    "Approved": "#16a34a",
    "Closed": "#6b7280",
    "Denied": "#dc2626",
}


def status_badge(status: str) -> str:
    color = STATUS_COLORS.get(status, "#6b7280")
    return f'<span class="status-badge" style="background-color:{color};">{status}</span>'


# ----------------------------------------------------------------------------
# Data helpers (read/write claims_data.json directly)
# ----------------------------------------------------------------------------
@st.cache_data(ttl=5)
def fetch_all_claims():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def fetch_claim(claim_number: str):
    claims = fetch_all_claims()
    for claim in claims:
        if claim["claimNumber"] == claim_number:
            return claim
    return None


def update_claim_status(claim_number: str, new_status: str):
    with open(DATA_FILE, "r") as f:
        claims = json.load(f)

    updated = None
    for claim in claims:
        if claim["claimNumber"] == claim_number:
            claim["claimStatus"] = new_status
            updated = claim
            break

    if updated is None:
        raise ValueError(f"Claim '{claim_number}' not found")

    with open(DATA_FILE, "w") as f:
        json.dump(claims, f, indent=2)

    return updated



# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "selected_claim" not in st.session_state:
    st.session_state.selected_claim = None


def go_to_claim(claim_number: str):
    st.session_state.selected_claim = claim_number


def go_back():
    st.session_state.selected_claim = None


# ----------------------------------------------------------------------------
# Claim Detail View
# ----------------------------------------------------------------------------
def render_claim_detail(claim_number: str):
    try:
        claim = fetch_claim(claim_number)
    except Exception as e:
        st.error(f"Could not load claim details: {e}")
        st.button("Back to Claims List", on_click=go_back)
        return

    if not claim or claim.get("error"):
        st.error("Claim not found.")
        st.button("Back to Claims List", on_click=go_back)
        return

    st.button("Back to Claims List", on_click=go_back)

    st.markdown(f"## Claim {claim['claimNumber']}")
    st.markdown(
        f"**Policy:** {claim.get('policyNumber','-')} &nbsp;|&nbsp; "
        f"**Line of Business:** {claim.get('lineOfBusiness','-')} &nbsp;|&nbsp; "
        f"**Status:** {status_badge(claim.get('claimStatus','-'))}",
        unsafe_allow_html=True,
    )
    st.divider()

    # Top-level metrics
    financials = claim.get("financials", {})
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Paid", f"${financials.get('totalPaid', 0):,.2f}")
    col2.metric("Total Reserved", f"${financials.get('totalReserved', 0):,.2f}")
    col3.metric("Total Incurred", f"${financials.get('totalIncurred', 0):,.2f}")
    col4.metric("Currency", financials.get("currency", "-"))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Loss Details")
        st.write(f"**Loss Date:** {claim.get('lossDate', '-')}")
        st.write(f"**Reported Date:** {claim.get('reportedDate', '-')}")
        st.write(f"**Loss Cause:** {claim.get('lossCause', '-')}")
        st.write(f"**Jurisdiction:** {claim.get('jurisdiction', '-')}")

        st.subheader("Insured")
        insured = claim.get("insured", {})
        st.write(f"**Name:** {insured.get('name', '-')}")
        st.write(f"**Insured ID:** {insured.get('insuredId', '-')}")

        st.subheader("Claimant")
        claimant = claim.get("claimant", {})
        st.write(f"**Name:** {claimant.get('name', '-')}")
        st.write(f"**Claimant ID:** {claimant.get('claimantId', '-')}")
        st.write(f"**Type:** {claimant.get('type', '-')}")

    with right:
        st.subheader("Assigned Adjuster")
        adjuster = claim.get("assignedAdjuster", {})
        st.write(f"**Name:** {adjuster.get('name', '-')}")
        st.write(f"**Adjuster ID:** {adjuster.get('adjusterId', '-')}")
        st.write(f"**Office:** {adjuster.get('office', '-')}")

        st.subheader("Coverages")
        coverages = claim.get("coverages", [])
        if coverages:
            st.dataframe(pd.DataFrame(coverages), use_container_width=True, hide_index=True)
        else:
            st.write("No coverage information available.")

        st.subheader("Exposures")
        exposures = claim.get("exposures", [])
        if exposures:
            st.dataframe(pd.DataFrame(exposures), use_container_width=True, hide_index=True)
        else:
            st.write("No exposure information available.")

        st.markdown("**Claim Status**")
        statuses = sorted(STATUS_COLORS.keys())
        current_status = claim.get("claimStatus", statuses[0])
        status_form_col1, status_form_col2 = st.columns([2, 1])
        with status_form_col1:
            new_status = st.selectbox(
                "New Status",
                statuses,
                index=statuses.index(current_status) if current_status in statuses else 0,
                key=f"status_select_{claim_number}",
                label_visibility="collapsed",
            )
        with status_form_col2:
            if st.button("Save", key=f"save_status_{claim_number}", use_container_width=True):
                if new_status != current_status:
                    try:
                        update_claim_status(claim_number, new_status)
                        fetch_all_claims.clear()
                        st.success(f"Status updated to '{new_status}'")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update status: {e}")
                else:
                    st.info("Status unchanged.")

    


# ----------------------------------------------------------------------------
# Claims List View
# ----------------------------------------------------------------------------
def render_claims_list():
    st.markdown("## Guidewire Claims Dashboard")
    st.caption("Browse and search all claims. Click a row action button to view full details.")

    try:
        claims = fetch_all_claims()
    except Exception as e:
        st.error(f"Could not load claims data from `{DATA_FILE}`. Error: {e}")
        return

    if not claims:
        st.warning("No claims found. If this is a fresh database, seed it first by calling the `/admin/seed` endpoint.")
        return

    df = pd.DataFrame(
        [
            {
                "Claim Number": c["claimNumber"],
                "Policy Number": c["policyNumber"],
                "Line of Business": c.get("lineOfBusiness", "-"),
                "Status": c.get("claimStatus", "-"),
                "Loss Cause": c.get("lossCause", "-"),
                "Loss Date": c.get("lossDate", "-"),
                "Total Incurred": c.get("financials", {}).get("totalIncurred", 0),
                "Adjuster": c.get("assignedAdjuster", {}).get("name", "-"),
            }
            for c in claims
        ]
    )

    # Top summary metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Claims", len(df))
    m2.metric("Open", int((df["Status"] == "Open").sum()))
    m3.metric("In Review", int((df["Status"] == "InReview").sum()))
    m4.metric("Total Incurred", f"${df['Total Incurred'].sum():,.2f}")

    st.divider()

    # Filters
    f1, f2, f3 = st.columns([2, 1, 1])
    search = f1.text_input("Search by claim #, policy #, or adjuster")
    status_filter = f2.multiselect("Status", sorted(df["Status"].unique()))
    lob_filter = f3.multiselect("Line of Business", sorted(df["Line of Business"].unique()))

    filtered = df.copy()
    if search:
        s = search.lower()
        filtered = filtered[
            filtered["Claim Number"].str.lower().str.contains(s)
            | filtered["Policy Number"].str.lower().str.contains(s)
            | filtered["Adjuster"].str.lower().str.contains(s)
        ]
    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]
    if lob_filter:
        filtered = filtered[filtered["Line of Business"].isin(lob_filter)]

    st.write(f"Showing **{len(filtered)}** of **{len(df)}** claims")

    # Header row
    header_cols = st.columns([2, 2, 1.5, 1.2, 1.5, 1.3, 1.5, 1])
    headers = ["Claim Number", "Policy Number", "Line of Business", "Status", "Loss Cause", "Loss Date", "Total Incurred", ""]
    for col, h in zip(header_cols, headers):
        col.markdown(f"**{h}**")

    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

    for _, row in filtered.iterrows():
        cols = st.columns([2, 2, 1.5, 1.2, 1.5, 1.3, 1.5, 1])
        cols[0].write(row["Claim Number"])
        cols[1].write(row["Policy Number"])
        cols[2].write(row["Line of Business"])
        cols[3].markdown(status_badge(row["Status"]), unsafe_allow_html=True)
        cols[4].write(row["Loss Cause"])
        cols[5].write(row["Loss Date"])
        cols[6].write(f"${row['Total Incurred']:,.2f}")
        cols[7].button("View", key=f"view_{row['Claim Number']}", on_click=go_to_claim, args=(row["Claim Number"],))


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Settings")
    st.text_input("Data File", value=DATA_FILE, key="data_file_display", disabled=True)
    if st.button("Refresh Data"):
        fetch_all_claims.clear()
        st.rerun()
    st.markdown("---")
    st.markdown("Built with **Streamlit**")

# ----------------------------------------------------------------------------
# Router
# ----------------------------------------------------------------------------
if st.session_state.selected_claim:
    render_claim_detail(st.session_state.selected_claim)
else:
    render_claims_list()
