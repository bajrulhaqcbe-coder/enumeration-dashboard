import streamlit as st
import pandas as pd
from datetime import date
import urllib.request
import json
import plotly.express as px
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.units import mm


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
# MAIN COLUMN
# ============================================================

HLB_COLUMN = "HLB NUMBER-ENUMERATOR NAME"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   REMOVE UNNECESSARY STREAMLIT UI
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =========================================================
   MAIN PAGE
   ========================================================= */

.block-container {

    max-width: 1150px;

    padding-top: 0.25rem;
    padding-bottom: 1rem;

    padding-left: 0.4rem;
    padding-right: 0.4rem;
}


/* =========================================================
   HEADER
   ========================================================= */

.hero {

    background:
    linear-gradient(
        135deg,
        #064e3b,
        #0f766e,
        #0891b2
    );

    color: white;

    border-radius: 17px;

    padding: 12px 8px;

    text-align: center;

    margin-bottom: 8px;

    box-shadow:
    0 6px 20px rgba(0,0,0,.14);
}

.hero-title {

    font-size: 21px;

    font-weight: 950;

    line-height: 1.25;
}

.hero-sub {

    font-size: 9px;

    opacity: .9;

    margin-top: 4px;
}


/* =========================================================
   SECTION TITLE
   ========================================================= */

.section-title {

    font-size: 16px;

    font-weight: 950;

    color: #0f172a;

    margin-top: 8px;

    margin-bottom: 6px;
}


/* =========================================================
   SEARCH
   ========================================================= */

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


/* =========================================================
   INFO CARD
   ========================================================= */

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

    font-weight: 950;
}

.info-value {

    color: #0f172a;

    font-size: 12px;

    font-weight: 900;

    margin-top: 2px;

    word-break: break-word;
}


/* =========================================================
   STATUS
   ========================================================= */

.status-card {

    border-radius: 12px;

    padding: 8px;

    text-align: center;

    font-size: 12px;

    font-weight: 950;

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


/* =========================================================
   SUCCESS CARD
   ========================================================= */

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

    padding: 14px 10px;

    margin: 8px 0 10px 0;

    text-align: center;

    box-shadow:
    0 8px 28px rgba(245,158,11,.20);

    animation:
    giftPop .35s ease-out;
}

.gift-title {

    font-size: 18px;

    font-weight: 950;

    color: #92400e;
}

.gift-sub {

    font-size: 10px;

    color: #475569;

    margin: 3px 0 9px 0;
}

.gift-grid {

    display: grid;

    grid-template-columns:
    repeat(3,1fr);

    gap: 5px;
}

.gift-item {

    background:
    rgba(255,255,255,.85);

    border-radius: 9px;

    padding: 7px 3px;
}

.gift-label {

    font-size: 7px;

    color: #64748b;

    font-weight: 950;
}

.gift-value {

    font-size: 10px;

    color: #0f172a;

    font-weight: 950;

    margin-top: 2px;
}

@keyframes giftPop {

    0% {
        transform: scale(.88);
        opacity: 0;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}


/* =========================================================
   SCORE CARDS
   ========================================================= */

.score-card {

    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    padding: 7px 3px;

    text-align: center;

    min-height: 66px;

    display: flex;

    flex-direction: column;

    justify-content: center;

    box-shadow:
    0 2px 8px rgba(0,0,0,.05);
}

.score-number {

    font-size: 20px;

    font-weight: 950;

    color: #0f172a;
}

.score-label {

    font-size: 7px;

    color: #64748b;

    font-weight: 950;

    line-height: 1.2;
}


/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {

    min-height: 44px !important;

    border-radius: 11px !important;

    font-size: 11px !important;

    font-weight: 950 !important;

    white-space: nowrap !important;

    visibility: visible !important;

    opacity: 1 !important;

    display: block !important;

    touch-action: manipulation;
}


/* =========================================================
   DOWNLOAD BUTTON
   ========================================================= */

.stDownloadButton > button {

    min-height: 46px !important;

    border-radius: 12px !important;

    font-size: 12px !important;

    font-weight: 950 !important;

    visibility: visible !important;

    opacity: 1 !important;

    display: block !important;
}


/* =========================================================
   MOBILE
   ========================================================= */

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

    .gift-label {

        font-size: 6px;
    }

    .gift-value {

        font-size: 9px;
    }

    .score-card {

        min-height: 60px;
    }

    .score-number {

        font-size: 16px;
    }

    .score-label {

        font-size: 6px;
    }

    .stButton > button {

        min-height: 44px !important;

        font-size: 10px !important;

    }

    .stDownloadButton > button {

        min-height: 46px !important;

        font-size: 10px !important;

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

        df = df.dropna(
            how="all"
        )

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
            df["STATUS"].isin(
                ["", "NAN"]
            ),
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

    df = pd.read_csv(
        CSV_URL
    )

    df = df.dropna(
        how="all"
    )

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
        df["STATUS"].isin(
            ["", "NAN"]
        ),
        "STATUS"
    ] = "NOT STARTED"

    return df


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

    return str(
        value
    ).strip()


# ============================================================
# SEND UPDATE
# ============================================================

def send_update(
    payload
):

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

    except:

        return {
            "success": False,
            "message": response_text
        }


# ============================================================
# SUMMARY
# ============================================================

def get_summary(df):

    total = len(df)

    completed = len(
        df[
            df["STATUS"]
            == "COMPLETED"
        ]
    )

    in_progress = len(
        df[
            df["STATUS"]
            == "IN PROGRESS"
        ]
    )

    not_started = len(
        df[
            df["STATUS"]
            == "NOT STARTED"
        ]
    )

    total_pending = 0

    if "PENDING" in df.columns:

        total_pending = int(

            pd.to_numeric(

                df["PENDING"],

                errors="coerce"

            )
            .fillna(0)
            .sum()

        )

    percentage = (

        completed /
        total *
        100

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
# PDF ESCAPE
# ============================================================

def pdf_text(value):

    if pd.isna(value):

        return ""

    value = str(
        value
    ).strip()

    return (
        value
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ============================================================
# CREATE FULL PDF
# ============================================================

def create_full_report_pdf(df):

    buffer = BytesIO()

    # A4 LANDSCAPE
    doc = SimpleDocTemplate(

        buffer,

        pagesize=landscape(A4),

        leftMargin=5 * mm,

        rightMargin=5 * mm,

        topMargin=7 * mm,

        bottomMargin=7 * mm,

        title=
        "ANAIMALAI TALUK - CENSUS ENUMERATION REPORT"

    )


    styles = getSampleStyleSheet()


    # ========================================================
    # PDF STYLES
    # ========================================================

    title_style = ParagraphStyle(

        "PDFTitle",

        parent=styles["Title"],

        fontName="Helvetica-Bold",

        fontSize=15,

        leading=18,

        alignment=TA_CENTER,

        textColor=colors.HexColor(
            "#172033"
        ),

        spaceAfter=3

    )


    subtitle_style = ParagraphStyle(

        "PDFSubtitle",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=8.5,

        leading=10,

        alignment=TA_CENTER,

        textColor=colors.HexColor(
            "#475569"
        ),

        spaceAfter=8

    )


    heading_style = ParagraphStyle(

        "PDFHeading",

        parent=styles["Heading2"],

        fontName="Helvetica-Bold",

        fontSize=10,

        leading=12,

        textColor=colors.HexColor(
            "#334155"
        ),

        spaceBefore=5,

        spaceAfter=5

    )


    cell_style = ParagraphStyle(

        "PDFCell",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=6.2,

        leading=7.5,

        textColor=colors.HexColor(
            "#111827"
        ),

        wordWrap="CJK"

    )


    header_style = ParagraphStyle(

        "PDFHeader",

        parent=styles["Normal"],

        fontName="Helvetica-Bold",

        fontSize=6.2,

        leading=7.5,

        textColor=colors.HexColor(
            "#172033"
        ),

        alignment=TA_CENTER,

        wordWrap="CJK"

    )


    # ========================================================
    # STORY
    # ========================================================

    story = []


    (
        total,
        completed,
        in_progress,
        not_started,
        total_pending,
        percentage

    ) = get_summary(df)


    # ========================================================
    # TITLE
    # ========================================================

    story.append(

        Paragraph(
            "ANAIMALAI TALUK - CENSUS ENUMERATION",
            title_style
        )

    )


    story.append(

        Paragraph(
            "Full Enumeration Report",
            subtitle_style
        )

    )


    # ========================================================
    # SUMMARY TABLE
    # ========================================================

    summary_data = [

        [
            "TOTAL ENUMERATOR",
            "COMPLETED",
            "IN PROGRESS",
            "NOT STARTED",
            "TOTAL PENDING",
            "PROGRESS"
        ],

        [
            str(total),
            str(completed),
            str(in_progress),
            str(not_started),
            str(total_pending),
            f"{percentage:.1f}%"
        ]

    ]


    summary_table = Table(

        summary_data,

        colWidths=[

            43 * mm,
            36 * mm,
            40 * mm,
            40 * mm,
            38 * mm,
            35 * mm

        ]

    )


    # LIGHT HEADING + DARK TEXT

    summary_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#e2e8f0"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.HexColor(
                    "#111827"
                )
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, 1),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7.5
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, 1),
                colors.HexColor(
                    "#f8fafc"
                )
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                .4,
                colors.HexColor(
                    "#94a3b8"
                )
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5
            )

        ])

    )


    story.append(
        summary_table
    )


    story.append(
        Spacer(1, 7)
    )


    # ========================================================
    # STATUS SUMMARY
    # ========================================================

    story.append(

        Paragraph(
            "Enumerator Status Summary",
            heading_style
        )

    )


    status_data = [

        [
            "STATUS",
            "COUNT"
        ],

        [
            "COMPLETED",
            str(completed)
        ],

        [
            "IN PROGRESS",
            str(in_progress)
        ],

        [
            "NOT STARTED",
            str(not_started)
        ]

    ]


    status_table = Table(

        status_data,

        colWidths=[
            65 * mm,
            35 * mm
        ]

    )


    status_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#e2e8f0"
                )
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.HexColor(
                    "#111827"
                )
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                .4,
                colors.HexColor(
                    "#94a3b8"
                )
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor(
                    "#ffffff"
                )
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7.5
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                4
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                4
            )

        ])

    )


    story.append(
        status_table
    )


    story.append(
        Spacer(1, 9)
    )


    # ========================================================
    # FULL ENUMERATION REPORT
    # ========================================================

    story.append(

        Paragraph(
            "Full Enumeration Report",
            heading_style
        )

    )


    report_columns = [

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


    report_columns = [

        c

        for c in report_columns

        if c in df.columns

    ]


    # ========================================================
    # IMPORTANT:
    # TOTAL WIDTH KEPT INSIDE A4 LANDSCAPE
    #
    # A4 landscape width = 297mm
    # Margins = 10mm total
    # Available = 287mm
    #
    # Total below = 284mm
    # ========================================================

    width_map = {

        HLB_COLUMN: 31,

        "CIRCLE NUMBER": 17,

        "SUPERVISOR NAME & MOBILE NUMBER": 27,

        "VILLAGE NAME": 23,

        "ENUMERATOR MOBILE NUMBER": 25,

        "HLB DESCRIPTION": 32,

        "STATUS": 20,

        "PENDING": 13,

        "REMARKS": 31,

        "EXPECTED DATE": 19,

        "LAST UPDATED": 21,

        "COMPLETED DATE": 25

    }


    col_widths = [

        width_map.get(
            col,
            20
        ) * mm

        for col in report_columns

    ]


    # ========================================================
    # HEADER
    # ========================================================

    pdf_data = []


    pdf_header = [

        Paragraph(
            pdf_text(col),
            header_style
        )

        for col in report_columns

    ]


    pdf_data.append(
        pdf_header
    )


    # ========================================================
    # ROWS
    # ========================================================

    for _, row in df.iterrows():

        row_data = []


        for col in report_columns:

            value = row[col]


            if pd.isna(value):

                value = ""


            value = str(
                value
            ).strip()


            # Allow more characters.
            # Paragraph will WRAP instead of cutting.

            if len(value) > 500:

                value = (
                    value[:500]
                    + "..."
                )


            row_data.append(

                Paragraph(
                    pdf_text(value),
                    cell_style
                )

            )


        pdf_data.append(
            row_data
        )


    # ========================================================
    # TABLE
    # ========================================================

    report_table = Table(

        pdf_data,

        colWidths=col_widths,

        repeatRows=1,

        splitByRow=1,

        hAlign="LEFT"

    )


    # ========================================================
    # PRINT-FRIENDLY STYLE
    # ========================================================

    report_table.setStyle(

        TableStyle([

            # LIGHT HEADER
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor(
                    "#e2e8f0"
                )
            ),

            # DARK TEXT
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.HexColor(
                    "#111827"
                )
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (0, 1),
                (-1, -1),
                "Helvetica"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, 0),
                "CENTER"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                .35,
                colors.HexColor(
                    "#94a3b8"
                )
            ),

            # WHITE BODY
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.white
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                2.5
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                2.5
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3
            )

        ])

    )


    story.append(
        report_table
    )


    # ========================================================
    # BUILD
    # ========================================================

    doc.build(
        story
    )


    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# SESSION STATE
# ============================================================

if "selected_enum" not in st.session_state:

    st.session_state.selected_enum = None


if "record" not in st.session_state:

    st.session_state.record = None


if "gift" not in st.session_state:

    st.session_state.gift = None


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
# LOAD DATA
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
# SUCCESS GIFT CARD
# ============================================================

if st.session_state.gift:

    g = st.session_state.gift

    st.markdown(

        f"""
<div class="gift-card">

<div class="gift-title">
🎁 UPDATE SUCCESSFULLY
</div>

<div class="gift-sub">
Google Sheet updated successfully
</div>

<div class="gift-grid">

<div class="gift-item">

<div class="gift-label">
HLB NUMBER
</div>

<div class="gift-value">
{g["hlb"]}
</div>

</div>

<div class="gift-item">

<div class="gift-label">
STATUS
</div>

<div class="gift-value">
{g["status"]}
</div>

</div>

<div class="gift-item">

<div class="gift-label">
PENDING
</div>

<div class="gift-value">
{g["pending"]}
</div>

</div>

</div>

</div>
""",

        unsafe_allow_html=True

    )


# ============================================================
# ENUMERATOR SEARCH
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Enumerator</div>',
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


selected = st.selectbox(

    "Enumerator",

    options,

    index=0,

    key="enumerator_dropdown"

)


# IMPORTANT:
# Separate row so button stays visible

search_clicked = st.button(

    "🔍 SEARCH",

    type="primary",

    width="stretch",

    key="search_button"

)


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# SEARCH
# ============================================================

if search_clicked:

    if selected == "— Select Enumerator —":

        st.warning(
            "Select Enumerator"
        )

    else:

        try:

            with st.spinner(
                "Loading..."
            ):

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
                    "Enumerator not found."
                )

            else:

                st.session_state.selected_enum = (
                    selected
                )

                st.session_state.record = (

                    found
                    .iloc[0]
                    .to_dict()

                )

                # Remove previous update card
                st.session_state.gift = None

                st.rerun()


        except Exception as e:

            st.error(
                "Google Sheet loading error."
            )

            st.code(
                str(e)
            )


# ============================================================
# ENUMERATOR DETAILS
# ============================================================

if st.session_state.record is not None:

    record = (
        st.session_state.record
    )

    selected_enum = (
        st.session_state.selected_enum
    )


    st.markdown(
        '<div class="section-title">'
        'Enumerator Details'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # HLB
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # MOBILE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

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

            '<div class="section-title">'
            'Update Enumeration'
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

                status_options
                .index(
                    current_status
                )

            )

        except:

            default_index = 0


        status = st.selectbox(

            "Status",

            status_options,

            index=default_index,

            key="update_status"

        )


        # ----------------------------------------------------
        # PENDING
        # ----------------------------------------------------

        try:

            current_pending = int(

                float(

                    get_value(
                        record,
                        "PENDING"
                    )
                    or 0

                )

            )

        except:

            current_pending = 0


        pending = st.number_input(

            "Pending Count",

            min_value=0,

            value=current_pending,

            step=1,

            key="update_pending"

        )


        # ----------------------------------------------------
        # EXPECTED DATE
        # ----------------------------------------------------

        expected_date = st.date_input(

            "Expected Completion Date",

            value=date.today(),

            key="expected_date"

        )


        # ----------------------------------------------------
        # REMARKS
        # ----------------------------------------------------

        remarks = st.text_area(

            "Reason / Remarks",

            value=get_value(
                record,
                "REMARKS"
            ),

            height=75,

            key="remarks"

        )


        # ----------------------------------------------------
        # SAVE BUTTON
        # ----------------------------------------------------

        if st.button(

            "💾 SAVE UPDATE",

            type="primary",

            width="stretch",

            key="save_update_button"

        ):


            # =================================================
            # IN PROGRESS VALIDATION
            # =================================================

            if status == "IN PROGRESS":

                if pending <= 0:

                    st.error(
                        "⚠️ Pending Count is required."
                    )

                    st.stop()


                if not remarks.strip():

                    st.error(
                        "⚠️ Reason / Remarks is required."
                    )

                    st.stop()


            # =================================================
            # COMPLETED
            # =================================================

            if status == "COMPLETED":

                pending = 0


            # =================================================
            # PAYLOAD
            # =================================================

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


            # =================================================
            # SAVE
            # =================================================

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

                        # -------------------------------------
                        # SAVE SUCCESS CARD
                        # -------------------------------------

                        st.session_state.gift = {

                            "hlb":
                            selected_enum,

                            "status":
                            status,

                            "pending":
                            pending

                        }


                        # -------------------------------------
                        # CLEAR CACHE
                        # -------------------------------------

                        st.cache_data.clear()


                        # -------------------------------------
                        # LOAD UPDATED RECORD
                        # -------------------------------------

                        latest = fresh_load()


                        new_record = latest[

                            latest[
                                HLB_COLUMN
                            ]
                            .astype(str)
                            .str.strip()

                            == selected_enum

                        ]


                        if not new_record.empty:

                            st.session_state.record = (

                                new_record
                                .iloc[0]
                                .to_dict()

                            )


                        # RERUN TO REFRESH
                        # GIFT CARD REMAINS
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
# TALUK OVERALL PROGRESS
# ============================================================

st.divider()


(
    total,
    completed,
    in_progress,
    not_started,
    total_pending,
    percentage

) = get_summary(df)


st.markdown(

    '<div class="section-title">'
    '📊 Taluk Overall Progress'
    '</div>',

    unsafe_allow_html=True

)


# ============================================================
# FIVE CARDS - ONE ROW
# ============================================================

c1, c2, c3, c4, c5 = st.columns(
    5,
    gap="small"
)


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
{in_progress}
</div>

<div class="score-label">
🟡 IN PROGRESS
</div>

</div>
""",

        unsafe_allow_html=True

    )


with c4:

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


with c5:

    st.markdown(

        f"""
<div class="score-card">

<div class="score-number">
{total_pending}
</div>

<div class="score-label">
📌 TOTAL PENDING
</div>

</div>
""",

        unsafe_allow_html=True

    )


# ============================================================
# PROGRESS
# ============================================================

st.progress(
    int(percentage)
)


st.markdown(

    f"""
<div style="
text-align:center;
font-weight:950;
font-size:12px;
margin-top:-3px;
margin-bottom:5px;
">

Overall Completion: {percentage:.1f}%

</div>
""",

    unsafe_allow_html=True

)


# ============================================================
# DONUT CHART
# ============================================================

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

    textinfo="label+percent",

    textposition="inside"

)


fig.update_layout(

    title={
        "text":
        "Enumerator Status",
        "x": .5
    },

    height=285,

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


# ============================================================
# ENUMERATOR STATUS TABLE
# ============================================================

st.markdown(

    '<div class="section-title">'
    '📋 Enumerator Status'
    '</div>',

    unsafe_allow_html=True

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


if status_filter != "ALL":

    display_df = display_df[

        display_df["STATUS"]
        == status_filter

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

    height=330

)


# ============================================================
# FULL PDF
# ============================================================

st.divider()


st.markdown(

    '<div class="section-title">'
    '📄 Full Enumeration Report'
    '</div>',

    unsafe_allow_html=True

)


try:

    pdf_bytes = create_full_report_pdf(
        df
    )


    st.download_button(

        "📥 Download Full Report PDF",

        data=pdf_bytes,

        file_name=
        "ANAIMALAI_TALUK_CENSUS_ENUMERATION_REPORT.pdf",

        mime=
        "application/pdf",

        width="stretch",

        type="primary",

        key="download_pdf"

    )


except Exception as e:

    st.error(
        "PDF உருவாக்குவதில் பிழை."
    )

    st.code(
        str(e)
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ANAIMALAI TALUK • Census Enumeration"
)