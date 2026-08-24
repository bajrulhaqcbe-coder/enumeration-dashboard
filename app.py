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
    page_title="ANAIMALAI TALUK - Census Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
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
# GOOGLE APPS SCRIPT
# ============================================================

APPS_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbw-BOTf7BpNfNS85RI5pIXnwIB10jR2WTLmnjGIhRbr0MhnoKr7QywBlZMXeGt5HKQdBg/exec"
)


# ============================================================
# ADMIN
# ============================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ============================================================
# MAIN COLUMN
# ============================================================

HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"


# ============================================================
# MOBILE + DESKTOP CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN PAGE
       ====================================================== */

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }


    /* ======================================================
       TITLE
       ====================================================== */

    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        font-size: 16px;
        margin-bottom: 18px;
    }


    /* ======================================================
       UPDATE TITLE
       ====================================================== */

    .update-title {
        font-size: 27px;
        font-weight: 800;
        margin-top: 5px;
        margin-bottom: 10px;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        width: 100%;
        min-height: 45px;
        font-weight: 700;
        border-radius: 10px;
    }


    /* ======================================================
       INPUTS
       ====================================================== */

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        border-radius: 8px;
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media only screen and (max-width: 768px) {

        .block-container {
            padding-top: 0.6rem;
            padding-bottom: 0.5rem;
            padding-left: 0.65rem;
            padding-right: 0.65rem;
        }

        .main-title {
            font-size: 21px;
            line-height: 1.25;
            margin-bottom: 3px;
        }

        .sub-title {
            font-size: 12px;
            margin-bottom: 10px;
        }

        .update-title {
            font-size: 21px;
            margin-top: 2px;
            margin-bottom: 7px;
        }

        h3 {
            font-size: 18px !important;
        }

        h4 {
            font-size: 16px !important;
        }

        .stMarkdown {
            font-size: 14px;
        }

        .stButton > button {
            min-height: 42px;
            font-size: 14px;
            border-radius: 8px;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input {
            font-size: 14px;
        }

        div[data-testid="stMetric"] {
            padding: 8px 5px;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 11px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 20px;
        }

        .stProgress {
            margin-top: 5px;
            margin-bottom: 5px;
        }

        [data-testid="stDataFrame"] {
            font-size: 11px;
        }

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

        st.error(
            "Google Sheet data could not be loaded."
        )

        st.code(str(e))

        return pd.DataFrame()


# ============================================================
# INITIAL DATA
# ============================================================

df = load_google_sheet()


# ============================================================
# DATA CHECK
# ============================================================

if df.empty:

    st.error(
        "❌ No data found in Google Sheet."
    )

    st.stop()


if HLB_COLUMN not in df.columns:

    st.error(
        f"❌ Column not found: {HLB_COLUMN}"
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
# COUNTS
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
# PROGRESS
# ============================================================

progress_percentage = (
    completed / total * 100
    if total > 0
    else 0
)


# ============================================================
# RECORD VALUE
# ============================================================

def get_record_value(
    record,
    column
):

    if column not in record:
        return ""

    value = record.get(
        column,
        ""
    )

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

    try:

        return json.loads(
            response_text
        )

    except Exception:

        return {
            "success": False,
            "message": response_text
        }


# ============================================================
# OVERALL PROGRESS
# ============================================================

def show_overall_progress():

    st.markdown(
        "### 📊 Overall Progress"
    )

    # Mobile friendly metric layout
    m1, m2 = st.columns(2)

    with m1:

        st.metric(
            "TOTAL HLB",
            total
        )

    with m2:

        st.metric(
            "🟢 COMPLETED",
            completed
        )

    m3, m4 = st.columns(2)

    with m3:

        st.metric(
            "🟡 IN PROGRESS",
            in_progress
        )

    with m4:

        st.metric(
            "🔴 NOT STARTED",
            not_started
        )

    m5, _ = st.columns(2)

    with m5:

        st.metric(
            "📌 TOTAL PENDING",
            total_pending
        )

    st.progress(
        int(progress_percentage)
    )

    st.markdown(
        f"**Progress: {progress_percentage:.1f}%**"
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
        hole=0.45
    )

    fig.update_layout(
        height=300,
        margin=dict(
            l=10,
            r=10,
            t=35,
            b=10
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )

    fig.update_traces(
        textinfo="label+percent",
        textposition="inside"
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# ENUMERATOR UPDATE
# ============================================================

def show_enumerator_update():

    st.markdown(
        '<div class="update-title">'
        '👤 Enumerator Update'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Select Enumerator → SEARCH → Load latest Google Sheet data"
    )

    # ========================================================
    # ENUMERATOR LIST
    # ========================================================

    enumerators = (
        df[HLB_COLUMN]
        .astype(str)
        .str.strip()
        .tolist()
    )

    enumerators = [
        x
        for x in enumerators
        if x
    ]

    selected = st.selectbox(
        "HLB Number - Enumerator",
        enumerators,
        key="enum_selector"
    )

    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    if st.button(
        "🔍 SEARCH",
        type="primary",
        width="stretch",
        key="search_enumerator"
    ):

        with st.spinner(
            "🔄 Loading latest Google Sheet data..."
        ):

            try:

                # --------------------------------------------
                # DIRECT FRESH GOOGLE SHEET FETCH
                # --------------------------------------------

                latest_df = pd.read_csv(
                    CSV_URL
                )

                latest_df = (
                    latest_df
                    .dropna(how="all")
                )

                latest_df.columns = (
                    latest_df.columns
                    .astype(str)
                    .str.strip()
                )

                latest_df = (
                    latest_df
                    .fillna("")
                )

                # --------------------------------------------
                # STATUS
                # --------------------------------------------

                if "STATUS" not in latest_df.columns:

                    latest_df["STATUS"] = (
                        "NOT STARTED"
                    )

                latest_df["STATUS"] = (
                    latest_df["STATUS"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                )

                latest_df.loc[
                    latest_df["STATUS"].isin(
                        ["", "NAN"]
                    ),
                    "STATUS"
                ] = "NOT STARTED"

                # --------------------------------------------
                # FIND ENUMERATOR
                # --------------------------------------------

                selected_rows = latest_df[
                    latest_df[HLB_COLUMN]
                    .astype(str)
                    .str.strip()
                    == selected
                ]

                if selected_rows.empty:

                    st.error(
                        "❌ Enumerator not found."
                    )

                    return

                # --------------------------------------------
                # SAVE SEARCH RESULT
                # --------------------------------------------

                st.session_state[
                    "searched_enumerator"
                ] = selected

                st.session_state[
                    "searched_record"
                ] = (
                    selected_rows
                    .iloc[0]
                    .to_dict()
                )

                st.success(
                    "✅ Latest data loaded."
                )

            except Exception as e:

                st.error(
                    "❌ Google Sheet loading failed."
                )

                st.code(
                    str(e)
                )

                return

    # ========================================================
    # WAIT FOR SEARCH
    # ========================================================

    if (
        "searched_enumerator"
        not in st.session_state
    ):

        st.info(
            "👆 Select Enumerator and press 🔍 SEARCH"
        )

        return

    # ========================================================
    # CHECK SELECTED ENUMERATOR
    # ========================================================

    if (
        st.session_state[
            "searched_enumerator"
        ]
        != selected
    ):

        st.warning(
            "⚠️ Enumerator changed. "
            "Please press 🔍 SEARCH again."
        )

        return

    # ========================================================
    # LATEST RECORD
    # ========================================================

    searched_record = (
        st.session_state[
            "searched_record"
        ]
    )

    current_status = get_record_value(
        searched_record,
        "STATUS"
    ).upper()

    if not current_status:

        current_status = "NOT STARTED"


    # ========================================================
    # STATUS
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
        "#### 📌 Enumerator Details"
    )

    # Desktop: two columns
    # Mobile: Streamlit automatically stacks columns

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "HLB Number - Enumerator",
            value=selected,
            disabled=True,
            key="detail_hlb"
        )

        st.text_input(
            "Circle Number",
            value=get_record_value(
                searched_record,
                "CIRCLE NUMBER"
            ),
            disabled=True,
            key="detail_circle"
        )

        st.text_input(
            "Supervisor Name & Mobile",
            value=get_record_value(
                searched_record,
                "SUPERVISOR NAME & MOBILE NUMBER"
            ),
            disabled=True,
            key="detail_supervisor"
        )

        st.text_input(
            "Enumerator Mobile",
            value=get_record_value(
                searched_record,
                "ENUMERATOR MOBILE NUMBER"
            ),
            disabled=True,
            key="detail_mobile"
        )

    with col2:

        st.text_input(
            "Village Name",
            value=get_record_value(
                searched_record,
                "VILLAGE NAME"
            ),
            disabled=True,
            key="detail_village"
        )

        st.text_area(
            "HLB Description",
            value=get_record_value(
                searched_record,
                "HLB DESCRIPTION"
            ),
            disabled=True,
            key="detail_description"
        )


    # ========================================================
    # COMPLETED LOCK
    # ========================================================

    if current_status == "COMPLETED":

        st.success(
            "🔒 This Enumerator is COMPLETED and LOCKED."
        )

        completed_date = get_record_value(
            searched_record,
            "COMPLETED DATE"
        )

        if completed_date:

            st.info(
                f"Completed Date: {completed_date}"
            )

        remarks = get_record_value(
            searched_record,
            "REMARKS"
        )

        if remarks:

            st.markdown(
                "**Remarks:**"
            )

            st.info(
                remarks
            )

        return


    # ========================================================
    # UPDATE FORM
    # ========================================================

    st.markdown(
        "#### 📝 Update Enumeration"
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


    # ========================================================
    # PENDING
    # ========================================================

    try:

        current_pending = int(
            float(
                get_record_value(
                    searched_record,
                    "PENDING"
                ) or 0
            )
        )

    except Exception:

        current_pending = 0

    pending = st.number_input(
        "📌 Pending Count",
        min_value=0,
        value=current_pending,
        step=1,
        key="update_pending"
    )


    # ========================================================
    # EXPECTED DATE
    # ========================================================

    existing_expected = get_record_value(
        searched_record,
        "EXPECTED DATE"
    )

    expected_default = date.today()

    if existing_expected:

        try:

            expected_default = (
                pd.to_datetime(
                    existing_expected,
                    dayfirst=True
                ).date()
            )

        except Exception:

            expected_default = date.today()

    expected_date = st.date_input(
        "📅 Expected Completion Date",
        value=expected_default,
        key="update_expected_date"
    )


    # ========================================================
    # REMARKS
    # ========================================================

    current_remarks = get_record_value(
        searched_record,
        "REMARKS"
    )

    remarks = st.text_area(
        "📝 Remarks / Reason for Pending",
        value=current_remarks,
        height=110,
        placeholder=(
            "Example: 25 entries completed, "
            "10 entries pending. "
            "Expected completion tomorrow."
        ),
        key="update_remarks"
    )


    # ========================================================
    # SAVE
    # ========================================================

    st.markdown("")

    if st.button(
        "💾 UPDATE ENUMERATION",
        type="primary",
        width="stretch",
        key="save_enumerator_update"
    ):

        # ----------------------------------------------------
        # IN PROGRESS
        # ----------------------------------------------------

        if status == "IN PROGRESS":

            if pending <= 0:

                st.error(
                    "⚠️ Pending Count is required."
                )

                return

            if not remarks.strip():

                st.error(
                    "⚠️ Remarks are required "
                    "for IN PROGRESS."
                )

                return


        # ----------------------------------------------------
        # COMPLETED
        # ----------------------------------------------------

        if status == "COMPLETED":

            pending = 0


        # ----------------------------------------------------
        # PAYLOAD
        # ----------------------------------------------------

        payload = {

            "hlb":
                selected,

            "circle":
                get_record_value(
                    searched_record,
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


        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        with st.spinner(
            "💾 Saving to Google Sheet..."
        ):

            try:

                result = send_update(
                    payload
                )

                if result.get(
                    "success"
                ):

                    st.success(
                        "✅ SAVE OK — "
                        "Google Sheet Updated Successfully."
                    )

                    # ----------------------------------------
                    # CLEAR SEARCH
                    # ----------------------------------------

                    st.session_state.pop(
                        "searched_enumerator",
                        None
                    )

                    st.session_state.pop(
                        "searched_record",
                        None
                    )

                    # ----------------------------------------
                    # CLEAR CACHE
                    # ----------------------------------------

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
# SEARCH / FILTER / TABLE
# ============================================================

def show_enumerator_status():

    st.divider()

    st.markdown(
        "### 🔎 Enumerator Search & Filter"
    )

    search = st.text_input(
        "Search HLB / Enumerator / Village",
        key="status_search"
    )

    status_filter = st.selectbox(
        "Status Filter",
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
    # SEARCH
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
    # STATUS
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
        c
        for c in table_columns
        if c in display_df.columns
    ]

    st.dataframe(
        display_df[
            table_columns
        ],
        width="stretch",
        hide_index=True,
        height=420
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


# ============================================================
# REFRESH
# ============================================================

if st.sidebar.button(
    "🔄 Refresh Data",
    width="stretch"
):

    st.cache_data.clear()

    st.session_state.pop(
        "searched_enumerator",
        None
    )

    st.session_state.pop(
        "searched_record",
        None
    )

    st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📋 ANAIMALAI TALUK - CENSUS ENUMERATION PROGRESS DASHBOARD'
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
    # TOP - ENUMERATOR UPDATE
    # ========================================================

    show_enumerator_update()

    # ========================================================
    # OVERALL PROGRESS
    # ========================================================

    st.divider()

    show_overall_progress()

    # ========================================================
    # STATUS TABLE
    # ========================================================

    show_enumerator_status()


# ============================================================
# ADMIN MODE
# ============================================================

else:

    # ========================================================
    # LOGIN
    # ========================================================

    if (
        "admin_logged_in"
        not in st.session_state
    ):

        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:

        st.markdown(
            "### 🔐 Admin Login"
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
            type="primary",
            width="stretch"
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
                    "✅ Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

        st.stop()


    # ========================================================
    # ADMIN HEADER
    # ========================================================

    a1, a2 = st.columns(
        [5, 2]
    )

    with a1:

        st.success(
            "🔓 Admin Dashboard"
        )

    with a2:

        if st.button(
            "Logout",
            width="stretch"
        ):

            st.session_state.admin_logged_in = False

            st.rerun()


    # ========================================================
    # ADMIN PROGRESS
    # ========================================================

    show_overall_progress()


    # ========================================================
    # ADMIN TABLE
    # ========================================================

    show_enumerator_status()


    # ========================================================
    # EXPORT
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
    "Enumeration Dashboard • Google Sheet Live Data"
)