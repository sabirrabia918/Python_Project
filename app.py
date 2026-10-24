import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from config import DB_PATH

st.set_page_config(page_title="Launch Tracker", page_icon="🚀", layout="wide")
st.title("🚀 Global Spacecraft Launch Tracker")

df = pd.read_sql("SELECT * FROM launches", sqlite3.connect(DB_PATH))
df["net"] = pd.to_datetime(df["net"], utc=True)
df["year"] = df["net"].dt.year
df["success"] = df["status"].str.contains("Success", case=False)

c1, c2, c3 = st.columns(3)
c1.metric("Total launches", len(df))
c2.metric("Success rate", f"{df['success'].mean()*100:.1f}%")
c3.metric("Agencies", df["agency"].nunique())

st.subheader("1. Kis agency ka success rate sabse zyada hai? (min 10 launches)")
g = df.groupby("agency")["success"].agg(["mean", "count"])
g = g[g["count"] >= 10].sort_values("mean", ascending=False).head(15)
st.plotly_chart(px.bar(g, y="mean", labels={"mean": "Success rate"}),
                use_container_width=True)

st.subheader("2. Saal ba saal launches (Commercial vs baaqi)")
t = df.groupby(["year", "agency_type"]).size().reset_index(name="launches")
st.plotly_chart(px.line(t, x="year", y="launches", color="agency_type"),
                use_container_width=True)

st.subheader("3. Failures ki wajah")
f = df[df["fail_reason"].notna() & (df["fail_reason"] != "")]
st.dataframe(f[["name", "agency", "net", "fail_reason"]],
             use_container_width=True)