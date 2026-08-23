import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
import urllib.request
import json


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enumeration Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GOOGLE SHEET CONFIGURATION
# ============================================================

SHEET_ID = "1vmxjbYABVPbu5PUVSLQO0H8J3TTflyTgGKOj5nH9Q14"

SHEET_GID = "1357887790"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=csv&gid={SHEET_GID}"
)


# ============================================================
# GOOGLE APPS SCRIPT SAVE URL
# ============================================================

APPS_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbw-BOTf7BpNfNS85RI5pIXnwIB10jR2WTLmnjGIhRbr0MhnoKr7QywBlZMXeGt5HKQdBg/exec"
)


# ============================================================
# ADMIN LOGIN
# ============================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ============================================================
# MAIN COLUMN
# ============================================================

HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD GOOGLE SHEET
# ============================================================

@st.cache_data(ttl=20)
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

        st.error("Google Sheet data could not be loaded.")

        st.code(str(e))

        return pd.DataFrame()


df = load_google_sheet()


# ============================================================
# CHECK DATA
# ============================================================

if df.empty:

    st.error("No data found in Google Sheet.")

    st.stop()


if HLB_COLUMN not in df.columns:

    st.error(
        f"Column not found: {HLB_COLUMN}"
    )

    st.write(
        "Available columns:",
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


# ============================================================
# TOTAL PENDING
# ============================================================

total_pending = 0

if "PENDING" in df.columns:

    pending_series = pd.to_numeric(
        df["PENDING"],
        errors="coerce"
    ).fillna(0)

    total_pending = int(
        pending_series.sum()
    )


# ============================================================
# OVERALL PROGRESS
# ============================================================

progress_percentage = (
    completed / total * 100
    if total > 0
    else 0
)


# ============================================================
# HELPER
# ============================================================

def get_value(record, column):

    if column not in df.columns:

        return ""

    value = record[column]

    if pd.isna(value):

        return ""

    return str(value).strip()


# ============================================================
# GOOGLE APPS SCRIPT UPDATE
# ============================================================

def send_update(payload):

    data = json.dumps(
        payload
    ).encode("utf-8")


    request = urllib.request.Request(
        APPS_SCRIPT_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
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


    try:

        return json.loads(
            response_text
        )

    except:

        return {
            "success": False,
            "message": response_text
        }


# ============================================================
# COMMON DASHBOARD
# ============================================================

def show_overall_progress():

    st.markdown(
        "### 📊 Overall Progress"
    )


    c1, c2, c3, c4, c5 = st.columns(5)


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


    with c5:

        st.metric(
            "📌 TOTAL PENDING",
            total_pending
        )


    st.progress(
        int(progress_percentage)
    )


    st.markdown(
        f"**Overall Enumeration Progress: "
        f"{progress_percentage:.1f}%**"
    )


    # ========================================================
    # PIE CHART
    # ========================================================

    chart_data = pd.DataFrame({

        "Status": [
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ],

        "Count": [
            completed,
            in_progress,
            not_started
        ]

    })


    fig = px.pie(
        chart_data,
        names="Status",
        values="Count",
        hole=0.40,
        title="Enumerator Status"
    )


    fig.update_traces(
        textinfo="label+percent",
        textposition="inside"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# SEARCH + FILTER + STATUS TABLE
# ============================================================

def show_enumerator_status():

    st.divider()


    # ========================================================
    # SEARCH
    # ========================================================

    st.markdown(
        "### 🔎 Enumerator Search & Filter"
    )


    f1, f2 = st.columns(2)


    with f1:

        search = st.text_input(
            "Search HLB / Enumerator / Village",
            key="status_search"
        )


    with f2:

        status_filter = st.selectbox(
            "Status",
            [
                "ALL",
                "COMPLETED",
                "IN PROGRESS",
                "NOT STARTED"
            ],
            key="status_filter"
        )


    display_df = df.copy()


    # ========================================================
    # SEARCH FILTER
    # ========================================================

    if search:

        mask = (
            display_df
            .astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        )


        display_df = display_df[
            mask
        ]


    # ========================================================
    # STATUS FILTER
    # ========================================================

    if status_filter != "ALL":

        display_df = display_df[
            display_df["STATUS"]
            == status_filter
        ]


    # ========================================================
    # TABLE
    # ========================================================

    st.markdown(
        "### 📋 Enumerator Status"
    )


    table_columns = [

        HLB_COLUMN,

        "CIRCLE NUMBER",

        "SUPERVISOR NAME & MOBILE NUMBER",

        "VILLAGE NAME",

        "ENUMERATOR MOBILE NUMBER",

        "HLB DESCRIPTION",

        "REMARKS",

        "EXPECTED DATE",

        "STATUS",

        "LAST UPDATED",

        "COMPLETED DATE",

        "PENDING"

    ]


    table_columns = [
        c for c in table_columns
        if c in display_df.columns
    ]


    st.dataframe(
        display_df[
            table_columns
        ],
        width="stretch",
        hide_index=True
    )


    st.caption(
        f"Showing {len(display_df)} "
        f"of {total} HLB records"
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "📋 Enumeration"
)


st.sidebar.markdown("---")


mode = st.sidebar.radio(
    "Select Mode",
    [
        "👤 Enumerator",
        "🔐 Admin"
    ]
)


if st.sidebar.button(
    "🔄 Refresh Data",
    width="stretch"
):

    st.cache_data.clear()

    st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📋 ENUMERATION PROGRESS DASHBOARD'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="sub-title">'
    'Enumeration Monitoring & Progress System'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ENUMERATOR MODE
# ============================================================

if mode == "👤 Enumerator":


    # ========================================================
    # 1. OVERALL PROGRESS
    # ========================================================

    show_overall_progress()


    # ========================================================
    # 2. ENUMERATOR SEARCH & FILTER
    # ========================================================

    show_enumerator_status()


    st.divider()


    # ========================================================
    # ENUMERATOR UPDATE
    # ========================================================

    st.markdown(
        "## 👤 Enumerator Update"
    )


    enumerators = (
        df[HLB_COLUMN]
        .astype(str)
        .str.strip()
        .tolist()
    )


    selected = st.selectbox(
        "Select HLB Number - Enumerator Name",
        enumerators,
        key="enum_selector"
    )


    selected_rows = df[
        df[HLB_COLUMN]
        .astype(str)
        .str.strip()
        == selected
    ]


    if selected_rows.empty:

        st.error(
            "Enumerator not found."
        )

        st.stop()


    record = selected_rows.iloc[0]


    current_status = get_value(
        record,
        "STATUS"
    ).upper()


    if not current_status:

        current_status = "NOT STARTED"


    # ========================================================
    # CURRENT STATUS
    # ========================================================

    if current_status == "COMPLETED":

        st.success(
            "🟢 COMPLETED"
        )

    elif current_status == "IN PROGRESS":

        st.warning(
            "🟡 IN PROGRESS"
        )

    else:

        st.error(
            "🔴 NOT STARTED"
        )


    # ========================================================
    # DETAILS
    # ========================================================

    st.markdown(
        "### 📌 Enumerator Details"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.text_input(
            "HLB Number - Enumerator",
            value=selected,
            disabled=True
        )


        st.text_input(
            "Circle Number",
            value=get_value(
                record,
                "CIRCLE NUMBER"
            ),
            disabled=True
        )


        st.text_input(
            "Supervisor Name & Mobile",
            value=get_value(
                record,
                "SUPERVISOR NAME & MOBILE NUMBER"
            ),
            disabled=True
        )


        st.text_input(
            "Enumerator Mobile",
            value=get_value(
                record,
                "ENUMERATOR MOBILE NUMBER"
            ),
            disabled=True
        )


    with col2:

        st.text_input(
            "Village Name",
            value=get_value(
                record,
                "VILLAGE NAME"
            ),
            disabled=True
        )


        st.text_area(
            "HLB Description",
            value=get_value(
                record,
                "HLB DESCRIPTION"
            ),
            disabled=True
        )


    # ========================================================
    # COMPLETED LOCK
    # ========================================================

    if current_status == "COMPLETED":


        st.success(
            "🔒 This Enumerator is COMPLETED and LOCKED."
        )


        completed_date = get_value(
            record,
            "COMPLETED DATE"
        )


        if completed_date:

            st.info(
                f"Completed Date: {completed_date}"
            )


        remarks = get_value(
            record,
            "REMARKS"
        )


        if remarks:

            st.write(
                "**Remarks:**"
            )

            st.info(
                remarks
            )


    else:


        # ====================================================
        # UPDATE FORM
        # ====================================================

        st.markdown(
            "### 📝 Update Enumeration"
        )


        status_options = [

            "NOT STARTED",

            "IN PROGRESS",

            "COMPLETED"

        ]


        try:

            default_index = (
                status_options.index(
                    current_status
                )
            )

        except ValueError:

            default_index = 0


        status = st.selectbox(
            "Status",
            status_options,
            index=default_index,
            key="update_status"
        )


        # ====================================================
        # PENDING
        # ====================================================

        current_pending = 0


        if "PENDING" in df.columns:

            try:

                current_pending = int(
                    float(
                        get_value(
                            record,
                            "PENDING"
                        ) or 0
                    )
                )

            except:

                current_pending = 0


        pending = st.number_input(
            "Pending Count",
            min_value=0,
            value=current_pending,
            step=1
        )


        # ====================================================
        # EXPECTED DATE
        # ====================================================

        expected_date = st.date_input(
            "Expected Completion Date",
            value=date.today()
        )


        # ====================================================
        # REMARKS
        # ====================================================

        current_remarks = get_value(
            record,
            "REMARKS"
        )


        remarks = st.text_area(
            "Remarks / Reason for Pending",
            value=current_remarks,
            height=130,
            placeholder=(
                "Enter detailed reason..."
            )
        )


        # ====================================================
        # SAVE
        # ====================================================

        if st.button(
            "💾 UPDATE ENUMERATION",
            type="primary",
            width="stretch"
        ):


            # ------------------------------------------------
            # IN PROGRESS VALIDATION
            # ------------------------------------------------

            if status == "IN PROGRESS":

                if pending <= 0:

                    st.error(
                        "⚠️ Pending Count is required."
                    )

                    st.stop()


                if not remarks.strip():

                    st.error(
                        "⚠️ Remarks are required "
                        "for IN PROGRESS."
                    )

                    st.stop()


            # ------------------------------------------------
            # COMPLETED
            # ------------------------------------------------

            if status == "COMPLETED":

                pending = 0


            payload = {

                "hlb":
                    selected,

                "circle":
                    get_value(
                        record,
                        "CIRCLE NUMBER"
                    ),

                "enumerator":
                    selected,

                "status":
                    status,

                "pending":
                    pending,

                "expected_date":
                    expected_date.strftime(
                        "%d-%m-%Y"
                    ),

                "remarks":
                    remarks.strip()

            }


            with st.spinner(
                "Saving to Google Sheet..."
            ):

                try:

                    result = send_update(
                        payload
                    )


                    if result.get(
                        "success"
                    ):

                        st.success(
                            "✅ SAVE OK"
                        )


                        st.cache_data.clear()


                        st.rerun()


                    else:

                        st.error(
                            "❌ SAVE FAILED"
                        )


                        st.code(
                            result.get(
                                "message",
                                "Unknown error"
                            )
                        )


                except Exception as e:

                    st.error(
                        "❌ Connection error"
                    )

                    st.code(
                        str(e)
                    )


# ============================================================
# ADMIN MODE
# ============================================================

else:


    # ========================================================
    # ADMIN LOGIN
    # ========================================================

    if (
        "admin_logged_in"
        not in st.session_state
    ):

        st.session_state.admin_logged_in = False


    if not st.session_state.admin_logged_in:


        st.subheader(
            "🔐 Admin Login"
        )


        username = st.text_input(
            "Admin Username"
        )


        password = st.text_input(
            "Admin Password",
            type="password"
        )


        if st.button(
            "🔐 LOGIN",
            type="primary"
        ):


            if (
                username
                == ADMIN_USERNAME
                and
                password
                == ADMIN_PASSWORD
            ):

                st.session_state.admin_logged_in = True

                st.success(
                    "Login successful."
                )

                st.rerun()


            else:

                st.error(
                    "❌ Invalid username or password."
                )


        st.stop()


    # ========================================================
    # ADMIN DASHBOARD
    # ========================================================

    a1, a2 = st.columns(
        [6, 1]
    )


    with a1:

        st.success(
            "🔓 Admin Dashboard"
        )


    with a2:

        if st.button(
            "Logout"
        ):

            st.session_state.admin_logged_in = False

            st.rerun()


    # ========================================================
    # 1. OVERALL PROGRESS
    # ========================================================

    show_overall_progress()


    # ========================================================
    # 2. SEARCH & FILTER
    # ========================================================

    show_enumerator_status()


    # ========================================================
    # DOWNLOAD REPORT
    # ========================================================

    st.divider()


    st.markdown(
        "### 📥 Export Report"
    )


    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        "⬇️ Download Full Enumeration Report",
        data=csv_data,
        file_name="Enumeration_Report.csv",
        mime="text/csv",
        width="stretch"
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "Enumeration Dashboard • "
    "Google Sheet Live Data"
)
