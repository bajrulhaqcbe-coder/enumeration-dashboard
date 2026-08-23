import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import urllib.request
import urllib.parse
import json


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
SHEET_GID = "1357887790"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=csv&gid={SHEET_GID}"
)


# ============================================================
# APPS SCRIPT WEB APP
# ============================================================

APPS_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbw-BOTf7BpNfNS85RI5pIXnwIB10jR2WTLmnjGIhRbr0MhnoKr7QywBlZMXeGt5HKQdBg/exec"
)


# ============================================================
# LOAD GOOGLE SHEET
# ============================================================

@st.cache_data(ttl=30)
def load_google_sheet():

    try:

        df = pd.read_csv(CSV_URL)

        df = df.dropna(how="all")

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        df = df.fillna("")

        return df

    except Exception as e:

        st.error("Google Sheet data load failed.")

        st.code(str(e))

        return pd.DataFrame()


df = load_google_sheet()


# ============================================================
# CHECK DATA
# ============================================================

if df.empty:

    st.error("No data found in Google Sheet.")

    st.stop()


HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"


if HLB_COLUMN not in df.columns:

    st.error(
        f"Required column not found: {HLB_COLUMN}"
    )

    st.write(
        "Columns found:",
        df.columns.tolist()
    )

    st.stop()


# ============================================================
# STATUS
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
    "Live Enumeration Monitoring System"
)


# ============================================================
# DASHBOARD
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

progress = (
    completed / total * 100
    if total > 0
    else 0
)


c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("TOTAL HLB", total)

with c2:
    st.metric("🟢 COMPLETED", completed)

with c3:
    st.metric("🟡 IN PROGRESS", in_progress)

with c4:
    st.metric("🔴 NOT STARTED", not_started)


st.divider()


# ============================================================
# PROGRESS
# ============================================================

st.subheader("📊 Overall Enumeration Progress")

st.progress(int(progress))

st.markdown(
    f"### {progress:.1f}% Completed"
)


# ============================================================
# CHARTS
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

    st.subheader("Status Distribution")

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

    st.subheader("Status Pie Chart")

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
# SELECT ENUMERATOR
# ============================================================

st.subheader("👤 Enumerator Update")


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
# FIND RECORD
# ============================================================

selected_rows = df[
    df[HLB_COLUMN]
    .astype(str)
    .str.strip()
    == selected
]


if selected_rows.empty:

    st.error("Enumerator record not found.")

    st.stop()


record = selected_rows.iloc[0]


# ============================================================
# HELPER
# ============================================================

def get_value(column):

    if column not in df.columns:
        return ""

    value = record[column]

    if pd.isna(value):
        return ""

    return str(value).strip()


# ============================================================
# CURRENT DETAILS
# ============================================================

st.markdown("### 📌 Enumerator Details")


left, right = st.columns(2)


with left:

    st.text_input(
        "Circle Number",
        value=get_value("CIRCLE NUMBER"),
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


with right:

    st.text_input(
        "Village Name",
        value=get_value("VILLAGE NAME"),
        disabled=True
    )

    st.text_area(
        "HLB Description",
        value=get_value("HLB DESCRIPTION"),
        disabled=True
    )


# ============================================================
# EXISTING DATA
# ============================================================

current_status = get_value("STATUS").upper()

if not current_status:
    current_status = "NOT STARTED"


current_pending = get_value("PENDING")

current_remarks = get_value("REMARKS")

current_expected = get_value("EXPECTED DATE")

current_completed_date = get_value(
    "COMPLETED DATE"
)


# ============================================================
# LOCK COMPLETED RECORD
# ============================================================

if current_status == "COMPLETED":

    st.success(
        "🔒 This enumeration is COMPLETED and LOCKED."
    )

    if current_completed_date:

        st.write(
            f"Completed Date: **{current_completed_date}**"
        )

    if current_remarks:

        st.write(
            f"Remarks: **{current_remarks}**"
        )

else:

    # ========================================================
    # UPDATE FORM
    # ========================================================

    st.markdown("### 📝 Update Enumeration")


    status_options = [
        "NOT STARTED",
        "IN PROGRESS",
        "COMPLETED"
    ]


    status_index = (
        status_options.index(current_status)
        if current_status in status_options
        else 0
    )


    status = st.selectbox(
        "Enumeration Status",
        status_options,
        index=status_index
    )


    # --------------------------------------------------------
    # PENDING
    # --------------------------------------------------------

    existing_pending = 0

    try:

        if current_pending:
            existing_pending = int(
                float(current_pending)
            )

    except:

        existing_pending = 0


    pending = st.number_input(
        "Pending Count",
        min_value=0,
        step=1,
        value=existing_pending
    )


    # --------------------------------------------------------
    # EXPECTED DATE
    # --------------------------------------------------------

    expected_default = date.today()


    expected_date = st.date_input(
        "Expected Completion Date",
        value=expected_default
    )


    # --------------------------------------------------------
    # REMARKS
    # --------------------------------------------------------

    remarks = st.text_area(
        "Remarks / Reason for Pending",
        value=current_remarks,
        placeholder=(
            "Example:\n"
            "18 entries pending.\n"
            "Some houses were locked.\n"
            "Will complete by expected date."
        ),
        height=130
    )


    # ========================================================
    # UPDATE BUTTON
    # ========================================================

    if st.button(
        "💾 UPDATE ENUMERATION",
        type="primary",
        width="stretch"
    ):


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if status == "IN PROGRESS":

            if pending <= 0:

                st.error(
                    "⚠️ Pending Count is compulsory."
                )

                st.stop()


            if not remarks.strip():

                st.error(
                    "⚠️ Remarks are compulsory "
                    "when status is IN PROGRESS."
                )

                st.stop()


        # ----------------------------------------------------
        # COMPLETED
        # ----------------------------------------------------

        if status == "COMPLETED":

            pending = 0


        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        payload = {

            "hlb": selected,

            "circle": get_value(
                "CIRCLE NUMBER"
            ),

            "enumerator": selected,

            "status": status,

            "pending": pending,

            "expected_date":
                expected_date.strftime(
                    "%d-%m-%Y"
                ),

            "remarks":
                remarks.strip()

        }


        # ----------------------------------------------------
        # SEND TO GOOGLE APPS SCRIPT
        # ----------------------------------------------------

        try:

            data = json.dumps(
                payload
            ).encode("utf-8")


            request = urllib.request.Request(

                APPS_SCRIPT_URL,

                data=data,

                headers={
                    "Content-Type":
                        "application/json"
                },

                method="POST"

            )


            with urllib.request.urlopen(
                request,
                timeout=30
            ) as response:

                response_text = (
                    response
                    .read()
                    .decode("utf-8")
                )


            result = json.loads(
                response_text
            )


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            if result.get("success"):

                st.success(
                    "✅ Enumeration updated successfully!"
                )

                st.info(
                    "Google Sheet updated. "
                    "Refreshing dashboard..."
                )

                st.cache_data.clear()

                st.rerun()


            else:

                st.error(
                    "❌ Google Sheet update failed."
                )

                st.code(
                    result.get(
                        "message",
                        "Unknown error"
                    )
                )


        except Exception as e:

            st.error(
                "❌ Connection to Google Apps Script failed."
            )

            st.code(str(e))


# ============================================================
# ALL ENUMERATOR STATUS
# ============================================================

st.divider()

st.subheader(
    "📋 Enumerator Status List"
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
        display_df[HLB_COLUMN]
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


for column in [
    "PENDING",
    "EXPECTED DATE",
    "LAST UPDATED",
    "COMPLETED DATE"
]:

    if column in display_df.columns:

        columns_to_show.append(column)


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
    "Live Google Sheet"
)
