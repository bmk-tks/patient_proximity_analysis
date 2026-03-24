# patient_proximity_analysis

telangana_proximity/
├── app/
│   ├── __init__.py
│   └── app.py                    # Streamlit entry point
├── src/
│   ├── __init__.py
│   ├── data_loader.py            # Load hospital xlsx + patient CSV
│   ├── shape_handler.py          # Download/load Telangana shape
│   └── visualizations.py         # Plotly charts
├── data/
│   ├── raw/                      # YOUR input files go here
│   │   ├── TG_hospitals_1544.xlsx  # Your hospital data (copy here)
│   │   └── patients.csv            # Your patient CSV (you'll create)
│   ├── processed/                # Generated after loading
│   │   ├── hospitals_processed.csv
│   │   └── patients_processed.csv
│   └── geo/                      # Shape files
│       └── telangana.geojson
├── tests/
│   └── test_loader.py
├── requirements.txt
└── README.md