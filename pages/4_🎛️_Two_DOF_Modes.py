import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Two‑DOF Modes", page_icon="🎛️", layout="wide")
st.title("🎛️ Two‑DOF Modes (Eigenfrequencies & Mode Shapes)")

with st.sidebar:
    st.header("Parameters")
    m1 = st.slider("m1 [kg]", 0.1, 10.0, 1.0, 0.1)
    m2 = st.slider("m2 [kg]", 0.1, 10.0, 1.0, 0.1)
    k1 = st.slider("k1 [N/m]", 10.0, 2000.0, 200.0, 10.0)
    k2 = st.slider("k2 [N/m]", 10.0, 2000.0, 300.0, 10.0)

M = np.array([[m1, 0],[0, m2]], dtype=float)
K = np.array([[k1+k2, -k2],[-k2, k2]], dtype=float)

# Solve generalized eigenproblem K phi = ω^2 M phi
w2, V = np.linalg.eig(np.linalg.inv(M)@K)
idx = np.argsort(w2)
w = np.sqrt(np.clip(w2[idx], 0, None))
V = V[:, idx]

st.write(f"**Natural frequencies (rad/s):** ω₁ = {w[0]:.3f}, ω₂ = {w[1]:.3f}")

# Normalize for nicer drawing
Vn = V / np.max(np.abs(V), axis=0, keepdims=True)

# Animation of mode 1 shape (illustrative harmonic motion of coordinates)
t = np.linspace(0, 2*np.pi, 60)
frames = []
for i, ti in enumerate(t):
    amp = np.sin(ti)
    x1 = float(Vn[0,0])*amp
    x2 = float(Vn[1,0])*amp
    frames.append(go.Frame(data=[
        go.Scatter(x=[x1], y=[0.6], mode="markers", marker=dict(size=24)),
        go.Scatter(x=[x2+1.5], y=[0.6], mode="markers", marker=dict(size=24)),
    ], name=f"f{i}"))

fig = go.Figure(
    data=[
        go.Scatter(x=[0], y=[0.6], mode="markers", marker=dict(size=24), name="m1 (mode 1)"),
        go.Scatter(x=[1.5], y=[0.6], mode="markers", marker=dict(size=24), name="m2 (mode 1)"),
    ],
    frames=frames
)
fig.update_layout(
    title="Mode 1 Animation (relative displacements)",
    xaxis=dict(range=[-1.0, 2.5], title="Relative position"),
    yaxis=dict(range=[0,1], visible=False),
    updatemenus=[{"type":"buttons","buttons":[
        {"label":"Play","method":"animate","args":[None,{"frame":{"duration":60,"redraw":True},"fromcurrent":True}]},
        {"label":"Pause","method":"animate","args":[[None],{"frame":{"duration":0,"redraw":False},"mode":"immediate"}]}
    ]}]
)

# Static bars to show eigenvectors
fig_vec = go.Figure()
fig_vec.add_trace(go.Bar(x=["m1","m2"], y=Vn[:,0], name="Mode 1"))
fig_vec.add_trace(go.Bar(x=["m1","m2"], y=Vn[:,1], name="Mode 2"))
fig_vec.update_layout(barmode="group", title="Normalized Mode Shapes (components)")

col1, col2 = st.columns(2)
col1.plotly_chart(fig, use_container_width=True)
col2.plotly_chart(fig_vec, use_container_width=True)
