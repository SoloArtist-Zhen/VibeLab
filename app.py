import streamlit as st

st.set_page_config(page_title="VibeFlow", page_icon="🧪", layout="wide")

st.title("VibeFlow · Interactive Vibration & Control Sandbox")
st.markdown('''
**VibeFlow** 是一个零门槛、工程向的交互式可视化项目：多张图 + 动画 + 即时交互。  
左侧切换模块：  
- 🌀 Mass–Spring–Damper：时域响应、相图、动态动画  
- 🧰 PID Tuning Lab：拖动 Kp/Ki/Kd 观察超调、稳态误差、整定效果  
- 🧱 Isolation Designer：传递率曲线与隔振经验法则 + 动画  
- 🎛️ Two‑DOF Modes：双自由度特征频率与模态形状动画
''')

st.info("首次使用？点击左侧 **页面（Pages）** 中的子页面进入模块。建议从“🌀 Mass–Spring–Damper”开始。")
st.success("提示：所有图都是 Plotly 交互图，可缩放、悬停查看数据；大多图支持一键 PNG 导出。")
