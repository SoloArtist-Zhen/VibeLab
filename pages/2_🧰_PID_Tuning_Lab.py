import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="PID Tuning Lab", page_icon="🧰", layout="wide")
st.title("🧰 PID Tuning Lab (Plant: Mass–Spring–Damper)")

with st.sidebar:
    st.header("Plant")
    m = st.slider("Mass m [kg]", 0.1, 10.0, 1.5, 0.1)
    k = st.slider("Stiffness k [N/m]", 10.0, 2000.0, 180.0, 10.0)
    zeta = st.slider("Damping ratio ζ", 0.0, 1.0, 0.1, 0.01)
    st.header("Controller")
    Kp = st.slider("Kp", 0.0, 50.0, 10.0, 0.1)
    Ki = st.slider("Ki", 0.0, 50.0, 1.5, 0.1)
    Kd = st.slider("Kd", 0.0, 10.0, 0.8, 0.05)
    t_end = st.slider("Sim time [s]", 2.0, 30.0, 12.0, 1.0)

# Derived params
c = 2*zeta*np.sqrt(k*m)

# Discrete simulation (simple Euler)
dt = 1/300
n = int(t_end/dt)
t = np.arange(n)*dt
r = np.ones_like(t)  # unit step

x = 0.0; v = 0.0; u = 0.0
e_prev = 0.0; integ = 0.0

xs = []; us = []; es = []

for i in range(n):
    y = x  # measure displacement as output
    e = r[i] - y
    integ += e * dt
    deriv = (e - e_prev)/dt
    u = Kp*e + Ki*integ + Kd*deriv
    e_prev = e

    # plant: m*xdd + c*xd + k*x = u
    xdd = (u - c*v - k*x)/m
    v += xdd * dt
    x += v * dt

    xs.append(x); us.append(u); es.append(e)

x = np.array(xs); u = np.array(us); e = np.array(es)

# Metrics
y = x
overshoot = max(0.0, (np.max(y) - 1.0)*100)
settle_idx = np.where(np.abs(y-1.0) <= 0.02)[0]
settle_time = t[settle_idx[0]] if settle_idx.size>0 else np.nan
iae = np.trapz(np.abs(e), t)

c1, c2, c3 = st.columns(3)
c1.metric("Overshoot [%]", f"{overshoot:.1f}")
c2.metric("Settling Time [s]", f"{settle_time:.2f}" if np.isfinite(settle_time) else "—")
c3.metric("IAE", f"{iae:.3f}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y, name="Output y", mode="lines"))
fig.add_trace(go.Scatter(x=t, y=r, name="Reference r", mode="lines"))
fig.add_trace(go.Scatter(x=t, y=u, name="Control u", mode="lines", yaxis="y2"))
fig.update_layout(
    title="Closed‑loop Step Response (Displacement as Output)",
    xaxis_title="Time [s]",
    yaxis=dict(title="y / r"),
    yaxis2=dict(title="u", overlaying="y", side="right"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)
