# SafeCity AI – Women & Child Safety Intelligence Platform

## 📌 Project Overview

SafeCity AI is a data-driven analytical platform designed to analyze historical crime records related to women and children.

The system integrates crime datasets, performs data cleaning and exploratory analysis, identifies crime patterns through visualizations, and applies a Random Forest Classifier to classify historical records into Low, Medium, and High risk levels.

An interactive Streamlit dashboard allows users to explore the analyzed information using state and year filters.

> **Note:** SafeCity AI is a historical crime-data analysis and awareness platform. It does not predict individual crimes, identify criminals, or guarantee future safety.

---

## 🎯 Objectives

- Analyze historical crime data related to women and children.
- Clean and preprocess raw datasets.
- Integrate compatible women and child crime records.
- Identify crime trends and major crime categories.
- Compare recorded cases across states and districts/police units.
- Classify historical records into Low, Medium, and High risk levels.
- Provide an interactive dashboard for easy data exploration.
- Allow users to download filtered data for further analysis.

---

## 🔄 System Workflow

Crime Data Collection  
↓  
Data Cleaning & Preprocessing  
↓  
Women & Child Data Integration  
↓  
Exploratory Data Analysis  
↓  
Feature Engineering  
↓  
Random Forest Classification  
↓  
Model Evaluation  
↓  
Interactive Streamlit Dashboard  
↓  
Historical Safety Insights

---

## 🤖 Machine Learning

### Algorithm

**Random Forest Classifier**

The model classifies historical records into:

- Low Risk
- Medium Risk
- High Risk

### Model Evaluation

| Metric | Result |
|---|---:|
| Accuracy | 95.26% |
| Precision | 95.29% |
| Recall | 95.26% |
| F1-Score | 95.27% |

These metrics are calculated on the historical test dataset and should not be interpreted as future-crime prediction accuracy.

---

## 📊 Dataset

The project uses historical crime statistics related to women and children.

### Dataset Period

**2001–2012**

### Final Dataset

- Records: **8,967**
- Features: **25**
- Missing values: **0**
- Duplicate records: **0**

### Overall Recorded Cases

- Women-related cases: **4,042,002**
- Children-related cases: **468,829**

The source data is based on publicly available Indian crime statistics.

---

## 🖥️ Dashboard Features

The Streamlit dashboard provides:

- Interactive State/UT filtering
- Year-range filtering
- Overall crime statistics
- Historical crime trends
- Women crime category analysis
- Children crime category analysis
- State-wise recorded crime comparison
- District/police-unit analysis
- Historical AI risk analysis
- Random Forest model metrics
- Confusion matrix
- Feature importance analysis
- Filtered CSV download

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- Seaborn
- Google Colab
- Visual Studio Code
- GitHub

---

## 📁 Project Structure

```text
SafeCity_AI/
│
├── app.py
├── requirements.txt
├── safecity_cleaned_data.csv
└── safecity_random_forest.pkl
