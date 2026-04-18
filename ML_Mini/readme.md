# Student Dropout Risk Predictor

## Overview

This project presents a machine learning-based web application designed to predict the likelihood of student dropout. The system leverages academic and financial indicators to estimate risk levels and provide actionable recommendations for early intervention.

The application is deployed using Streamlit, enabling real-time interaction and prediction through a simple user interface.

---

## Objectives

* Develop a predictive model for student dropout risk
* Address class imbalance in educational datasets
* Compare multiple models to identify the most effective approach
* Provide interpretable outputs for decision-making

---

## Methodology

### Models Implemented

* Logistic Regression
* Random Forest
* Gradient Boosting (selected as the final model based on performance)

### Evaluation Strategy

Models were evaluated using the F1-score due to class imbalance, ensuring balanced consideration of precision and recall.

### Data Handling Techniques

* SMOTE (Synthetic Minority Oversampling Technique) was applied to handle class imbalance
* Hyperparameter tuning was performed to optimize model performance
* Feature selection focused on academically and financially relevant variables

---

## Features Used

* Age at enrollment
* Scholarship status
* Debt status
* Tuition fee status
* Academic performance (Semester 1 and Semester 2)

---

## System Functionality

### Inputs

Users provide student-related information including academic performance and financial status.

### Outputs

* Dropout probability (continuous value)
* Risk classification (Low / Medium / High)
* Key contributing factor
* Suggested intervention strategy

---

## Technology Stack

* Python
* Streamlit
* Scikit-learn
* Pandas, NumPy

---

## Execution

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
streamlit run app.py
```

---

## Limitations

* Model performance depends on dataset quality and representativeness
* Limited feature scope (does not include behavioral or psychological factors)
* Predictions should support, not replace, institutional decision-making

---

## Future Work

* Incorporate additional features such as attendance and behavioral metrics
* Improve model interpretability (e.g., SHAP or feature importance visualization)
* Enhance UI/UX for better usability
* Deploy as a scalable web service

---

## Author

Angel Xavier
