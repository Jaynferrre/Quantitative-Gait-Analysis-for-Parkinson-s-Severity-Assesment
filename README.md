# Quantitative-Gait-Analysis-for-Parkinson-s-Severity-Assesment
This is my submission for my course project requirement for DH302(Introduction to Public Health Informatics) by KCDH, IIT Bombay, working under Professors Saket Choudhary and Nirmal Punjabi in the Autumn Semester, 2025. I collaborated with Ishan Yadu, from ESED IIT Bombay on this project.
---
## Problem Statement
- Parkinson’s Disease is a **progressive neurodegenerative disorder** primarily caused by a deficiency of dopamine in the brain. This chemical imbalance leads to debilitating motor symptoms that significantly impair quality of life.
- Patients typically present with *bradykinesia* (slowness of movement), rigidity, resting tremors, and postural instability. As the disease progresses, these
symptoms disrupt daily mobility and increase the risk of falls.
---
## Societal Impact 
- Experts estimate that India is poised to have the highest absolute prevalence of the disease globally, with rates ranging from 15 to 43 per 100,000 people. Most alarmingly, the demographic profile is shifting younger.
- Approximately **40-45%** of Indian patients present with **Early Onset Parkinson’s Disease (EOPD)**, experiencing motor symptoms between the ages of **22 and 49**.
- The average age of onset in India is now 51 years, nearly a decade younger than the global average, necessitating immediate and scalable diagnostic interventions.
- Currently, management relies on a combination of pharmacological treatments like *Levodopa*, surgical interventions such as Deep Brain Stimulation (DBS), and holistic care including nutrition and physiotherapy.
- However, accurate tracking of these motor symptoms is crucial for effective management
---
## [Dataset](https://physionet.org/content/gaitpdb/1.0.0/) 
- This balanced cohort of **166 participants** includes 93 Parkinson’s patients and 73 healthy controls, age-matched at a mean of 66.3 years to strictly isolate pathology from aging. The dataset reflects the *Hoehn & Yahr stages*[^1] (1.5–3) and UPDRS scores
- This study quantifies gait dynamics using **Vertical Ground Reaction Force (VGRF)** sensors. The data was collected using specialized insoles with eight sensors located under each foot, recording force measures at 100 samples per second
---
## Hypothesis 
Gait kinematic parameters (specifically gait speed and Timed Up and Go duration), when integrated with demographic factors (Age, BMI), serve as robust, non-invasive biomarkers for classifying the severity of Parkinson's Disease(*Hoehn & Yahr stages*[^1])
---
## Key Clinical Variables
1. The *Hoehn & Yahr*[^1] Scale provides a staging system for disease progression, ranging from 1 (mild, unilateral) to 5 (wheelchair-bound); our dataset largely focuses on early-to-moderate stages.
2. We also analyze the Unified Parkinson’s Disease Rating Scale (UPDRS)[^2], where higher scores indicate greater disability.
3. Functional mobility is captured via the Timed Up and Go (TUAG)[^3] test, measuring the time to stand, walk, and sit, where times exceeding 12 seconds suggest a high fall risk.
4. Gait Speed serves as a vital functional vital sign, often reduced significantly in the PD cohort.

[^1] : Read about them [here.](https://www.ncbi.nlm.nih.gov/books/NBK379751/)
[^2] : Read about them [here.](https://www.parkinsons.va.gov/resources/UPDRS.asp)
[^3] : Read about them [here.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3094679/)
