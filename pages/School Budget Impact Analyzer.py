import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="School Budget Impact Analyzer", layout="wide")


st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

        * {
            font-family: 'Montserrat', sans-serif;
        }

        /* Gradient Title Section */
        .title-container {
            background: linear-gradient(135deg, #1E3A5F, #567C8D);
            padding: 2.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }

        /* Body Background */
        body {
            background-color: #E3F2FD; /* Light blue background */
            color: #0D47A1; /* Dark blue text */
        }

        /* Input Fields */
        .stTextInput>div>div>input {
            background-color: #FFFFFF; /* White input fields */
            color: #0D47A1;
        }

        /* Select Boxes */
        .stSelectbox>div>div>div {
            color: #0D47A1;
        }

        /* Buttons */
        .stButton>button {
            background-color: #0D47A1 !important;
            color: white !important;
            border-radius: 8px;
            padding: 8px 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


with st.container():
    st.markdown("""
        <div class='title-container'>
            <h1 style="margin: 0;">📊 School Budget Impact Analyzer</h1>
            <h3>Data-Driven Insights for Smarter Educational Spending 💰</h3>
        </div>
    """, unsafe_allow_html=True)


uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "county-year" in df.columns:
        df["county"] = df["county-year"].str.extract(r'^(.+)-\d{4}$', expand=True)
        df["year"] = df["county-year"].str.extract(r'-(\d{4})$', expand=True)

        df.dropna(subset=["county", "year"], inplace=True)

        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

        df.dropna(subset=["year"], inplace=True)

        df.drop(columns=['county-year'], inplace=True)

        numeric_cols = [
            'spending_per_student',
            'per_pupil_instructional_spending',
            'student_teacher_ratio',
            'math_score',
            'reading_score',
            'graduation_rate',
            'higher_education_pursuit_rate'
        ]

      
        numeric_cols = [col for col in numeric_cols if col in df.columns]

       
        means = df[numeric_cols].mean()
        std_devs = df[numeric_cols].std()

  
        if numeric_cols:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

 
        independent_vars = ['spending_per_student', 'student_teacher_ratio', 'per_pupil_instructional_spending']
        dependent_vars = ['math_score', 'reading_score', 'graduation_rate', 'higher_education_pursuit_rate']


        independent_vars = [col for col in independent_vars if col in df.columns]


        label_map = {
            "spending_per_student": "Spending per Student ($)",
            "student_teacher_ratio": "Student-Teacher Ratio",
            "per_pupil_instructional_spending": "Per Pupil Instructional Spending ($)",
            "math_score": "Math Score",
            "reading_score": "Reading Score",
            "graduation_rate": "Graduation Rate (%)",
            "higher_education_pursuit_rate": "Higher Education Pursuit Rate (%)"
        }

   
        models = {}

        for dep_var in dependent_vars:
            if dep_var in df.columns:
                X = df[independent_vars]
                y = df[dep_var]
                X = sm.add_constant(X) 

                model = sm.OLS(y, X).fit()
                models[dep_var] = model  

                st.markdown(f"### 📊 Partial Regression Plots for {label_map[dep_var]}")
                fig, axes = plt.subplots(1, len(independent_vars), figsize=(15, 5))

                for i, col in enumerate(independent_vars):
                    x_original = df[col] * std_devs[col] + means[col]
                    y_original = df[dep_var] * std_devs[dep_var] + means[dep_var]

                    sns.regplot(
                        x=x_original, 
                        y=y_original, 
                        ax=axes[i], 
                        ci=None,
                        scatter_kws={"alpha": 0.4, "color": "gray", "s": 80},
                        line_kws={"color": "#2a818c", "linewidth": 2.5}
                    )

                   
                    if i == len(independent_vars) // 2:
                        axes[i].set_title(f'{label_map[dep_var]} vs Independent Variables', fontsize=14)

                    axes[i].set_xlabel(label_map[col], fontsize=12)
                    axes[i].set_ylabel("") 
                    axes[i].grid(False)

                st.pyplot(fig)

        st.subheader("🎛️ Interactive Prediction Tool")

      
        user_inputs = {}
        for var in independent_vars:
            min_val = float(means[var] - 2 * std_devs[var])
            max_val = float(means[var] + 2 * std_devs[var])
            mean_val = float(means[var])

            user_inputs[var] = st.slider(
                f"Adjust {label_map[var]}",
                min_value=min_val,
                max_value=max_val,
                value=mean_val
            )

   
        user_input_df = pd.DataFrame([user_inputs])

     
        for col in independent_vars:
            user_input_df[col] = (user_input_df[col] - means[col]) / std_devs[col]

        user_input_df = sm.add_constant(user_input_df.reindex(columns=['const'] + independent_vars, fill_value=1.0))

    
        st.subheader("📊 Predicted Outcomes")

        for dep_var in dependent_vars:
            if dep_var in models:
                try:
                    prediction = models[dep_var].predict(user_input_df)[0]
                    prediction_original = prediction * std_devs[dep_var] + means[dep_var]

                    st.metric(
                        label=f"{label_map[dep_var]}",
                        value=f"{prediction_original:.2f}"
                    )
                except Exception as e:
                    st.error(f"Error predicting {dep_var}: {str(e)}")

    else:
        st.error("⚠️ CSV file must contain a 'county-year' column. Please check your file format.")
