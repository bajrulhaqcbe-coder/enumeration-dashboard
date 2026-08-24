import streamlit as st
import pandas as pd
from datetime import date
import urllib.request
import json
import time
import plotly.express as px


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ANAIMALAI TALUK - CENSUS",
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
# APPS SCRIPT
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


HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================
   BASIC
   ========================= */

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

    max-width: 1000px;

    padding-top: 0.25rem;
    padding-bottom: 1rem;

    padding-left: 0.35rem;
    padding-right: 0.35rem;
}


/* =========================
   HEADER
   ========================= */

.hero {

    background:
    linear-gradient(
        135deg,
        #064e3b,
        #0f766e,
        #0891b2
    );

    color: white;

    border-radius: 18px;

    padding: 14px 8px;

    text-align: center;

    margin-bottom: 8px;

    box-shadow:
    0 6px 20px rgba(0,0,0,.14);
}

.hero-title {

    font-size: 21px;

    font-weight: 900;

    line-height: 1.25;
}

.hero-sub {

    font-size: 9px;

    margin-top: 4px;

    opacity: .9;
}


/* =========================
   MENU
   ========================= */

.menu-box {

    background: white;

    border: 1px solid #dbeafe;

    border-radius: 12px;

    padding: 4px;

    margin-bottom: 7px;

    box-shadow:
    0 3px 10px rgba(0,0,0,.05);
}


/* =========================
   SECTION
   ========================= */

.section-title {

    font-size: 16px;

    font-weight: 900;

    color: #0f172a;

    margin-top: 7px;

    margin-bottom: 5px;
}


/* =========================
   SEARCH
   ========================= */

.search-box {

    background:
    linear-gradient(
        135deg,
        #ffffff,
        #f0fdfa
    );

    border: 1px solid #99f6e4;

    border-radius: 14px;

    padding: 7px;

    margin-bottom: 7px;
}


/* =========================
   INFO CARD
   ========================= */

.info-card {

    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 11px;

    padding: 7px 9px;

    margin-bottom: 5px;

    box-shadow:
    0 2px 8px rgba(15,23,42,.05);
}

.info-label {

    color: #64748b;

    font-size: 8px;

    font-weight: 900;
}

.info-value {

    color: #0f172a;

    font-size: 12px;

    font-weight: 850;

    margin-top: 2px;

    word-break: break-word;
}


/* =========================
   STATUS
   ========================= */

.status-card {

    border-radius: 12px;

    padding: 8px;

    text-align: center;

    font-size: 12px;

    font-weight: 900;

    margin: 6px 0;
}

.status-completed {

    background: #dcfce7;

    color: #166534;

    border: 1px solid #86efac;
}

.status-progress {

    background: #fef3c7;

    color: #92400e;

    border: 1px solid #fcd34d;
}

.status-notstarted {

    background: #fee2e2;

    color: #991b1b;

    border: 1px solid #fca5a5;
}


/* =========================
   GIFT SUCCESS CARD
   ========================= */

.gift-card {

    position: relative;

    overflow: hidden;

    background:
    linear-gradient(
        135deg,
        #fff7ed,
        #fef3c7,
        #ecfdf5
    );

    border: 2px solid #f59e0b;

    border-radius: 20px;

    padding: 15px 12px;

    margin: 8px 0 10px 0;

    text-align: center;

    box-shadow:
    0 8px 25px rgba(245,158,11,.20);

    animation:
    giftPop .35s ease-out;
}

.gift-card:before {

    content: "🎁";

    position: absolute;

    font-size: 65px;

    opacity: .08;

    right: -5px;

    top: -13px;
}

.gift-title {

    font-size: 18px;

    font-weight: 950;

    color: #92400e;
}

.gift-sub {

    font-size: 10px;

    color: #475569;

    margin: 4px 0 8px 0;
}

.gift-grid {

    display: grid;

    grid-template-columns:
    repeat(3,1fr);

    gap: 5px;
}

.gift-item {

    background:
    rgba(255,255,255,.75);

    border-radius: 9px;

    padding: 6px 3px;
}

.gift-label {

    font-size: 7px;

    color: #64748b;

    font-weight: 900;
}

.gift-value {

    font-size: 10px;

    color: #0f172a;

    font-weight: 950;

    margin-top: 2px;
}

@keyframes giftPop {

    from {

        transform: scale(.88);

        opacity: 0;
    }

    to {

        transform: scale(1);

        opacity: 1;
    }
}


/* =========================
   SCORE
   ========================= */

.score-card {

    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    padding: 7px 3px;

    text-align: center;

    box-shadow:
    0 2px 8px rgba(0,0,0,.05);
}

.score-number {

    font-size: 19px;

    font-weight: 950;

    color: #0f172a;
}

.score-label {

    font-size: 7px;

    color: #64748b;

    font-weight: 900;
}


/* =========================
   BUTTON
   ========================= */

.stButton > button {

    min-height: 42px;

    border-radius: 11px;

    font-size: 11px;

    font-weight: 950;

    white-space: nowrap;

    width: 100%;

    touch-action: manipulation;
}

button[kind="primary"] {

    min-height: 44px;

    font-weight: 950;
}


/* =========================
   INPUT
   ========================= */

div[data-baseweb="select"] {

    border-radius: 10px;
}

textarea {

    border-radius: 10px !important;
}


/* =========================
   MOBILE
   ========================= */

@media(max-width:768px) {

    .block-container {

        padding-left: .18rem;
        padding-right: .18rem;
        padding-top: .15rem;
    }

    .hero {

        border-radius: 13px;

        padding: 9px 5px;
    }

    .hero-title {

        font-size: 15px;
    }

    .hero-sub {

        font-size: 7px;
    }

    .section-title {

        font-size: 13px;
    }

    .info-value {

        font-size: 11px;
    }

    .gift-card {

        padding: 12px 7px;

        border-radius: 15px;
    }

    .gift-title {

        font-size: 15px;
    }

    .gift-grid {

        gap: 3px;
    }

    .gift-label {

        font-size: 6px;
    }

    .gift-value {

        font-size: 9px;
    }

    .score-number {

        font-size: 16px;
    }

    .score-label {

        font-size: 6px;
    }

    .stButton > button {

        min-height: 42px;

        font-size: 10px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD SHEET
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
# FRESH LOAD
# ============================================================

def fresh_load():

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


# ============================================================
# VALUE
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

        text = (
            response
            .read()
            .decode("utf-8")
        )

    try:

        return json.loads(text)

    except:

        return {
            "success": False,
            "message": text
        }


# ============================================================
# SUMMARY
# ============================================================

def get_summary(df):

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

    percent = (

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
        percent
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="hero">

<div class="hero-title">

📋 ANAIMALAI TALUK
<br>
CENSUS ENUMERATION PROGRESS DASHBOARD

</div>

<div class="hero-sub">

Enumeration Monitoring & Progress System

</div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "enumerator"

if "admin_logged" not in st.session_state:

    st.session_state.admin_logged = False

if "selected_enum" not in st.session_state:

    st.session_state.selected_enum = None

if "record" not in st.session_state:

    st.session_state.record = None

if "gift" not in st.session_state:

    st.session_state.gift = None


# ============================================================
# TOP MENU
# ============================================================

st.markdown(
    '<div class="menu-box">',
    unsafe_allow_html=True
)

m1, m2 = st.columns(2)

with m1:

    if st.button(
        "👤 Enumerator",
        width="stretch"
    ):

        st.session_state.page = "enumerator"

        st.rerun()


with m2:

    if st.button(
        "🔐 Admin Panel",
        width="stretch"
    ):

        st.session_state.page = "admin"

        st.rerun()


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# DATA
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
# ENUMERATOR PAGE
# ============================================================

if st.session_state.page == "enumerator":


    # ========================================================
    # GIFT CARD
    # ========================================================

    if st.session_state.gift:

        g = st.session_state.gift

        st.markdown(
            f"""
<div class="gift-card">

<div class="gift-title">
🎁 UPDATE COMPLETED
</div>

<div class="gift-sub">
Saved successfully
</div>

<div class="gift-grid">

<div class="gift-item">
<div class="gift-label">HLB</div>
<div class="gift-value">{g["hlb"]}</div>
</div>

<div class="gift-item">
<div class="gift-label">STATUS</div>
<div class="gift-value">{g["status"]}</div>
</div>

<div class="gift-item">
<div class="gift-label">PENDING</div>
<div class="gift-value">{g["pending"]}</div>
</div>

</div>

</div>
""",
            unsafe_allow_html=True
        )

        time.sleep(2.5)

        st.session_state.gift = None

        st.rerun()


    # ========================================================
    # SEARCH
    # ========================================================

    st.markdown(
        '<div class="section-title">🔎 Enumerator</div>',
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


    options = [
        "— Select Enumerator —"
    ] + enumerators


    st.markdown(
        '<div class="search-box">',
        unsafe_allow_html=True
    )


    selected = st.selectbox(

        "Enumerator",

        options,

        index=0,

        key="enum_select"

    )


    # ========================================================
    # SEARCH BUTTON
    # ========================================================

    search_clicked = st.button(

        "🔍 SEARCH",

        type="primary",

        width="stretch",

        key="search"

    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # SEARCH
    # ========================================================

    if search_clicked:

        if selected == "— Select Enumerator —":

            st.warning(
                "Select Enumerator"
            )

        else:

            with st.spinner(
                "Loading..."
            ):

                try:

                    latest = fresh_load()

                    found = latest[
                        latest[
                            HLB_COLUMN
                        ]
                        .astype(str)
                        .str.strip()
                        == selected
                    ]


                    if found.empty:

                        st.error(
                            "Enumerator not found"
                        )

                    else:

                        st.session_state.selected_enum = selected

                        st.session_state.record = (
                            found
                            .iloc[0]
                            .to_dict()
                        )

                        st.rerun()


                except Exception as e:

                    st.error(
                        "Loading error"
                    )

                    st.code(str(e))


    # ========================================================
    # NO RECORD
    # ========================================================

    if st.session_state.record is None:

        st.stop()


    record = st.session_state.record

    selected_enum = st.session_state.selected_enum


    # ========================================================
    # DETAILS
    # ========================================================

    st.markdown(
        '<div class="section-title">Enumerator Details</div>',
        unsafe_allow_html=True
    )


    # HLB

    st.markdown(
        f"""
<div class="info-card">

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


    # MOBILE

    st.markdown(
        f"""
<div class="info-card">

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


    # DESCRIPTION

    st.markdown(
        f"""
<div class="info-card">

<div class="info-label">
HLB DESCRIPTION
</div>

<div class="info-value">
{get_value(record, "HLB DESCRIPTION")}
</div>

</div>
""",
        unsafe_allow_html=True
    )


    # ========================================================
    # CURRENT STATUS
    # ========================================================

    current_status = get_value(
        record,
        "STATUS"
    ).upper()

    if not current_status:

        current_status = "NOT STARTED"


    if current_status == "COMPLETED":

        st.markdown(
            """
<div class="status-card status-completed">
🟢 COMPLETED
</div>
""",
            unsafe_allow_html=True
        )

    elif current_status == "IN PROGRESS":

        st.markdown(
            """
<div class="status-card status-progress">
🟡 IN PROGRESS
</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
<div class="status-card status-notstarted">
🔴 NOT STARTED
</div>
""",
            unsafe_allow_html=True
        )


    # ========================================================
    # COMPLETED
    # ========================================================

    if current_status == "COMPLETED":

        st.success(
            "🔒 Completed"
        )

        completed_date = get_value(
            record,
            "COMPLETED DATE"
        )

        if completed_date:

            st.caption(
                f"Completed Date: {completed_date}"
            )

        remarks = get_value(
            record,
            "REMARKS"
        )

        if remarks:

            st.info(
                remarks
            )


    # ========================================================
    # UPDATE
    # ========================================================

    else:

        st.markdown(
            '<div class="section-title">Update Enumeration</div>',
            unsafe_allow_html=True
        )


        status_options = [

            "NOT STARTED",
            "IN PROGRESS",
            "COMPLETED"

        ]


        try:

            default_status = (
                status_options
                .index(current_status)
            )

        except:

            default_status = 0


        status = st.selectbox(

            "Status",

            status_options,

            index=default_status,

            key="status"

        )


        # ====================================================
        # PENDING
        # ====================================================

        try:

            old_pending = int(
                float(
                    get_value(
                        record,
                        "PENDING"
                    ) or 0
                )
            )

        except:

            old_pending = 0


        pending = st.number_input(

            "Pending Count",

            min_value=0,

            value=old_pending,

            step=1,

            key="pending"

        )


        # ====================================================
        # EXPECTED DATE
        # ====================================================

        expected_date = st.date_input(

            "Expected Completion Date",

            value=date.today(),

            key="expected"

        )


        # ====================================================
        # REMARKS
        # ====================================================

        remarks = st.text_area(

            "Reason / Remarks",

            value=get_value(
                record,
                "REMARKS"
            ),

            height=75,

            key="remarks"

        )


        # ====================================================
        # SAVE
        # ====================================================

        if st.button(

            "💾 SAVE UPDATE",

            type="primary",

            width="stretch",

            key="save"

        ):

            # IN PROGRESS VALIDATION

            if status == "IN PROGRESS":

                if pending <= 0:

                    st.error(
                        "Pending Count required"
                    )

                    st.stop()


                if not remarks.strip():

                    st.error(
                        "Reason required"
                    )

                    st.stop()


            # COMPLETED

            if status == "COMPLETED":

                pending = 0


            payload = {

                "hlb":
                selected_enum,

                "circle":
                get_value(
                    record,
                    "CIRCLE NUMBER"
                ),

                "enumerator":
                selected_enum,

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
                "Saving..."
            ):

                try:

                    result = send_update(
                        payload
                    )


                    if result.get(
                        "success"
                    ):

                        # ====================================
                        # GIFT DATA
                        # ====================================

                        st.session_state.gift = {

                            "hlb":
                            selected_enum,

                            "status":
                            status,

                            "pending":
                            pending

                        }


                        # ====================================
                        # CLEAR
                        # ====================================

                        st.session_state.record = None

                        st.session_state.selected_enum = None

                        st.cache_data.clear()

                        st.rerun()


                    else:

                        st.error(
                            "Save failed"
                        )

                        st.code(
                            result.get(
                                "message",
                                ""
                            )
                        )


                except Exception as e:

                    st.error(
                        "Connection error"
                    )

                    st.code(str(e))


    # ========================================================
    # OVERALL
    # ========================================================

    st.divider()


    (
        total,
        completed,
        in_progress,
        not_started,
        total_pending,
        percent
    ) = get_summary(df)


    st.markdown(
        '<div class="section-title">Overall Progress</div>',
        unsafe_allow_html=True
    )


    # SCORE 3

    a, b, c = st.columns(3)


    with a:

        st.markdown(
            f"""
<div class="score-card">

<div class="score-number">
{total}
</div>

<div class="score-label">
TOTAL ENUMERATOR
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with b:

        st.markdown(
            f"""
<div class="score-card">

<div class="score-number">
{completed}
</div>

<div class="score-label">
🟢 COMPLETED
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with c:

        st.markdown(
            f"""
<div class="score-card">

<div class="score-number">
{total_pending}
</div>

<div class="score-label">
TOTAL PENDING
</div>

</div>
""",
            unsafe_allow_html=True
        )


    # SCORE 2

    a, b = st.columns(2)


    with a:

        st.markdown(
            f"""
<div class="score-card">

<div class="score-number">
{in_progress}
</div>

<div class="score-label">
🟡 IN PROGRESS
</div>

</div>
""",
            unsafe_allow_html=True
        )


    with b:

        st.markdown(
            f"""
<div class="score-card">

<div class="score-number">
{not_started}
</div>

<div class="score-label">
🔴 NOT STARTED
</div>

</div>
""",
            unsafe_allow_html=True
        )


    # ========================================================
    # PROGRESS
    # ========================================================

    st.progress(
        int(percent)
    )

    st.markdown(
        f"""
<div style="
text-align:center;
font-weight:900;
font-size:12px;
">

{percent:.1f}% Completed

</div>
""",
        unsafe_allow_html=True
    )


    # ========================================================
    # DONUT
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

        hole=.62

    )


    fig.update_traces(
        textinfo="label+percent"
    )


    fig.update_layout(

        title={
            "text":
            "Enumerator Status",
            "x": .5
        },

        height=280,

        margin=dict(
            l=0,
            r=0,
            t=45,
            b=0
        ),

        legend=dict(
            orientation="h",
            y=-.08,
            x=.5,
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
        '<div class="section-title">Enumerator Status</div>',
        unsafe_allow_html=True
    )


    filter_status = st.selectbox(

        "Status",

        [
            "ALL",
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ],

        key="status_filter"

    )


    table_df = df.copy()


    if filter_status != "ALL":

        table_df = table_df[
            table_df["STATUS"]
            == filter_status
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

        x for x in table_columns

        if x in table_df.columns

    ]


    st.dataframe(

        table_df[
            table_columns
        ],

        width="stretch",

        hide_index=True,

        height=320

    )


# ============================================================
# ADMIN
# ============================================================

else:


    if not st.session_state.admin_logged:


        st.markdown(
            '<div class="section-title">Admin Login</div>',
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

                st.session_state.admin_logged = True

                st.rerun()

            else:

                st.error(
                    "Invalid Login"
                )


        st.stop()


    # ========================================================
    # ADMIN HEADER
    # ========================================================

    st.success(
        "🔓 Admin Panel"
    )


    admin_menu = st.radio(

        "Admin Menu",

        [

            "📊 Dashboard",

            "📋 Enumerator Status",

            "📥 Full Enumeration Report"

        ],

        horizontal=True

    )


    # ========================================================
    # ADMIN DASHBOARD
    # ========================================================

    if admin_menu == "📊 Dashboard":


        (
            total,
            completed,
            in_progress,
            not_started,
            total_pending,
            percent
        ) = get_summary(df)


        a, b, c = st.columns(3)


        with a:

            st.metric(
                "TOTAL ENUMERATOR",
                total
            )


        with b:

            st.metric(
                "🟢 COMPLETED",
                completed
            )


        with c:

            st.metric(
                "TOTAL PENDING",
                total_pending
            )


        a, b = st.columns(2)


        with a:

            st.metric(
                "🟡 IN PROGRESS",
                in_progress
            )


        with b:

            st.metric(
                "🔴 NOT STARTED",
                not_started
            )


        st.progress(
            int(percent)
        )


        chart = pd.DataFrame({

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

            chart,

            names="Status",

            values="Count",

            hole=.6

        )


        fig.update_layout(
            height=330
        )


        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


    # ========================================================
    # ADMIN STATUS
    # ========================================================

    elif admin_menu == "📋 Enumerator Status":


        filter_status = st.selectbox(

            "Status",

            [
                "ALL",
                "COMPLETED",
                "IN PROGRESS",
                "NOT STARTED"
            ]

        )


        admin_df = df.copy()


        if filter_status != "ALL":

            admin_df = admin_df[
                admin_df["STATUS"]
                == filter_status
            ]


        columns = [

            HLB_COLUMN,

            "CIRCLE NUMBER",

            "SUPERVISOR NAME & MOBILE NUMBER",

            "VILLAGE NAME",

            "ENUMERATOR MOBILE NUMBER",

            "HLB DESCRIPTION",

            "STATUS",

            "PENDING",

            "REMARKS",

            "EXPECTED DATE",

            "LAST UPDATED",

            "COMPLETED DATE"

        ]


        columns = [

            x for x in columns

            if x in admin_df.columns

        ]


        st.dataframe(

            admin_df[
                columns
            ],

            width="stretch",

            hide_index=True,

            height=550

        )


    # ========================================================
    # FULL REPORT
    # ========================================================

    else:


        st.markdown(
            '<div class="section-title">Full Enumeration Report</div>',
            unsafe_allow_html=True
        )


        st.dataframe(

            df,

            width="stretch",

            hide_index=True,

            height=500

        )


        csv_data = (
            df
            .to_csv(index=False)
            .encode("utf-8")
        )


        st.download_button(

            "Download Full Report",

            data=csv_data,

            file_name="Enumeration_Report.csv",

            mime="text/csv",

            width="stretch"

        )


    # ========================================================
    # LOGOUT
    # ========================================================

    st.divider()


    if st.button(
        "🚪 Logout",
        width="stretch"
    ):

        st.session_state.admin_logged = False

        st.session_state.page = "enumerator"

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ANAIMALAI TALUK • Census Enumeration"
)