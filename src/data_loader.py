"""
data_loader.py
Loads hospital data from xlsx and generates sample patient data
"""
import pandas as pd
import os
import random
from datetime import datetime, timedelta

TELANGANA_DISTRICTS = {
    "Adilabad": {"coords": (19.6667, 78.5333), "pincodes": ["504001", "504002", "504003", "504101", "504102"]},
    "Bhadradri Kothagudem": {"coords": (17.5540, 80.6208), "pincodes": ["507101", "507102", "507103", "507104"]},
    "Hanumakonda": {"coords": (18.0018, 79.5631), "pincodes": ["506001", "506002", "506003", "506101"]},
    "Hyderabad": {"coords": (17.3850, 78.4867), "pincodes": ["500001", "500002", "500003", "500004", "500008", "500009", "500010"]},
    "Jagtial": {"coords": (18.7947, 78.9131), "pincodes": ["505001", "505101", "505102", "505153"]},
    "Jangaon": {"coords": (17.7269, 79.1519), "pincodes": ["506101", "506122", "506163", "506164"]},
    "Jayashankar Bhupalpally": {"coords": (18.2553, 79.8231), "pincodes": ["506169", "506172", "506175", "506185"]},
    "Jogulamba Gadwal": {"coords": (16.2361, 77.7961), "pincodes": ["509101", "509102", "509103", "509104", "509105"]},
    "Kamareddy": {"coords": (18.2667, 78.3333), "pincodes": ["503101", "503102", "503103", "503104", "503105"]},
    "Karimnagar": {"coords": (18.4386, 79.1288), "pincodes": ["505001", "505002", "505003", "505004", "505005"]},
    "Khammam": {"coords": (17.2473, 80.1514), "pincodes": ["507001", "507002", "507003", "507004", "507005"]},
    "Kumuram Bheem Asifabad": {"coords": (19.3586, 79.1972), "pincodes": ["504293", "504295", "504296", "504297", "504298", "504299"]},
    "Mahabubabad": {"coords": (17.8486, 79.8969), "pincodes": ["506101", "506105", "506134", "506135", "506142"]},
    "Mahabubnagar": {"coords": (16.7483, 77.9861), "pincodes": ["509001", "509002", "509003", "509004", "509005"]},
    "Mancherial": {"coords": (18.8686, 79.4364), "pincodes": ["504201", "504202", "504208", "504215", "504216", "504231"]},
    "Medak": {"coords": (18.0464, 78.2644), "pincodes": ["502001", "502002", "502003", "502004", "502005"]},
    "Medchal-Malkajgiri": {"coords": (17.6264, 78.5478), "pincodes": ["500058", "500076", "500077", "500078", "500079", "500100"]},
    "Mulugu": {"coords": (18.0892, 80.8258), "pincodes": ["506101", "506102", "506103", "506104", "506105", "506122"]},
    "Nagarkurnool": {"coords": (16.5047, 78.3231), "pincodes": ["509101", "509102", "509105", "509107", "509110", "509120"]},
    "Nalgonda": {"coords": (17.0500, 79.2700), "pincodes": ["508001", "508002", "508003", "508004", "508005"]},
    "Narayanpet": {"coords": (16.7436, 77.4958), "pincodes": ["509201", "509202", "509205", "509207", "509210", "509301"]},
    "Nirmal": {"coords": (19.0967, 78.3444), "pincodes": ["504001", "504101", "504102", "504103", "504106", "504107", "504208"]},
    "Nizamabad": {"coords": (18.6725, 78.0940), "pincodes": ["503001", "503002", "503003", "503004", "503005"]},
    "Peddapalli": {"coords": (18.6158, 79.1217), "pincodes": ["505101", "505172", "505174", "505185", "505187", "505188"]},
    "Rajanna Sircilla": {"coords": (18.3878, 78.8378), "pincodes": ["505301", "505302", "505303", "505324", "505325", "505326"]},
    "Ranga Reddy": {"coords": (17.3167, 78.5500), "pincodes": ["500078", "500079", "500080", "501218", "501301", "501350"]},
    "Sangareddy": {"coords": (17.6386, 78.0778), "pincodes": ["502001", "502008", "502034", "502058", "502078", "502098"]},
    "Siddipet": {"coords": (18.1019, 78.8497), "pincodes": ["502103", "502110", "502113", "502117", "502120", "502247"]},
    "Suryapet": {"coords": (17.1400, 79.6364), "pincodes": ["508201", "508202", "508203", "508204", "508213", "508218"]},
    "Vikarabad": {"coords": (17.3381, 77.9050), "pincodes": ["501101", "501102", "501121", "501141", "501142", "501143"]},
    "Wanaparthy": {"coords": (16.3617, 78.0608), "pincodes": ["509101", "509103", "509104", "509105", "509130", "509203"]},
    "Warangal": {"coords": (17.9784, 79.5941), "pincodes": ["506001", "506002", "506003", "506004", "506005"]},
    "Yadadri Bhuvanagiri": {"coords": (17.5167, 78.8833), "pincodes": ["508101", "508102", "508103", "508107", "508111", "508112"]},
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

STATUS_REGISTERED = "Registered"
STATUS_ONGOING = "Ongoing"
STATUS_COMPLETED = "Completed"

TREATMENTS = ["Hemodialysis", "Chemotherapy", "Radiation Therapy", "Thalassemia"]


def load_hospitals():
    """Load hospitals from xlsx file"""
    xlsx_path = os.path.join(RAW_DIR, "TG_hospitals_1544.xlsx")

    if not os.path.exists(xlsx_path):
        raise FileNotFoundError(f"Hospital file not found: {xlsx_path}")

    df = pd.read_excel(xlsx_path)
    df.columns = df.columns.str.strip()

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_path = os.path.join(PROCESSED_DIR, "hospitals_processed.csv")
    df.to_csv(out_path, index=False)

    print(f"Loaded {len(df)} hospitals from {xlsx_path}")
    return df


def generate_patients(n=500, seed=42):
    """
    Generate sample patient data for testing.

    Logic for dates:
    REGISTERED: only registration_date, admission_date=null, discharge_date=null
    ONGOING: registration_date + admission_date, discharge_date=null
    COMPLETED: registration_date + admission_date + discharge_date
    """
    random.seed(seed)

    today = datetime.now()
    one_year_ago = today - timedelta(days=365)

    patients = []
    districts = list(TELANGANA_DISTRICTS.keys())

    for i in range(n):
        district = random.choice(districts)
        district_info = TELANGANA_DISTRICTS[district]
        lat, lon = district_info["coords"]
        pincode = random.choice(district_info["pincodes"])

        lat += random.uniform(-0.05, 0.05)
        lon += random.uniform(-0.05, 0.05)

        treatment = random.choice(TREATMENTS)

        status_rand = random.random()
        if status_rand < 0.25:
            status = STATUS_REGISTERED
        elif status_rand < 0.50:
            status = STATUS_ONGOING
        else:
            status = STATUS_COMPLETED

        max_reg_days = (today - one_year_ago).days
        reg_days_ago = random.randint(1, max_reg_days)
        reg_date = today - timedelta(days=reg_days_ago)

        if status == STATUS_REGISTERED:
            # Only registration date
            admission_date = None
            discharge_date = None

        elif status == STATUS_ONGOING:
            # Admission 1-7 days after registration
            admission_days_after = random.randint(1, 7)
            admission_date = reg_date + timedelta(days=admission_days_after)
            discharge_date = None

        else:  # COMPLETED
            # Admission 1-7 days after registration
            admission_days_after = random.randint(1, 7)
            admission_date = reg_date + timedelta(days=admission_days_after)

            if treatment == "Hemodialysis":
                # 30-90 days of regular dialysis
                treatment_duration = random.randint(30, 90)
            elif treatment == "Chemotherapy":
                # 60-180 days (course of chemo)
                treatment_duration = random.randint(60, 180)
            elif treatment == "Radiation Therapy":
                # 30-60 days
                treatment_duration = random.randint(30, 60)
            else:  # Thalassemia
                # Ongoing management: 90-365 days
                treatment_duration = random.randint(90, 365)

            discharge_date = admission_date + timedelta(days=treatment_duration)
            if discharge_date > today:
                discharge_date = today

        patients.append({
            "patient_id": f"P{i+1:05d}",
            "treatment": treatment,
            "pincode": pincode,
            "district": district,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "status": status,
            "registration_date": reg_date.strftime("%Y-%m-%d"),
            "admission_date": admission_date.strftime("%Y-%m-%d") if admission_date else None,
            "discharge_date": discharge_date.strftime("%Y-%m-%d") if discharge_date else None,
        })

    df = pd.DataFrame(patients)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    out_path = os.path.join(PROCESSED_DIR, "patients_processed.csv")
    df.to_csv(out_path, index=False)

    print(f"Generated {len(df)} sample patients")
    print(f"  - {len(df[df['status']==STATUS_REGISTERED])} Registered")
    print(f"  - {len(df[df['status']==STATUS_ONGOING])} Ongoing")
    print(f"  - {len(df[df['status']==STATUS_COMPLETED])} Completed")

    return df


def load_patients():
    """Load existing patient CSV if available, otherwise generate"""
    csv_path = os.path.join(PROCESSED_DIR, "patients_processed.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} patients from {csv_path}")
        return df
    else:
        print("No patient CSV found, generating sample data...")
        return generate_patients()


if __name__ == "__main__":
    hospitals = load_hospitals()
    print(f"\nHospitals shape: {hospitals.shape}")
    print(hospitals.head())

    patients = generate_patients(500)
    print(f"\nPatients shape: {patients.shape}")
    print(patients.head(10))
