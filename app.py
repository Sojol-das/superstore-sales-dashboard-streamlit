import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# ── Global Chart Font Settings
pio.templates["custom"] = pio.templates["plotly_white"]
pio.templates["custom"].layout.update(
    font=dict(family="Arial", size=14, color="#1a1a2e"),
    title_font=dict(size=18, color="#1a1a2e", family="Arial"),
    xaxis=dict(
        tickfont=dict(size=16, color="black"),
        title_font=dict(size=18, color="black"),
        gridcolor='#f0f0f0'
    ),
    yaxis=dict(
        tickfont=dict(size=16, color="black"),
        title_font=dict(size=18, color="black"),
        gridcolor='#f0f0f0'
    ),
    legend=dict(font=dict(size=16, color="black")),
    coloraxis_colorbar=dict(
        tickfont=dict(size=16, color="black"),
        title_font=dict(size=18, color="black")
    )
)
pio.templates.default = "custom"

# ── Color Palette (Professional Blue Theme)
PRIMARY   = "#1B4F72"   # Deep navy blue  → main color
SECONDARY = "#2E86C1"   # Medium blue     → charts
ACCENT    = "#27AE60"   # Green           → profit / positive
NEGATIVE  = "#C0392B"   # Red             → ONLY for losses
LIGHT     = "#D6EAF8"   # Light blue      → backgrounds
GRAY      = "#566573"   # Dark gray       → secondary text
COLORS    = ["#1B4F72", "#2E86C1", "#27AE60", "#F39C12", "#8E44AD"]

# ── Page Config
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Month'] = df['Order Date'].dt.strftime('%b')
    df['Month_Num'] = df['Order Date'].dt.month
    df['Year'] = df['Order Date'].dt.year

    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
    }
    df['State_Code'] = df['State'].map(state_abbrev)
    return df

df = load_data()

# ── Custom CSS
st.markdown(f"""
<style>
    .main {{ background-color: #f4f6f9; }}
    [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: {PRIMARY} !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: {GRAY} !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-size: 0.9rem !important;
    }}
    h1, h2, h3, h4 {{ color: {PRIMARY}; }}
    .stMultiSelect span {{ background-color: {SECONDARY} !important; }}
</style>
""", unsafe_allow_html=True)

# ── Title
st.markdown(f"""
<h1 style='text-align:center; color:{PRIMARY}; font-size:2.3rem; font-weight:800;'>
📊 Superstore Sales Performance Dashboard
</h1>
<p style='text-align:center; color:{GRAY}; margin-top:-10px; font-size:1rem;'>
Interactive analysis of sales, profit, and customer trends
</p>
<hr style='border:2px solid {SECONDARY}; margin-top:5px;'>
""", unsafe_allow_html=True)

# ── Sidebar Filters
st.sidebar.markdown(f"<h2 style='color:{PRIMARY};'>🔍 Filter Data</h2>",
    unsafe_allow_html=True)
st.sidebar.markdown("---")

year_options   = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("📅 Year",
    options=year_options, default=year_options)

region   = st.sidebar.multiselect("🌍 Region",
    options=df['Region'].unique(), default=df['Region'].unique())

segment  = st.sidebar.multiselect("👥 Segment",
    options=df['Segment'].unique(), default=df['Segment'].unique())

category = st.sidebar.multiselect("📦 Category",
    options=df['Category'].unique(), default=df['Category'].unique())

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"<p style='color:{GRAY}; font-size:0.85rem;'>Dashboard by <b>Sojol Das</b><br>"
    "Data Analysis & AI/ML Freelancer</p>",
    unsafe_allow_html=True)

# ── Apply Filters
df_filtered = df[
    (df['Year'].isin(selected_years)) &
    (df['Region'].isin(region)) &
    (df['Segment'].isin(segment)) &
    (df['Category'].isin(category))
]

# ── KPI Cards
st.markdown("### 📋 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_sales   = df_filtered['Sales'].sum()
total_profit  = df_filtered['Profit'].sum()
total_qty     = df_filtered['Quantity'].sum()
total_orders  = df_filtered['Order ID'].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

with col1:
    st.metric("💰 Total Sales",   f"${total_sales:,.0f}")
with col2:
    st.metric("📈 Total Profit",  f"${total_profit:,.0f}")
with col3:
    st.metric("📦 Total Quantity", f"{total_qty:,}")
with col4:
    st.metric("🧾 Total Orders",  f"{total_orders:,}")

# ── Info Banner
st.markdown(f"""
<div style='background:linear-gradient(90deg, {PRIMARY}, {SECONDARY});
     padding:12px 20px; border-radius:8px; margin:12px 0;'>
  <span style='color:white; font-size:1rem; font-weight:600;'>
  📊 Profit Margin: {profit_margin:.1f}% &nbsp;|&nbsp;
  📅 Years: {min(selected_years)} – {max(selected_years)} &nbsp;|&nbsp;
  🌍 Regions Selected: {len(region)}
  </span>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #dde;'>", unsafe_allow_html=True)

# ── Row 1: Line Chart + Donut Chart
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### 📈 Monthly Sales Trend")
    monthly = (df_filtered
               .groupby(['Month_Num', 'Month'])['Sales']
               .sum().reset_index()
               .sort_values('Month_Num'))
    fig1 = px.line(monthly, x='Month', y='Sales',
        markers=True, line_shape='spline',
        color_discrete_sequence=[SECONDARY])
    fig1.update_traces(
        line=dict(width=3),
        marker=dict(size=9, color=PRIMARY))
    fig1.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis_title="Month", yaxis_title="Sales ($)",
        hovermode='x unified',
        xaxis=dict(showgrid=False,
                   tickfont=dict(size=13, color='#1a1a2e')),
        yaxis=dict(gridcolor='#f0f0f0',
                   tickfont=dict(size=13, color='#1a1a2e')))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### 🍩 Sales by Category")
    cat_sales = df_filtered.groupby('Category')['Sales'].sum().reset_index()
    fig2 = px.pie(cat_sales, names='Category', values='Sales',
        hole=0.55,
        color_discrete_sequence=COLORS)
    fig2.update_traces(
        textposition='outside',
        textinfo='percent+label',
        textfont=dict(size=14, color='#1a1a2e'))
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        showlegend=False,
        margin=dict(t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Bar Chart + Scatter
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Profit by Sub-Category")
    sub_profit = (df_filtered.groupby('Sub-Category')['Profit']
                  .sum().reset_index().sort_values('Profit'))
    # Green for positive, red ONLY for negative — correct usage!
    fig3 = px.bar(sub_profit, x='Profit', y='Sub-Category',
        orientation='h', color='Profit',
        color_continuous_scale=[NEGATIVE, '#f5f5f5', ACCENT],
        color_continuous_midpoint=0)
    fig3.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0',
                   tickfont=dict(size=13, color='#1a1a2e')),
        yaxis=dict(showgrid=False,
                   tickfont=dict(size=13, color='#1a1a2e')))
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("#### 📉 Discount vs Profit Impact")
    fig4 = px.scatter(df_filtered, x='Discount', y='Profit',
        color='Category', size='Sales',
        hover_data=['Sub-Category', 'Region'],
        color_discrete_sequence=COLORS,
        opacity=0.7)
    fig4.add_hline(y=0, line_dash='dash',
        line_color=NEGATIVE, opacity=0.6,
        annotation_text="Break-even",
        annotation_font=dict(size=13, color=NEGATIVE))
    fig4.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0',
                   tickfont=dict(size=13, color='#1a1a2e')),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0',
                   tickfont=dict(size=13, color='#1a1a2e')),
        legend=dict(font=dict(size=13, color='#1a1a2e')))
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Map + Segment Chart
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🗺️ Sales by State")
    state_sales = (df_filtered
                   .groupby(['State', 'State_Code'])['Sales']
                   .sum().reset_index())
    fig5 = px.choropleth(state_sales,
        locations='State_Code',
        locationmode='USA-states',
        color='Sales',
        scope='usa',
        hover_name='State',
        color_continuous_scale='Blues',
        labels={'Sales': 'Total Sales ($)'})
    fig5.update_layout(
        paper_bgcolor='white',
        geo=dict(bgcolor='white'),
        margin=dict(t=0, b=0),
        coloraxis_colorbar=dict(
            tickfont=dict(size=12, color='#1a1a2e'),
            title_font=dict(size=13, color='#1a1a2e')))
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.markdown("#### 👥 Sales by Customer Segment")
    seg_sales = (df_filtered
                 .groupby(['Segment', 'Category'])['Sales']
                 .sum().reset_index())
    fig6 = px.bar(seg_sales, x='Segment', y='Sales',
        color='Category', barmode='stack',
        color_discrete_sequence=COLORS,
        text_auto='.2s')
    fig6.update_traces(textfont=dict(size=13, color='white'))
    fig6.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False,
                   tickfont=dict(size=13, color='#1a1a2e')),
        yaxis=dict(gridcolor='#f0f0f0',
                   tickfont=dict(size=13, color='#1a1a2e')),
        legend=dict(
            font=dict(size=13, color='#1a1a2e'),
            orientation='h', yanchor='bottom',
            y=1.02, xanchor='right', x=1))
    st.plotly_chart(fig6, use_container_width=True)

# ── Year-wise Sales & Profit
st.markdown("<hr style='border:1px solid #dde;'>", unsafe_allow_html=True)
st.markdown("#### 📅 Year-wise Sales & Profit Comparison")
yearly = (df_filtered.groupby('Year')
          .agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum'))
          .reset_index())
fig7 = px.bar(yearly, x='Year', y=['Sales', 'Profit'],
    barmode='group',
    color_discrete_sequence=[SECONDARY, ACCENT],
    text_auto='.2s')
fig7.update_traces(textfont=dict(size=13, color='white'))
fig7.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    xaxis=dict(showgrid=False, type='category',
               tickfont=dict(size=13, color='#1a1a2e')),
    yaxis=dict(gridcolor='#f0f0f0',
               tickfont=dict(size=13, color='#1a1a2e')),
    legend=dict(
        font=dict(size=13, color='#1a1a2e'),
        orientation='h', yanchor='bottom',
        y=1.02, xanchor='right', x=1))
st.plotly_chart(fig7, use_container_width=True)

# ── Top 10 Products Table
st.markdown("<hr style='border:1px solid #dde;'>", unsafe_allow_html=True)
st.markdown("#### 🏆 Top 10 Products by Sales")
top_products = (df_filtered.groupby('Product Name')
                .agg(Sales=('Sales', 'sum'),
                     Profit=('Profit', 'sum'),
                     Orders=('Order ID', 'count'))
                .reset_index()
                .sort_values('Sales', ascending=False)
                .head(10))
top_products['Sales']  = top_products['Sales'].map('${:,.2f}'.format)
top_products['Profit'] = top_products['Profit'].map('${:,.2f}'.format)
st.dataframe(top_products, use_container_width=True, hide_index=True)

# ── Footer
st.markdown("<hr style='border:1px solid #dde;'>", unsafe_allow_html=True)
st.markdown(f"""
<p style='text-align:center; color:{GRAY}; font-size:0.9rem;'>
📊 Superstore Sales Dashboard &nbsp;|&nbsp;
Built by <strong style='color:{PRIMARY};'>Sojol Das</strong> &nbsp;|&nbsp;
Data Analysis & AI/ML 
</p>
""", unsafe_allow_html=True)