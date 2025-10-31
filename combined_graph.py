import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the datasets
inflation_df = pd.read_csv('data/inflation_01012000-01012024.csv')
gdp_df = pd.read_csv('data/gdp_per_capita_01012000-01012024.csv')

# Convert date columns to datetime
inflation_df['Date'] = pd.to_datetime(inflation_df['Date'])
gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add GDP per Capita trace on primary y-axis
fig.add_trace(
    go.Scatter(
        x=gdp_df['Date'],
        y=gdp_df['GDP per Capita'],
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

# Add Inflation Rate trace on secondary y-axis
fig.add_trace(
    go.Scatter(
        x=inflation_df['Date'],
        y=inflation_df['Inflation Rate'],
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

# Add horizontal line at y=0 for inflation
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

# Set x-axis title
fig.update_xaxes(title_text="Year", showgrid=True, gridwidth=1, gridcolor='LightGray')

# Set y-axes titles
fig.update_yaxes(
    title_text="<b>GDP per Capita ($)</b>", 
    secondary_y=False,
    showgrid=True,
    gridwidth=1,
    gridcolor='LightGray'
)
fig.update_yaxes(
    title_text="<b>Inflation Rate (%)</b>", 
    secondary_y=True,
    showgrid=False
)

# Update layout
fig.update_layout(
    title={
        'text': 'Economic Indicators: GDP per Capita vs Inflation Rate (2000-2024)',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 22, 'color': '#2c3e50', 'family': 'Arial Black'}
    },
    height=700,
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="gray",
        borderwidth=1
    ),
    plot_bgcolor='white',
    font=dict(family="Arial, sans-serif", size=12)
)

# Add annotations for key events
annotations = [
    dict(
        x='2008-01-01',
        y=27449,
        xref='x',
        yref='y',
        text='2008 Financial Crisis',
        showarrow=True,
        arrowhead=2,
        ax=-50,
        ay=-40,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='red'
    ),
    dict(
        x='2020-01-01',
        y=27391,
        xref='x',
        yref='y',
        text='COVID-19 Pandemic',
        showarrow=True,
        arrowhead=2,
        ax=50,
        ay=-40,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='red'
    ),
    dict(
        x='2022-01-01',
        y=8.4,
        xref='x',
        yref='y2',
        text='High Inflation',
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-60,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='orange'
    )
]

fig.update_layout(annotations=annotations)

# Show the interactive plot
fig.show()

# Save as HTML file
fig.write_html('combined_economic_graph.html')
print("Combined interactive graph has been created!")
print("Opening in browser... (also saved as 'combined_economic_graph.html')")
