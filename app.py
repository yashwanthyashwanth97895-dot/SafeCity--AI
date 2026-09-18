import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SafeCity AI",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Main title */
.main-title {
    font-size: 48px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 22px;
    font-weight: 500;
    margin-top: 0px;
    margin-bottom: 10px;
}

/* Description */
.description {
    font-size: 16px;
    margin-bottom: 20px;
}

/* Section headings */
.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* KPI cards */
.kpi-card {
    padding: 20px;
    border-radius: 15px;
    background-color: rgb(38, 39, 48);;
    border: 1px solid #e6e9ef;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
    text-align: center;
    min-height: 125px;
}

.kpi-title {
    font-size: 15px;
    font-weight: 600;
}

.kpi-value {
    font-size: 30px;
    font-weight: 750;
    margin-top: 8px;
}

/* Insight cards */
.insight-card {
    padding: 18px;
    border-radius: 14px;
    background-color: white;
    border-left: 5px solid #4f46e5;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("safecity_cleaned_data.csv")


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🔎 Filters")

st.sidebar.markdown(
    "Use the filters below to explore the historical crime dataset."
)

states = sorted(df["STATE/UT"].dropna().unique())

selected_state = st.sidebar.selectbox(
    "📍 Select State / UT",
    ["All"] + states
)

min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "📅 Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Dataset Period")

st.sidebar.write(
    f"**{min_year} – {max_year}**"
)

st.sidebar.markdown("---")

st.sidebar.info(
    "SafeCity AI uses historical recorded-crime data for analytical "
    "and awareness purposes."
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["STATE/UT"] == selected_state
    ]

filtered_df = filtered_df[
    (filtered_df["Year"] >= selected_years[0]) &
    (filtered_df["Year"] <= selected_years[1])
]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏙️ SafeCity AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Women & Child Safety Intelligence Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="description">'
    'An interactive data-driven platform for analyzing historical '
    'recorded-crime patterns related to women and children.'
    '</div>',
    unsafe_allow_html=True
)

st.warning(
    "⚠️ This platform analyzes historical recorded-crime data. "
    "The risk levels shown are historical classifications and should "
    "not be interpreted as predictions of individual crimes or "
    "guaranteed safety."
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📊 Dataset Overview</div>',
    unsafe_allow_html=True
)

total_records = len(df)
total_columns = len(df.columns)
total_women = df["Women_Total_Crimes"].sum()
total_children = df["Total"].sum()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📋 Total Records</div>
            <div class="kpi-value">{total_records:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🗂️ Total Features</div>
            <div class="kpi-value">{total_columns}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">👩 Women-related Cases</div>
            <div class="kpi-value">{total_women:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">👧 Children-related Cases</div>
            <div class="kpi-value">{total_children:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FILTERED SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">📌 Current Selection</div>',
    unsafe_allow_html=True
)

f1, f2, f3 = st.columns(3)

with f1:
    st.metric(
        "Filtered Records",
        f"{len(filtered_df):,}"
    )

with f2:
    st.metric(
        "Women Cases",
        f"{filtered_df['Women_Total_Crimes'].sum():,}"
    )

with f3:
    st.metric(
        "Children Cases",
        f"{filtered_df['Total'].sum():,}"
    )


# ============================================================
# YEAR-WISE TREND
# ============================================================

st.markdown(
    '<div class="section-title">📈 Historical Crime Trend</div>',
    unsafe_allow_html=True
)

yearly_data = (
    filtered_df
    .groupby("Year")
    .agg(
        Women_Crimes=("Women_Total_Crimes", "sum"),
        Children_Crimes=("Total", "sum")
    )
    .reset_index()
)

st.line_chart(
    yearly_data.set_index("Year"),
    use_container_width=True
)

st.caption(
    "Trend shows recorded cases in the selected state and year range."
)


# ============================================================
# WOMEN VS CHILDREN
# ============================================================

st.markdown(
    '<div class="section-title">👩 Women vs 👧 Children</div>',
    unsafe_allow_html=True
)

comparison_data = pd.DataFrame({
    "Category": [
        "Women-related Crimes",
        "Children-related Crimes"
    ],
    "Cases": [
        filtered_df["Women_Total_Crimes"].sum(),
        filtered_df["Total"].sum()
    ]
})

st.bar_chart(
    comparison_data.set_index("Category"),
    use_container_width=True
)


# ============================================================
# WOMEN CRIME ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">👩 Women Crime Category Analysis</div>',
    unsafe_allow_html=True
)

women_categories = {
    "Rape": "Rape_Women",
    "Kidnapping & Abduction": "Kidnapping and Abduction_Women",
    "Dowry Deaths": "Dowry Deaths",
    "Assault on Women": "Assault on women with intent to outrage her modesty",
    "Insult to Modesty": "Insult to modesty of Women",
    "Cruelty by Husband / Relatives": "Cruelty by Husband or his Relatives",
    "Importation of Girls": "Importation of Girls"
}

women_category_data = []

for category, column in women_categories.items():
    women_category_data.append({
        "Crime Category": category,
        "Cases": filtered_df[column].sum()
    })

women_category_df = pd.DataFrame(women_category_data)

women_category_df = women_category_df.sort_values(
    "Cases",
    ascending=False
)

st.bar_chart(
    women_category_df.set_index("Crime Category"),
    use_container_width=True
)


# ============================================================
# CHILDREN CRIME ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">👧 Children Crime Category Analysis</div>',
    unsafe_allow_html=True
)

children_categories = {
    "Murder": "Murder",
    "Rape": "Rape_Children",
    "Kidnapping & Abduction": "Kidnapping and Abduction_Children",
    "Foeticide": "Foeticide",
    "Abetment of Suicide": "Abetment of suicide",
    "Exposure & Abandonment": "Exposure and abandonment",
    "Procuration of Minor Girls": "Procuration of minor girls",
    "Buying Girls for Prostitution": "Buying of girls for prostitution",
    "Selling Girls for Prostitution": "Selling of girls for prostitution",
    "Child Marriage Act": "Prohibition of child marriage act",
    "Other Crimes": "Other Crimes"
}

children_category_data = []

for category, column in children_categories.items():
    children_category_data.append({
        "Crime Category": category,
        "Cases": filtered_df[column].sum()
    })

children_category_df = pd.DataFrame(children_category_data)

children_category_df = children_category_df.sort_values(
    "Cases",
    ascending=False
)

st.bar_chart(
    children_category_df.set_index("Crime Category"),
    use_container_width=True
)


# ============================================================
# STATE-WISE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🗺️ State-wise Recorded Crime Analysis</div>',
    unsafe_allow_html=True
)

state_data = (
    filtered_df
    .groupby("STATE/UT")
    .agg(
        Women_Crimes=("Women_Total_Crimes", "sum"),
        Children_Crimes=("Total", "sum")
    )
    .reset_index()
)

state_data["Combined_Crimes"] = (
    state_data["Women_Crimes"] +
    state_data["Children_Crimes"]
)

state_data = state_data.sort_values(
    "Combined_Crimes",
    ascending=False
)

st.dataframe(
    state_data,
    use_container_width=True
)


# ============================================================
# TOP STATES
# ============================================================

st.markdown(
    '<div class="section-title">🏆 Top States by Recorded Cases</div>',
    unsafe_allow_html=True
)

top_states = state_data.head(10)

if len(top_states) > 0:
    st.bar_chart(
        top_states.set_index("STATE/UT")["Combined_Crimes"],
        use_container_width=True
    )


# ============================================================
# DISTRICT ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📍 District / Police-Unit Analysis</div>',
    unsafe_allow_html=True
)

district_data = filtered_df[
    ~filtered_df["DISTRICT"]
    .str.upper()
    .str.contains("TOTAL", na=False)
].copy()

district_summary = (
    district_data
    .groupby(["STATE/UT", "DISTRICT"])
    .agg(
        Women_Crimes=("Women_Total_Crimes", "sum"),
        Children_Crimes=("Total", "sum")
    )
    .reset_index()
)

district_summary["Combined_Crimes"] = (
    district_summary["Women_Crimes"] +
    district_summary["Children_Crimes"]
)

district_summary = district_summary.sort_values(
    "Combined_Crimes",
    ascending=False
)

st.dataframe(
    district_summary.head(15),
    use_container_width=True
)


# ============================================================
# HISTORICAL RISK LEVEL
# ============================================================

st.markdown(
    '<div class="section-title">⚠️ Historical Risk-Level Analysis</div>',
    unsafe_allow_html=True
)

risk_counts = (
    filtered_df["Risk_Level"]
    .value_counts()
    .reindex(["Low", "Medium", "High"])
    .fillna(0)
)

risk_df = pd.DataFrame({
    "Risk Level": risk_counts.index,
    "Records": risk_counts.values
})

st.bar_chart(
    risk_df.set_index("Risk Level"),
    use_container_width=True
)


# ============================================================
# RISK CARDS
# ============================================================

r1, r2, r3 = st.columns(3)

with r1:
    st.success(
        f"🟢 **Low Risk Records**\n\n"
        f"### {int(risk_counts['Low']):,}"
    )

with r2:
    st.warning(
        f"🟡 **Medium Risk Records**\n\n"
        f"### {int(risk_counts['Medium']):,}"
    )

with r3:
    st.error(
        f"🔴 **High Risk Records**\n\n"
        f"### {int(risk_counts['High']):,}"
    )


# ============================================================
# ============================================================
# ============================================================
# DETAILED CRIME ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Detailed Crime Analysis</div>',
    unsafe_allow_html=True
)

st.write(
    "Explore historical recorded-crime patterns by state, "
    "district/police unit, crime category and year."
)


# ============================================================
# STATE AND YEAR ANALYSIS
# ============================================================

analysis_col1, analysis_col2 = st.columns(2)

with analysis_col1:

    analysis_states = sorted(
        df["STATE/UT"].dropna().unique()
    )

    selected_analysis_state = st.selectbox(
        "📍 Select State / UT",
        ["All"] + analysis_states,
        key="analysis_state"
    )

with analysis_col2:

    analysis_years = sorted(
        df["Year"].dropna().unique()
    )

    selected_analysis_year = st.selectbox(
        "📅 Select Year",
        ["All"] + analysis_years,
        key="analysis_year"
    )


# Apply filters
analysis_data = df.copy()

if selected_analysis_state != "All":

    analysis_data = analysis_data[
        analysis_data["STATE/UT"] == selected_analysis_state
    ]

if selected_analysis_year != "All":

    analysis_data = analysis_data[
        analysis_data["Year"] == selected_analysis_year
    ]


# ============================================================
# SUMMARY CARDS
# ============================================================

st.markdown("---")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:

    st.metric(
        "📋 Records",
        f"{len(analysis_data):,}"
    )

with summary_col2:

    st.metric(
        "👩 Women Cases",
        f"{int(analysis_data['Women_Total_Crimes'].sum()):,}"
    )

with summary_col3:

    st.metric(
        "👧 Children Cases",
        f"{int(analysis_data['Total'].sum()):,}"
    )


# ============================================================
# YEAR-WISE TREND
# ============================================================

st.subheader("📈 Year-wise Crime Trend")

if len(analysis_data) > 0:

    yearly_analysis = (
        analysis_data
        .groupby("Year")
        .agg(
            Women_Cases=("Women_Total_Crimes", "sum"),
            Children_Cases=("Total", "sum")
        )
        .reset_index()
    )

    yearly_analysis["Combined_Cases"] = (
        yearly_analysis["Women_Cases"] +
        yearly_analysis["Children_Cases"]
    )

    yearly_chart = yearly_analysis.set_index("Year")[
        ["Women_Cases", "Children_Cases"]
    ]

    st.line_chart(
        yearly_chart,
        use_container_width=True
    )

else:

    st.warning("No data available for the selected filters.")


# ============================================================
# WOMEN CRIME CATEGORY ANALYSIS
# ============================================================

st.subheader("👩 Women-related Crime Categories")

women_category_columns = {
    "Rape": "Rape_Women",
    "Kidnapping and Abduction": "Kidnapping and Abduction_Women",
    "Dowry Deaths": "Dowry Deaths",
    "Assault on women": "Assault on women with intent to outrage her modesty",
    "Insult to modesty": "Insult to modesty of Women",
    "Cruelty by Husband/Relatives": "Cruelty by Husband or his Relatives",
    "Importation of Girls": "Importation of Girls"
}

women_category_data = pd.DataFrame({
    "Crime Category": list(women_category_columns.keys()),
    "Recorded Cases": [
        analysis_data[column].sum()
        for column in women_category_columns.values()
    ]
})

women_category_data = women_category_data.sort_values(
    "Recorded Cases",
    ascending=False
)

st.bar_chart(
    women_category_data.set_index("Crime Category"),
    use_container_width=True
)


# ============================================================
# CHILDREN CRIME CATEGORY ANALYSIS
# ============================================================

st.subheader("👧 Children-related Crime Categories")

children_category_columns = {
    "Murder": "Murder",
    "Rape": "Rape_Children",
    "Kidnapping and Abduction": "Kidnapping and Abduction_Children",
    "Foeticide": "Foeticide",
    "Abetment of suicide": "Abetment of suicide",
    "Exposure and abandonment": "Exposure and abandonment",
    "Procuration of minor girls": "Procuration of minor girls",
    "Buying of girls for prostitution": "Buying of girls for prostitution",
    "Selling of girls for prostitution": "Selling of girls for prostitution",
    "Prohibition of child marriage act": "Prohibition of child marriage act",
    "Other Crimes": "Other Crimes"
}

children_category_data = pd.DataFrame({
    "Crime Category": list(children_category_columns.keys()),
    "Recorded Cases": [
        analysis_data[column].sum()
        for column in children_category_columns.values()
    ]
})

children_category_data = children_category_data.sort_values(
    "Recorded Cases",
    ascending=False
)

st.bar_chart(
    children_category_data.set_index("Crime Category"),
    use_container_width=True
)


# ============================================================
# TOP DISTRICTS / POLICE UNITS
# ============================================================

st.subheader("🏙️ Top Districts / Police Units")

district_analysis = analysis_data[
    ~analysis_data["DISTRICT"]
    .astype(str)
    .str.upper()
    .str.contains("TOTAL", na=False)
].copy()

if len(district_analysis) > 0:

    top_districts = (
        district_analysis
        .groupby(["STATE/UT", "DISTRICT"])
        .agg(
            Women_Cases=("Women_Total_Crimes", "sum"),
            Children_Cases=("Total", "sum")
        )
        .reset_index()
    )

    top_districts["Combined_Cases"] = (
        top_districts["Women_Cases"] +
        top_districts["Children_Cases"]
    )

    top_districts = top_districts.sort_values(
        "Combined_Cases",
        ascending=False
    ).head(15)

    district_chart_data = top_districts.copy()

    district_chart_data["District"] = (
        district_chart_data["STATE/UT"] +
        " — " +
        district_chart_data["DISTRICT"]
    )

    st.bar_chart(
        district_chart_data.set_index("District")[
            ["Combined_Cases"]
        ],
        use_container_width=True
    )

    st.dataframe(
        top_districts[
            [
                "STATE/UT",
                "DISTRICT",
                "Women_Cases",
                "Children_Cases",
                "Combined_Cases"
            ]
        ],
        use_container_width=True
    )

else:

    st.warning("No district-level records available for the selected filters.")


st.caption(
    "All values represent recorded historical cases in the dataset. "
    "Higher recorded totals do not by themselves mean that a location "
    "is inherently more unsafe, because population, reporting and "
    "registration patterns can differ."
)
# AI RISK ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🤖 AI Risk Analysis</div>',
    unsafe_allow_html=True
)

st.write(
    "Explore historical risk classifications generated during the "
    "machine-learning stage of SafeCity AI."
)

# AI analysis filters
ai_col1, ai_col2 = st.columns(2)

with ai_col1:

    ai_states = sorted(
        df["STATE/UT"].dropna().unique()
    )

    ai_selected_state = st.selectbox(
        "📍 Select State / UT for AI Analysis",
        ["All"] + ai_states,
        key="ai_state"
    )

with ai_col2:

    ai_years = sorted(
        df["Year"].dropna().unique()
    )

    ai_selected_year = st.selectbox(
        "📅 Select Year for AI Analysis",
        ai_years,
        index=len(ai_years) - 1,
        key="ai_year"
    )


# Apply AI filters
ai_data = df[
    df["Year"] == ai_selected_year
].copy()

if ai_selected_state != "All":

    ai_data = ai_data[
        ai_data["STATE/UT"] == ai_selected_state
    ]


# Check whether data exists
if len(ai_data) > 0:

    # Risk distribution
    ai_risk_counts = (
        ai_data["Risk_Level"]
        .value_counts()
        .reindex(["Low", "Medium", "High"])
        .fillna(0)
    )

    # Determine dominant historical risk
    dominant_risk = ai_risk_counts.idxmax()
    dominant_count = int(ai_risk_counts.max())

    # Calculate recorded cases
    ai_women_cases = int(
        ai_data["Women_Total_Crimes"].sum()
    )

    ai_children_cases = int(
        ai_data["Total"].sum()
    )

    ai_combined_cases = (
        ai_women_cases + ai_children_cases
    )

    # --------------------------------------------------------
    # AI RESULT CARD
    # --------------------------------------------------------

    st.markdown("---")

    result_col1, result_col2, result_col3, result_col4 = st.columns(4)

    with result_col1:

        st.metric(
            "🤖 Historical Risk",
            dominant_risk
        )

    with result_col2:

        st.metric(
            "📋 Records Analysed",
            f"{len(ai_data):,}"
        )

    with result_col3:

        st.metric(
            "👩 Women Cases",
            f"{ai_women_cases:,}"
        )

    with result_col4:

        st.metric(
            "👧 Children Cases",
            f"{ai_children_cases:,}"
        )


    # --------------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------------

    st.subheader("📊 Historical Risk Distribution")

    ai_risk_df = pd.DataFrame({
        "Risk Level": ai_risk_counts.index,
        "Records": ai_risk_counts.values
    })

    st.bar_chart(
        ai_risk_df.set_index("Risk Level"),
        use_container_width=True
    )


    # --------------------------------------------------------
    # AI INTERPRETATION
    # --------------------------------------------------------

    if dominant_risk == "High":

        st.error(
            f"🔴 The selected historical data is predominantly "
            f"classified as **High Risk**, with {dominant_count:,} "
            f"records receiving this classification."
        )

    elif dominant_risk == "Medium":

        st.warning(
            f"🟡 The selected historical data is predominantly "
            f"classified as **Medium Risk**, with {dominant_count:,} "
            f"records receiving this classification."
        )

    else:

        st.success(
            f"🟢 The selected historical data is predominantly "
            f"classified as **Low Risk**, with {dominant_count:,} "
            f"records receiving this classification."
        )


    st.info(
        f"For {ai_selected_year}"
        + (
            f" in {ai_selected_state}"
            if ai_selected_state != "All"
            else ""
        )
        + f", the dataset contains **{ai_combined_cases:,} "
        "combined recorded cases** across the selected records."
    )


    st.caption(
        "Risk levels shown here are historical classifications generated "
        "during the machine-learning stage. They are not predictions of "
        "future crimes, individual offenders, or guaranteed safety."
    )

else:

    st.warning(
        "No records are available for the selected state and year."
    )


# ============================================================
# MACHINE LEARNING MODEL
# ============================================================

st.markdown(
    '<div class="section-title">🧠 Machine Learning Model</div>',
    unsafe_allow_html=True
)

st.write(
    "SafeCity AI uses a Random Forest Classifier for historical "
    "risk-level classification."
)

ml_col1, ml_col2, ml_col3, ml_col4 = st.columns(4)

with ml_col1:
    st.metric("Algorithm", "Random Forest")

with ml_col2:
    st.metric("Accuracy", "95.26%")

with ml_col3:
    st.metric("Precision", "95.29%")

with ml_col4:
    st.metric("F1-Score", "95.27%")


st.write(
    "The model was trained and evaluated using the cleaned historical "
    "dataset in Google Colab. The dashboard uses the resulting historical "
    "risk classifications stored in the cleaned dataset."
)

st.warning(
    "The reported accuracy measures performance on the historical test "
    "dataset. It should not be interpreted as 95.26% accuracy for "
    "predicting future crimes."
)
# ============================================================
# MACHINE LEARNING EVALUATION
# ============================================================

st.markdown(
    '<div class="section-title">🧠 Machine Learning Evaluation</div>',
    unsafe_allow_html=True
)

st.write(
    "The Random Forest Classifier was trained and evaluated using "
    "the historical crime dataset in Google Colab."
)


# ============================================================
# MODEL PERFORMANCE
# ============================================================

performance_col1, performance_col2, performance_col3, performance_col4 = st.columns(4)

with performance_col1:
    st.metric("Algorithm", "Random Forest")

with performance_col2:
    st.metric("Accuracy", "95.26%")

with performance_col3:
    st.metric("Precision", "95.29%")

with performance_col4:
    st.metric("F1-Score", "95.27%")


st.caption(
    "These metrics represent performance on the historical test dataset."
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

st.subheader("📊 Confusion Matrix")

st.write(
    "The confusion matrix shows how the Random Forest model classified "
    "the historical Low, Medium and High risk records."
)

# Actual confusion matrix from the Colab model evaluation
confusion_matrix_data = pd.DataFrame(
    [
        [583, 17, 0],
        [13, 560, 24],
        [0, 31, 566]
    ],
    index=["Actual Low", "Actual Medium", "Actual High"],
    columns=["Predicted Low", "Predicted Medium", "Predicted High"]
)

st.dataframe(
    confusion_matrix_data,
    use_container_width=True
)

st.caption(
    "Most classifications fall on the diagonal, indicating correct "
    "classification of the historical test records."
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

st.subheader("🎯 Feature Importance")

st.write(
    "Feature importance shows which input variables contributed most "
    "to the Random Forest's historical risk classification."
)

feature_importance_data = pd.DataFrame({
    "Feature": [
        "Cruelty by Husband or his Relatives",
        "Assault on women with intent to outrage her modesty",
        "Kidnapping and Abduction - Women",
        "Rape - Women",
        "Insult to modesty of Women",
        "Dowry Deaths",
        "Rape - Children",
        "Kidnapping and Abduction - Children",
        "Other Crimes",
        "Murder",
        "Year",
        "Exposure and abandonment",
        "Prohibition of child marriage act",
        "Procuration of minor girls",
        "Foeticide",
        "Importation of Girls",
        "Abetment of suicide",
        "Selling of girls for prostitution",
        "Buying of girls for prostitution"
    ],
    "Importance": [
        0.307781,
        0.185630,
        0.132140,
        0.121316,
        0.053665,
        0.047618,
        0.039231,
        0.036192,
        0.025189,
        0.018424,
        0.013699,
        0.007868,
        0.002649,
        0.002647,
        0.001707,
        0.001663,
        0.001246,
        0.000980,
        0.000355
    ]
})

feature_importance_data = feature_importance_data.sort_values(
    "Importance",
    ascending=False
)

st.bar_chart(
    feature_importance_data.set_index("Feature"),
    use_container_width=True
)

st.caption(
    "Feature importance indicates model influence on classification; "
    "it does not establish a causal relationship between a crime category "
    "and risk."
)


# ============================================================
# MODEL INTERPRETATION
# ============================================================

st.info(
    "The Random Forest model classifies historical records into Low, "
    "Medium and High risk levels. The model is not intended to predict "
    "individual crimes, identify offenders, or guarantee future safety."
)
# SAFETY INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Key Insights</div>',
    unsafe_allow_html=True
)

if len(women_category_df) > 0:

    highest_women = women_category_df.iloc[0]

    st.markdown(
        f"""
        <div class="insight-card">
        👩 <b>Women-related analysis:</b>
        <br>
        The highest recorded women-related crime category in the
        selected data is <b>{highest_women['Crime Category']}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )


if len(children_category_df) > 0:

    highest_children = children_category_df.iloc[0]

    st.markdown(
        f"""
        <div class="insight-card">
        👧 <b>Children-related analysis:</b>
        <br>
        The highest recorded children-related crime category in the
        selected data is <b>{highest_children['Crime Category']}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )


if len(state_data) > 0:

    highest_state = state_data.iloc[0]

    st.markdown(
        f"""
        <div class="insight-card">
        🗺️ <b>State-level observation:</b>
        <br>
        <b>{highest_state['STATE/UT']}</b> has the highest combined
        recorded case total within the current selection.
        </div>
        """,
        unsafe_allow_html=True
    )


st.info(
    "These observations are based on recorded historical cases. "
    "Differences between regions can be influenced by population size, "
    "reporting practices, registration patterns, and data coverage."
)


# ============================================================
# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.markdown(
    '<div class="section-title">📥 Download Filtered Data</div>',
    unsafe_allow_html=True
)

st.write(
    "Download the records currently selected using the dashboard filters."
)

download_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=download_data,
    file_name="SafeCity_filtered_data.csv",
    mime="text/csv"
)

st.caption(
    f"Current selection contains {len(filtered_df):,} records."
)
# DATA PREVIEW
# ============================================================

with st.expander("📋 View Dataset Records"):

    st.write(
        f"Showing the first 20 records from the current selection "
        f"of {len(filtered_df):,} records."
    )

    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

with st.expander("ℹ️ About SafeCity AI"):

    st.write(
        """
        **SafeCity AI – Women & Child Safety Intelligence Platform**

        SafeCity AI is a data-driven analytical platform designed to
        study historical recorded-crime patterns related to women and
        children.

        The project uses data preprocessing, exploratory data analysis,
        visualization and machine-learning-based historical risk
        classification.

        The Random Forest model was developed and evaluated separately
        during the machine learning stage. The dashboard displays the
        historical risk classifications stored in the cleaned dataset.

        This system is intended for academic analysis, awareness and
        visualization. It is not a law-enforcement system and does not
        predict individual crimes.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="footer">'
    '🏙️ <b>SafeCity AI</b> | Women & Child Safety Intelligence Platform'
    '<br>'
    'Built with Python • Pandas • Streamlit • Machine Learning'
    '</div>',
    unsafe_allow_html=True
)