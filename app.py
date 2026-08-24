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
    page_title="ஆனைமலை வட்டம் - கணக்கெடுப்பு",
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
# ADMIN LOGIN
# ============================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ============================================================
# GOOGLE SHEET MAIN COLUMN
# ============================================================

HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   HIDE STREAMLIT DEFAULT
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ==========================================================
   MAIN CONTAINER
   ========================================================== */

.block-container {

    max-width: 1050px;

    padding-top: 0.25rem;
    padding-left: 0.40rem;
    padding-right: 0.40rem;
    padding-bottom: 1rem;
}


/* ==========================================================
   HEADER
   ========================================================== */

.dashboard-header {

    background: linear-gradient(
        135deg,
        #0f766e,
        #115e59
    );

    color: white;

    border-radius: 14px;

    padding: 12px 8px;

    text-align: center;

    margin-bottom: 10px;

    box-shadow:
        0 4px 12px rgba(0,0,0,0.10);
}

.dashboard-title {

    font-size: 21px;

    font-weight: 900;

    line-height: 1.3;
}

.dashboard-subtitle {

    font-size: 10px;

    margin-top: 4px;

    opacity: 0.90;
}


/* ==========================================================
   SECTION
   ========================================================== */

.section-title {

    font-size: 17px;

    font-weight: 900;

    color: #0f172a;

    margin-top: 8px;

    margin-bottom: 7px;
}


/* ==========================================================
   SEARCH CARD
   ========================================================== */

.search-card {

    background: #ffffff;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    padding: 8px;

    margin-bottom: 8px;

    box-shadow:
        0 2px 8px rgba(15,23,42,0.05);
}


/* ==========================================================
   RESULT CARD
   ========================================================== */

.result-card {

    background: #ffffff;

    border: 1px solid #dbeafe;

    border-radius: 11px;

    padding: 8px;

    margin-bottom: 7px;

    box-shadow:
        0 2px 7px rgba(15,23,42,0.04);
}

.result-label {

    font-size: 9px;

    font-weight: 900;

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


/* ==========================================================
   STATUS
   ========================================================== */

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


/* ==========================================================
   SUMMARY
   ========================================================== */

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


/* ==========================================================
   BUTTON
   ========================================================== */

.stButton > button {

    min-height: 38px;

    border-radius: 9px;

    font-weight: 850;

    font-size: 12px;
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media only screen and (max-width: 768px) {

    .block-container {

        padding-left: 0.22rem;
        padding-right: 0.22rem;
        padding-top: 0.15rem;
    }

    .dashboard-header {

        border-radius: 10px;

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
            "Google Sheet தரவை ஏற்ற முடியவில்லை."
        )

        st.code(str(e))

        return pd.DataFrame()


# ============================================================
# FRESH DATA
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
# PAGE HEADER
# ============================================================

st.markdown(
    """
<div class="dashboard-header">

<div class="dashboard-title">

📋 ஆனைமலை வட்டம்
<br>
மக்கள் தொகை கணக்கெடுப்பு
<br>
முன்னேற்ற நிலை

</div>

<div class="dashboard-subtitle">

கணக்கெடுப்பு பணிகளை கண்காணிக்கும் அமைப்பு

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

    st.error(
        "Google Sheet-ல் தரவு இல்லை."
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
# SIDEBAR MENU
# ============================================================

with st.sidebar:

    st.markdown(
        "## 📋 கணக்கெடுப்பு"
    )

    st.divider()

    menu = st.radio(
        "Menu",
        [
            "👤 Enumerator",
            "🔐 Admin Panel"
        ]
    )

    st.divider()

    if st.button(
        "🔄 தரவை புதுப்பிக்கவும்",
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
# ENUMERATOR MENU
# ============================================================

if menu == "👤 Enumerator":


    # ========================================================
    # SEARCH
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🔎 கணக்கெடுப்பாளரைத் தேடுக'
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
        "— கணக்கெடுப்பாளரைத் தேர்வு செய்யவும் —"
    ] + enumerators


    st.markdown(
        '<div class="search-card">',
        unsafe_allow_html=True
    )


    with st.form(
        "enumerator_search_form"
    ):

        selected = st.selectbox(

            "கணக்கெடுப்பாளர்",

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
    # SEARCH ACTION
    # ========================================================

    if search_clicked:

        if (
            selected
            ==
            "— கணக்கெடுப்பாளரைத் தேர்வு செய்யவும் —"
        ):

            st.warning(
                "⚠️ முதலில் கணக்கெடுப்பாளரைத் தேர்வு செய்யவும்."
            )

        else:

            with st.spinner(
                "Google Sheet தரவு ஏற்றப்படுகிறது..."
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
                            "❌ கணக்கெடுப்பாளர் கிடைக்கவில்லை."
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
                            "✅ தரவு வெற்றிகரமாக ஏற்றப்பட்டது."
                        )

                except Exception as e:

                    st.error(
                        "❌ Google Sheet தரவை ஏற்றுவதில் பிழை."
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
            "👆 கணக்கெடுப்பாளரைத் தேர்வு செய்து SEARCH அழுத்தவும்."
        )

        st.stop()


    # ========================================================
    # RECORD
    # ========================================================

    record = st.session_state[
        "searched_record"
    ]

    selected_enum = st.session_state[
        "searched_enumerator"
    ]


    # ========================================================
    # CURRENT STATUS
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
        '📋 கணக்கெடுப்பாளர் விவரங்கள்'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # HLB
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
    # DESCRIPTION
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
    # STATUS DISPLAY
    # ========================================================

    if current_status == "COMPLETED":

        st.markdown(
            """
<div class="status-completed">

🟢 பணி முழுமையாக முடிக்கப்பட்டது

</div>
""",
            unsafe_allow_html=True
        )

    elif current_status == "IN PROGRESS":

        st.markdown(
            """
<div class="status-progress">

🟡 பணி நடைபெற்று வருகிறது

</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
<div class="status-notstarted">

🔴 பணி இன்னும் தொடங்கப்படவில்லை

</div>
""",
            unsafe_allow_html=True
        )


    # ========================================================
    # COMPLETED LOCK
    # ========================================================

    if current_status == "COMPLETED":

        st.success(
            "🔒 இந்த கணக்கெடுப்பாளர் பணி முடிக்கப்பட்டு LOCK செய்யப்பட்டுள்ளது."
        )


        completed_date = get_value(
            record,
            "COMPLETED DATE"
        )


        if completed_date:

            st.info(
                f"முடிக்கப்பட்ட தேதி: {completed_date}"
            )


        existing_remarks = get_value(
            record,
            "REMARKS"
        )


        if existing_remarks:

            st.write(
                "**குறிப்புகள்:**"
            )

            st.info(
                existing_remarks
            )


    # ========================================================
    # UPDATE
    # ========================================================

    else:

        st.markdown(
            '<div class="section-title">'
            '📝 கணக்கெடுப்பு புதுப்பிப்பு'
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

            "பணி நிலை",

            status_options,

            index=default_index,

            key="update_status"

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

            key="pending_count"

        )


        # ====================================================
        # IN PROGRESS WARNING
        # ====================================================

        if status == "IN PROGRESS":

            st.warning(
                "⚠️ பணி நடைபெற்று வருகிறது என்பதைத் தேர்வு செய்தால் "
                "நிலுவை எண்ணிக்கையும் காரணமும் கட்டாயம் பதிவு செய்ய வேண்டும்."
            )


        # ====================================================
        # EXPECTED DATE
        # English as requested
        # ====================================================

        expected_date = st.date_input(

            "Expected Completion Date",

            value=date.today(),

            key="expected_date"

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

            height=90,

            placeholder=(
                "நிலுவையில் இருப்பதற்கான காரணத்தை "
                "தெளிவாக பதிவு செய்யவும்..."
            ),

            key="remarks"

        )


        # ====================================================
        # SAVE
        # English as requested
        # ====================================================

        if st.button(

            "SAVE UPDATE",

            type="primary",

            width="stretch",

            key="save_update"

        ):


            # ------------------------------------------------
            # IN PROGRESS VALIDATION
            # ------------------------------------------------

            if status == "IN PROGRESS":


                if pending <= 0:

                    st.error(
                        "❌ நிலுவையில் உள்ள எண்ணிக்கை கட்டாயம்."
                    )

                    st.stop()


                if not remarks.strip():

                    st.error(
                        "❌ நிலுவைக்கான காரணம் கட்டாயம்."
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

                        st.success(
                            "✅ விவரங்கள் வெற்றிகரமாக சேமிக்கப்பட்டன."
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
                            "❌ விவரங்களைச் சேமிக்க முடியவில்லை."
                        )

                        st.code(
                            result.get(
                                "message",
                                "Unknown error"
                            )
                        )


                except Exception as e:

                    st.error(
                        "❌ இணைப்பில் பிழை ஏற்பட்டுள்ளது."
                    )

                    st.code(
                        str(e)
                    )


    # ========================================================
    # OVERALL PROGRESS
    # English as requested
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-title">'
        'Overall Progress'
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
margin-top:9px;
">

மொத்த முடிவு:
{percentage:.1f}%

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
    # ENUMERATOR STATUS TABLE
    # English as requested
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Enumerator Status'
        '</div>',
        unsafe_allow_html=True
    )


    table_search = st.text_input(

        "🔎 கணக்கெடுப்பாளர் / HLB தேடல்",

        key="status_search"

    )


    table_status = st.selectbox(

        "பணி நிலை",

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
# ADMIN PANEL
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


    if (
        "admin_logged_in"
        not in st.session_state
    ):

        st.session_state.admin_logged_in = False


    if not st.session_state.admin_logged_in:


        username = st.text_input(
            "பயனர் பெயர்"
        )


        password = st.text_input(
            "கடவுச்சொல்",
            type="password"
        )


        if st.button(

            "🔐 உள்நுழையவும்",

            type="primary",

            width="stretch"

        ):


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
    # ADMIN MENU
    # ========================================================

    st.success(
        "🔓 Admin Panel"
    )


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
    # ADMIN LOGOUT
    # ========================================================

    if st.button(
        "Logout"
    ):

        st.session_state.admin_logged_in = False

        st.rerun()


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
            percentage
        ) = calculate_summary(df)


        st.markdown(
            '<div class="section-title">'
            'Overall Progress'
            '</div>',
            unsafe_allow_html=True
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
font-weight:900;
">

மொத்த முடிவு:
{percentage:.1f}%

</div>
""",
            unsafe_allow_html=True
        )


        # ====================================================
        # ADMIN DONUT
        # ====================================================

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

            height=330,

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
    # ADMIN STATUS
    # ========================================================

    elif admin_menu == "📋 Enumerator Status":


        st.markdown(
            '<div class="section-title">'
            'Enumerator Status'
            '</div>',
            unsafe_allow_html=True
        )


        search = st.text_input(
            "🔎 தேடல்"
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


        if search:

            mask = (

                admin_df

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

            admin_df = admin_df[
                mask
            ]


        if status_filter != "ALL":

            admin_df = admin_df[
                admin_df["STATUS"]
                == status_filter
            ]


        table_columns = [

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


        table_columns = [

            c for c in table_columns

            if c in admin_df.columns

        ]


        st.dataframe(

            admin_df[
                table_columns
            ],

            width="stretch",

            hide_index=True,

            height=550

        )


    # ========================================================
    # FULL REPORT
    # ========================================================

    elif admin_menu == "📥 Full Enumeration Report":


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

            .encode("utf-8")

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


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "📋 ஆனைமலை வட்டம் – மக்கள் தொகை கணக்கெடுப்பு • Google Sheet Live Data"
)