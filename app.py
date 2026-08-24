import streamlit as st
import pandas as pd
from datetime import date
import urllib.request
import json
import time
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ANAIMALAI TALUK - CENSUS ENUMERATION",
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

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ============================================================
   MAIN AREA
   ============================================================ */

.block-container {

    max-width: 1050px;

    padding-top: 0.25rem;
    padding-bottom: 1rem;
    padding-left: 0.45rem;
    padding-right: 0.45rem;
}


/* ============================================================
   MAIN HEADER
   ============================================================ */

.hero {

    background:
        linear-gradient(
            135deg,
            #064e3b 0%,
            #0f766e 45%,
            #0891b2 100%
        );

    border-radius: 18px;

    padding: 15px 10px;

    text-align: center;

    color: white;

    margin-bottom: 9px;

    box-shadow:
        0 7px 20px rgba(0,0,0,0.14);

    border: 1px solid rgba(255,255,255,0.20);
}

.hero-title {

    font-size: 21px;

    font-weight: 950;

    line-height: 1.25;

    letter-spacing: 0.2px;
}

.hero-sub {

    font-size: 9px;

    margin-top: 5px;

    opacity: 0.92;
}


/* ============================================================
   TOP MENU
   ============================================================ */

.top-menu {

    background: white;

    border-radius: 12px;

    padding: 5px;

    border: 1px solid #dbeafe;

    box-shadow:
        0 3px 12px rgba(15,23,42,0.06);

    margin-bottom: 8px;
}


/* ============================================================
   SECTION TITLE
   ============================================================ */

.section-title {

    font-size: 17px;

    font-weight: 950;

    color: #0f172a;

    margin-top: 8px;

    margin-bottom: 6px;
}


/* ============================================================
   SEARCH BOX
   ============================================================ */

.search-box {

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #f0fdfa
        );

    border: 1px solid #99f6e4;

    border-radius: 14px;

    padding: 8px;

    margin-bottom: 8px;

    box-shadow:
        0 4px 14px rgba(15,118,110,0.08);
}


/* ============================================================
   RESULT CARD
   ============================================================ */

.info-card {

    background: white;

    border-radius: 12px;

    padding: 8px;

    margin-bottom: 6px;

    border: 1px solid #e2e8f0;

    box-shadow:
        0 3px 10px rgba(15,23,42,0.05);
}

.info-label {

    font-size: 8px;

    font-weight: 950;

    color: #64748b;

    letter-spacing: 0.3px;
}

.info-value {

    font-size: 13px;

    font-weight: 850;

    color: #0f172a;

    margin-top: 3px;

    word-break: break-word;
}


/* ============================================================
   STATUS CARDS
   ============================================================ */

.status-completed {

    background:
        linear-gradient(
            135deg,
            #dcfce7,
            #bbf7d0
        );

    border: 1px solid #86efac;

    color: #166534;

    border-radius: 12px;

    padding: 8px;

    text-align: center;

    font-size: 12px;

    font-weight: 950;

    margin: 7px 0;
}

.status-progress {

    background:
        linear-gradient(
            135deg,
            #fef3c7,
            #fde68a
        );

    border: 1px solid #fcd34d;

    color: #92400e;

    border-radius: 12px;

    padding: 8px;

    text-align: center;

    font-size: 12px;

    font-weight: 950;

    margin: 7px 0;
}

.status-notstarted {

    background:
        linear-gradient(
            135deg,
            #fee2e2,
            #fecaca
        );

    border: 1px solid #fca5a5;

    color: #991b1b;

    border-radius: 12px;

    padding: 8px;

    text-align: center;

    font-size: 12px;

    font-weight: 950;

    margin: 7px 0;
}


/* ============================================================
   MINI SCORE CARD
   ============================================================ */

.save-card {

    background:
        linear-gradient(
            135deg,
            #ecfdf5,
            #d1fae5
        );

    border: 1px solid #6ee7b7;

    color: #065f46;

    border-radius: 14px;

    padding: 10px;

    margin: 7px 0;

    text-align: center;

    box-shadow:
        0 5px 18px rgba(16,185,129,0.15);

    animation: popCard 0.35s ease-out;
}

.save-card-title {

    font-size: 15px;

    font-weight: 950;
}

.save-card-small {

    font-size: 9px;

    margin-top: 3px;
}

@keyframes popCard {

    0% {
        transform: scale(0.90);
        opacity: 0;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}


/* ============================================================
   SUMMARY CARD
   ============================================================ */

.score-card {

    background: white;

    border-radius: 13px;

    border: 1px solid #e2e8f0;

    padding: 8px 3px;

    text-align: center;

    box-shadow:
        0 3px 10px rgba(15,23,42,0.05);
}

.score-number {

    font-size: 20px;

    font-weight: 950;

    color: #0f172a;
}

.score-label {

    font-size: 7px;

    font-weight: 950;

    color: #64748b;

    margin-top: 2px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    min-height: 40px;

    border-radius: 10px;

    font-size: 12px;

    font-weight: 950;

    border: 1px solid #cbd5e1;

    transition: all 0.2s ease;
}

.stButton > button:hover {

    transform: translateY(-1px);

    box-shadow:
        0 5px 12px rgba(15,23,42,0.10);
}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

button[kind="primary"] {

    min-height: 42px;

    font-weight: 950;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="select"] {

    border-radius: 10px;
}

div[data-baseweb="input"] {

    border-radius: 10px;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

[data-testid="stDataFrame"] {

    border-radius: 10px;

    overflow: hidden;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media only screen and (max-width: 768px) {

    .block-container {

        padding-left: 0.20rem;
        padding-right: 0.20rem;
        padding-top: 0.15rem;
    }

    .hero {

        padding: 10px 5px;

        border-radius: 12px;
    }

    .hero-title {

        font-size: 16px;
    }

    .hero-sub {

        font-size: 7px;
    }

    .section-title {

        font-size: 14px;

        margin-top: 5px;

        margin-bottom: 4px;
    }

    .search-box {

        padding: 5px;

        border-radius: 10px;
    }

    .info-card {

        padding: 7px;

        border-radius: 9px;
    }

    .info-label {

        font-size: 7px;
    }

    .info-value {

        font-size: 11px;
    }

    .score-card {

        padding: 6px 2px;

        border-radius: 9px;
    }

    .score-number {

        font-size: 17px;
    }

    .score-label {

        font-size: 6px;
    }

    .save-card {

        padding: 8px;

        border-radius: 10px;
    }

    .save-card-title {

        font-size: 13px;
    }

    .save-card-small {

        font-size: 8px;
    }

    .stButton > button {

        min-height: 38px;

        font-size: 10px;
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
            data["STATUS"].isin(
                ["", "NAN"]
            ),
            "STATUS"
        ] = "NOT STARTED"

        return data

    except Exception as e:

        st.error(
            "Google Sheet தரவை ஏற்ற முடியவில்லை."
        )

        st.code(str(e))

        return pd.DataFrame()


# ============================================================
# FRESH LOAD
# ============================================================

def fresh_load():

    data = pd.read_csv(
        CSV_URL
    )

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

        data["STATUS"] = "NOT STARTED"

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


# ============================================================
# GET VALUE
# ============================================================

def get_value(
    record,
    column
):

    if column not in record:

        return ""

    value = record[column]

    if pd.isna(value):

        return ""

    return str(value).strip()


# ============================================================
# SEND UPDATE
# ============================================================

def send_update(
    payload
):

    data = json.dumps(
        payload
    ).encode(
        "utf-8"
    )

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
            .decode(
                "utf-8"
            )
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

def summary_data(data):

    total = len(data)

    completed = len(
        data[
            data["STATUS"]
            == "COMPLETED"
        ]
    )

    progress = len(
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

    percent = (

        completed /
        total *
        100

        if total > 0

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

மக்கள் தொகை கணக்கெடுப்பு பணியின் முன்னேற்ற கண்காணிப்பு அமைப்பு

</div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATES
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "enumerator"


if "admin_logged_in" not in st.session_state:

    st.session_state.admin_logged_in = False


if "selected_enum" not in st.session_state:

    st.session_state.selected_enum = None


if "record" not in st.session_state:

    st.session_state.record = None


# ============================================================
# TOP MENU
# ============================================================

st.markdown(
    '<div class="top-menu">',
    unsafe_allow_html=True
)

menu1, menu2 = st.columns(
    2
)

with menu1:

    if st.button(
        "👤 Enumerator",
        width="stretch"
    ):

        st.session_state.page = "enumerator"

        st.rerun()


with menu2:

    if st.button(
        "🔐 Admin Panel",
        width="stretch"
    ):

        st.session_state.page = "admin"

        st.rerun()


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

df = load_google_sheet()


if df.empty:

    st.error(
        "Google Sheet-ல் தரவு இல்லை."
    )

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
    # SUCCESS MINI CARD
    # ========================================================

    if (
        "save_message"
        in st.session_state
    ):

        st.markdown(
            """
<div class="save-card">

<div class="save-card-title">

✅ UPDATE SUCCESSFUL

</div>

<div class="save-card-small">

விவரங்கள் Google Sheet-ல் வெற்றிகரமாக சேமிக்கப்பட்டன

</div>

</div>
""",
            unsafe_allow_html=True
        )

        time.sleep(2)

        del st.session_state[
            "save_message"
        ]

        st.rerun()


    # ========================================================
    # SEARCH
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🔎 கணக்கெடுப்பாளரைத் தேர்வு செய்யவும்'
        '</div>',
        unsafe_allow_html=True
    )


    enumerators = (
        df[
            HLB_COLUMN
        ]
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


    # IMPORTANT:
    # No text_input here.
    # Therefore mobile keyboard will not cover SEARCH.

    selected = st.selectbox(

        "Enumerator",

        options,

        index=0,

        key="enum_dropdown"

    )


    # SEARCH BUTTON IS IMMEDIATELY BELOW DROPDOWN

    search_clicked = st.button(

        "🔍 SEARCH",

        type="primary",

        width="stretch",

        key="search_button"

    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SEARCH
    # ========================================================

    if search_clicked:

        if selected == "— Select Enumerator —":

            st.warning(
                "⚠️ முதலில் Enumerator-ஐ தேர்வு செய்யவும்."
            )

        else:

            with st.spinner(
                "Google Sheet data loading..."
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
                            "❌ Enumerator கிடைக்கவில்லை."
                        )

                    else:

                        st.session_state[
                            "selected_enum"
                        ] = selected

                        st.session_state[
                            "record"
                        ] = (
                            found
                            .iloc[0]
                            .to_dict()
                        )

                        st.rerun()


                except Exception as e:

                    st.error(
                        "❌ Google Sheet loading error."
                    )

                    st.code(
                        str(e)
                    )


    # ========================================================
    # DISPLAY SEARCHED RECORD
    # ========================================================

    if (
        st.session_state.record
        is None
    ):

        st.info(
            "👆 Enumerator-ஐ தேர்வு செய்து SEARCH அழுத்தவும்."
        )

        st.stop()


    record = (
        st.session_state.record
    )

    selected_enum = (
        st.session_state.selected_enum
    )


    # ========================================================
    # STATUS
    # ========================================================

    current_status = get_value(
        record,
        "STATUS"
    ).upper()


    if not current_status:

        current_status = "NOT STARTED"


    # ========================================================
    # ENUMERATOR DETAILS
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
<div class="info-card">

<div class="info-label">
HLB NUMBER - ENUMERATOR
</div>

<div class="info-value">
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
<div class="info-card">

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
    # HLB DESCRIPTION
    # ========================================================

    st.markdown(
        f"""
<div class="info-card">

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
    # STATUS DISPLAY
    # ========================================================

    if current_status == "COMPLETED":

        st.markdown(
            """
<div class="status-completed">

🟢 COMPLETED

<br>

பணி முழுமையாக முடிக்கப்பட்டுள்ளது

</div>
""",
            unsafe_allow_html=True
        )


    elif current_status == "IN PROGRESS":

        st.markdown(
            """
<div class="status-progress">

🟡 IN PROGRESS

<br>

பணி நடைபெற்று வருகிறது

</div>
""",
            unsafe_allow_html=True
        )


    else:

        st.markdown(
            """
<div class="status-notstarted">

🔴 NOT STARTED

<br>

பணி இன்னும் தொடங்கப்படவில்லை

</div>
""",
            unsafe_allow_html=True
        )


    # ========================================================
    # UPDATE AREA
    # ========================================================

    if current_status == "COMPLETED":

        st.success(
            "🔒 இந்த Enumerator COMPLETED நிலையில் LOCK செய்யப்பட்டுள்ளது."
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

            st.markdown(
                "**குறிப்புகள்:**"
            )

            st.info(
                remarks
            )


    else:

        st.markdown(
            '<div class="section-title">'
            '📝 கணக்கெடுப்பு புதுப்பிப்பு'
            '</div>',
            unsafe_allow_html=True
        )


        # ====================================================
        # STATUS
        # ====================================================

        statuses = [

            "NOT STARTED",

            "IN PROGRESS",

            "COMPLETED"

        ]


        try:

            status_index = statuses.index(
                current_status
            )

        except Exception:

            status_index = 0


        status = st.selectbox(

            "பணி நிலை",

            statuses,

            index=status_index,

            key="status_update"

        )


        # ====================================================
        # PENDING
        # ====================================================

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

            "📌 நிலுவையில் உள்ள எண்ணிக்கை",

            min_value=0,

            value=current_pending,

            step=1,

            key="pending_update"

        )


        # ====================================================
        # IN PROGRESS NOTICE
        # ====================================================

        if status == "IN PROGRESS":

            st.warning(
                "⚠️ IN PROGRESS என்றால் Pending Count மற்றும் Reason கட்டாயம்."
            )


        # ====================================================
        # EXPECTED DATE
        # ====================================================

        expected_date = st.date_input(

            "Expected Completion Date",

            value=date.today(),

            key="expected_date_update"

        )


        # ====================================================
        # REMARKS
        # ====================================================

        current_remarks = get_value(
            record,
            "REMARKS"
        )


        remarks = st.text_area(

            "📝 காரணம் / குறிப்புகள்",

            value=current_remarks,

            height=85,

            placeholder=
            "நிலுவைக்கான காரணத்தை பதிவு செய்யவும்.",

            key="remarks_update"

        )


        # ====================================================
        # SAVE UPDATE
        # ====================================================

        if st.button(

            "SAVE UPDATE",

            type="primary",

            width="stretch",

            key="save_update_button"

        ):


            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if status == "IN PROGRESS":

                if pending <= 0:

                    st.error(
                        "❌ Pending Count கட்டாயம்."
                    )

                    st.stop()


                if not remarks.strip():

                    st.error(
                        "❌ Reason / Remarks கட்டாயம்."
                    )

                    st.stop()


            # ------------------------------------------------
            # COMPLETED
            # ------------------------------------------------

            if status == "COMPLETED":

                pending = 0


            # ------------------------------------------------
            # PAYLOAD
            # ------------------------------------------------

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


            # ------------------------------------------------
            # SAVE
            # ------------------------------------------------

            with st.spinner(
                "Google Sheet-ல் சேமிக்கப்படுகிறது..."
            ):

                try:

                    result = send_update(
                        payload
                    )


                    if result.get(
                        "success"
                    ):

                        # ------------------------------------
                        # MINI SCORE CARD FLAG
                        # ------------------------------------

                        st.session_state[
                            "save_message"
                        ] = True


                        # ------------------------------------
                        # CLEAR CACHE
                        # ------------------------------------

                        st.cache_data.clear()


                        # ------------------------------------
                        # CLEAR OLD RECORD
                        # ------------------------------------

                        st.session_state[
                            "record"
                        ] = None

                        st.session_state[
                            "selected_enum"
                        ] = None


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
    # OVERALL PROGRESS
    # ========================================================

    st.divider()


    (
        total,
        completed,
        in_progress,
        not_started,
        total_pending,
        percentage
    ) = summary_data(
        df
    )


    st.markdown(
        '<div class="section-title">'
        'Overall Progress'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SCORE CARDS
    # ========================================================

    c1, c2, c3 = st.columns(3)


    with c1:

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


    with c2:

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


    with c3:

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


    c1, c2 = st.columns(2)


    with c1:

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


    with c2:

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
        int(percentage)
    )


    st.markdown(
        f"""
<div style="
text-align:center;
font-size:13px;
font-weight:950;
margin-top:-3px;
">

மொத்த முன்னேற்றம்:
{percentage:.1f}%

</div>
""",
        unsafe_allow_html=True
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

        hole=0.62

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

        height=290,

        margin=dict(
            l=0,
            r=0,
            t=45,
            b=0
        ),

        showlegend=True,

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
    # ENUMERATOR STATUS TABLE
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Enumerator Status'
        '</div>',
        unsafe_allow_html=True
    )


    table_status = st.selectbox(

        "பணி நிலையைத் தேர்வு செய்யவும்",

        [
            "ALL",
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED"
        ],

        key="enum_status_filter"

    )


    status_df = df.copy()


    if table_status != "ALL":

        status_df = status_df[
            status_df["STATUS"]
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

        x for x in table_columns

        if x in status_df.columns

    ]


    st.dataframe(

        status_df[
            table_columns
        ],

        width="stretch",

        hide_index=True,

        height=350

    )


# ============================================================
# ADMIN PAGE
# ============================================================

else:


    # ========================================================
    # ADMIN LOGIN
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Admin Login'
        '</div>',
        unsafe_allow_html=True
    )


    if not st.session_state.admin_logged_in:


        username = st.text_input(
            "பயனர் பெயர்"
        )


        password = st.text_input(
            "கடவுச்சொல்",
            type="password"
        )


        login = st.button(

            "🔐 LOGIN",

            type="primary",

            width="stretch"

        )


        if login:

            if (

                username
                ==
                ADMIN_USERNAME

                and

                password
                ==
                ADMIN_PASSWORD

            ):

                st.session_state.admin_logged_in = True

                st.rerun()

            else:

                st.error(
                    "❌ பயனர் பெயர் அல்லது கடவுச்சொல் தவறாக உள்ளது."
                )


        st.stop()


    # ========================================================
    # ADMIN HEADER
    # ========================================================

    st.success(
        "🔓 Admin Panel"
    )


    # ========================================================
    # ADMIN MENU
    # ========================================================

    admin_menu = st.radio(

        "Admin Panel Menu",

        [

            "📊 Dashboard",

            "📋 Enumerator Status",

            "📥 Full Enumeration Report"

        ],

        horizontal=True

    )


    st.divider()


    # ========================================================
    # DASHBOARD
    # ========================================================

    if admin_menu == "📊 Dashboard":


        (
            total,
            completed,
            in_progress,
            not_started,
            total_pending,
            percentage
        ) = summary_data(
            df
        )


        c1, c2, c3 = st.columns(3)


        with c1:

            st.metric(
                "TOTAL ENUMERATOR",
                total
            )


        with c2:

            st.metric(
                "🟢 COMPLETED",
                completed
            )


        with c3:

            st.metric(
                "TOTAL PENDING",
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
font-weight:950;
">

மொத்த முன்னேற்றம்:
{percentage:.1f}%

</div>
""",
            unsafe_allow_html=True
        )


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

            height=350,

            margin=dict(
                l=0,
                r=0,
                t=50,
                b=0
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
    # ENUMERATOR STATUS
    # ========================================================

    elif admin_menu == "📋 Enumerator Status":


        st.markdown(
            '<div class="section-title">'
            'Enumerator Status'
            '</div>',
            unsafe_allow_html=True
        )


        status_filter = st.selectbox(

            "பணி நிலை",

            [
                "ALL",
                "COMPLETED",
                "IN PROGRESS",
                "NOT STARTED"
            ]

        )


        admin_df = df.copy()


        if status_filter != "ALL":

            admin_df = admin_df[
                admin_df["STATUS"]
                == status_filter
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
            '<div class="section-title">'
            'Full Enumeration Report'
            '</div>',
            unsafe_allow_html=True
        )


        st.dataframe(

            df,

            width="stretch",

            hide_index=True,

            height=550

        )


        csv_data = (

            df
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            )

        )


        st.download_button(

            "Download Full Report",

            data=csv_data,

            file_name=
            "Enumeration_Report.csv",

            mime=
            "text/csv",

            width="stretch"

        )


    # ========================================================
    # ADMIN LOGOUT
    # ========================================================

    st.divider()


    if st.button(
        "🚪 Logout",
        width="stretch"
    ):

        st.session_state.admin_logged_in = False

        st.session_state.page = "enumerator"

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "📋 ANAIMALAI TALUK • Census Enumeration • Google Sheet Live Data"
)