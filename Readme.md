<p align="center">
  <img src="https://img.icons8.com/fluency/96/steam.png" alt="Steam Logo" width="80" />
</p>

<h1 align="center">Game Success Predictor</h1>
<h2 align="center">基于多源数据的 Steam 游戏成功率预测模型</h2>

<p align="center">
  <strong>融合 Steam 核心指标与 Twitch 流媒体趋势，利用机器学习洞察游戏爆款逻辑</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Dataset-Steam%20%26%20Twitch-black?style=flat-square&logo=kaggle" />
  <img src="https://img.shields.io/badge/Framework-Scikit--Learn-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/UI-Streamlit-ff4b4b?style=flat-square" />
  <img src="https://img.shields.io/badge/Task-Binary%20Classification-blue?style=flat-square" />
</p>

---

## 🎯 项目核心 (Core Objective)

**我们能否根据游戏特征预判其在 Steam 上的成败？**
本项目通过对 110,000+ 款游戏的数据挖掘，构建了一个二分类模型（Success vs. Not Success），帮助开发者理解哪些特征驱动了商业表现与玩家口碑。

### 🏆 什么是“成功”？ (The Gold Standard)
在本模型中，一款“成功”的游戏必须同时满足：
1.  **极佳口碑**：好评率 (Positive Ratio) $\ge 85\%$。
2.  **受众规模**：推荐数 $> 1,000$ 或 拥有者数量 $> 50,000$。

---

## 📊 数据来源 (Data Sources)

项目通过游戏名称作为主键，深度融合了两大权威数据集：
* **Steam Games Dataset**: 涵盖 110,000+ 游戏的元数据（价格、类型、开发商等）。
* **Twitch Game Data (2016-2023)**: 包含每月 Top 200 游戏在流媒体平台的曝光度数据。

---

## 🚀 快速开始 (Quick Start)

### 1. 环境准备
```bash
# 进入应用目录
cd app
# 安装依赖
pip install -r requirements.txt

```

### 2. 获取数据

由于数据集体积庞大，请从以下链接下载并放置于本地数据目录：

* [Steam Games Dataset (Kaggle)](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)
* [Evolution of Top Games on Twitch (Kaggle)](https://www.kaggle.com/datasets/rankirsh/evolution-of-top-games-on-twitch)

### 3. 运行可视化界面

```bash
streamlit run app.py

```

> [!IMPORTANT]
> **重要提示**：请勿将超过 100MB 的原始数据集上传至 GitHub，这会导致仓库崩溃或上传失败。请务必使用 `.gitignore` 忽略大文件。

---

## 🎨 项目演示 (Slides)

想要了解更多关于特征工程、模型评估及“Twitch 悖论”的深度分析？
👉 **[查看项目在线演示 (Gamma App)](https://gamma.app/docs/Game-Success-Prediction-Steam-Twitch-xtyxo5ogqvz6512?mode=present#card-jhoevtjv81nus25)**

---

## 🛠️ 技术栈 (Tech Stack)

* **数据处理**: Pandas, NumPy
* **机器学习**: Scikit-Learn (Random Forest / XGBoost)
* **向量化与相似度**: RapidFuzz (用于数据集名称对齐)
* **可视化界面**: Streamlit
* **展示工具**: Gamma App

---

## 📈 核心洞察 (Key Insights)

* **口碑与销量的关联性**：高好评率不代表高销量，但高销量往往伴随着稳健的好评。
* **Twitch 效应**：高曝光度对新游成功率有显著加成，但对特定品类存在“流失风暴”。

---

<p align="center">
<i>"在数字海洋中，用数据为游戏开发者寻找灯塔。"</i>
</p>

```

策问题*”？

```
