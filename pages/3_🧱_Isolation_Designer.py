import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Isolation Designer", page_icon="🧱", layout="wide")
st.title("🧱 Vibration Isolation Designer")

with st.sidebar:
    st.header("Parameters")
    zeta = st.slider("Damping ratio ζ", 0.0, 0.9, 0.08, 0.01)
    freq_ratio = st.slider("Frequency ratio range (max r=ω/ωn)", 2.0, 10.0, 5.0, 0.5)
    animate = st.checkbox("Show base‑excitation animation", True)

r = np.linspace(0.01, freq_ratio, 1000)
T = np.sqrt((1 + (2*zeta*r)**2) / ((1 - r**2)**2 + (2*zeta*r)**2))

fig = go.Figure()
fig.add_trace(go.Scatter(x=r, y=T, mode="lines", name="Transmissibility T"))
fig.add_vline(x=np.sqrt(2), line_dash="dash", annotation_text="r=√2 (start of isolation)")
fig.update_layout(title="Transmissibility Curve T(r, ζ)", xaxis_title="r = ω/ωₙ", yaxis_title="T")

st.plotly_chart(fig, use_container_width=True)

st.info("经验法则：当激励频率 ω 至少高于固有频率 ωₙ 的 √2 倍时（r>√2），隔振才明显。阻尼并非越大越好：增大阻尼可降低共振峰，但会略抬高高频段的传递率。")

if animate:
    # simple animation: base (sine) vs mass response (illustrative)
    A_base = 0.02
    t = np.linspace(0, 6, 300)
    x_base = A_base*np.sin(6*np.pi*t)
    x_mass = 0.4*A_base*np.sin(6*np.pi*t - 0.8)  # phase lag + reduced amplitude
    frames = []
    for i in range(0, len(t), 3):
        frames.append(go.Frame(data=[
            go.Scatter(x=[x_base[i], x_base[i]], y=[0, 1], mode="lines", line=dict(width=6)),
            go.Scatter(x=[x_mass[i]], y=[0.5], mode="markers", marker=dict(size=28)),
        ]))
    fig2 = go.Figure(
        data=[
            go.Scatter(x=[x_base[0], x_base[0]], y=[0, 1], mode="lines", line=dict(width=6), showlegend=False),
            go.Scatter(x=[x_mass[0]], y=[0.5], mode="markers", marker=dict(size=28), showlegend=False),
        ],
        frames=frames
    )
    fig2.update_layout(title="Base‑Excited Isolator (Animation)",
        xaxis=dict(range=[-0.04,0.04], title="Displacement [m]"),
        yaxis=dict(range=[0,1], visible=False),
        updatemenus=[{"type":"buttons","buttons":[
            {"label":"Play","method":"animate","args":[None,{"frame":{"duration":40,"redraw":True},"fromcurrent":True}]},
            {"label":"Pause","method":"animate","args":[[None],{"frame":{"duration":0,"redraw":False},"mode":"immediate"}]}
        ]}]
    )
    st.plotly_chart(fig2, use_container_width=True)
