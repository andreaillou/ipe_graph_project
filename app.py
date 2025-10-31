import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Economic Indicators Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
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

# Sidebar
st.sidebar.header("📈 Dashboard Controls")
st.sidebar.markdown("---")

# Date range selector
min_year = gdp_df['Date'].dt.year.min()
max_year = gdp_df['Date'].dt.year.max()

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(min_year),
    max_value=int(max_year),
    value=(int(min_year), int(max_year))
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

# Visualization type selector
st.sidebar.markdown("---")
viz_type = st.sidebar.radio(
    "Select Visualization Type",
    ["Combined View (Dual Axis)", "Separate Subplots", "Individual Metrics"]
)

# Show annotations toggle
show_annotations = st.sidebar.checkbox("Show Event Annotations", value=True)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Hover over the charts to see detailed values. Use the toolbar to zoom, pan, or download the charts.")

# Key metrics
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    latest_gdp = gdp_filtered['GDP per Capita'].iloc[-1]
    st.metric(
        label="Latest GDP per Capita",
        value=f"${latest_gdp:,.2f}",
        delta=f"{((latest_gdp / gdp_filtered['GDP per Capita'].iloc[0] - 1) * 100):.1f}% since {year_range[0]}"
    )

with col2:
    latest_inflation = inflation_filtered['Inflation Rate'].iloc[-1]
    st.metric(
        label="Latest Inflation Rate",
        value=f"{latest_inflation:.2f}%",
        delta=f"{(latest_inflation - inflation_filtered['Inflation Rate'].iloc[0]):.2f}pp since {year_range[0]}"
    )

with col3:
    avg_gdp_growth = ((gdp_filtered['GDP per Capita'].iloc[-1] / gdp_filtered['GDP per Capita'].iloc[0]) ** (1 / len(gdp_filtered)) - 1) * 100
    st.metric(
        label="Avg Annual GDP Growth",
        value=f"{avg_gdp_growth:.2f}%"
    )

with col4:
    avg_inflation = inflation_filtered['Inflation Rate'].mean()
    st.metric(
        label="Average Inflation",
        value=f"{avg_inflation:.2f}%"
    )

st.markdown("---")

# Visualization
if viz_type == "Combined View (Dual Axis)":
    st.markdown("### 📈 GDP per Capita vs Inflation Rate")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # GDP trace
    fig.add_trace(
        go.Scatter(
            x=gdp_filtered['Date'],
            y=gdp_filtered['GDP per Capita'],
            name='GDP per Capita',
            mode='lines+markers',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=7),
            hovertemplate='<b>Date:</b> %{x|%Y}<br>' +
                          '<b>GDP per Capita:</b> $%{y:,.2f}<br>' +
                          '<extra></extra>'
        ),
        secondary_y=False
    )
    
    # Inflation trace
    fig.add_trace(
        go.Scatter(
            x=inflation_filtered['Date'],
            y=inflation_filtered['Inflation Rate'],
            name='Inflation Rate',
            mode='lines+markers',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=7),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.1)',
            hovertemplate='<b>Date:</b> %{x|%Y}<br>' +
                          '<b>Inflation Rate:</b> %{y:.2f}%<br>' +
                          '<extra></extra>'
        ),
        secondary_y=True
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_xaxes(title_text="Year", showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(title_text="<b>GDP per Capita ($)</b>", secondary_y=False, showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(title_text="<b>Inflation Rate (%)</b>", secondary_y=True, showgrid=False)
    
    if show_annotations and year_range[0] <= 2008 <= year_range[1]:
        fig.add_annotation(
            x='2008-01-01', y=27449,
            text='2008 Financial Crisis',
            showarrow=True, arrowhead=2,
            ax=-50, ay=-40,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='red'
        )
    
    if show_annotations and year_range[0] <= 2020 <= year_range[1]:
        fig.add_annotation(
            x='2020-01-01', y=27391,
            text='COVID-19 Pandemic',
            showarrow=True, arrowhead=2,
            ax=50, ay=-40,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='red'
        )
    
    if show_annotations and year_range[0] <= 2022 <= year_range[1]:
        fig.add_annotation(
            x='2022-01-01', y=8.4, yref='y2',
            text='High Inflation',
            showarrow=True, arrowhead=2,
            ax=0, ay=-60,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='orange'
        )
    
    fig.update_layout(
        height=600,
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif viz_type == "Separate Subplots":
    st.markdown("### 📈 Economic Indicators Overview")
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('GDP per Capita', 'Inflation Rate'),
        vertical_spacing=0.12
    )
    
    fig.add_trace(
        go.Scatter(
            x=gdp_filtered['Date'],
            y=gdp_filtered['GDP per Capita'],
            name='GDP per Capita',
            mode='lines+markers',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6),
            hovertemplate='<b>Date:</b> %{x|%Y}<br><b>GDP per Capita:</b> $%{y:,.2f}<br><extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=inflation_filtered['Date'],
            y=inflation_filtered['Inflation Rate'],
            name='Inflation Rate',
            mode='lines+markers',
            line=dict(color='#ff7f0e', width=2),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(255, 127, 14, 0.1)',
            hovertemplate='<b>Date:</b> %{x|%Y}<br><b>Inflation Rate:</b> %{y:.2f}%<br><extra></extra>'
        ),
        row=2, col=1
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=2, col=1)
    
    fig.update_xaxes(title_text="Year", showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(title_text="GDP per Capita ($)", row=1, col=1, showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(title_text="Inflation Rate (%)", row=2, col=1, showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    fig.update_layout(
        height=800,
        hovermode='x unified',
        showlegend=True,
        plot_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:  # Individual Metrics
    tab1, tab2 = st.tabs(["💰 GDP per Capita", "📈 Inflation Rate"])
    
    with tab1:
        st.markdown("### GDP per Capita Over Time")
        
        fig_gdp = go.Figure()
        fig_gdp.add_trace(
            go.Scatter(
                x=gdp_filtered['Date'],
                y=gdp_filtered['GDP per Capita'],
                mode='lines+markers',
                line=dict(color='#2ecc71', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(46, 204, 113, 0.1)',
                hovertemplate='<b>Year:</b> %{x|%Y}<br><b>GDP per Capita:</b> $%{y:,.2f}<br><extra></extra>'
            )
        )
        
        fig_gdp.update_layout(
            height=500,
            xaxis_title="Year",
            yaxis_title="GDP per Capita ($)",
            plot_bgcolor='white',
            showgrid=True,
            hovermode='x'
        )
        
        st.plotly_chart(fig_gdp, use_container_width=True)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Minimum", f"${gdp_filtered['GDP per Capita'].min():,.2f}")
        with col2:
            st.metric("Maximum", f"${gdp_filtered['GDP per Capita'].max():,.2f}")
        with col3:
            st.metric("Average", f"${gdp_filtered['GDP per Capita'].mean():,.2f}")
    
    with tab2:
        st.markdown("### Inflation Rate Over Time")
        
        fig_inflation = go.Figure()
        fig_inflation.add_trace(
            go.Scatter(
                x=inflation_filtered['Date'],
                y=inflation_filtered['Inflation Rate'],
                mode='lines+markers',
                line=dict(color='#e74c3c', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(231, 76, 60, 0.1)',
                hovertemplate='<b>Year:</b> %{x|%Y}<br><b>Inflation Rate:</b> %{y:.2f}%<br><extra></extra>'
            )
        )
        
        fig_inflation.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig_inflation.update_layout(
            height=500,
            xaxis_title="Year",
            yaxis_title="Inflation Rate (%)",
            plot_bgcolor='white',
            showgrid=True,
            hovermode='x'
        )
        
        st.plotly_chart(fig_inflation, use_container_width=True)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Minimum", f"{inflation_filtered['Inflation Rate'].min():.2f}%")
        with col2:
            st.metric("Maximum", f"{inflation_filtered['Inflation Rate'].max():.2f}%")
        with col3:
            st.metric("Average", f"{inflation_filtered['Inflation Rate'].mean():.2f}%")

# Data table
st.markdown("---")
with st.expander("📋 View Raw Data"):
    tab1, tab2 = st.tabs(["GDP per Capita", "Inflation Rate"])
    
    with tab1:
        st.dataframe(
            gdp_filtered.style.format({'GDP per Capita': '${:,.2f}'}),
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        st.dataframe(
            inflation_filtered.style.format({'Inflation Rate': '{:.2f}%'}),
            use_container_width=True,
            hide_index=True
        )

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
