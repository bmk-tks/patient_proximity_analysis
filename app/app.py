import streamlit as st
import sys
import os

sys.path.append("..")
from src.data_loader import load_hospitals, load_patients
from src.visualizations import (
    load_geojson,
    create_patient_hospital_map,
    create_patient_bar_chart,
    create_treatment_pie_chart,
    create_status_bar_chart,
    create_district_treatment_heatmap
)

st.set_page_config(page_title="Telangana Patient Proximity Analysis", layout="wide")
st.title("Telangana Patient Proximity Analysis")

@st.cache_data
def get_data():
    patients = load_patients()
    hospitals = load_hospitals()
    geojson = load_geojson("telangana_districts")
    return patients, hospitals, geojson

patients, hospitals, geojson = get_data()

st.sidebar.header("Filters")

districts = ["All"] + sorted(patients["district"].unique().tolist())
selected_district = st.sidebar.selectbox("Select District", districts)

treatments = ["All"] + sorted(patients["treatment"].unique().tolist())
selected_treatment = st.sidebar.selectbox("Select Treatment", treatments)

statuses = ["All"] + sorted(patients["status"].unique().tolist())
selected_status = st.sidebar.selectbox("Select Status", statuses)

filtered = patients.copy()
if selected_district != "All":
    filtered = filtered[filtered["district"] == selected_district]
if selected_treatment != "All":
    filtered = filtered[filtered["treatment"] == selected_treatment]
if selected_status != "All":
    filtered = filtered[filtered["status"] == selected_status]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", len(patients))
col2.metric("Filtered Patients", len(filtered))
col3.metric("Hospitals", len(hospitals))
col4.metric("Districts", patients["district"].nunique())

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Map", "District Analysis", "Treatment Analysis", "Status Analysis"])

with tab1:
    st.subheader("Patient & Hospital Map")
    fig_map = create_patient_hospital_map(filtered, hospitals, geojson)
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.subheader("Patients by District")
    fig_bar = create_patient_bar_chart(filtered)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Treatment Demand Heatmap")
    fig_heatmap = create_district_treatment_heatmap(filtered)
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab3:
    st.subheader("Treatment Distribution")
    fig_pie = create_treatment_pie_chart(filtered)
    st.plotly_chart(fig_pie, use_container_width=True)

with tab4:
    st.subheader("Patient Status Distribution")
    fig_status = create_status_bar_chart(filtered)
    st.plotly_chart(fig_status, use_container_width=True)

st.markdown("---")
st.subheader("Patient Data")
st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False)
st.download_button("Download CSV", csv, "filtered_patients.csv", "text/csv")