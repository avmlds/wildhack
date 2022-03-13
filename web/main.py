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

image = Image.open("G0015158.JPG")
image = image.rotate(180)

st.sidebar.title("""Choose data for analysis""")


camera = st.sidebar.selectbox("Observation point", ["Angola", "Zambia", "Tanzania", "Uganda", "Zimbabwe", "Botswana", "Mozambique", "Namibia", "Lesotho", "South Africa", "Cameroon", "Ethiopia", "Mauritius"])
size = st.sidebar.selectbox("Plot scale", ["1sec", "5sec", "30sec", "1min", "5min"])
data_sidebar = st.sidebar.date_input("Observation period", value=d, min_value=df.reset_index()["date"].min(),  max_value=df.reset_index()["date"].max() + timedelta(days=1))
st.sidebar.write("---")
expander1 = st.sidebar.expander("Manual adding")
expander1.date_input("Date of observation", value=d)
expander1.number_input("Animal counting")
expander1.text_input("Animal")
expander1.button("Confirm", key="12")
expander4 = st.sidebar.expander("Load data")

if camera:
    st.subheader(camera)

expander2 = st.expander("Results")
if size:
    expander2.line_chart(data[size], use_container_width=True)
expander2.write("---")
expander2.header("Additional info")
if size:
    mean_today_metric = expander2.metric(label="Mean animal num",
        value=round(df.reset_index().loc[df.reset_index()["date"].dt.date == data_sidebar].groupby("filename")["quantity"].max().mean(), 2))
expander2.metric("Total for the entire period ", str(sum_metric), 20)
expander2.metric("Mean for the entire period", round(mean_metric, 2), 0.2)

tables = expander4.file_uploader("Load XLS/CSV file", type=None, accept_multiple_files=False)
expander4.button("Send", key="1231")

expander3 = st.expander("Photo analysis")
photos = expander3.file_uploader("Load photos", type=None, accept_multiple_files=True)
videos = expander3.file_uploader("Load video", type=None, accept_multiple_files=False)
expander3.button("Send", key="12312")

expander00 = st.expander("Live")
expander00.image(image, caption="Watch stream (beta)", channels="RGB", output_format="auto")
expander00.button("Zoom", key="113131ds2312")
expander00.date_input("Date of observation", value=d, key="wksjfaksjdnf")
expander00.number_input(" Number of animals", key="wksjfaksjdasdfasdfasdf")
expander00.button("Confirm and finish", key="113132")


expander = st.sidebar.expander("Look on map")
expander.map(coords, zoom=8)

#st.metric("Рыбы зафиксировано сегодня", sum_metric, 2)
#st.metric("Среднее количество рыбы", 42, 2)
