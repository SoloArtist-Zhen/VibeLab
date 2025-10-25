import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

st.set_page_config(page_title="Mass–Spring–Damper", page_icon="🌀", layout="wide")

st.title("🌀 Mass–Spring–Damper Explorer")

with st.sidebar:
    st.header("Parameters")
    m = st.slider("Mass m [kg]", 0.1, 10.0, 1.0, 0.1)
    k = st.slider("Stiffness k [N/m]", 10.0, 2000.0, 200.0, 10.0)
    zeta = st.slider("Damping ratio ζ", 0.0, 1.0, 0.08, 0.01)
    ftype = st.selectbox("Excitation", ["Step (F0)", "Sine (F0·sin ωt)", "None (free)"])
    F0 = st.slider("F0 [N]", 0.0, 50.0, 5.0, 0.5)
    omega = st.slider("ω [rad/s] (for sine)", 0.0, 80.0, 15.0, 0.5)
    x0 = st.slider("x(0) [m]", -0.1, 0.1, 0.0, 0.005)
    v0 = st.slider("ẋ(0) [m/s]", -0.5, 0.5, 0.0, 0.01)
    t_end = st.slider("Simulation time [s]", 2.0, 30.0, 10.0, 1.0)
    export = st.checkbox("Enable PNG export")

c = 2*zeta*np.sqrt(k*m)

def forcing(t):
    if ftype == "Step (F0)":
        return F0
    elif ftype == "Sine (F0·sin ωt)":
        return F0*np.sin(omega*t)
    else:
        return 0.0

def ode(t, y):
    x, v = y
    dxdt = v
    dvdt = (forcing(t) - c*v - k*x)/m
    return [dxdt, dvdt]

t_eval = np.linspace(0, t_end, 1200)
sol = solve_ivp(ode, [0, t_end], [x0, v0], t_eval=t_eval, rtol=1e-7, atol=1e-9)
t = sol.t
x = sol.y[0]
v = sol.y[1]

# --- Time history
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=t, y=x, mode="lines", name="x [m]"))
fig1.add_trace(go.Scatter(x=t, y=v, mode="lines", name="ẋ [m/s]", yaxis="y2"))
fig1.update_layout(
    title="Time Response",
    xaxis_title="Time [s]",
    yaxis=dict(title="Displacement x [m]"),
    yaxis2=dict(title="Velocity ẋ [m/s]", overlaying="y", side="right"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# --- Phase portrait
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x, y=v, mode="lines", name="Phase"))
fig2.update_layout(title="Phase Portrait", xaxis_title="x [m]", yaxis_title="ẋ [m/s]")

# --- Animation (mass on spring)
A = max(0.15, 0.6*max(1e-6, np.max(np.abs(x))))
frames = []
for i in range(0, len(t), 8):
    mx = float(x[i])
    frames.append(go.Frame(
        data=[
            go.Scatter(x=[-A, A], y=[0, 0], mode="lines", line=dict(width=6), showlegend=False),
            go.Scatter(x=[mx], y=[0.05], mode="markers", marker=dict(size=30), showlegend=False),
        ],
        name=f"f{i}"
    ))

fig3 = go.Figure(
    data=[
        go.Scatter(x=[-A, A], y=[0, 0], mode="lines", line=dict(width=6), showlegend=False),
        go.Scatter(x=[x[0]], y=[0.05], mode="markers", marker=dict(size=30), showlegend=False),
    ],
    frames=frames
)
fig3.update_layout(
    title="Animated Mass Motion",
    xaxis=dict(range=[-A*1.2, A*1.2], title="Position [m]"),
    yaxis=dict(range=[-0.2, 0.3], visible=False),
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]},
            {"label": "Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]}
        ]
    }]
)

col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

st.plotly_chart(fig3, use_container_width=True)

if export:
    import plotly.io as pio
    st.download_button("Download Time Response (PNG)", data=pio.to_image(fig1, format="png", scale=2), file_name="time_response.png")
    st.download_button("Download Phase Portrait (PNG)", data=pio.to_image(fig2, format="png", scale=2), file_name="phase_portrait.png")
