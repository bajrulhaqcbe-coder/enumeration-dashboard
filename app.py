import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Enumeration Progress Dashboard",
    page_icon="📋",
    layout="wide"
)

# ============================================================
# GOOGLE SHEET
# ============================================================

SHEET_ID = "1vmxjbYABVPbu5PUVSLQO0H8J3TTflyTgGKOj5nH9Q14"

# IMPORTANT:
# Replace 1357887790 below with the GID of the sheet
# containing your Enumerator Master data.
SHEET_GID = "1357887790"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=csv&gid={SHEET_GID}"
)


# ============================================================
# LOAD GOOGLE SHEET
# ============================================================

@st.cache_data(ttl=30)
def load_google_sheet():

    try:

        df = pd.read_csv(CSV_URL)

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Clean column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Convert NaN to blank
        df = df.fillna("")

        return df

    except Exception as e:

        st.error(
            "Google Sheet data load failed."
        )

        st.code(str(e))

        return pd.DataFrame()


df = load_google_sheet()


# ============================================================
# CHECK DATA
# ============================================================

if df.empty:

    st.error(
        "No data found in Google Sheet."
    )

    st.stop()


# ============================================================
# REQUIRED COLUMN
# ============================================================

HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"

if HLB_COLUMN not in df.columns:

    st.error(
        f"Required column not found: {HLB_COLUMN}"
    )

    st.write("Columns found in Google Sheet:")

    st.write(
        df.columns.tolist()
    )

    st.stop()


# ============================================================
# STATUS NORMALIZATION
# ============================================================

if "STATUS" not in df.columns:

    df["STATUS"] = "NOT STARTED"

df["STATUS"] = (
    df["STATUS"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df.loc[
    df["STATUS"].isin(["", "NAN"]),
    "STATUS"
] = "NOT STARTED"


# ============================================================
# TITLE
# ============================================================

st.markdown(
    """
    <h1 style="text-align:center;">
    📋 ENUMERATION PROGRESS DASHBOARD
    </h1>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Live data from Google Sheet"
)


# ============================================================
# DASHBOARD COUNTS
# ============================================================

total = len(df)

completed = len(
    df[df["STATUS"] == "COMPLETED"]
)

in_progress = len(
    df[df["STATUS"] == "IN PROGRESS"]
)

not_started = len(
    df[df["STATUS"] == "NOT STARTED"]
)

if total > 0:
    progress = (
        completed / total
    ) * 100
else:
    progress = 0


# ============================================================
# SUMMARY
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "TOTAL HLB",
        total
    )

with c2:

    st.metric(
        "🟢 COMPLETED",
        completed
    )

with c3:

    st.metric(
        "🟡 IN PROGRESS",
        in_progress
    )

with c4:

    st.metric(
        "🔴 NOT STARTED",
        not_started
    )


st.divider()


# ============================================================
# PROGRESS
# ============================================================

st.subheader(
    "📊 Overall Enumeration Progress"
)

st.progress(
    int(progress)
)

st.markdown(
    f"### {progress:.1f}% Completed"
)


# ============================================================
# CHART DATA
# ============================================================

chart_df = pd.DataFrame({
    "Status": [
        "Completed",
        "In Progress",
        "Not Started"
    ],
    "Count": [
        completed,
        in_progress,
        not_started
    ]
})


chart1, chart2 = st.columns(2)


with chart1:

    st.subheader(
        "Status Distribution"
    )

    fig = px.bar(
        chart_df,
        x="Status",
        y="Count",
        text="Count"
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


with chart2:

    st.subheader(
        "Status Percentage"
    )

    fig2 = px.pie(
        chart_df,
        names="Status",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )


st.divider()


# ============================================================
# ENUMERATOR SELECTION
# ============================================================

st.subheader(
    "👤 Enumerator Details"
)

enumerator_list = (
    df[HLB_COLUMN]
    .astype(str)
    .str.strip()
    .tolist()
)

selected = st.selectbox(
    "HLB NUMBER - ENUMERATOR NAME",
    enumerator_list
)


# ============================================================
# SELECTED RECORD
# ============================================================

selected_rows = df[
    df[HLB_COLUMN].astype(str).str.strip()
    == selected
]

if selected_rows.empty:

    st.error(
        "Enumerator record not found."
    )

    st.stop()


record = selected_rows.iloc[0]


# ============================================================
# HELPER
# ============================================================

def get_value(column):

    if column in df.columns:

        value = record[column]

        if pd.isna(value):
            return ""

        return str(value)

    return ""


# ============================================================
# AUTOMATIC DETAILS
# ============================================================

st.markdown(
    "### 📌 Automatic Details"
)

c1, c2 = st.columns(2)

with c1:

    st.text_input(
        "Circle Number",
        value=get_value(
            "CIRCLE NUMBER"
        ),
        disabled=True
    )

    st.text_input(
        "Supervisor Name & Mobile",
        value=get_value(
            "SUPERVISOR NAME & MOBILE NUMBER"
        ),
        disabled=True
    )

    st.text_input(
        "Enumerator Mobile",
        value=get_value(
            "ENUMERATOR MOBILE NUMBER"
        ),
        disabled=True
    )


with c2:

    st.text_input(
        "Village Name",
        value=get_value(
            "VILLAGE NAME"
        ),
        disabled=True
    )

    st.text_area(
        "HLB Description",
        value=get_value(
            "HLB DESCRIPTION"
        ),
        disabled=True
    )


# ============================================================
# CURRENT STATUS
# ============================================================

st.markdown(
    "### 📝 Current Status"
)

current_status = get_value(
    "STATUS"
).upper()

if not current_status:

    current_status = "NOT STARTED"


st.info(
    f"Current Status: **{current_status}**"
)


# ============================================================
# CURRENT REMARKS
# ============================================================

current_remarks = get_value(
    "REMARKS"
)

current_expected = get_value(
    "EXPECTED DATE"
)

current_pending = get_value(
    "PENDING"
)


if current_pending:

    st.write(
        f"**Current Pending:** {current_pending}"
    )

if current_expected:

    st.write(
        f"**Expected Completion:** {current_expected}"
    )

if current_remarks:

    st.write(
        f"**Current Remarks:** {current_remarks}"
    )


# ============================================================
# REFRESH
# ============================================================

st.divider()

st.info(
    "ℹ️ Google Sheet data is refreshed automatically "
    "approximately every 30 seconds."
)

if st.button(
    "🔄 Refresh Data",
    width="stretch"
):

    st.cache_data.clear()

    st.rerun()


# ============================================================
# ALL HLB LIST
# ============================================================

st.divider()

st.subheader(
    "📋 All Enumerator Status"
)


search = st.text_input(
    "🔍 Search HLB / Enumerator"
)

filter_status = st.selectbox(
    "Filter Status",
    [
        "ALL",
        "COMPLETED",
        "IN PROGRESS",
        "NOT STARTED"
    ]
)


display_df = df.copy()


if search:

    display_df = display_df[
        display_df[
            HLB_COLUMN
        ]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


if filter_status != "ALL":

    display_df = display_df[
        display_df["STATUS"]
        == filter_status
    ]


columns_to_show = [
    HLB_COLUMN,
    "CIRCLE NUMBER",
    "VILLAGE NAME",
    "STATUS"
]


if "PENDING" in display_df.columns:

    columns_to_show.append(
        "PENDING"
    )

if "EXPECTED DATE" in display_df.columns:

    columns_to_show.append(
        "EXPECTED DATE"
    )

if "LAST UPDATED" in display_df.columns:

    columns_to_show.append(
        "LAST UPDATED"
    )

if "COMPLETED DATE" in display_df.columns:

    columns_to_show.append(
        "COMPLETED DATE"
    )


existing_columns = [
    c for c in columns_to_show
    if c in display_df.columns
]


st.dataframe(
    display_df[existing_columns],
    width="stretch",
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Enumeration Progress Dashboard | "
    "Google Sheet Connected"
)
