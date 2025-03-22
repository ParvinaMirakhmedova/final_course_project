import streamlit as st
import pandas as pd
import plotly.express as px
from db import fetch_patients

st.set_page_config(page_title="Diabetes Dashboard", layout="wide")

@st.cache_data
def load_data():
    return fetch_patients()

df = load_data()

# ---------- ФИЛЬТРЫ ----------
st.sidebar.header("Фильтры")

def apply_categorical_filter(df, column, label):
    if column in df.columns:
        if df[column].dropna().empty:
            st.warning(f"Нет данных по {label.lower()}.")
            return df
        df[column] = df[column].fillna(df[column].mode().iloc[0])
        options = df[column].unique().tolist()
        selected = st.sidebar.multiselect(label, options=options, default=options)
        df = df[df[column].isin(selected)]
    return df

def apply_numerical_filter(df, column, label):
    if column in df.columns:
        df[column] = df[column].fillna(df[column].median())
        min_val, max_val = float(df[column].min()), float(df[column].max())
        selected_range = st.sidebar.slider(label, min_val, max_val, (min_val, max_val))
        df = df[df[column].between(*selected_range)]
    return df

df = apply_categorical_filter(df, "sex", "Пол")
df = apply_categorical_filter(df, "dm_type", "Тип диабета")
df = apply_numerical_filter(df, "bmi", "BMI")

# ---------- ОСНОВНОЙ КОНТЕНТ ----------
st.title("📊 Diabetes Patient Dashboard")
st.write(f"Количество записей: {len(df)}")
st.dataframe(df)

# ---------- ДИАГРАММЫ ----------
st.subheader("Визуализация")

def show_histogram(column, title):
    if column in df.columns:
        df[column] = df[column].fillna(df[column].median())
        st.plotly_chart(px.histogram(df, x=column, nbins=20, title=title), use_container_width=True)

show_histogram("bmi", "Распределение BMI")
show_histogram("fbg", "Распределение FBG")

if all(col in df.columns for col in ["bmi", "fbg"]):
    st.plotly_chart(
        px.scatter(df, x="bmi", y="fbg", color="sex", title="BMI vs FBG", hover_data=["full_name"]),
        use_container_width=True
    )

if "dm_type" in df.columns:
    st.plotly_chart(px.pie(df, names="dm_type", title="Распределение по типу диабета"), use_container_width=True)
