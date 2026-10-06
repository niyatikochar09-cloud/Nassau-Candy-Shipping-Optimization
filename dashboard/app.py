from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy | Factory Optimization",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = BASE_DIR / "outputs"
ASSETS_DIR = BASE_DIR / "assets"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 38px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .sub-title {
            font-size: 17px;
            color: #666666;
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 26px;
            font-weight: 650;
            margin-top: 10px;
            margin-bottom: 15px;
        }

        .info-box {
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #dddddd;
            margin-bottom: 15px;
        }

        .small-note {
            font-size: 13px;
            color: #777777;
        }

        div[data-testid="stMetric"] {
            padding: 10px 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data
def load_csv(filename: str) -> pd.DataFrame:
    """Load a CSV file from the outputs directory."""
    file_path = OUTPUTS_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found:\n{file_path}"
        )

    return pd.read_csv(file_path)


def safe_mean(df: pd.DataFrame, column: str, default=0):
    """Return a safe column mean."""
    if column not in df.columns or df.empty:
        return default

    value = pd.to_numeric(
        df[column],
        errors="coerce"
    ).mean()

    return default if pd.isna(value) else value


def safe_sum(df: pd.DataFrame, column: str, default=0):
    """Return a safe column sum."""
    if column not in df.columns or df.empty:
        return default

    value = pd.to_numeric(
        df[column],
        errors="coerce"
    ).sum()

    return default if pd.isna(value) else value


def safe_nunique(df: pd.DataFrame, column: str, default=0):
    """Return a safe unique-value count."""
    if column not in df.columns or df.empty:
        return default

    return df[column].nunique()


# ============================================================
# LOAD PROJECT OUTPUTS
# ============================================================

try:

    # Main transaction-level dataset
    clean_df = load_csv(
        "clean_nassau_dataset.csv"
    )

    # Recommendation-level datasets
    decision_df = load_csv(
        "dashboard_ready_decision_table.csv"
    )

    scenario_df = load_csv(
        "dashboard_scenario_matrix.csv"
    )

    # Analysis datasets
    route_df = load_csv(
        "route_level_performance.csv"
    )

    model_df = load_csv(
        "model_comparison.csv"
    )

    risk_df = load_csv(
        "recommendation_risk_distribution.csv"
    )

    overall_df = load_csv(
        "current_vs_optimized_state.csv"
    )

except Exception as e:

    st.error(
        "Unable to load the required project output files."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏭 Nassau Candy")

st.sidebar.markdown(
    "**Factory Reallocation & Shipping Optimization**"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Dashboard Sections",
    [
        "Executive Overview",
        "Factory Recommendations",
        "Scenario Simulator",
        "Route Performance",
        "Predictive Model",
    ],
)

st.sidebar.divider()

st.sidebar.info(
    "Recommendation results are model-based what-if estimates "
    "and should be validated using real operational constraints."
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Nassau Candy Factory Reallocation & Shipping Optimization</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-title">Predictive Decision-Support Dashboard | Unified Mentor Internship Project</div>',
    unsafe_allow_html=True,
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True,
    )

    st.write(
        """
        This dashboard evaluates current factory assignments, shipping
        performance, predictive lead-time estimates, and potential factory
        reallocation opportunities using a machine-learning-based
        what-if framework.
        """
    )

    # --------------------------------------------------------
    # CORE BUSINESS KPIs
    # --------------------------------------------------------

    total_records = len(clean_df)

    total_orders = safe_nunique(
        clean_df,
        "Order_ID",
        8549
    )

    total_products = safe_nunique(
        clean_df,
        "Product_Name",
        15
    )

    total_customers = safe_nunique(
        clean_df,
        "Customer_ID",
        5044
    )

    total_factories = safe_nunique(
        clean_df,
        "Current_Factory",
        5
    )

    total_regions = safe_nunique(
        clean_df,
        "Region",
        4
    )

    total_units = safe_sum(
        clean_df,
        "Units",
        38654
    )

    total_sales = safe_sum(
        clean_df,
        "Sales",
        141783.63
    )

    total_profit = safe_sum(
        clean_df,
        "Gross_Profit",
        93442.80
    )

    avg_margin = safe_mean(
        clean_df,
        "Profit_Margin",
        66.51
    )

    avg_lead_time = safe_mean(
        clean_df,
        "Lead_Time_Days",
        1320.84
    )

    # --------------------------------------------------------
    # KPI ROW 1
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Transaction Records",
            f"{total_records:,}"
        )

    with col2:
        st.metric(
            "Unique Orders",
            f"{total_orders:,}"
        )

    with col3:
        st.metric(
            "Products",
            total_products
        )

    with col4:
        st.metric(
            "Customers",
            f"{total_customers:,}"
        )

    # --------------------------------------------------------
    # KPI ROW 2
    # --------------------------------------------------------

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            "Factories",
            total_factories
        )

    with col6:
        st.metric(
            "Regions",
            total_regions
        )

    with col7:
        st.metric(
            "Total Sales",
            f"${total_sales:,.2f}"
        )

    with col8:
        st.metric(
            "Gross Profit",
            f"${total_profit:,.2f}"
        )

    # --------------------------------------------------------
    # KPI ROW 3
    # --------------------------------------------------------

    col9, col10, col11, col12 = st.columns(4)

    with col9:
        st.metric(
            "Total Units",
            f"{total_units:,.0f}"
        )

    with col10:
        st.metric(
            "Avg. Profit Margin",
            f"{avg_margin:.2f}%"
        )

    with col11:
        st.metric(
            "Avg. Lead Time",
            f"{avg_lead_time:.2f} days"
        )

    with col12:

        positive_opportunities = 0

        if "Decision_Status" in decision_df.columns:

            positive_opportunities = (
                decision_df["Decision_Status"]
                .astype(str)
                .str.contains(
                    "Reallocation",
                    case=False,
                    na=False
                )
                .sum()
            )

        st.metric(
            "Reallocation Opportunities",
            positive_opportunities
        )

    st.divider()

    # --------------------------------------------------------
    # OPTIMIZATION SNAPSHOT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Optimization Snapshot</div>',
        unsafe_allow_html=True,
    )

    avg_reduction = safe_mean(
        decision_df,
        "Lead_Time_Reduction_Days",
        0
    )

    avg_reduction_pct = safe_mean(
        decision_df,
        "Lead_Time_Reduction_Percent",
        0
    )

    avg_confidence = safe_mean(
        decision_df,
        "Scenario_Confidence_Score",
        0
    )

    avg_profit_stability = safe_mean(
        decision_df,
        "Profit_Stability_Score",
        0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Avg. Predicted Reduction",
            f"{avg_reduction:.2f} days"
        )

    with col2:
        st.metric(
            "Avg. Reduction %",
            f"{avg_reduction_pct:.2f}%"
        )

    with col3:
        st.metric(
            "Avg. Confidence Score",
            f"{avg_confidence:.2f}"
        )

    with col4:
        st.metric(
            "Avg. Profit Stability",
            f"{avg_profit_stability:.2f}"
        )

    st.divider()

    # --------------------------------------------------------
    # CURRENT VS OPTIMIZED
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Current vs Model-Based Optimized State</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        overall_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "The optimized state represents model-based what-if estimates, "
        "not guaranteed operational results."
    )

    st.divider()

    # --------------------------------------------------------
    # VISUAL INSIGHTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Visual Insights</div>',
        unsafe_allow_html=True,
    )

    image_files = [
        (
            "lead_time_distribution.png",
            "Lead-Time Distribution"
        ),
        (
            "lead_time_by_region.png",
            "Lead Time by Region"
        ),
        (
            "lead_time_by_factory.png",
            "Lead Time by Factory"
        ),
        (
            "product_sales_gross_profit.png",
            "Product Sales and Gross Profit"
        ),
        (
            "current_vs_optimized_lead_time.png",
            "Current vs Optimized Lead Time"
        ),
        (
            "recommendation_risk_distribution.png",
            "Recommendation Risk Distribution"
        ),
    ]

    for filename, title in image_files:

        image_path = ASSETS_DIR / filename

        if image_path.exists():

            st.markdown(f"### {title}")

            st.image(
                str(image_path),
                use_container_width=True
            )


# ============================================================
# FACTORY RECOMMENDATIONS
# ============================================================

elif page == "Factory Recommendations":

    st.markdown(
        '<div class="section-title">Factory Reallocation Recommendations</div>',
        unsafe_allow_html=True,
    )

    st.write(
        """
        This section identifies product-region combinations where an
        alternative factory produces a positive predicted improvement
        in shipping lead time.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        product_options = ["All Products"]

        if "Product_Name" in decision_df.columns:

            product_options += sorted(
                decision_df["Product_Name"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        selected_product = st.selectbox(
            "Product",
            product_options
        )

    with col2:

        region_options = ["All Regions"]

        if "Region" in decision_df.columns:

            region_options += sorted(
                decision_df["Region"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        selected_region = st.selectbox(
            "Region",
            region_options
        )

    with col3:

        risk_options = ["All Risk Levels"]

        if "Final_Risk_Level" in decision_df.columns:

            risk_options += sorted(
                decision_df["Final_Risk_Level"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        selected_risk = st.selectbox(
            "Risk Level",
            risk_options
        )

    filtered_df = decision_df.copy()

    if selected_product != "All Products":

        filtered_df = filtered_df[
            filtered_df["Product_Name"]
            .astype(str)
            == selected_product
        ]

    if selected_region != "All Regions":

        filtered_df = filtered_df[
            filtered_df["Region"]
            .astype(str)
            == selected_region
        ]

    if selected_risk != "All Risk Levels":

        filtered_df = filtered_df[
            filtered_df["Final_Risk_Level"]
            .astype(str)
            == selected_risk
        ]

    st.markdown(
        "### Recommendation Table"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    if not filtered_df.empty:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Opportunities",
                len(filtered_df)
            )

        with col2:
            st.metric(
                "Avg. Reduction",
                f"{safe_mean(filtered_df, 'Lead_Time_Reduction_Days', 0):.2f} days"
            )

        with col3:
            st.metric(
                "Avg. Optimization Score",
                f"{safe_mean(filtered_df, 'Optimization_Score', 0):.2f}"
            )

        with col4:
            st.metric(
                "Avg. Confidence",
                f"{safe_mean(filtered_df, 'Scenario_Confidence_Score', 0):.2f}"
            )

        st.markdown(
            "### Recommendation Visualization"
        )

        chart_path = (
            ASSETS_DIR
            / "top_reallocation_opportunities.png"
        )

        if chart_path.exists():

            st.image(
                str(chart_path),
                use_container_width=True
            )


# ============================================================
# SCENARIO SIMULATOR
# ============================================================

elif page == "Scenario Simulator":

    st.markdown(
        '<div class="section-title">Factory What-If Scenario Simulator</div>',
        unsafe_allow_html=True,
    )

    st.write(
        """
        Select a product, region, shipping mode, and candidate factory
        to examine the predicted lead-time outcome under that scenario.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # PRODUCT
    # --------------------------------------------------------

    products = sorted(
        scenario_df["Product_Name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_product = st.selectbox(
        "Select Product",
        products
    )

    filtered_product = scenario_df[
        scenario_df["Product_Name"].astype(str)
        == selected_product
    ]

    # --------------------------------------------------------
    # REGION
    # --------------------------------------------------------

    regions = sorted(
        filtered_product["Region"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_region = st.selectbox(
        "Select Region",
        regions
    )

    filtered_region = filtered_product[
        filtered_product["Region"].astype(str)
        == selected_region
    ]

    # --------------------------------------------------------
    # SHIP MODE
    # --------------------------------------------------------

    ship_modes = sorted(
        filtered_region["Ship_Mode"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_ship_mode = st.selectbox(
        "Select Shipping Mode",
        ship_modes
    )

    filtered_mode = filtered_region[
        filtered_region["Ship_Mode"].astype(str)
        == selected_ship_mode
    ]

    # --------------------------------------------------------
    # FACTORY
    # --------------------------------------------------------

    factories = sorted(
        filtered_mode["Candidate_Factory"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_factory = st.selectbox(
        "Select Candidate Factory",
        factories
    )

    scenario_result = filtered_mode[
        filtered_mode["Candidate_Factory"].astype(str)
        == selected_factory
    ]

    st.divider()

    if not scenario_result.empty:

        result = scenario_result.iloc[0]

        current_factory = result.get(
            "Current_Factory",
            "N/A"
        )

        predicted_lead = pd.to_numeric(
            result.get(
                "Predicted_Lead_Time",
                0
            ),
            errors="coerce"
        )

        reduction_days = pd.to_numeric(
            result.get(
                "Lead_Time_Reduction_Days",
                0
            ),
            errors="coerce"
        )

        reduction_pct = pd.to_numeric(
            result.get(
                "Lead_Time_Reduction_Percent",
                0
            ),
            errors="coerce"
        )

        st.markdown(
            "### Scenario Result"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Current Factory",
                current_factory
            )

        with col2:
            st.metric(
                "Candidate Factory",
                selected_factory
            )

        with col3:
            st.metric(
                "Predicted Lead Time",
                f"{predicted_lead:.2f} days"
            )

        with col4:
            st.metric(
                "Predicted Reduction",
                f"{reduction_days:.2f} days"
            )

        st.metric(
            "Predicted Reduction %",
            f"{reduction_pct:.2f}%"
        )

        st.divider()

        st.markdown(
            "### Factory Comparison"
        )

        comparison_columns = [
            "Candidate_Factory",
            "Predicted_Lead_Time",
            "Lead_Time_Reduction_Days",
            "Lead_Time_Reduction_Percent",
        ]

        available_columns = [
            col
            for col in comparison_columns
            if col in filtered_mode.columns
        ]

        comparison_df = filtered_mode[
            available_columns
        ].copy()

        comparison_df = comparison_df.sort_values(
            "Predicted_Lead_Time"
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )

        if "Predicted_Lead_Time" in comparison_df.columns:

            chart_data = comparison_df[
                [
                    "Candidate_Factory",
                    "Predicted_Lead_Time"
                ]
            ].set_index(
                "Candidate_Factory"
            )

            st.bar_chart(
                chart_data
            )

        st.divider()

        st.markdown(
            "### Selected Scenario Details"
        )

        detail_df = scenario_result.T.reset_index()

        detail_df.columns = [
            "Variable",
            "Value"
        ]

        st.dataframe(
            detail_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No matching factory scenario was found."
        )


# ============================================================
# ROUTE PERFORMANCE
# ============================================================

elif page == "Route Performance":

    st.markdown(
        '<div class="section-title">Factory-Region Route Performance</div>',
        unsafe_allow_html=True,
    )

    st.write(
        """
        Route-level analysis compares factory-region combinations using
        operational and financial performance indicators.
        """
    )

    st.divider()

    st.dataframe(
        route_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    if (
        "Current_Factory" in route_df.columns
        and "Average_Lead_Time" in route_df.columns
    ):

        st.markdown(
            "### Average Lead Time by Factory"
        )

        factory_chart = (
            route_df.groupby(
                "Current_Factory"
            )["Average_Lead_Time"]
            .mean()
            .sort_values()
        )

        st.bar_chart(
            factory_chart
        )

    if (
        "Region" in route_df.columns
        and "Average_Lead_Time" in route_df.columns
    ):

        st.markdown(
            "### Average Lead Time by Region"
        )

        region_chart = (
            route_df.groupby(
                "Region"
            )["Average_Lead_Time"]
            .mean()
            .sort_values()
        )

        st.bar_chart(
            region_chart
        )


# ============================================================
# PREDICTIVE MODEL
# ============================================================

elif page == "Predictive Model":

    st.markdown(
        '<div class="section-title">Predictive Model Performance</div>',
        unsafe_allow_html=True,
    )

    st.write(
        """
        Three regression models were evaluated for predicting shipping
        lead time. Gradient Boosting Regressor was selected because it
        achieved the strongest overall performance among the tested models.
        """
    )

    st.divider()

    st.markdown(
        "### Model Comparison"
    )

    st.dataframe(
        model_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.success(
        "Selected Model: Gradient Boosting Regressor"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "R² Score",
            "0.5933"
        )

    with col2:
        st.metric(
            "MAE",
            "159.87 days"
        )

    with col3:
        st.metric(
            "RMSE",
            "169.59 days"
        )

    st.divider()

    feature_path = (
        ASSETS_DIR
        / "gradient_boosting_feature_importance.png"
    )

    if feature_path.exists():

        st.markdown(
            "### Feature Importance"
        )

        st.image(
            str(feature_path),
            use_container_width=True
        )

    st.info(
        "The model shows strong dependence on temporal variables, "
        "especially Order Year. Therefore, predictions should be "
        "interpreted as model-based estimates rather than causal "
        "measurements of factory performance."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Nassau Candy Factory Reallocation & Shipping Optimization "
    "| Unified Mentor Internship Project"
)