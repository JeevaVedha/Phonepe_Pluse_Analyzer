# 📊 PhonePe Transaction Insights Dashboard

An interactive dashboard and analytical study of digital payment trends across India, powered by PhonePe Pulse data.

---

## 1. 🏷️ Project Title

**PhonePe Transaction Insights Dashboard**

---

## 2. 📌 Project Overview

This project analyzes PhonePe’s publicly available data to uncover insights into digital payment trends, user behavior, and geographic variations across India. Built using **Python**, **SQL**, and **Streamlit**, it transforms complex datasets into actionable business intelligence through interactive visualizations.

---

## 3. 💼 Domain

**Finance / Digital Payments**

---

## 4. 🧠 Key Technologies & Skills

- **Programming:** Python  
- **Database:** PostgreSQL, SQLAlchemy  
- **Visualization:** Plotly, Seaborn, Matplotlib  
- **Web App:** Streamlit  
- **Data Handling:** Pandas, JSON, CSV  

---

## 5. 🎯 Objectives

- Transform and analyze PhonePe data to extract key insights.
- Visualize trends across states, districts, and quarters.
- Build an interactive dashboard for dynamic user exploration.
- Provide strategic recommendations based on analysis.

---

## 6. 🗂️ Dataset Overview

**Source:** [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse)

**Data Categories:**
- **Aggregated Data:** User metrics, transactions, insurance
- **Map Data:** Geospatial metrics by state/district
- **Top Data:** Rankings of top-performing regions

**Transformation:** Raw JSON ➝ Cleaned CSV using custom Python scripts.

---

## 7. 📁 Project Structure

```plaintext
PHONEPE_PLUSE_ANALYZER/
├── data/
│   └── Data_Extract/                  # CSV files derived from raw JSON
├── image/
│   ├── Image.jpg
│   └── PhonePe_Logo.png
├── db_load.py                         # Loads data to PostgreSQL
├── main.ipynb                         # Main analysis & EDA
├── phonepe.py                         # Streamlit app
├── Phonepe_Docs.docx                  # Detailed project documentation
├── README.md                          # This file
├── .gitignore
├── LICENSE

---

## 8. ⚙️ Setup Instructions

### 8.1. Clone the Repository

```bash
git clone https://github.com/JeevaVedha/Phonepe_Pluse_Analyzer.git
cd Phonepe_Pluse_Analyzer

### 8.2. Install Required Packages

```bash
pip install -r requirements.txt

### 8.3. Load Data into PostgreSQL
```bash
Update your DB credentials in db_load.py and run:
python db_load.py

### 8.4. Launch Streamlit Dashboard
```bash
streamlit run phonepe.py

## 9. 🚀 Key Features
📍 User Registration Analysis – Map-based registration trends over time

📈 Transaction Trends – Top-performing states and districts

📱 Device Analysis – Brand-wise user engagement metrics

🛡️ Insurance Insights – Regional breakdown and growth

📅 Quarterly & Yearly Filters – Drill-down for precise analysis

## 10. 📸 Sample Visualizations
🌐 Choropleth Maps

📊 Bar & Line Charts

📋 Dynamic Tables

🎛️ Interactive Dropdowns & Sliders

11. 🔍 Analysis Insights
🚀 Top & Bottom Performing Regions

📊 Growth Trends by Quarter

👥 User Adoption Rates

🧾 Category-Wise Transaction Distribution

📱 Device-Based Usage Trends

## 12. 🔮 Future Improvements
🔁 Integrate live API to auto-refresh data

🔍 Add advanced filters and forecasting models

🔐 Role-based access to dashboard and reports

## 13. 📚 References
📘 PhonePe Pulse

📊 Plotly Documentation

🧾 Streamlit Docs

📘 Pandas Docs

🗃️ SQLAlchemy Docs

