import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Cyprus Economic Indicators | International Political Economy",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 Economic Indicators Dashboard</h1>', unsafe_allow_html=True)
st.markdown("**Interactive visualization of GDP per Capita and Inflation Rate (2000-2024)**")

# Load data
@st.cache_data
def load_data():
    inflation_df = pd.read_csv('data/inflation_01012000-01012024.csv')
    gdp_df = pd.read_csv('data/gdp_per_capita_01012000-01012024.csv')
    
    inflation_df['Date'] = pd.to_datetime(inflation_df['Date'])
    gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])
    
    return inflation_df, gdp_df

inflation_df, gdp_df = load_data()

# Year range selector
min_year = gdp_df['Date'].dt.year.min()
max_year = gdp_df['Date'].dt.year.max()

st.markdown("### 📅 Select Year Range")
year_range = st.slider(
    "Year Range",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year)),
    label_visibility="collapsed"
)

# Filter data based on year range
gdp_filtered = gdp_df[
    (gdp_df['Date'].dt.year >= year_range[0]) & 
    (gdp_df['Date'].dt.year <= year_range[1])
]
inflation_filtered = inflation_df[
    (inflation_df['Date'].dt.year >= year_range[0]) & 
    (inflation_df['Date'].dt.year <= year_range[1])
]

# Key metrics
st.markdown("### 📊 Latest Metrics")
col1, col2 = st.columns(2)

with col1:
    latest_gdp = gdp_filtered['GDP per Capita'].iloc[-1]
    st.metric(
        label="GDP per Capita (Latest)",
        value=f"${latest_gdp:,.2f}",
        delta=f"{((latest_gdp / gdp_filtered['GDP per Capita'].iloc[0] - 1) * 100):.1f}% since {year_range[0]}"
    )

with col2:
    latest_inflation = inflation_filtered['Inflation Rate'].iloc[-1]
    st.metric(
        label="Inflation Rate (Latest)",
        value=f"{latest_inflation:.2f}%",
        delta=f"{(latest_inflation - inflation_filtered['Inflation Rate'].iloc[0]):.2f}pp since {year_range[0]}"
    )

st.markdown("---")

# Visualization - Two separate graphs
st.markdown("### 📈 GDP per Capita")

fig_gdp = go.Figure()
fig_gdp.add_trace(
    go.Scatter(
        x=gdp_filtered['Date'],
        y=gdp_filtered['GDP per Capita'],
        mode='lines+markers',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.1)',
        hovertemplate='<b>Year:</b> %{x|%Y}<br><b>GDP per Capita:</b> $%{y:,.2f}<br><extra></extra>'
    )
)

fig_gdp.update_layout(
    height=400,
    plot_bgcolor='white',
    hovermode='x',
    font=dict(family="Arial, sans-serif", size=12)
)

fig_gdp.update_xaxes(
    title_text="Year",
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray'
)

fig_gdp.update_yaxes(
    title_text="GDP per Capita ($)",
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray'
)

st.plotly_chart(fig_gdp, use_container_width=True)

st.markdown("### 📉 Inflation Rate")

fig_inflation = go.Figure()
fig_inflation.add_trace(
    go.Scatter(
        x=inflation_filtered['Date'],
        y=inflation_filtered['Inflation Rate'],
        mode='lines+markers',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.1)',
        hovertemplate='<b>Year:</b> %{x|%Y}<br><b>Inflation Rate:</b> %{y:.2f}%<br><extra></extra>'
    )
)

fig_inflation.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

fig_inflation.update_layout(
    height=400,
    plot_bgcolor='white',
    hovermode='x',
    font=dict(family="Arial, sans-serif", size=12)
)

fig_inflation.update_xaxes(
    title_text="Year",
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray'
)

fig_inflation.update_yaxes(
    title_text="Inflation Rate (%)",
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray'
)

st.plotly_chart(fig_inflation, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
        <p>📊 Economic Indicators Dashboard | Data Period: 2000-2024</p>
        <p style='font-size: 0.8rem;'>Built with Streamlit & Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)
