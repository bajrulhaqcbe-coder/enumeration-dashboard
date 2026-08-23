import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enumeration Progress Dashboard",
    page_icon="📋",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f7fa;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.card-title {
    font-size: 15px;
    color: #666;
}

.card-number {
    font-size: 30px;
    font-weight: bold;
}

.info-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SAMPLE MASTER DATA
# ============================================================

MASTER_DATA = [
    {
        "HLB NUMBER-ENUMERATOR NAME": "1-M.BANUMATHI",
        "CIRCLE NUMBER": "1",
        "SUPERVISOR NAME & MOBILE NUMBER": "ANANDAJOTHI/KANNIYAPPAN 6369054136",
        "VILLAGE NAME": "MARCHINAICKENPALAYAM, ATHUPOLLACHI",
        "ENUMERATOR MOBILE NUMBER": "9489512472",
        "HLB DESCRIPTION": "THOTATHU SALAI, ANNA NAGAR, MARIYAMMAN KOVIL VEEDHI",
        "REMARKS": "",
        "EXPECTED DATE": "",
        "STATUS": "IN PROGRESS",
        "LAST UPDATED": "",
        "COMPLETED DATE": "",
        "PENDING": ""
    },

    {
        "HLB NUMBER-ENUMERATOR NAME": "2-P.JAYASREE",
        "CIRCLE NUMBER": "1",
        "SUPERVISOR NAME & MOBILE NUMBER": "",
        "VILLAGE NAME": "",
        "ENUMERATOR MOBILE NUMBER": "",
        "HLB DESCRIPTION": "",
        "REMARKS": "",
        "EXPECTED DATE": "",
        "STATUS": "NOT STARTED",
        "LAST UPDATED": "",
        "COMPLETED DATE": "",
        "PENDING": ""
    },

    {
        "HLB NUMBER-ENUMERATOR NAME": "3-SAKTHI",
        "CIRCLE NUMBER": "1",
        "SUPERVISOR NAME & MOBILE NUMBER": "",
        "VILLAGE NAME": "",
        "ENUMERATOR MOBILE NUMBER": "",
        "HLB DESCRIPTION": "",
        "REMARKS": "",
        "EXPECTED DATE": "",
        "STATUS": "NOT STARTED",
        "LAST UPDATED": "",
        "COMPLETED DATE": "",
        "PENDING": ""
    },

    {
        "HLB NUMBER-ENUMERATOR NAME": "4-K.PRASANNA",
        "CIRCLE NUMBER": "1",
        "SUPERVISOR NAME & MOBILE NUMBER": "",
        "VILLAGE NAME": "",
        "ENUMERATOR MOBILE NUMBER": "",
        "HLB DESCRIPTION": "",
        "REMARKS": "",
        "EXPECTED DATE": "",
        "STATUS": "NOT STARTED",
        "LAST UPDATED": "",
        "COMPLETED DATE": "",
        "PENDING": ""
    },

    {
        "HLB NUMBER-ENUMERATOR NAME": "5-A.NAGARAJ",
        "CIRCLE NUMBER": "1",
        "SUPERVISOR NAME & MOBILE NUMBER": "",
        "VILLAGE NAME": "",
        "ENUMERATOR MOBILE NUMBER": "",
        "HLB DESCRIPTION": "",
        "REMARKS": "",
        "EXPECTED DATE": "",
        "STATUS": "NOT STARTED",
        "LAST UPDATED": "",
        "COMPLETED DATE": "",
        "PENDING": ""
    }
]

df = pd.DataFrame(MASTER_DATA)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">📋 ENUMERATION PROGRESS DASHBOARD</div>',
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD COUNTS
# ============================================================

total = len(df)

completed = len(
    df[df["STATUS"].str.upper() == "COMPLETED"]
)

in_progress = len(
    df[df["STATUS"].str.upper() == "IN PROGRESS"]
)

not_started = len(
    df[df["STATUS"].str.upper() == "NOT STARTED"]
)

if total > 0:
    progress = (completed / total) * 100
else:
    progress = 0


# ============================================================
# SUMMARY CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "TOTAL ENUMERATORS",
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


st.divider()


# ============================================================
# OVERALL PROGRESS
# ============================================================

st.subheader("📊 Overall Enumeration Progress")

st.progress(
    int(progress)
)

st.markdown(
    f"### {progress:.1f}% Completed"
)


# ============================================================
# CHARTS
# ============================================================

chart_col1, chart_col2 = st.columns(2)

status_df = pd.DataFrame({
    "Status": [
        "Completed",
        "In Progress",
        "Not Started"
    ],
    "Count": [
        completed,
        in_progress,
        not_started
    ]
})


with chart_col1:

    st.subheader("Status Distribution")

    fig = px.bar(
        status_df,
        x="Status",
        y="Count",
        text="Count"
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with chart_col2:

    st.subheader("Status Pie Chart")

    fig2 = px.pie(
        status_df,
        names="Status",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


st.divider()


# ============================================================
# ENUMERATOR UPDATE
# ============================================================

st.subheader("👤 Enumerator Update")

enumerator_list = df[
    "HLB NUMBER-ENUMERATOR NAME"
].tolist()

selected = st.selectbox(
    "HLB NUMBER - ENUMERATOR NAME",
    enumerator_list
)


# ============================================================
# FIND SELECTED RECORD
# ============================================================

row_index = df.index[
    df["HLB NUMBER-ENUMERATOR NAME"] == selected
][0]

record = df.loc[row_index]


# ============================================================
# AUTOMATIC DETAILS
# ============================================================

st.markdown("### 📌 Enumerator Details")

d1, d2 = st.columns(2)

with d1:

    st.text_input(
        "Circle Number",
        value=str(record["CIRCLE NUMBER"]),
        disabled=True
    )

    st.text_input(
        "Supervisor Name & Mobile",
        value=str(
            record["SUPERVISOR NAME & MOBILE NUMBER"]
        ),
        disabled=True
    )

    st.text_input(
        "Enumerator Mobile",
        value=str(
            record["ENUMERATOR MOBILE NUMBER"]
        ),
        disabled=True
    )


with d2:

    st.text_input(
        "Village Name",
        value=str(
            record["VILLAGE NAME"]
        ),
        disabled=True
    )

    st.text_area(
        "HLB Description",
        value=str(
            record["HLB DESCRIPTION"]
        ),
        disabled=True
    )


# ============================================================
# CURRENT STATUS
# ============================================================

st.markdown("### 📝 Update Enumeration")

current_status = str(
    record["STATUS"]
).upper()

status_options = [
    "NOT STARTED",
    "IN PROGRESS",
    "COMPLETED"
]

status = st.selectbox(
    "Enumeration Status",
    status_options,
    index=status_options.index(current_status)
)


# ============================================================
# PENDING
# ============================================================

pending = st.number_input(
    "Pending Count",
    min_value=0,
    step=1,
    value=0
)


# ============================================================
# EXPECTED DATE
# ============================================================

expected_date = st.date_input(
    "Expected Completion Date",
    value=date.today()
)


# ============================================================
# REMARKS
# ============================================================

remarks = st.text_area(
    "Remarks / Reason for Pending",
    placeholder=(
        "Example: 18 entries pending. "
        "Some houses were locked. "
        "Will complete by expected date."
    ),
    height=120
)


# ============================================================
# UPDATE BUTTON
# ============================================================

if st.button(
    "💾 UPDATE ENUMERATION",
    type="primary",
    use_container_width=True
):

    # --------------------------------------------
    # VALIDATION
    # --------------------------------------------

    if status == "IN PROGRESS":

        if pending <= 0:
            st.error(
                "⚠️ Pending Count must be entered."
            )

            st.stop()

        if not remarks.strip():
            st.error(
                "⚠️ Remarks are compulsory when status is IN PROGRESS."
            )

            st.stop()

    # --------------------------------------------
    # COMPLETED VALIDATION
    # --------------------------------------------

    if status == "COMPLETED":

        pending = 0

    # --------------------------------------------
    # UPDATE DATA
    # --------------------------------------------

    now = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    df.loc[
        row_index,
        "STATUS"
    ] = status

    df.loc[
        row_index,
        "PENDING"
    ] = pending

    df.loc[
        row_index,
        "REMARKS"
    ] = remarks

    df.loc[
        row_index,
        "EXPECTED DATE"
    ] = expected_date.strftime(
        "%d-%m-%Y"
    )

    df.loc[
        row_index,
        "LAST UPDATED"
    ] = now

    if status == "COMPLETED":

        df.loc[
            row_index,
            "COMPLETED DATE"
        ] = datetime.now().strftime(
            "%d-%m-%Y"
        )

    st.success(
        f"✅ {selected} updated successfully!"
    )

    st.rerun()


# ============================================================
# ENUMERATOR STATUS TABLE
# ============================================================

st.divider()

st.subheader("📋 Enumerator Status List")


search = st.text_input(
    "🔍 Search Enumerator"
)

filter_status = st.selectbox(
    "Filter Status",
    [
        "ALL",
        "COMPLETED",
        "IN PROGRESS",
        "NOT STARTED"
    ]
)


display_df = df.copy()


if search:

    display_df = display_df[
        display_df[
            "HLB NUMBER-ENUMERATOR NAME"
        ].str.contains(
            search,
            case=False,
            na=False
        )
    ]


if filter_status != "ALL":

    display_df = display_df[
        display_df["STATUS"] == filter_status
    ]


columns_to_show = [
    "HLB NUMBER-ENUMERATOR NAME",
    "CIRCLE NUMBER",
    "VILLAGE NAME",
    "STATUS",
    "PENDING",
    "EXPECTED DATE",
    "LAST UPDATED",
    "COMPLETED DATE"
]


st.dataframe(
    display_df[columns_to_show],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Enumeration Progress Dashboard"
)