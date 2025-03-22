CREATE TABLE IF NOT EXISTS patients_1 (
    patient_ID INTEGER PRIMARY KEY,
    full_name VARCHAR(100),
    age INTEGER,
    sex VARCHAR(10),
    occupation VARCHAR(100),
    address VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS diabetic_retinopathy_1 (
    patient_ID INTEGER PRIMARY KEY,
    dm_type VARCHAR(50),
    renal_function VARCHAR(50),
    duration INTEGER,
    diabetic_retinopathy VARCHAR(50),
    fbg INTEGER,
    hereditary VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS diseases_1 (
    patient_ID INTEGER PRIMARY KEY,
    neuropathy VARCHAR(50),
    nephropathy VARCHAR(50),
    smoking VARCHAR(50),
    bmi INTEGER
);
