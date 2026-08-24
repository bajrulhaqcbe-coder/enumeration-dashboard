import streamlit as st
import pandas as pd
from datetime import date
import urllib.request
import json


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
# CONFIG
# ============================================================

SHEET_ID = "1vmxjbYABVPbu5PUVSLQO0H8J3TTflyTgGKOj5nH9Q14"
SHEET_GID = "1357887790"

CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=csv&gid={SHEET_GID}"
)

APPS_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbw-BOTf7BpNfNS85RI5pIXnwIB10jR2WTLmnjGIhRbr0MhnoKr7QywBlZMXeGt5HKQdBg/exec"
)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    max-width: 1100px;
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
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
    padding: 18px 20px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}

.dashboard-title {
    font-size: 28px;
    font-weight: 800;
    line-height: 1.25;
}

.dashboard-subtitle {
    font-size: 13px;
    opacity: 0.9;
    margin-top: 5px;
}


/* =========================================================
   SECTION TITLE
   ========================================================= */

.section-title {
    font-size: 21px;
    font-weight: 800;
    margin-top: 8px;
    margin-bottom: 12px;
}


/* =========================================================
   SEARCH CARD
   ========================================================= */

.search-card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}


/* =========================================================
   ENUMERATOR CARD
   ========================================================= */

.enum-card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07);
    margin-top: 12px;
    margin-bottom: 15px;
}


/* =========================================================
   STATUS BADGES
   ========================================================= */

.status-completed {
    background: #dcfce7;
    color: #166534;
    padding: 9px 15px;
    border-radius: 30px;
    font-weight: 800;
    text-align: center;
}

.status-progress {
    background: #fef3c7;
    color: #92400e;
    padding: 9px 15px;
    border-radius: 30px;
    font-weight: 800;
    text-align: center;
}

.status-notstarted {
    background: #fee2e2;
    color: #991b1b;
    padding: 9px 15px;
    border-radius: 30px;
    font-weight: 800;
    text-align: center;
}


/* =========================================================
   INFO CARDS
   ========================================================= */

.info-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 8px;
}

.info-label {
    color: #64748b;
    font-size: 11px;
    font-weight: 600;
}

.info-value {
    color: #0f172a;
    font-size: 15px;
    font-weight: 700;
    margin-top: 2px;
}


/* =========================================================
   PENDING CARD
   ========================================================= */

.pending-card {
    background: linear-gradient(
        135deg,
        #fff7ed,
        #ffedd5
    );
    border: 1px solid #fed7aa;
    border-radius: 16px;
    padding: 15px;
    text-align: center;
    margin: 10px 0;
}

.pending-number {
    font-size: 32px;
    font-weight: 900;
    color: #c2410c;
}

.pending-label {
    font-size: 12px;
    color: #9a3412;
    font-weight: 700;
}


/* =========================================================
   PROGRESS CARD
   ========================================================= */

.progress-card {
    background: #f8fafc;
    padding: 16px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
}


/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {
    width: 100%;
    min-height: 45px;
    border-radius: 10px;
    font-weight: 800;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media only screen and (max-width: 768px) {

    .block-container {
        padding: 0.55rem 0.65rem 1.2rem 0.65rem;
    }

    .dashboard-header {
        padding: 13px 10px;
        border-radius: 14px;
        margin-bottom: 12px;
    }

    .dashboard-title {
        font-size: 19px;
    }

    .dashboard-subtitle {
        font-size: 10px;
    }

    .section-title {
        font-size: 18px;
        margin-bottom: 8px;
    }

    .search-card {
        padding: 12px;
        border-radius: 13px;
    }

    .enum-card {
        padding: 12px;
        border-radius: 14px;
    }

    .info-box {
        padding: 9px;
    }

    .info-value {
        font-size: 14px;
    }

    .pending-number {
        font-size: 27px;
    }

    div[data-testid="stMetric"] {
        padding: 7px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 10px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 20px;
    }

    .stTextArea textarea {
        min-height: 90px;
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

        return df

    except Exception as e:

        st.error(
            "Google Sheet data could not be loaded."
        )

        st.code(str(e))

        return pd.DataFrame()


# ============================================================
# GET VALUE
# ============================================================

def get_value(record, column):

    if column not in record:
        return ""

    value = record.get(column, "")

    if pd.isna(value):
        return ""

    return str(value).strip()


# ============================================================
# SEND UPDATE
# ============================================================

def send_update(payload):

    data = json.dumps(payload).encode("utf-8")

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

        return json.loads(response_text)

    except Exception:

        return {
            "success": False,
            "message": response_text
        }


# ============================================================
# GET DASHBOARD COUNTS
# ============================================================

def get_counts(df):

    total = len(df)

    completed = len(
        df[df["STATUS"] == "COMPLETED"]
    )

    progress = len(
        df[df["STATUS"] == "IN PROGRESS"]
    )

    not_started = len(
        df[df["STATUS"] == "NOT STARTED"]
    )

    pending = 0

    if "PENDING" in df.columns:

        pending = int(
            pd.to_numeric(
                df["PENDING"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

    percentage = (
        completed / total * 100
        if total
        else 0
    )

    return (
        total,
        completed,
        progress,
        not_started,
        pending,
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
CENSUS ENUMERATION PROGRESS
</div>

<div class="dashboard-subtitle">
Enumeration Monitoring & Progress System
</div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

df = load_google_sheet()

if df.empty:
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
        "Mode",
        [
            "👤 Enumerator",
            "🔐 Admin"
        ]
    )

    st.divider()

    if st.button(
        "🔄 Refresh Data"
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
    # ENUMERATOR UPDATE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '👤 Enumerator Update'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="search-card">',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ENUMERATOR LIST
    # --------------------------------------------------------

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

    selected = st.selectbox(
        "Select HLB Number - Enumerator",
        enumerators,
        key="enum_selector"
    )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if st.button(
        "🔍 SEARCH",
        type="primary",
        width="stretch"
    ):

        with st.spinner(
            "Loading latest data..."
        ):

            try:

                # Fresh Google Sheet read
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

                latest_df = latest_df.fillna("")

                if "STATUS" not in latest_df.columns:
                    latest_df["STATUS"] = "NOT STARTED"

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

                rows = latest_df[
                    latest_df[HLB_COLUMN]
                    .astype(str)
                    .str.strip()
                    == selected
                ]

                if rows.empty:

                    st.error(
                        "Enumerator not found."
                    )

                else:

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
                        "✅ Latest data loaded"
                    )

            except Exception as e:

                st.error(
                    "Unable to load Google Sheet."
                )

                st.code(str(e))

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # WAIT FOR SEARCH
    # ========================================================

    if (
        "searched_enumerator"
        not in st.session_state
    ):

        st.info(
            "Select an Enumerator and press SEARCH."
        )

        st.stop()


    # ========================================================
    # CHECK SEARCH
    # ========================================================

    if (
        st.session_state[
            "searched_enumerator"
        ]
        != selected
    ):

        st.warning(
            "Enumerator changed. "
            "Please press SEARCH again."
        )

        st.stop()


    record = st.session_state[
        "searched_record"
    ]


    # ========================================================
    # STATUS
    # ========================================================

    current_status = get_value(
        record,
        "STATUS"
    ).upper()

    if not current_status:
        current_status = "NOT STARTED"


    if current_status == "COMPLETED":

        st.markdown(
            '<div class="status-completed">'
            '🟢 COMPLETED'
            '</div>',
            unsafe_allow_html=True
        )

    elif current_status == "IN PROGRESS":

        st.markdown(
            '<div class="status-progress">'
            '🟡 IN PROGRESS'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="status-notstarted">'
            '🔴 NOT STARTED'
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # BASIC DETAILS ONLY
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📌 HLB Details'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="info-box">
            <div class="info-label">HLB NUMBER</div>
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
            <div class="info-label">VILLAGE</div>
            <div class="info-value">
            {get_value(record, "VILLAGE NAME")}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # PENDING
    # ========================================================

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


    st.markdown(
        f"""
        <div class="pending-card">

        <div class="pending-number">
        {current_pending}
        </div>

        <div class="pending-label">
        📌 PENDING ENTRIES
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # COMPLETED LOCK
    # ========================================================

    if current_status == "COMPLETED":

        st.success(
            "🔒 Enumeration completed. "
            "This HLB is locked."
        )

        completed_date = get_value(
            record,
            "COMPLETED DATE"
        )

        if completed_date:

            st.caption(
                f"Completed: {completed_date}"
            )

        remarks = get_value(
            record,
            "REMARKS"
        )

        if remarks:

            st.markdown(
                "#### 📝 Remarks"
            )

            st.info(
                remarks
            )

        st.stop()


    # ========================================================
    # UPDATE SECTION
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📝 Update Enumeration'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # STATUS
    # ========================================================

    status_options = [
        "NOT STARTED",
        "IN PROGRESS",
        "COMPLETED"
    ]

    try:

        default_status = (
            status_options.index(
                current_status
            )
        )

    except Exception:

        default_status = 0


    status = st.selectbox(
        "Status",
        status_options,
        index=default_status,
        key="update_status"
    )


    # ========================================================
    # PENDING
    # ========================================================

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

    expected_default = date.today()

    old_expected = get_value(
        record,
        "EXPECTED DATE"
    )

    if old_expected:

        try:

            expected_default = (
                pd.to_datetime(
                    old_expected,
                    dayfirst=True
                ).date()
            )

        except Exception:
            pass


    expected_date = st.date_input(
        "📅 Expected Completion Date",
        value=expected_default,
        key="update_expected"
    )


    # ========================================================
    # REMARKS
    # ========================================================

    remarks = st.text_area(
        "📝 Remarks / Reason for Pending",
        value=get_value(
            record,
            "REMARKS"
        ),
        height=100,
        placeholder=(
            "Example: 20 entries completed, "
            "5 entries pending. "
            "Expected to complete tomorrow."
        ),
        key="update_remarks"
    )


    # ========================================================
    # SAVE
    # ========================================================

    if st.button(
        "💾 SAVE UPDATE",
        type="primary",
        width="stretch"
    ):

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if status == "IN PROGRESS":

            if pending <= 0:

                st.error(
                    "⚠️ Pending Count must be greater than 0."
                )

                st.stop()

            if not remarks.strip():

                st.error(
                    "⚠️ Please enter the reason for pending."
                )

                st.stop()


        if status == "COMPLETED":

            pending = 0


        # ----------------------------------------------------
        # PAYLOAD
        # ----------------------------------------------------

        payload = {

            "hlb": selected,

            "circle": get_value(
                record,
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
        # SAVE
        # ----------------------------------------------------

        with st.spinner(
            "Saving..."
        ):

            try:

                result = send_update(
                    payload
                )

                if result.get(
                    "success"
                ):

                    st.success(
                        "✅ Successfully updated Google Sheet."
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

                st.code(str(e))


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
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "🔐 LOGIN",
            type="primary"
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
                    "❌ Invalid login details."
                )

        st.stop()


    # ========================================================
    # ADMIN HEADER
    # ========================================================

    a1, a2 = st.columns([4, 1])

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
    # COUNTS
    # ========================================================

    (
        total,
        completed,
        in_progress,
        not_started,
        total_pending,
        percentage
    ) = get_counts(df)


    # ========================================================
    # SUMMARY
    # ========================================================

    st.markdown(
        "### 📊 Overall Progress"
    )

    c1, c2 = st.columns(2)

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

    c3, c4 = st.columns(2)

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

    st.metric(
        "📌 TOTAL PENDING",
        total_pending
    )

    st.progress(
        int(percentage)
    )

    st.caption(
        f"Overall Completion: {percentage:.1f}%"
    )


    # ========================================================
    # ADMIN SEARCH
    # ========================================================

    st.divider()

    st.markdown(
        "### 🔎 Search"
    )

    search = st.text_input(
        "Search HLB / Enumerator / Village"
    )

    status_filter = st.selectbox(
        "Status",
        [
            "ALL",
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ]
    )

    display_df = df.copy()

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


    if status_filter != "ALL":

        display_df = display_df[
            display_df["STATUS"]
            == status_filter
        ]


    # ========================================================
    # ADMIN TABLE
    # ========================================================

    columns = [

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

    columns = [
        c for c in columns
        if c in display_df.columns
    ]


    st.dataframe(
        display_df[columns],
        width="stretch",
        hide_index=True,
        height=450
    )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.divider()

    st.markdown(
        "### 📥 Export"
    )

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Full Report",
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
padding-top:20px;
">
📋 Anaimalai Taluk Census Enumeration
<br>
Google Sheet Live Data
</div>
""",
    unsafe_allow_html=True
)