import streamlit as st
import pandas as pd
import plotly.express as px
from db import fetch_patients

st.set_page_config(page_title="Diabetes Dashboard", layout="wide")

# Загружаем данные из DuckDB
@st.cache_data
def load_data():
    return fetch_patients()

df = load_data()

# ---------- ФИЛЬТРЫ ----------
st.sidebar.header("Фильтры")

if "age" in df.columns:
    df["age"] = df["age"].fillna(df["age"].median())
    min_age, max_age = int(df["age"].min()), int(df["age"].max())
    age_range = st.sidebar.slider("Возраст", min_age, max_age, (min_age, max_age))
    df = df[df["age"].between(age_range[0], age_range[1])]

if "sex" in df.columns:
    df["sex"] = df["sex"].fillna(df["sex"].mode().iloc[0])
    options = df["sex"].unique().tolist()
    selected = st.sidebar.multiselect("Пол", options=options, default=options)
    df = df[df["sex"].isin(selected)]

if "dm_type" in df.columns:
    df["dm_type"] = df["dm_type"].fillna(df["dm_type"].mode().iloc[0])
    dm_options = df["dm_type"].unique().tolist()
    selected_dm = st.sidebar.multiselect("Тип диабета", options=dm_options, default=dm_options)
    df = df[df["dm_type"].isin(selected_dm)]

if "bmi" in df.columns:
    df["bmi"] = df["bmi"].fillna(df["bmi"].median())
    min_bmi, max_bmi = float(df["bmi"].min()), float(df["bmi"].max())
    bmi_range = st.sidebar.slider("BMI", min_bmi, max_bmi, (min_bmi, max_bmi))
    df = df[df["bmi"].between(bmi_range[0], bmi_range[1])]

# ---------- ОСНОВНОЙ КОНТЕНТ ----------
st.title("📊 Diabetes Patient Dashboard")
st.write(f"Количество записей: {len(df)}")
st.dataframe(df)

# ---------- ДИАГРАММЫ ----------
st.subheader("Визуализация")

if "bmi" in df.columns:
    st.plotly_chart(px.histogram(df, x="bmi", nbins=20, title="Распределение BMI"), use_container_width=True)

if "fbg" in df.columns:
    df["fbg"] = df["fbg"].fillna(df["fbg"].median())
    st.plotly_chart(px.histogram(df, x="fbg", nbins=20, title="Распределение FBG"), use_container_width=True)

if "bmi" in df.columns and "fbg" in df.columns:
    st.plotly_chart(
        px.scatter(df, x="bmi", y="fbg", color="sex", title="BMI vs FBG", hover_data=["full_name"]),
        use_container_width=True
    )

if "dm_type" in df.columns:
    st.plotly_chart(px.pie(df, names="dm_type", title="Распределение по типу диабета"), use_container_width=True)
