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
# GOOGLE SHEET
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
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ================= GLOBAL ================= */

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
    max-width: 1150px;
    padding-top: 0.4rem;
    padding-left: 0.6rem;
    padding-right: 0.6rem;
    padding-bottom: 2rem;
}


/* ================= HEADER ================= */

.dashboard-header {
    background: linear-gradient(
        135deg,
        #0f766e,
        #115e59,
        #134e4a
    );

    color: white;

    border-radius: 20px;

    padding: 20px 14px;

    text-align: center;

    margin-bottom: 18px;

    box-shadow:
        0 8px 25px rgba(15,118,110,0.20);
}

.dashboard-title {
    font-size: 28px;
    font-weight: 900;
    line-height: 1.25;
}

.dashboard-subtitle {
    margin-top: 6px;
    font-size: 13px;
    opacity: 0.9;
}


/* ================= SECTION ================= */

.section-title {
    font-size: 21px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 8px;
    margin-bottom: 12px;
}


/* ================= CARD ================= */

.search-card,
.report-card {
    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 18px;

    padding: 16px;

    box-shadow:
        0 5px 18px rgba(15,23,42,0.07);

    margin-bottom: 18px;
}


/* ================= INFO BOX ================= */

.info-box {
    background: #f8fafc;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    padding: 11px;

    margin-bottom: 10px;

    min-height: 58px;
}

.info-label {
    color: #64748b;

    font-size: 10px;

    font-weight: 850;

    text-transform: uppercase;
}

.info-value {
    color: #0f172a;

    font-size: 14px;

    font-weight: 750;

    margin-top: 4px;

    word-break: break-word;
}


/* ================= STATUS ================= */

.status-completed {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;

    padding: 11px;

    border-radius: 14px;

    text-align: center;

    font-weight: 900;

    margin-bottom: 14px;
}

.status-progress {
    background: #fef3c7;
    color: #92400e;
    border: 1px solid #fcd34d;

    padding: 11px;

    border-radius: 14px;

    text-align: center;

    font-weight: 900;

    margin-bottom: 14px;
}

.status-notstarted {
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fca5a5;

    padding: 11px;

    border-radius: 14px;

    text-align: center;

    font-weight: 900;

    margin-bottom: 14px;
}


/* ================= SUMMARY ================= */

.summary-card {
    border-radius: 15px;

    padding: 12px;

    text-align: center;

    border: 1px solid #e2e8f0;

    background: #ffffff;

    box-shadow:
        0 3px 12px rgba(15,23,42,0.05);
}

.summary-number {
    font-size: 25px;
    font-weight: 900;
    color: #0f172a;
}

.summary-label {
    font-size: 10px;
    font-weight: 800;
    color: #64748b;
}


/* ================= BUTTON ================= */

.stButton > button {
    width: 100%;
    min-height: 45px;
    border-radius: 11px;
    font-weight: 850;
}


/* ================= MOBILE ================= */

@media only screen and (max-width: 768px) {

    .block-container {
        padding-top: 0.2rem;
        padding-left: 0.35rem;
        padding-right: 0.35rem;
    }

    .dashboard-header {
        padding: 14px 8px;
        border-radius: 15px;
        margin-bottom: 12px;
    }

    .dashboard-title {
        font-size: 18px;
    }

    .dashboard-subtitle {
        font-size: 9px;
    }

    .section-title {
        font-size: 18px;
    }

    .search-card,
    .report-card {
        padding: 10px;
        border-radius: 14px;
    }

    .info-box {
        padding: 9px;
        min-height: 52px;
    }

    .info-label {
        font-size: 8px;
    }

    .info-value {
        font-size: 12px;
    }

    .summary-number {
        font-size: 20px;
    }

    .summary-label {
        font-size: 8px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 9px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 19px;
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
# FRESH GOOGLE SHEET LOAD
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
# INITIAL DATA
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

    st.write(
        "Available columns:",
        df.columns.tolist()
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
    # SELECT ENUMERATOR
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '👤 Select Enumerator'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="search-card">',
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


    # IMPORTANT:
    # FIRST OPTION
    dropdown_options = [
        "-- Select Enumerator --"
    ] + enumerators


    selected = st.selectbox(
        "HLB Number - Enumerator",
        dropdown_options,
        index=0,
        key="enum_selector"
    )


    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    if st.button(
        "🔍 SEARCH ENUMERATOR",
        type="primary",
        width="stretch"
    ):

        # ----------------------------------------------
        # MUST SELECT ENUMERATOR
        # ----------------------------------------------

        if selected == "-- Select Enumerator --":

            st.warning(
                "⚠️ Please select an Enumerator first."
            )

            st.stop()


        # ----------------------------------------------
        # LOAD LATEST GOOGLE SHEET
        # ----------------------------------------------

        with st.spinner(
            "🔄 Loading latest Google Sheet data..."
        ):

            try:

                latest_df = (
                    load_fresh_google_sheet()
                )


                # --------------------------------------
                # FIND ENUMERATOR
                # --------------------------------------

                rows = latest_df[
                    latest_df[HLB_COLUMN]
                    .astype(str)
                    .str.strip()
                    == selected
                ]


                if rows.empty:

                    st.error(
                        "❌ Enumerator not found in Google Sheet."
                    )

                    st.stop()


                # --------------------------------------
                # SAVE SEARCH RESULT
                # --------------------------------------

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


                # Also update cached data
                st.cache_data.clear()


                st.success(
                    "✅ Enumerator details loaded successfully."
                )


            except Exception as e:

                st.error(
                    "❌ Unable to load Google Sheet."
                )

                st.code(
                    str(e)
                )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # NO SEARCH YET
    # ========================================================

    if (
        "searched_enumerator"
        not in st.session_state
    ):

        st.info(
            "👆 Select an Enumerator and click SEARCH to view the full report."
        )

        st.stop()


    # ========================================================
    # IF DROPDOWN CHANGED
    # SEARCH AGAIN
    # ========================================================

    if (
        st.session_state[
            "searched_enumerator"
        ]
        != selected
    ):

        st.warning(
            "⚠️ Enumerator changed. Please click SEARCH again."
        )

        st.stop()


    # ========================================================
    # GET RECORD
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
    # STATUS BANNER
    # ========================================================

    if current_status == "COMPLETED":

        st.markdown(
            """
            <div class="status-completed">
            🟢 ENUMERATION COMPLETED
            </div>
            """,
            unsafe_allow_html=True
        )

    elif current_status == "IN PROGRESS":

        st.markdown(
            """
            <div class="status-progress">
            🟡 ENUMERATION IN PROGRESS
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="status-notstarted">
            🔴 ENUMERATION NOT STARTED
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # FULL ENUMERATOR DETAILS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📋 Enumerator Full Report'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="report-card">',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # HLB + CIRCLE
    # --------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="info-box">

            <div class="info-label">
            HLB NUMBER - ENUMERATOR
            </div>

            <div class="info-value">
            {get_value(record, HLB_COLUMN)}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="info-box">

            <div class="info-label">
            CIRCLE NUMBER
            </div>

            <div class="info-value">
            {get_value(record, "CIRCLE NUMBER")}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # VILLAGE + ENUMERATOR MOBILE
    # --------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="info-box">

            <div class="info-label">
            VILLAGE NAME
            </div>

            <div class="info-value">
            {get_value(record, "VILLAGE NAME")}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="info-box">

            <div class="info-label">
            ENUMERATOR MOBILE NUMBER
            </div>

            <div class="info-value">
            📱 {get_value(record, "ENUMERATOR MOBILE NUMBER")}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="info-box">

        <div class="info-label">
        SUPERVISOR NAME & MOBILE NUMBER
        </div>

        <div class="info-value">
        {get_value(
            record,
            "SUPERVISOR NAME & MOBILE NUMBER"
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # HLB DESCRIPTION
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="info-box">

        <div class="info-label">
        HLB DESCRIPTION
        </div>

        <div class="info-value">
        {get_value(
            record,
            "HLB DESCRIPTION"
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # STATUS + PENDING
    # --------------------------------------------------------

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


    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            f"""
            <div class="info-box">

            <div class="info-label">
            CURRENT STATUS
            </div>

            <div class="info-value">
            {current_status}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
            <div class="info-box">

            <div class="info-label">
            PENDING COUNT
            </div>

            <div class="info-value">
            📌 {current_pending}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # EXPECTED DATE
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="info-box">

        <div class="info-label">
        EXPECTED COMPLETION DATE
        </div>

        <div class="info-value">
        📅 {get_value(
            record,
            "EXPECTED DATE"
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # LAST UPDATED
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="info-box">

        <div class="info-label">
        LAST UPDATED
        </div>

        <div class="info-value">
        🕒 {get_value(
            record,
            "LAST UPDATED"
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # COMPLETED DATE
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="info-box">

        <div class="info-label">
        COMPLETED DATE
        </div>

        <div class="info-value">
        {get_value(
            record,
            "COMPLETED DATE"
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # REMARKS
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="info-box">

        <div class="info-label">
        REMARKS / REASON FOR PENDING
        </div>

        <div class="info-value">
        {get_value(
            record,
            "REMARKS"
        )}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # UPDATE ENUMERATION
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
            index=default_index,
            key="update_status"
        )


        pending = st.number_input(
            "📌 Pending Count",
            min_value=0,
            value=current_pending,
            step=1,
            key="update_pending"
        )


        expected_date = st.date_input(
            "📅 Expected Completion Date",
            value=date.today(),
            key="update_expected_date"
        )


        remarks = st.text_area(
            "📝 Remarks / Reason for Pending",
            value=get_value(
                record,
                "REMARKS"
            ),
            height=110,
            placeholder=(
                "Enter detailed reason for pending..."
            ),
            key="update_remarks"
        )


        # ====================================================
        # SAVE
        # ====================================================

        if st.button(
            "💾 SAVE ENUMERATION UPDATE",
            type="primary",
            width="stretch"
        ):


            # -----------------------------------------------
            # IN PROGRESS VALIDATION
            # -----------------------------------------------

            if status == "IN PROGRESS":

                if pending <= 0:

                    st.error(
                        "⚠️ Pending Count is required."
                    )

                    st.stop()


                if not remarks.strip():

                    st.error(
                        "⚠️ Remarks are required for IN PROGRESS."
                    )

                    st.stop()


            # -----------------------------------------------
            # COMPLETED
            # -----------------------------------------------

            if status == "COMPLETED":

                pending = 0


            # -----------------------------------------------
            # PAYLOAD
            # -----------------------------------------------

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


            # -----------------------------------------------
            # SEND
            # -----------------------------------------------

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
                            "✅ Data successfully saved to Google Sheet."
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
                        "❌ Connection Error"
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
        '📊 Overall Enumeration Progress'
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
    # SUMMARY
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
            👥 TOTAL ENUMERATOR
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
            📌 TOTAL PENDING
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
    # PROGRESS
    # ========================================================

    st.markdown(
        f"""
        <div style="
        text-align:center;
        margin-top:16px;
        font-size:17px;
        font-weight:900;
        ">
        Overall Completion: {percentage:.1f}%
        </div>
        """,
        unsafe_allow_html=True
    )


    st.progress(
        int(percentage)
    )


    # ========================================================
    # DONUT CHART
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
        hole=0.58
    )


    fig.update_traces(
        textinfo="label+percent",
        textposition="inside",

        hovertemplate=(
            "<b>%{label}</b>"
            "<br>Enumerator: %{value}"
            "<extra></extra>"
        )
    )


    fig.update_layout(

        title={
            "text":
            "👥 Enumerator Status",
            "x": 0.5,
            "xanchor": "center"
        },

        height=350,

        margin=dict(
            l=5,
            r=5,
            t=55,
            b=5
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5
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
    # ENUMERATOR STATUS TABLE
    # ========================================================

    st.divider()


    st.markdown(
        '<div class="section-title">'
        '📋 Enumerator Status Report'
        '</div>',
        unsafe_allow_html=True
    )


    table_search = st.text_input(
        "🔎 Search HLB / Enumerator / Village",
        key="enum_table_search"
    )


    table_status = st.selectbox(
        "Filter Status",
        [
            "ALL",
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ],
        key="enum_table_status"
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
        hide_index=True,
        height=430
    )


    st.caption(
        f"Showing {len(display_df)} "
        f"of {len(df)} HLB records"
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
    # ADMIN HEADER
    # ========================================================

    c1, c2 = st.columns([5, 1])


    with c1:

        st.success(
            "🔓 Admin Dashboard"
        )


    with c2:

        if st.button("Logout"):

            st.session_state.admin_logged_in = False

            st.rerun()


    # ========================================================
    # ADMIN SUMMARY
    # ========================================================

    (
        total,
        completed,
        in_progress,
        not_started,
        total_pending,
        percentage
    ) = calculate_summary(df)


    st.markdown(
        '<div class="section-title">'
        '📊 Overall Progress'
        '</div>',
        unsafe_allow_html=True
    )


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "👥 TOTAL ENUMERATOR",
            total
        )


    with c2:

        st.metric(
            "🟢 COMPLETED",
            completed
        )


    with c3:

        st.metric(
            "📌 TOTAL PENDING",
            total_pending
        )


    c1, c2 = st.columns(2)


    with c1:

        st.metric(
            "🟡 IN PROGRESS",
            in_progress
        )


    with c2:

        st.metric(
            "🔴 NOT STARTED",
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
        font-size:17px;
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
        hole=0.58
    )


    admin_fig.update_traces(
        textinfo="label+percent"
    )


    admin_fig.update_layout(

        title={
            "text":
            "👥 Enumerator Status",
            "x": 0.5
        },

        height=350,

        margin=dict(
            l=5,
            r=5,
            t=55,
            b=5
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
    # ADMIN REPORT
    # ========================================================

    st.divider()


    st.markdown(
        '<div class="section-title">'
        '📋 Full Enumeration Report'
        '</div>',
        unsafe_allow_html=True
    )


    admin_search = st.text_input(
        "🔎 Search HLB / Enumerator / Village",
        key="admin_search"
    )


    admin_status = st.selectbox(
        "Filter Status",
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


    admin_columns = [

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


    admin_columns = [
        c for c in admin_columns
        if c in admin_df.columns
    ]


    st.dataframe(
        admin_df[
            admin_columns
        ],
        width="stretch",
        hide_index=True,
        height=500
    )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.divider()


    st.markdown(
        "### 📥 Export Report"
    )


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
font-size:11px;
padding-top:22px;
">

📋 Anaimalai Taluk Census Enumeration
<br>
Google Sheet Live Data

</div>
""",
    unsafe_allow_html=True
)