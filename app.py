import streamlit as st
import pandas as pd
from datetime import date
import urllib.request
import json
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Anaimalai Taluk Census",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GOOGLE SHEET CONFIG
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
# ADMIN LOGIN
# ============================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ============================================================
# MAIN COLUMN
# ============================================================

HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"


# ============================================================
# CSS - COMPACT MOBILE DESIGN
# ============================================================

st.markdown(
    """
<style>

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 1050px;
    padding-top: 0.25rem;
    padding-left: 0.45rem;
    padding-right: 0.45rem;
    padding-bottom: 1rem;
}


/* =========================================================
HEADER
========================================================= */

.dashboard-header {

    background: linear-gradient(
        135deg,
        #0f766e,
        #115e59
    );

    color: white;

    border-radius: 14px;

    padding: 11px 8px;

    text-align: center;

    margin-bottom: 10px;
}

.dashboard-title {

    font-size: 20px;

    font-weight: 900;

    line-height: 1.2;
}

.dashboard-subtitle {

    font-size: 9px;

    margin-top: 4px;

    opacity: 0.9;
}


/* =========================================================
SECTION
========================================================= */

.section-title {

    font-size: 17px;

    font-weight: 900;

    color: #0f172a;

    margin-top: 7px;

    margin-bottom: 7px;
}


/* =========================================================
SEARCH CARD
========================================================= */

.search-card {

    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    padding: 8px;

    margin-bottom: 9px;

    box-shadow:
        0 2px 8px rgba(15,23,42,0.05);
}


/* =========================================================
RESULT CARD
========================================================= */

.result-card {

    background: #ffffff;

    border: 1px solid #dbeafe;

    border-radius: 12px;

    padding: 9px;

    margin-bottom: 10px;

    box-shadow:
        0 2px 8px rgba(15,23,42,0.05);
}

.result-label {

    font-size: 9px;

    font-weight: 850;

    color: #64748b;

    text-transform: uppercase;
}

.result-value {

    font-size: 13px;

    font-weight: 850;

    color: #0f172a;

    margin-top: 2px;

    word-break: break-word;
}


/* =========================================================
STATUS
========================================================= */

.status-completed {

    background: #dcfce7;

    color: #166534;

    border: 1px solid #86efac;

    border-radius: 9px;

    padding: 7px;

    text-align: center;

    font-size: 12px;

    font-weight: 900;

    margin-bottom: 8px;
}

.status-progress {

    background: #fef3c7;

    color: #92400e;

    border: 1px solid #fcd34d;

    border-radius: 9px;

    padding: 7px;

    text-align: center;

    font-size: 12px;

    font-weight: 900;

    margin-bottom: 8px;
}

.status-notstarted {

    background: #fee2e2;

    color: #991b1b;

    border: 1px solid #fca5a5;

    border-radius: 9px;

    padding: 7px;

    text-align: center;

    font-size: 12px;

    font-weight: 900;

    margin-bottom: 8px;
}


/* =========================================================
SUMMARY
========================================================= */

.summary-card {

    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 10px;

    padding: 7px 3px;

    text-align: center;

    box-shadow:
        0 2px 6px rgba(15,23,42,0.04);
}

.summary-number {

    font-size: 19px;

    font-weight: 900;

    color: #0f172a;
}

.summary-label {

    font-size: 7px;

    font-weight: 850;

    color: #64748b;
}


/* =========================================================
BUTTON
========================================================= */

.stButton > button {

    min-height: 38px;

    border-radius: 9px;

    font-weight: 850;

    font-size: 12px;
}


/* =========================================================
INPUT
========================================================= */

div[data-baseweb="select"] {

    font-size: 12px;
}


/* =========================================================
MOBILE
========================================================= */

@media only screen and (max-width: 768px) {

    .block-container {

        padding-left: 0.25rem;

        padding-right: 0.25rem;

        padding-top: 0.15rem;
    }

    .dashboard-header {

        border-radius: 11px;

        padding: 9px 5px;

        margin-bottom: 7px;
    }

    .dashboard-title {

        font-size: 16px;
    }

    .dashboard-subtitle {

        font-size: 8px;
    }

    .section-title {

        font-size: 15px;

        margin-top: 5px;

        margin-bottom: 5px;
    }

    .search-card {

        padding: 6px;

        border-radius: 9px;
    }

    .result-card {

        padding: 7px;

        border-radius: 9px;
    }

    .result-label {

        font-size: 8px;
    }

    .result-value {

        font-size: 11px;
    }

    .summary-number {

        font-size: 17px;
    }

    .summary-label {

        font-size: 6px;
    }

    .stButton > button {

        min-height: 36px;

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

        data = pd.read_csv(CSV_URL)

        data = data.dropna(how="all")

        data.columns = (
            data.columns
            .astype(str)
            .str.strip()
        )

        data = data.fillna("")

        if "STATUS" not in data.columns:

            data["STATUS"] = "NOT STARTED"

        data["STATUS"] = (
            data["STATUS"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        data.loc[
            data["STATUS"].isin(["", "NAN"]),
            "STATUS"
        ] = "NOT STARTED"

        return data

    except Exception as e:

        st.error(
            "Google Sheet data could not be loaded."
        )

        st.code(str(e))

        return pd.DataFrame()


# ============================================================
# FRESH LOAD
# ============================================================

def load_fresh_google_sheet():

    data = pd.read_csv(CSV_URL)

    data = data.dropna(how="all")

    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
    )

    data = data.fillna("")

    if "STATUS" not in data.columns:

        data["STATUS"] = "NOT STARTED"

    data["STATUS"] = (
        data["STATUS"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    data.loc[
        data["STATUS"].isin(["", "NAN"]),
        "STATUS"
    ] = "NOT STARTED"

    return data


# ============================================================
# GET VALUE
# ============================================================

def get_value(record, column):

    if column not in record:

        return ""

    value = record[column]

    if pd.isna(value):

        return ""

    return str(value).strip()


# ============================================================
# SEND UPDATE
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
# SUMMARY
# ============================================================

def calculate_summary(data):

    total = len(data)

    completed = len(
        data[
            data["STATUS"] == "COMPLETED"
        ]
    )

    in_progress = len(
        data[
            data["STATUS"] == "IN PROGRESS"
        ]
    )

    not_started = len(
        data[
            data["STATUS"] == "NOT STARTED"
        ]
    )

    total_pending = 0

    if "PENDING" in data.columns:

        total_pending = int(
            pd.to_numeric(
                data["PENDING"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

    percentage = (

        completed / total * 100

        if total > 0

        else 0
    )

    return (
        total,
        completed,
        in_progress,
        not_started,
        total_pending,
        percentage
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="dashboard-header">

<div class="dashboard-title">
📋 ANAIMALAI TALUK
<br>
CENSUS ENUMERATION PROGRESS DASHBOARD
</div>

<div class="dashboard-subtitle">
Enumeration Monitoring & Progress System
</div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# DATA
# ============================================================

df = load_google_sheet()


if df.empty:

    st.error(
        "No data found in Google Sheet."
    )

    st.stop()


if HLB_COLUMN not in df.columns:

    st.error(
        f"Column not found: {HLB_COLUMN}"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 📋 Enumeration"
    )

    st.divider()

    mode = st.radio(
        "Select Mode",
        [
            "👤 Enumerator",
            "🔐 Admin"
        ]
    )

    st.divider()

    if st.button(
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
# ENUMERATOR MODE
# ============================================================

if mode == "👤 Enumerator":


    # ========================================================
    # SEARCH
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🔎 Enumerator Search'
        '</div>',
        unsafe_allow_html=True
    )


    enumerators = (
        df[HLB_COLUMN]
        .astype(str)
        .str.strip()
        .tolist()
    )


    enumerators = [
        x for x in enumerators
        if x
    ]


    dropdown_options = [
        "-- Select Enumerator --"
    ] + enumerators


    st.markdown(
        '<div class="search-card">',
        unsafe_allow_html=True
    )


    # ========================================================
    # FORM
    #
    # ENTER / KEYBOARD SEARCH ALSO WORKS
    # ========================================================

    with st.form(
        "enumerator_search_form"
    ):

        selected = st.selectbox(

            "👤 HLB Number - Enumerator",

            dropdown_options,

            index=0,

            key="enum_selector"
        )


        search_clicked = st.form_submit_button(

            "🔍 SEARCH",

            type="primary",

            use_container_width=True
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SEARCH PROCESS
    # ========================================================

    if search_clicked:

        if selected == "-- Select Enumerator --":

            st.warning(
                "⚠️ Please select an Enumerator."
            )

            st.stop()


        with st.spinner(
            "🔄 Loading Google Sheet..."
        ):

            try:

                latest_df = (
                    load_fresh_google_sheet()
                )


                rows = latest_df[
                    latest_df[
                        HLB_COLUMN
                    ]
                    .astype(str)
                    .str.strip()
                    == selected
                ]


                if rows.empty:

                    st.error(
                        "❌ Enumerator not found."
                    )

                    st.stop()


                st.session_state[
                    "searched_enumerator"
                ] = selected


                st.session_state[
                    "searched_record"
                ] = (
                    rows
                    .iloc[0]
                    .to_dict()
                )


                st.success(
                    "✅ Data loaded"
                )


            except Exception as e:

                st.error(
                    "❌ Google Sheet loading failed."
                )

                st.code(
                    str(e)
                )


    # ========================================================
    # NO SEARCH
    # ========================================================

    if (
        "searched_enumerator"
        not in st.session_state
    ):

        st.info(
            "Select Enumerator → SEARCH"
        )

        st.stop()


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
            "⚠️ Enumerator changed. Press SEARCH again."
        )

        st.stop()


    # ========================================================
    # RECORD
    # ========================================================

    record = st.session_state[
        "searched_record"
    ]


    current_status = get_value(
        record,
        "STATUS"
    ).upper()


    if not current_status:

        current_status = "NOT STARTED"


    # ========================================================
    # ONLY 3 DETAILS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📋 Enumerator Details'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # HLB NUMBER
    # ========================================================

    st.markdown(
        f"""
        <div class="result-card">

        <div class="result-label">
        HLB NUMBER - ENUMERATOR
        </div>

        <div class="result-value">
        {get_value(
            record,
            HLB_COLUMN
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MOBILE
    # ========================================================

    st.markdown(
        f"""
        <div class="result-card">

        <div class="result-label">
        ENUMERATOR MOBILE NUMBER
        </div>

        <div class="result-value">
        📱 {get_value(
            record,
            "ENUMERATOR MOBILE NUMBER"
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # HLB DESCRIPTION
    # ========================================================

    st.markdown(
        f"""
        <div class="result-card">

        <div class="result-label">
        HLB DESCRIPTION
        </div>

        <div class="result-value">
        {get_value(
            record,
            "HLB DESCRIPTION"
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CURRENT STATUS
    # ========================================================

    if current_status == "COMPLETED":

        st.markdown(
            """
            <div class="status-completed">
            🟢 COMPLETED
            </div>
            """,
            unsafe_allow_html=True
        )

    elif current_status == "IN PROGRESS":

        st.markdown(
            """
            <div class="status-progress">
            🟡 IN PROGRESS
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="status-notstarted">
            🔴 NOT STARTED
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # UPDATE
    # ========================================================

    if current_status == "COMPLETED":

        st.success(
            "🔒 Enumerator is COMPLETED and LOCKED."
        )

        completed_date = get_value(
            record,
            "COMPLETED DATE"
        )

        if completed_date:

            st.caption(
                f"Completed Date: {completed_date}"
            )


    else:

        st.markdown(
            '<div class="section-title">'
            '📝 Update Enumeration'
            '</div>',
            unsafe_allow_html=True
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

        except Exception:

            default_index = 0


        status = st.selectbox(
            "Status",
            status_options,
            index=default_index
        )


        try:

            current_pending = int(
                float(
                    get_value(
                        record,
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
            step=1
        )


        expected_date = st.date_input(
            "📅 Expected Completion Date",
            value=date.today()
        )


        remarks = st.text_area(
            "📝 Remarks / Reason for Pending",
            value=get_value(
                record,
                "REMARKS"
            ),
            height=80,
            placeholder="Enter reason..."
        )


        if st.button(
            "💾 SAVE UPDATE",
            type="primary",
            width="stretch"
        ):


            if status == "IN PROGRESS":

                if pending <= 0:

                    st.error(
                        "⚠️ Pending Count is required."
                    )

                    st.stop()


                if not remarks.strip():

                    st.error(
                        "⚠️ Remarks are required."
                    )

                    st.stop()


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
                "💾 Saving..."
            ):

                try:

                    result = send_update(
                        payload
                    )


                    if result.get(
                        "success"
                    ):

                        st.success(
                            "✅ Saved successfully."
                        )

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


                    else:

                        st.error(
                            "❌ Save failed."
                        )

                        st.code(
                            result.get(
                                "message",
                                "Unknown error"
                            )
                        )


                except Exception as e:

                    st.error(
                        "❌ Connection error."
                    )

                    st.code(
                        str(e)
                    )


    # ========================================================
    # OVERALL PROGRESS
    # ========================================================

    st.divider()


    st.markdown(
        '<div class="section-title">'
        '📊 Overall Progress'
        '</div>',
        unsafe_allow_html=True
    )


    (
        total,
        completed,
        in_progress,
        not_started,
        total_pending,
        percentage
    ) = calculate_summary(df)


    # ========================================================
    # SUMMARY CARDS
    # ========================================================

    c1, c2, c3 = st.columns(3)


    with c1:

        st.markdown(
            f"""
            <div class="summary-card">

            <div class="summary-number">
            {total}
            </div>

            <div class="summary-label">
            TOTAL ENUMERATOR
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="summary-card">

            <div class="summary-number">
            {completed}
            </div>

            <div class="summary-label">
            🟢 COMPLETED
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
            <div class="summary-card">

            <div class="summary-number">
            {total_pending}
            </div>

            <div class="summary-label">
            📌 PENDING
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            f"""
            <div class="summary-card">

            <div class="summary-number">
            {in_progress}
            </div>

            <div class="summary-label">
            🟡 IN PROGRESS
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="summary-card">

            <div class="summary-number">
            {not_started}
            </div>

            <div class="summary-label">
            🔴 NOT STARTED
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # PROGRESS BAR
    # ========================================================

    st.markdown(
        f"""
        <div style="
        text-align:center;
        font-size:14px;
        font-weight:900;
        margin-top:8px;
        ">
        {percentage:.1f}% COMPLETED
        </div>
        """,
        unsafe_allow_html=True
    )


    st.progress(
        int(percentage)
    )


    # ========================================================
    # DONUT
    # ========================================================

    chart_data = pd.DataFrame({

        "STATUS": [
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ],

        "COUNT": [
            completed,
            in_progress,
            not_started
        ]
    })


    fig = px.pie(
        chart_data,
        names="STATUS",
        values="COUNT",
        hole=0.60
    )


    fig.update_traces(
        textinfo="label+percent"
    )


    fig.update_layout(

        title={
            "text":
            "Enumerator Status",
            "x": 0.5
        },

        height=300,

        margin=dict(
            l=0,
            r=0,
            t=45,
            b=0
        ),

        legend=dict(
            orientation="h",
            y=-0.08,
            x=0.5,
            xanchor="center"
        )
    )


    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )


    # ========================================================
    # STATUS TABLE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📋 Enumerator Status'
        '</div>',
        unsafe_allow_html=True
    )


    table_search = st.text_input(
        "🔎 Search",
        key="status_search"
    )


    table_status = st.selectbox(
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


    if table_search:

        mask = (
            display_df
            .astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    table_search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        )

        display_df = display_df[
            mask
        ]


    if table_status != "ALL":

        display_df = display_df[
            display_df["STATUS"]
            == table_status
        ]


    table_columns = [

        HLB_COLUMN,

        "VILLAGE NAME",

        "ENUMERATOR MOBILE NUMBER",

        "STATUS",

        "PENDING",

        "EXPECTED DATE",

        "REMARKS"
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
        hide_index=True,
        height=380
    )


# ============================================================
# ADMIN MODE
# ============================================================

else:

    if (
        "admin_logged_in"
        not in st.session_state
    ):

        st.session_state.admin_logged_in = False


    if not st.session_state.admin_logged_in:

        st.markdown(
            '<div class="section-title">'
            '🔐 Admin Login'
            '</div>',
            unsafe_allow_html=True
        )


        username = st.text_input(
            "Username"
        )


        password = st.text_input(
            "Password",
            type="password"
        )


        if st.button(
            "🔐 LOGIN",
            type="primary",
            width="stretch"
        ):

            if (
                username == ADMIN_USERNAME
                and
                password == ADMIN_PASSWORD
            ):

                st.session_state.admin_logged_in = True

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )


        st.stop()


    # ========================================================
    # ADMIN
    # ========================================================

    c1, c2 = st.columns(
        [5, 1]
    )


    with c1:

        st.success(
            "🔓 Admin Dashboard"
        )


    with c2:

        if st.button(
            "Logout"
        ):

            st.session_state.admin_logged_in = False

            st.rerun()


    (
        total,
        completed,
        in_progress,
        not_started,
        total_pending,
        percentage
    ) = calculate_summary(df)


    # ========================================================
    # ADMIN SUMMARY
    # ========================================================

    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "TOTAL",
            total
        )


    with c2:

        st.metric(
            "COMPLETED",
            completed
        )


    with c3:

        st.metric(
            "PENDING",
            total_pending
        )


    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "IN PROGRESS",
            in_progress
        )


    with c2:

        st.metric(
            "NOT STARTED",
            not_started
        )


    st.progress(
        int(percentage)
    )


    st.markdown(
        f"""
        <div style="
        text-align:center;
        font-weight:900;
        ">
        Overall Completion: {percentage:.1f}%
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # ADMIN DONUT
    # ========================================================

    admin_chart = pd.DataFrame({

        "STATUS": [
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ],

        "COUNT": [
            completed,
            in_progress,
            not_started
        ]
    })


    admin_fig = px.pie(
        admin_chart,
        names="STATUS",
        values="COUNT",
        hole=0.60
    )


    admin_fig.update_traces(
        textinfo="label+percent"
    )


    admin_fig.update_layout(

        title={
            "text":
            "Enumerator Status",
            "x": 0.5
        },

        height=300,

        margin=dict(
            l=0,
            r=0,
            t=45,
            b=0
        )
    )


    st.plotly_chart(
        admin_fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )


    # ========================================================
    # ADMIN TABLE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📋 Full Enumeration Report'
        '</div>',
        unsafe_allow_html=True
    )


    admin_search = st.text_input(
        "🔎 Search",
        key="admin_search"
    )


    admin_status = st.selectbox(
        "Status",
        [
            "ALL",
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ],
        key="admin_status"
    )


    admin_df = df.copy()


    if admin_search:

        mask = (
            admin_df
            .astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    admin_search,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        )

        admin_df = admin_df[
            mask
        ]


    if admin_status != "ALL":

        admin_df = admin_df[
            admin_df["STATUS"]
            == admin_status
        ]


    st.dataframe(
        admin_df,
        width="stretch",
        hide_index=True,
        height=500
    )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    csv_data = (
        df
        .to_csv(index=False)
        .encode("utf-8")
    )


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

st.markdown(
    """
<div style="
text-align:center;
color:#94a3b8;
font-size:9px;
padding-top:12px;
">

📋 Anaimalai Taluk Census Enumeration
<br>
Google Sheet Live Data

</div>
""",
    unsafe_allow_html=True
)