#!/usr/bin/env python
# -*- coding: utf-8 -*-
 prostate cancer bone metastasis survival prediction
""" prostate cancer prostate cancer bone metastasis survival prediction
 prostate cancer bone metastasis survival prediction - Interactive web application
Based on Extra Survival Trees model
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os


def load_model_and_info():
    """Load trained model and configuration information"""
    try:
        model = joblib.load('extra_survival_trees_model.pkl')
        with open('model_info.json', 'r', encoding='utf-8') as f:
            model_info = json.load(f)
        return model, model_info
    except FileNotFoundError:
        st.error("❌ Model file not found! Please run train_model.py first to train the model.")
        st.info("To deploy on Streamlit Cloud, make sure to include these files:")
        st.code("""
- app.py
- train_model.py
- data.csv
- extra_survival_trees_model.pkl
- model_info.json
- requirements.txt
        """)
        return None, None


def main():
    st.set_page_config(
        page_title=" prostate cancer bone metastasis survival prediction",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🏥 prostate cancer bone metastasis survival prediction System")
    st.markdown("---")

    st.sidebar.markdown("## ℹ️ Model Information")

    model, model_info = load_model_and_info()

    if model is None:
        st.stop()

    # Display model information
    st.sidebar.info(f"""
    **Model Type**: {model_info['model_type']}

    **Evaluation Metrics**:
    - C-index: {model_info['c_index']:.4f}
    - Training Samples: {model_info['training_samples']}
    - Test Samples: {model_info['test_samples']}

    **Model Parameters**:
    - n_estimators: {model_info['n_estimators']}
    - max_depth: {model_info['max_depth']}
    - min_samples_split: {model_info['min_samples_split']}
    """)

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📋 Input Instructions")
    st.sidebar.info("""
    Please enter the patient's clinical features:

    - **PSA**: Prostate Specific Antigen (ng/mL)
    - **Bone Metastasis**: Whether there is bone metastasis (0=no, 1=yes)
    - **Age**: Patient's age
    - **T stage**: Primary tumor staging (1-4)
    - **N stage**: Lymph node metastasis staging (0-1)
    - **Gleason Score**: Pathological grading score (6-10)
    """)

    # User input interface
    st.header("📊 Patient Feature Input")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Biochemical Indicators")
        psa = st.number_input(
            "PSA (Prostate Specific Antigen)",
            min_value=0.0,
            max_value=1000.0,
            value=50.0,
            step=0.1,
            help="Normal value is usually < 4 ng/mL"
        )

        metastasis = st.selectbox(
            "Bone Metastasis (combine_metastasis)",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            index=0,
            help="0=No bone metastasis, 1=Have bone metastasis"
        )

    with col2:
        st.subheader("Clinical Staging")

        age = st.number_input(
            "Age (years)",
            min_value=30,
            max_value=100,
            value=65,
            step=1
        )

        t_stage = st.selectbox(
            "T Stage (Primary Tumor)",
            options=[1, 2, 3, 4],
            index=1,
            help="""
            T1: Tumor cannot be palpated, usually discovered by biopsy
            T2: Tumor confined to the prostate
            T3: Tumor invades the prostate capsule or seminal vesicles
            T4: Tumor invades other organs such as bladder neck, rectum
            """
        )

        n_stage = st.selectbox(
            "N Stage (Lymph Nodes)",
            options=[0, 1],
            format_func=lambda x: "N0(No Metastasis)" if x == 0 else "N1(Metastasis)",
            index=0,
            help="N0=No lymph node metastasis, N1=Has lymph node metastasis"
        )

        gleason = st.selectbox(
            "Gleason Score",
            options=[6, 7, 8, 9, 10],
            index=2,
            help="""
            6 points: Low risk
            7 points: Medium risk
            8-10 points: High risk
            """
        )

    st.markdown("---")

    # Prediction button
    if st.button("🔍 Start Prediction", type="primary", use_container_width=True):
        st.success("✅ Performing prediction...")

        # Construct input data
        input_data = pd.DataFrame({
            'PSA': [psa],
            'combine_metastasis': [metastasis],
            'Age': [age],
            'T_stage': [t_stage],
            'N_stage': [n_stage],
            'Gleason': [gleason]
        })

        # Predict risk score
        risk_score = model.predict(input_data)[0]

        # Calculate risk level
        if os.path.exists('data.csv'):
            df_train = pd.read_csv('data.csv')
            X_train = df_train[['PSA', 'combine_metastasis', 'Age', 'T_stage', 'N_stage', 'Gleason']]
            train_risks = model.predict(X_train)
            risk_level = "Low Risk" if risk_score < np.percentile(train_risks, 33) else \
                        "Medium Risk" if risk_score < np.percentile(train_risks, 66) else "High Risk"
        else:
            risk_level = "Medium Risk"

        # Get survival function
        try:
            surv_func = model.predict_survival_function(input_data)[0]

            # Extract survival probabilities for 12, 24, 36, 60 months
            time_points = [12, 24, 36, 60]
            survival_probs = [surv_func(t) for t in time_points]

            # Display prediction results
            st.header("📈 Prediction Results")

            # Risk score and level
            col_risk1, col_risk2 = st.columns(2)

            with col_risk1:
                st.metric(
                    label="Risk Score",
                    value=f"{risk_score:.4f}",
                    help="Higher risk score indicates worse prognosis"
                )

            with col_risk2:
                if risk_level == "Low Risk":
                    st.metric(label="Risk Level", value="Low Risk", delta="✓")
                elif risk_level == "Medium Risk":
                    st.metric(label="Risk Level", value="Medium Risk")
                else:
                    st.metric(label="Risk Level", value="⚠ High Risk")

            st.markdown("---")

            # Survival probability table
            st.subheader("📊 Survival Probability Prediction")

            survival_data = {
                "Time Point": [f"{t} months" for t in time_points],
                "Survival Probability": [f"{prob*100:.1f}%" for prob in survival_probs]
            }
            st.dataframe(
                pd.DataFrame(survival_data),
                use_container_width=True,
                hide_index=True
            )

            # Survival probability visualization
            st.markdown("---")
            st.subheader("📉 Survival Curve")

            import matplotlib.pyplot as plt

            times_array = np.arange(0, 61, 1)
            probs_array = [surv_func(t) for t in times_array]

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(times_array, probs_array, linewidth=3, color='#1f77b4')

            for t, prob in zip(time_points, survival_probs):
                ax.scatter(t, prob, s=200, color='red', zorder=5)
                ax.annotate(f"{prob*100:.1f}%",
                           (t, prob),
                           textcoords="offset points",
                           xytext=(0, 10),
                           ha='center',
                           fontsize=10,
                           fontweight='bold')

            ax.set_xlabel('Time (months)', fontsize=12)
            ax.set_ylabel('Survival Probability', fontsize=12)
            ax.set_title('Predicted Survival Curve', fontsize=14, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_ylim(0, 1.05)

            st.pyplot(fig)

            # Clinical recommendations
            st.markdown("---")
            st.subheader("💡 Clinical Recommendations")

            if risk_level == "Low Risk":
                st.info("""
                **Recommendations for Low-risk Patients:**

                - Regular follow-up, PSA test and clinical assessment every 6-12 months
                - Maintain a healthy lifestyle
                - Seek medical attention immediately if symptoms change
                """)
            elif risk_level == "Medium Risk":
                st.warning("""
                **Recommendations for Medium-risk Patients:**

                - Close follow-up, assessment every 3-6 months
                - Consider more active monitoring strategies
                - Consider adjuvant therapy based on condition
                - Regular imaging examinations
                """)
            else:
                st.error("""
                **Recommendations for High-risk Patients:**

                - Needs close monitoring and active treatment
                - Recommend multidisciplinary team (MDT) consultation
                - Consider comprehensive treatment plan: surgery + radiotherapy + endocrine therapy
                - More frequent follow-up (every 1-3 months)
                - Focus on quality of life and supportive care
                """)

            # Input feature summary
            st.markdown("---")
            st.subheader("📋 Input Feature Summary")

            feature_summary = {
                "Feature": ["PSA", "Bone Metastasis", "Age", "T Stage", "N Stage", "Gleason Score"],
                "Value": [
                    f"{psa} ng/mL",
                    "Yes" if metastasis else "No",
                    f"{age} years old",
                    f"T{t_stage}",
                    f"N{n_stage}",
                    f"{gleason} points"
                ]
            }
            st.dataframe(
                pd.DataFrame(feature_summary),
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:
            st.error(f"❌ Error during prediction: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>⚠️ Disclaimer: This system is for medical research and educational reference only and cannot replace professional medical diagnosis and treatment advice.</p>
        <p>Please consult a professional physician before making clinical decisions.</p>
        <p>Model: Extra Survival Trees | Data Source: SEER Database</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
