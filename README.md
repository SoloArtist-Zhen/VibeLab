# VibeFlow · 交互式振动与控制小工具

一个面向工程初学者与课堂演示的可视化小项目。包含常见的单/双自由度模型、PID 闭环响应、隔振传递率等，配有交互控件与简洁动画。目标是**能跑、好看、容易改**。

## 功能概览
- **Mass–Spring–Damper**：位移/速度时域曲线、相图，附质量块往复动画
- **PID Tuning Lab**：拖动 Kp、Ki、Kd 查看超调、整定时间、IAE 等指标
- **Isolation Designer**：传递率曲线 T(ω/ωₙ, ζ) 与“r≈√2 开始隔振”的经验位
- **Two-DOF Modes**：双自由度特征频率与模态向量，可视化模态振型动画

<!-- ===== 功能插图位（1~3 张静态图） ===== -->

<!--<img width="400" height="450" alt="newplot" src="https://github.com/user-attachments/assets/58028c44-d1e6-4f4a-8bc9-878fe8e66d42" />
<img width="816" height="450" alt="newplot-3" src="https://github.com/user-attachments/assets/bd36b5e9-887e-40dc-8f56-d99749e3a047" />
<img width="400" height="450" alt="newplot-2" src="https://github.com/user-attachments/assets/36d438c1-1184-4ba7-8ef2-b00e4df6b8da" />

-->

## 快速开始
```bash
# 建议使用虚拟环境
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```
浏览器会打开 `http://localhost:8501`。左侧 **Pages** 选择不同模块。

## 页面说明
- 🌀 **Mass–Spring–Damper**：选择激励（阶跃/正弦/自由）与初值，观察响应与动画。
- 🧰 **PID Tuning Lab**：单位阶跃跟踪，实时显示超调、整定时间、IAE 指标。
- 🧱 **Isolation Designer**：调整阻尼比与频率比范围，查看传递率曲线及简易基座激励动画。
- 🎛️ **Two-DOF Modes**：输入 m₁/m₂、k₁/k₂，计算 ω₁、ω₂，查看模态分量与动画。

## 导出与插图占位
- 大多数图表可以通过图表菜单导出为 PNG（若提示导出失败，确保已安装 `kaleido`，本仓库 `requirements.txt` 已包含）。
- 建议将**封面 GIF**与**3 张代表性截图**放在 `screenshots/` 中，并在本文档对应位置替换文件名。

## 常见问题
- **无法导出 PNG？** 试试：`pip install -U kaleido`，然后重启 `streamlit run app.py`。
- **浏览器没有自动打开？** 访问命令行输出的本地地址 `http://localhost:8501`。
- **想改成其他工程主题？** 可以把方程替换为你的系统模型，沿用交互与绘图框架即可。

## 目录结构（简要）
```
VibeFlow/
├─ app.py
├─ pages/
│  ├─ 1_🌀_Mass_Spring_Damper.py
│  ├─ 2_🧰_PID_Tuning_Lab.py
│  ├─ 3_🧱_Isolation_Designer.py
│  └─ 4_🎛️_Two_DOF_Modes.py
├─ assets/
├─ screenshots/      # ← 放你的封面 GIF 和截图
├─ requirements.txt
├─ LICENSE
└─ .streamlit/config.toml
```

## 许可证
MIT License（可自由使用与二次开发，保留版权声明）。
