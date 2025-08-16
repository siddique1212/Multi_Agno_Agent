
import streamlit as st
import pandas as pd
from agents import TeamOrchestrator

st.set_page_config(page_title="Multi-Agent Task Force: Mission Sustainability", layout="wide")

st.title("🌱 Multi-Agent Task Force: Mission Sustainability")
st.caption("Run single agents or the full task force to build a sustainability proposal.")

mode = st.radio("Choose mode:", ["Single Agent", "Full Task Force"], horizontal=True)

orchestrator = TeamOrchestrator()

if mode == "Single Agent":
    agent = st.selectbox("Select an agent:", ["News Analyst", "Data Analyst", "Policy Reviewer", "Innovations Scout"])

    if agent == "News Analyst":
        topic = st.text_input("Topic", "city-level green projects")
        if st.button("Run News Analyst"):
            res = orchestrator.run_single("News Analyst", topic=topic, limit=5)
            st.subheader(res.title)
            st.markdown(res.summary)

    elif agent == "Policy Reviewer":
        city = st.text_input("City", "Karachi")
        if st.button("Run Policy Reviewer"):
            res = orchestrator.run_single("Policy Reviewer", city=city, limit=5)
            st.subheader(res.title)
            st.markdown(res.summary)

    elif agent == "Innovations Scout":
        query = st.text_input("Search query", "urban sustainability tech")
        if st.button("Run Innovations Scout"):
            res = orchestrator.run_single("Innovations Scout", query=query, limit=5)
            st.subheader(res.title)
            st.markdown(res.summary)

    elif agent == "Data Analyst":
        city = st.text_input("City", "Karachi")
        up = st.file_uploader("Upload CSV (optional) with columns date,pm25,pm10,no2,city", type=["csv"])
        csv_bytes = up.read() if up is not None else None
        if st.button("Run Data Analyst"):
            res = orchestrator.run_single("Data Analyst", csv_bytes=csv_bytes, city=city)
            st.subheader(res.title)
            st.markdown(res.summary)
            df = res.artifacts.get("dataframe")
            if isinstance(df, pd.DataFrame):
                st.dataframe(df)

else:
    st.subheader("Team Inputs")
    city = st.text_input("City", "Karachi")
    news_topic = st.text_input("News topic", "sustainability initiatives in Pakistan cities")
    innov_query = st.text_input("Innovation query", "urban sustainability tech")
    up = st.file_uploader("Upload CSV (optional) with columns date,pm25,pm10,no2,city", type=["csv"])
    csv_bytes = up.read() if up is not None else None
    if st.button("Run Full Task Force"):
        res = orchestrator.run_team({
            "city": city,
            "news_topic": news_topic,
            "innov_query": innov_query,
            "csv_bytes": csv_bytes,
        })
        st.subheader(res.title)
        st.markdown(res.summary)
