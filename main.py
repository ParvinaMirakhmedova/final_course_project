import streamlit as st
import pandas as pd
import plotly.express as px
from db import fetch_patients

# Настройки страницы
st.set_page_config(page_title="Diabetes Dashboard", layout="wide")

# 📥 Загрузка данных из DuckDB
@st.cache_data
def load_data():
    return fetch_patients()

df = load_data()

# ---------- ФИЛЬТРЫ ----------
st.sidebar.header("Фильтры")

# 🔁 Кнопка сброса фильтров
if st.sidebar.button("🔄 Сбросить фильтры"):
    st.rerun()

# 🧩 Категориальный фильтр (пол, тип диабета)
def apply_categorical_filter(df, column, label):
    if column not in df.columns:
        return df
    options = sorted(df[column].unique())
    selected = st.sidebar.multiselect(label, options, default=options)
    return df[df[column].isin(selected)]

# 📊 Числовой фильтр (BMI, возраст, FBG)
def apply_numerical_filter(df, column, label):
    if column not in df.columns:
        return df
    min_val, max_val = float(df[column].min()), float(df[column].max())
    selected_range = st.sidebar.slider(label, min_val, max_val, (min_val, max_val))
    return df[df[column].between(*selected_range)]


# ✅ Применяем фильтры
df = apply_categorical_filter(df, "sex", "Пол")
df = apply_categorical_filter(df, "dm_type", "Тип диабета")
df = apply_numerical_filter(df, "bmi", "BMI")
df = apply_numerical_filter(df, "age", "Возраст")
df = apply_numerical_filter(df, "fbg", "FBG")

# ---------- ОСНОВНОЙ КОНТЕНТ ----------
st.title("📊 Diabetes Patient Dashboard")
st.write(f"Количество записей: {len(df)}")
st.dataframe(df)

# ---------- ВИЗУАЛИЗАЦИЯ ----------
st.subheader("📈 Визуализация")

# Переключатель типа диаграммы
chart_type = st.selectbox(
    "Выберите тип диаграммы:",
    [
        "Распределение BMI",
        "Распределение FBG",
        "BMI vs FBG (по полу)",
        "Распределение по типу диабета (pie)",
        "Средний возраст по полу (bar)",
        "Тип диабета по возрасту и BMI (scatter)"
    ]
)

# 1. Гистограмма BMI
if chart_type == "Распределение BMI" and "bmi" in df.columns:
    st.plotly_chart(
        px.histogram(df,
                    x="bmi",
                    nbins=25, 
                    title="Распределение BMI", 
                    color_discrete_sequence=["#2ca02c"]),
        use_container_width=True
    )

# 2. Гистограмма FBG
elif chart_type == "Распределение FBG" and "fbg" in df.columns:
    st.plotly_chart(
        px.histogram(df, 
                     x="fbg", 
                     nbins=20, 
                     title="Распределение FBG",
                     color_discrete_sequence=["#ff7f0e"]),
        use_container_width=True
    )

# 3. Scatter: BMI vs FBG, цвет — пол
elif chart_type == "BMI vs FBG (по полу)" and all(col in df.columns for col in ["bmi", "fbg", "sex"]):
    st.plotly_chart(
        px.scatter(df, 
                   x="bmi", 
                   y="fbg", 
                   color="sex", 
                   title="BMI vs FBG", 
                   hover_data=["full_name"],
                   color_discrete_map={
        "female": "#e377c2",  # розовый
        "male": "#1f77b4"} #синий
        ),
        use_container_width=True
    )

# 4. Pie: по типу диабета
elif chart_type == "Распределение по типу диабета (pie)" and "dm_type" in df.columns:
    st.plotly_chart(
        px.pie(df, names="dm_type", title="Распределение по типу диабета"),
        use_container_width=True
    )

# 5. Bar: средний возраст по полу
elif chart_type == "Средний возраст по полу (bar)" and all(col in df.columns for col in ["sex", "age"]):
    avg_age = df.groupby("sex")["age"].mean().reset_index()
    st.plotly_chart(
        px.bar(
            avg_age,
            x="sex",
            y="age",
            title="Средний возраст по полу",
            hover_data=["age"],
            text_auto=".1f",  # подписи на колонках, 1 знак после запятой
            color="sex",
            color_discrete_map={
                "female": "#e377c2",
                "male": "#1f77b4",
            }
        ),
        use_container_width=True
    )


# 6. Scatter: тип диабета по возрасту и BMI
elif chart_type == "Тип диабета по возрасту и BMI (scatter)" and all(col in df.columns for col in ["dm_type", "age", "bmi"]):
    st.plotly_chart(
        px.scatter(
            df, x="age", y="bmi", color="dm_type",
            title="Распределение типов диабета по возрасту и BMI",
            hover_data=["full_name", "sex"]
        ),
        use_container_width=True
    )
