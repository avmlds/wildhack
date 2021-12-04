import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta

d = datetime.strptime("2021-08-11", "%Y-%m-%d")
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

data = {
    "1с": df["quantity"].resample("s").sum(),
    "5с": df["quantity"].resample("5s").sum(),
    "30с": df["quantity"].resample("30s").sum(),
    "1мин": df["quantity"].resample("60s").sum(),
    "5мин": df["quantity"].resample("300s").sum()
}

sum_metric = df.groupby("filename")["quantity"].max().sum()
mean_metric = df.groupby("filename")["quantity"].max().mean()

coords = df.loc[(~df["N"].isnull()) & (~df["E"].isnull()), ["N", "E"]]
coords.columns = ["lat", "lon"]

image = Image.open("../train1/G0015158.JPG")
image = image.rotate(180)

st.sidebar.title("""Выбор данных для анализа""")


camera = st.sidebar.selectbox("Точка наблюдения", ["Курильское озеро", "р. Быстрая", "р. Жупанова", "р. Колпакова", "р. Опала", "о. Калагирь", "о. Дальнее", "о. Кроноцкое", "о. Начикинское", "о. Налычево", "р. Авача", "р. Хламовитка", "р. Широкая", "Авачинская бухта"])
size = st.sidebar.selectbox("Масштаб графика", ["1с", "5с", "30с", "1мин", "5мин"])
data_sidebar = st.sidebar.date_input("Период наблюдений", value=d, min_value=df.reset_index()["date"].min(),  max_value=df.reset_index()["date"].max() + timedelta(days=1))
st.sidebar.write("---")
expander1 = st.sidebar.expander("Добавить данные вручную")
expander1.date_input("Дата наблюдений", value=d)
expander1.number_input("Число рыб")
expander1.text_input("Порода рыб")
expander1.button("Подтвердить", key="12")
expander4 = st.sidebar.expander("Загрузить таблицу")

if camera:
    st.subheader(camera)

expander2 = st.expander("Результаты подсчетов")
if size:
    expander2.line_chart(data[size], use_container_width=True)
expander2.write("---")
expander2.header("Дополнительная аналитика")
if size:
    mean_today_metric = expander2.metric(label="Рыб в среднем за сегодня, шт.",
        value=round(df.reset_index().loc[df.reset_index()["date"].dt.date == data_sidebar].groupby("filename")["quantity"].max().mean(), 2))
expander2.metric("Суммарно за весь период ", str(sum_metric), 20)
expander2.metric("Среднее за весь период", round(mean_metric, 2), 0.2)

tables = expander4.file_uploader("Загрузить XLS/CSV таблицу", type=None, accept_multiple_files=False)
expander4.button("Отправить", key="1231")

expander3 = st.expander("Распознать фото/видео")
photos = expander3.file_uploader("Загрузить фотографии", type=None, accept_multiple_files=True)
videos = expander3.file_uploader("Загрузить видео", type=None, accept_multiple_files=False)
expander3.button("Отправить", key="12312")

expander00 = st.expander("Режим онлайн")
expander00.image(image, caption="Смотреть трансляцию (экспериментально)", channels="RGB", output_format="auto")
expander00.button("Увеличить", key="113131ds2312")
expander00.date_input("Дата наблюдений", value=d, key="wksjfaksjdnf")
expander00.number_input("Число рыб", key="wksjfaksjdasdfasdfasdf")
expander00.button("Подтвердить и завершить просмотр", key="113132")


expander = st.sidebar.expander("Показать на карте")
expander.map(coords, zoom=8)

#st.metric("Рыбы зафиксировано сегодня", sum_metric, 2)
#st.metric("Среднее количество рыбы", 42, 2)
