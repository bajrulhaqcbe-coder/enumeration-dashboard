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

/* ============================================================
   REMOVE DEFAULT STREAMLIT UI
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ============================================================
   PAGE
   ============================================================ */

.block-container {
    max-width: 1150px;
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}


/* ============================================================
   HEADER
   ============================================================ */

.dashboard-header {
    background: linear-gradient(
        135deg,
        #0f766e,
        #115e59
    );

    color: white;

    padding: 18px 20px;

    border-radius: 18px;

    text-align: center;

    margin-bottom: 18px;

    box-shadow:
        0 6px 18px rgba(0,0,0,0.12);
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


/* ============================================================
   SECTION
   ============================================================ */

.section-title {
    font-size: 21px;
    font-weight: 800;
    margin-top: 8px;
    margin-bottom: 12px;
}


/* ============================================================
   SEARCH CARD
   ============================================================ */

.search-card {
    background: white;

    padding: 18px;

    border-radius: 16px;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 3px 12px rgba(0,0,0,0.06);

    margin-bottom: 15px;
}


/* ============================================================
   FULL DETAILS CARD
   ============================================================ */

.details-card {
    background: white;

    padding: 18px;

    border-radius: 18px;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 4px 15px rgba(0,0,0,0.07);

    margin-bottom: 15px;
}


/* ============================================================
   INFO BOX
   ============================================================ */

.info-box {
    background: #f8fafc;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    padding: 12px;

    margin-bottom: 9px;

    min-height: 62px;
}

.info-label {
    color: #64748b;

    font-size: 11px;

    font-weight: 700;

    text-transform: uppercase;
}

.info-value {
    color: #0f172a;

    font-size: 14px;

    font-weight: 700;

    margin-top: 4px;

    word-break: break-word;
}


/* ============================================================
   STATUS
   ============================================================ */

.status-completed {
    background: #dcfce7;

    color: #166534;

    padding: 10px 16px;

    border-radius: 30px;

    font-weight: 800;

    text-align: center;

    margin-bottom: 12px;
}

.status-progress {
    background: #fef3c7;

    color: #92400e;

    padding: 10px 16px;

    border-radius: 30px;

    font-weight: 800;

    text-align: center;

    margin-bottom: 12px;
}

.status-notstarted {
    background: #fee2e2;

    color: #991b1b;

    padding: 10px 16px;

    border-radius: 30px;

    font-weight: 800;

    text-align: center;

    margin-bottom: 12px;
}


/* ============================================================
   PENDING CARD
   ============================================================ */

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

    margin: 10px 0 15px 0;
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


/* ============================================================
   TABLE
   ============================================================ */

.table-title {
    font-size: 20px;

    font-weight: 800;

    margin-top: 18px;

    margin-bottom: 10px;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {
    width: 100%;

    min-height: 45px;

    border-radius: 10px;

    font-weight: 800;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media only screen and (max-width: 768px) {

    .block-container {
        padding:
            0.5rem
            0.55rem
            1.2rem
            0.55rem;
    }

    .dashboard-header {
        padding: 13px 9px;

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
    }

    .search-card {
        padding: 12px;

        border-radius: 13px;
    }

    .details-card {
        padding: 12px;

        border-radius: 14px;
    }

    .info-box {
        padding: 9px;

        min-height: 55px;
    }

    .info-label {
        font-size: 10px;
    }

    .info-value {
        font-size: 13px;
    }

    .pending-number {
        font-size: 27px;
    }

    .table-title {
        font-size: 18px;
    }

    div[data-testid="stMetric"] {
        padding: 6px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 10px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 20px;
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

        data = pd.read_csv(CSV_URL)

        data = data.dropna(
            how="all"
        )

        data.columns = (
            data.columns
            .astype(str)
            .str.strip()
        )

        data = data.fillna("")

        if "STATUS" not in data.columns:

            data["STATUS"] = (
                "NOT STARTED"
            )

        data["STATUS"] = (
            data["STATUS"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        data.loc[
            data["STATUS"].isin(
                ["", "NAN"]
            ),
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
# GET VALUE
# ============================================================

def get_value(record, column):

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
            "message":
                response_text
        }


# ============================================================
# COUNTS
# ============================================================

def get_counts(data):

    total = len(data)

    completed = len(
        data[
            data["STATUS"]
            == "COMPLETED"
        ]
    )

    in_progress = len(
        data[
            data["STATUS"]
            == "IN PROGRESS"
        ]
    )

    not_started = len(
        data[
            data["STATUS"]
            == "NOT STARTED"
        ]
    )

    pending = 0

    if "PENDING" in data.columns:

        pending = int(
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
    # ENUMERATOR UPDATE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '👤 Enumerator Update'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SEARCH CARD
    # ========================================================

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
        x
        for x in enumerators
        if x
    ]

    selected = st.selectbox(
        "Select HLB Number - Enumerator",
        enumerators,
        key="enum_selector"
    )


    # ========================================================
    # SEARCH
    # ========================================================

    if st.button(
        "🔍 SEARCH",
        type="primary",
        width="stretch",
        key="enumerator_search"
    ):

        with st.spinner(
            "🔄 Loading latest Google Sheet data..."
        ):

            try:

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


                rows = latest_df[
                    latest_df[HLB_COLUMN]
                    .astype(str)
                    .str.strip()
                    == selected
                ]


                if rows.empty:

                    st.error(
                        "❌ Enumerator not found."
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
                        "✅ Latest Google Sheet data loaded."
                    )

            except Exception as e:

                st.error(
                    "❌ Google Sheet loading failed."
                )

                st.code(
                    str(e)
                )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # BEFORE SEARCH
    # ========================================================

    if (
        "searched_enumerator"
        not in st.session_state
    ):

        st.info(
            "👆 Select the Enumerator and press SEARCH."
        )

        st.stop()


    # ========================================================
    # SELECTED ENUMERATOR CHANGED
    # ========================================================

    if (
        st.session_state[
            "searched_enumerator"
        ]
        != selected
    ):

        st.warning(
            "⚠️ Enumerator changed. "
            "Please press SEARCH again."
        )

        st.stop()


    # ========================================================
    # RECORD
    # ========================================================

    record = (
        st.session_state[
            "searched_record"
        ]
    )


    # ========================================================
    # CURRENT STATUS
    # ========================================================

    current_status = get_value(
        record,
        "STATUS"
    ).upper()

    if not current_status:

        current_status = (
            "NOT STARTED"
        )


    # ========================================================
    # STATUS BADGE
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
    # FULL ENUMERATOR DETAILS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📋 Enumerator Full Details'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="details-card">',
        unsafe_allow_html=True
    )


    # ========================================================
    # ROW 1
    # ========================================================

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


    # ========================================================
    # ROW 2
    # ========================================================

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="info-box">
            <div class="info-label">
            SUPERVISOR NAME & MOBILE
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


    with c2:

        st.markdown(
            f"""
            <div class="info-box">
            <div class="info-label">
            ENUMERATOR MOBILE NUMBER
            </div>
            <div class="info-value">
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
    # ROW 3
    # ========================================================

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="info-box">
            <div class="info-label">
            VILLAGE NAME
            </div>
            <div class="info-value">
            {get_value(
                record,
                "VILLAGE NAME"
            )}
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
            STATUS
            </div>
            <div class="info-value">
            {current_status}
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


    # ========================================================
    # EXPECTED DATE
    # ========================================================

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="info-box">

            <div class="info-label">
            EXPECTED DATE
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


    with c2:

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


    # ========================================================
    # COMPLETED DATE
    # ========================================================

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


    # ========================================================
    # REMARKS
    # ========================================================

    st.markdown(
        f"""
        <div class="info-box">

        <div class="info-label">
        REMARKS
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
        📌 TOTAL PENDING ENTRIES
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
            "🔒 This Enumerator is COMPLETED and LOCKED."
        )

    else:

        # ====================================================
        # UPDATE
        # ====================================================

        st.divider()

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


        # ====================================================
        # EXPECTED DATE
        # ====================================================

        expected_default = date.today()

        old_date = get_value(
            record,
            "EXPECTED DATE"
        )

        if old_date:

            try:

                expected_default = (
                    pd.to_datetime(
                        old_date,
                        dayfirst=True
                    ).date()
                )

            except Exception:

                pass


        expected_date = st.date_input(
            "📅 Expected Completion Date",
            value=expected_default,
            key="update_expected_date"
        )


        # ====================================================
        # REMARKS
        # ====================================================

        remarks = st.text_area(
            "📝 Remarks / Reason for Pending",
            value=get_value(
                record,
                "REMARKS"
            ),
            height=110,
            placeholder=(
                "Example: "
                "25 entries completed, "
                "10 entries pending. "
                "Expected completion tomorrow."
            ),
            key="update_remarks"
        )


        # ====================================================
        # SAVE
        # ====================================================

        if st.button(
            "💾 SAVE UPDATE",
            type="primary",
            width="stretch",
            key="save_update"
        ):

            # ----------------------------------------------
            # VALIDATION
            # ----------------------------------------------

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


            # ----------------------------------------------
            # COMPLETED
            # ----------------------------------------------

            if status == "COMPLETED":

                pending = 0


            # ----------------------------------------------
            # PAYLOAD
            # ----------------------------------------------

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


            # ----------------------------------------------
            # SAVE
            # ----------------------------------------------

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


    # ========================================================
    # ENUMERATOR STATUS TABLE
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="table-title">'
        '📋 Enumerator Status Report'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SEARCH TABLE
    # ========================================================

    search_table = st.text_input(
        "🔎 Search HLB / Enumerator / Village",
        key="enum_table_search"
    )


    table_status = st.selectbox(
        "Status Filter",
        [
            "ALL",
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ],
        key="enum_table_status"
    )


    display_df = df.copy()


    if search_table:

        mask = (
            display_df
            .astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search_table,
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


    # ========================================================
    # STATUS TABLE COLUMNS
    # ========================================================

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
        column
        for column in table_columns
        if column in display_df.columns
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

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

        st.stop()


    # ========================================================
    # ADMIN HEADER
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
            "Logout",
            width="stretch"
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
    # ADMIN SUMMARY
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
        f"Overall Completion: "
        f"{percentage:.1f}%"
    )


    # ========================================================
    # ADMIN TABLE
    # ========================================================

    st.divider()

    st.markdown(
        "### 📋 Full Enumeration Report"
    )


    admin_search = st.text_input(
        "🔎 Search HLB / Enumerator / Village",
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
        column
        for column in admin_columns
        if column in admin_df.columns
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
    # EXPORT
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
padding-top:20px;
">

📋 Anaimalai Taluk Census Enumeration
<br>
Google Sheet Live Data

</div>
""",
    unsafe_allow_html=True
)