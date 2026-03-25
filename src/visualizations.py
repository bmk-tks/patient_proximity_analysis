"""
visualizations.py
Plotly charts for patient proximity analysis
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
GEO_DIR = os.path.join(DATA_DIR, "geo")


def load_geojson(name):
    path = os.path.join(GEO_DIR, f"{name}.geojson")
    with open(path, "r") as f:
        return json.load(f)


def create_patient_hospital_map(patients_df, hospitals_df, geojson):
    fig = go.Figure()

    fig.add_trace(go.Choroplethmap(
        geojson=geojson,
        locations=patients_df["district"].unique(),
        featureidkey="properties.DISTRICT",
        z=[1] * len(patients_df["district"].unique()),
        colorscale=[[0, "rgba(200,200,200,0.3)"], [1, "rgba(200,200,200,0.3)"]],
        showscale=False,
        marker_line_width=2,
        marker_line_color="darkgray",
        name="Districts",
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scattermap(
        lat=hospitals_df["LATITUDE"],
        lon=hospitals_df["LONGITUDE"],
        mode="markers",
        marker=dict(size=10, color="red", opacity=0.7),
        name="Hospitals",
        text=hospitals_df.apply(lambda x: f"Hospital: {x['HOSP_ID']}", axis=1),
        hoverinfo="text"
    ))

    fig.add_trace(go.Scattermap(
        lat=patients_df["latitude"],
        lon=patients_df["longitude"],
        mode="markers",
        marker=dict(size=8, color="blue", opacity=0.6),
        name="Patients",
        text=patients_df.apply(lambda x: f"Patient: {x['patient_id']}<br>Treatment: {x['treatment']}<br>District: {x['district']}", axis=1),
        hoverinfo="text"
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 17.5, "lon": 78.8},
        mapbox_zoom=6,
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    return fig


def create_patient_bar_chart(patients_df):
    district_counts = patients_df.groupby("district").size().reset_index(name="count")
    district_counts = district_counts.sort_values("count", ascending=False)

    fig = px.bar(
        district_counts,
        x="district",
        y="count",
        title="Patients by District",
        color="count",
        color_continuous_scale="Blues"
    )
    fig.update_layout(height=400, xaxis_tickangle=-45, margin=dict(b=100))
    return fig


def create_treatment_pie_chart(patients_df):
    treatment_counts = patients_df.groupby("treatment").size().reset_index(name="count")
    fig = px.pie(treatment_counts, values="count", names="treatment", title="Patients by Treatment Type")
    fig.update_layout(height=400)
    return fig


def create_status_bar_chart(patients_df):
    status_counts = patients_df.groupby("status").size().reset_index(name="count")
    fig = px.bar(
        status_counts,
        x="status",
        y="count",
        title="Patients by Status",
        color="status",
        color_discrete_map={"Registered": "yellow", "Ongoing": "orange", "Completed": "green"}
    )
    fig.update_layout(height=300, showlegend=False)
    return fig


def create_district_treatment_heatmap(patients_df):
    pivot = patients_df.groupby(["district", "treatment"]).size().reset_index(name="count")
    pivot = pivot.pivot_table(index="treatment", columns="district", values="count", fill_value=0)

    fig = px.imshow(
        pivot.values,
        x=pivot.columns,
        y=pivot.index,
        title="Treatment Demand by District",
        color_continuous_scale="YlOrRd",
        labels=dict(x="District", y="Treatment", color="Count")
    )
    fig.update_layout(height=500, xaxis_tickangle=-45)
    return fig


if __name__ == "__main__":
    from src.data_loader import load_hospitals, load_patients

    patients = load_patients()
    hospitals = load_hospitals()
    geojson = load_geojson("telangana_districts")

    print("Testing visualizations...")
    fig_map = create_patient_hospital_map(patients, hospitals, geojson)
    fig_bar = create_patient_bar_chart(patients)
    fig_pie = create_treatment_pie_chart(patients)
    fig_status = create_status_bar_chart(patients)
    fig_heatmap = create_district_treatment_heatmap(patients)
    print("All charts created!")