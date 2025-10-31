import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the datasets
inflation_df = pd.read_csv('data/inflation_01012000-01012024.csv')
gdp_df = pd.read_csv('data/gdp_per_capita_01012000-01012024.csv')

# Convert date columns to datetime
inflation_df['Date'] = pd.to_datetime(inflation_df['Date'])
gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])

# Create subplots with secondary y-axis
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=('GDP per Capita (2000-2024)', 'Inflation Rate (2000-2024)'),
    vertical_spacing=0.12,
    specs=[[{"secondary_y": False}],
           [{"secondary_y": False}]]
)

# Add GDP per Capita trace
fig.add_trace(
    go.Scatter(
        x=gdp_df['Date'],
        y=gdp_df['GDP per Capita'],
        name='GDP per Capita',
        mode='lines+markers',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6),
        hovertemplate='<b>Date:</b> %{x|%Y}<br>' +
                      '<b>GDP per Capita:</b> $%{y:,.2f}<br>' +
                      '<extra></extra>'
    ),
    row=1, col=1
)

# Add Inflation Rate trace
fig.add_trace(
    go.Scatter(
        x=inflation_df['Date'],
        y=inflation_df['Inflation Rate'],
        name='Inflation Rate',
        mode='lines+markers',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(255, 127, 14, 0.1)',
        hovertemplate='<b>Date:</b> %{x|%Y}<br>' +
                      '<b>Inflation Rate:</b> %{y:.2f}%<br>' +
                      '<extra></extra>'
    ),
    row=2, col=1
)

# Update x-axes
fig.update_xaxes(title_text="Year", row=1, col=1, showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_xaxes(title_text="Year", row=2, col=1, showgrid=True, gridwidth=1, gridcolor='LightGray')

# Update y-axes
fig.update_yaxes(title_text="GDP per Capita ($)", row=1, col=1, showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxes(title_text="Inflation Rate (%)", row=2, col=1, showgrid=True, gridwidth=1, gridcolor='LightGray')

# Add a horizontal line at y=0 for inflation
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5, row=2, col=1)

# Update layout
fig.update_layout(
    title={
        'text': 'Economic Indicators: GDP per Capita & Inflation Rate (2000-2024)',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20, 'color': '#2c3e50'}
    },
    height=800,
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    plot_bgcolor='white',
    font=dict(family="Arial, sans-serif", size=12)
)

# Show the interactive plot
fig.show()

# Optional: Save as HTML file
fig.write_html('interactive_economic_graph.html')
print("Interactive graph has been created!")
print("Opening in browser... (also saved as 'interactive_economic_graph.html')")
