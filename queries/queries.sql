1. Средний FBG и BMI по типу диабета
SELECT 
    dm_type, 
    AVG(fbg) AS avg_fbg,
    AVG(bmi) AS avg_bmi
FROM view1_patients_1
GROUP BY dm_type;

-- 2. Пациенты с самой высокой глюкозой (TOP-5)
SELECT 
    full_name, age, sex, fbg, bmi
FROM view1_patients_1
ORDER BY fbg DESC
LIMIT 5;

-- 3. Распределение пациентов по возрастным группам с оконной функцией
SELECT 
    patient_ID,
    full_name,
    age,
    sex,
    NTILE(4) OVER (ORDER BY age) AS age_quartile
FROM view1_patients_1;

-- 4. Пациенты, у которых есть и невропатия, и нефропатия
SELECT *
FROM view1_patients_1
WHERE LOWER(neuropathy) = 'yes' AND LOWER(nephropathy) = 'yes';

-- 5. Подсчёт количества пациентов по полу и типу диабета
SELECT sex, dm_type, COUNT(*) AS total
FROM view1_patients_1
GROUP BY sex, dm_type
ORDER BY sex;
