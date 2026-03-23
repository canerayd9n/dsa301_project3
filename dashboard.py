import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Japan Immigration Dashboard", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
            background-color: #0d0d0d;
            color: #f0ede6;
        }
        .stApp { background-color: #0d0d0d; }
        h1, h2, h3 { font-family: 'Shippori Mincho', serif; color: #f0ede6; }
        .block-container { padding: 2rem 3rem; }
        .stMultiSelect > label { color: #a89f8c !important; font-size: 0.8rem; letter-spacing: 0.12em; text-transform: uppercase; }
        div[data-baseweb="tag"] { background-color: #c0392b !important; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='font-size:2.6rem; margin-bottom:0'>日本の移民統計</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a89f8c; font-size:0.95rem; letter-spacing:0.06em; margin-top:0.2rem'>Japan Inbound Immigration Trends</p>", unsafe_allow_html=True)
st.markdown("<hr style='border:none; border-top:1px solid #2a2a2a; margin:1.2rem 0 2rem'>", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("japan_immigration_statistics_inbound.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

CONTINENTS = ["asia", "europe", "africa", "north_america", "south_america", "oceania"]
available = [c for c in CONTINENTS if c in df.columns]

COLORS = {
    "asia":          "#e05c3a",
    "europe":        "#5b8fcc",
    "africa":        "#e8b84b",
    "north_america": "#7dbf8e",
    "south_america": "#b07fc7",
    "oceania":       "#d07aaa",
}

# --- Controls ---
col_sel, col_total = st.columns([3, 1])
with col_sel:
    selected = st.multiselect(
        "Select continents to display",
        options=available,
        default=available,
        format_func=lambda x: x.replace("_", " ").title()
    )
with col_total:
    show_total = st.checkbox("Show Total", value=True)

# --- Chart ---
fig = go.Figure()

if show_total and "total" in df.columns:
    fig.add_trace(go.Scatter(
        x=df["year"], y=df["total"],
        name="Total",
        line=dict(color="#f0ede6", width=2.5, dash="dot"),
        mode="lines+markers",
        marker=dict(size=5),
    ))

for continent in selected:
    fig.add_trace(go.Scatter(
        x=df["year"], y=df[continent],
        name=continent.replace("_", " ").title(),
        line=dict(color=COLORS.get(continent, "#888"), width=2),
        mode="lines+markers",
        marker=dict(size=5),
        hovertemplate=f"<b>{continent.replace('_',' ').title()}</b><br>Year: %{{x}}<br>Count: %{{y:,}}<extra></extra>"
    ))

fig.update_layout(
    plot_bgcolor="#0d0d0d",
    paper_bgcolor="#0d0d0d",
    font=dict(family="DM Sans", color="#a89f8c", size=12),
    xaxis=dict(
        showgrid=False, zeroline=False,
        tickcolor="#2a2a2a", linecolor="#2a2a2a",
        title=dict(text="Year", font=dict(color="#a89f8c"))
    ),
    yaxis=dict(
        gridcolor="#1e1e1e", zeroline=False,
        tickcolor="#2a2a2a", linecolor="#2a2a2a",
        title=dict(text="Number of Immigrants", font=dict(color="#a89f8c"))
    ),
    legend=dict(
        bgcolor="#161616", bordercolor="#2a2a2a", borderwidth=1,
        font=dict(color="#f0ede6"), orientation="v"
    ),
    hovermode="x unified",
    margin=dict(l=20, r=20, t=20, b=20),
    height=500,
)

st.plotly_chart(fig, use_container_width=True)

# --- Summary Stats ---
if selected:
    st.markdown("<h3 style='font-size:1rem; color:#a89f8c; letter-spacing:0.1em; text-transform:uppercase; margin-top:2rem'>Summary Statistics</h3>", unsafe_allow_html=True)
    summary_cols = ["year"] + selected + (["total"] if show_total and "total" in df.columns else [])
    display_df = df[summary_cols].copy()
    display_df.columns = [c.replace("_", " ").title() for c in display_df.columns]
    st.dataframe(display_df.set_index("Year"), use_container_width=True)
