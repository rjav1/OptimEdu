import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Ensure this is the first command to prevent errors
st.set_page_config(page_title="School Budget Impact Analyzer", layout="wide")



st.title("📊 School Budget Impact Analyzer")

# File Upload Section
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_csv(uploaded_file)

    # Ensure 'county-year' column exists before proceeding
    if "county-year" in df.columns:
        # Extract county name and year using regex
        df["county"] = df["county-year"].str.extract(r'^(.+)-\d{4}$', expand=True)
        df["year"] = df["county-year"].str.extract(r'-(\d{4})$', expand=True)

        # Drop rows where extraction failed
        df.dropna(subset=["county", "year"], inplace=True)

        # Convert year to integer safely
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

        # Drop rows with invalid years
        df.dropna(subset=["year"], inplace=True)

        # Drop the original "county-year" column
        df.drop(columns=['county-year'], inplace=True)

        # Columns to normalize (including student_teacher_ratio)
        numeric_cols = [
            'spending_per_student',
            'per_pupil_instructional_spending',
            'student_teacher_ratio',
            'math_score',
            'reading_score',
            'graduation_rate',
            'higher_education_pursuit_rate'
        ]

        # Ensure all numeric columns exist in the dataset
        numeric_cols = [col for col in numeric_cols if col in df.columns]

        # Store original means and standard deviations before normalization
        means = df[numeric_cols].mean()
        std_devs = df[numeric_cols].std()

        # Apply Z-score normalization
        if numeric_cols:
            scaler = StandardScaler()
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        # Define independent and dependent variables
        independent_vars = ['spending_per_student', 'student_teacher_ratio', 'per_pupil_instructional_spending']
        dependent_vars = ['math_score', 'reading_score', 'graduation_rate', 'higher_education_pursuit_rate']

        # Check if all independent variables exist
        independent_vars = [col for col in independent_vars if col in df.columns]

        # Define better labels for plot aesthetics
        label_map = {
            "spending_per_student": "Spending per Student ($)",
            "student_teacher_ratio": "Student-Teacher Ratio",
            "per_pupil_instructional_spending": "Per Pupil Instructional Spending ($)",
            "math_score": "Math Score",
            "reading_score": "Reading Score",
            "graduation_rate": "Graduation Rate (%)",
            "higher_education_pursuit_rate": "Higher Education Pursuit Rate (%)"
        }

        # Run regression models (store models for later prediction)
        models = {}

        for dep_var in dependent_vars:
            if dep_var in df.columns:
                # Prepare data
                X = df[independent_vars]
                y = df[dep_var]
                X = sm.add_constant(X)  # Add intercept

                # Fit the model
                model = sm.OLS(y, X).fit()
                models[dep_var] = model  # Store model for later predictions

                # Extract coefficients
                coefficients = model.params[1:]  # Skip the intercept

                # Calculate real-world impact (denormalized effect)
                st.write(f"🔹 **Real-World Impact for {label_map[dep_var]}**")
                for i, col in enumerate(independent_vars):
                    coef = coefficients[i]

                    # Reverse the standardization effect to get the actual impact per unit
                    std_dev_x = std_devs[col]  # Get standard deviation of the independent variable
                    std_dev_y = std_devs[dep_var]  # Get standard deviation of the dependent variable

                    real_world_impact = coef * (std_dev_y / std_dev_x)

                    # Convert to an interpretable format (e.g., per $500 increase in spending)
                    example_increase = std_dev_x / 2  # Example: Half a standard deviation increase
                    estimated_change = coef * (std_dev_y * example_increase / std_dev_x)

                    interpretation = (
                        f"An increase of {example_increase:.0f} units in {label_map[col]} "
                        f"is estimated to result in a {estimated_change:.2f} point change in {label_map[dep_var]}."
                    )
                    
                    st.write(interpretation)

                # Create improved scatter plots without gridlines and adjusted aesthetics
                st.write(f"📊 **Partial Regression Plots for {label_map[dep_var]}**")
                fig, axes = plt.subplots(1, len(independent_vars), figsize=(15, 5))

                for i, col in enumerate(independent_vars):
                    # Convert X and Y axes back to original values
                    x_original = df[col] * std_devs[col] + means[col]
                    y_original = df[dep_var] * std_devs[dep_var] + means[dep_var]

                    # Create a cleaner scatter plot with requested style changes
                    sns.regplot(
                        x=x_original, 
                        y=y_original, 
                        ax=axes[i], 
                        ci=None,  # Removes confidence interval shading
                        scatter_kws={"alpha": 0.4, "color": "gray", "s": 80},  # 20% transparency, gray dots
                        line_kws={"color": "#2a818c", "linewidth": 2.5}  # Blue regression line
                    )

                    # Improve labels and formatting
                    axes[i].set_title(f'{label_map[col]} vs {label_map[dep_var]}', fontsize=14)
                    axes[i].set_xlabel(label_map[col], fontsize=12)
                    axes[i].set_ylabel(label_map[dep_var], fontsize=12)
                    axes[i].grid(False)  # Remove gridlines

                st.pyplot(fig)

        # Interactive Section for Adjusting Variables
        st.subheader("🎛️ Interactive Prediction Tool")

        # Sliders for adjusting independent variables
        user_inputs = {}
        for var in independent_vars:
            # Calculate original min, max, and mean values
            min_val = float(means[var] - 2 * std_devs[var])  # 2 standard deviations below mean
            max_val = float(means[var] + 2 * std_devs[var])  # 2 standard deviations above mean
            mean_val = float(means[var])  # Original mean

            user_inputs[var] = st.slider(
                f"Adjust {label_map[var]}",
                min_value=min_val,
                max_value=max_val,
                value=mean_val
            )

        # Convert user input into a dataframe for prediction
        user_input_df = pd.DataFrame([user_inputs])

        # Normalize user inputs using the stored means and standard deviations
        for col in independent_vars:
            user_input_df[col] = (user_input_df[col] - means[col]) / std_devs[col]

        # Ensure independent variables match regression model format
        user_input_df = sm.add_constant(user_input_df.reindex(columns=['const'] + independent_vars, fill_value=1.0))

        # Display predicted values based on user inputs
        st.subheader("📊 Predicted Outcomes")

        for dep_var in dependent_vars:
            if dep_var in models:
                try:
                    # Predict using the normalized user inputs
                    prediction = models[dep_var].predict(user_input_df)[0]

                    # Convert prediction back to original units
                    prediction_original = prediction * std_devs[dep_var] + means[dep_var]

                    st.metric(
                        label=f"{label_map[dep_var]}",
                        value=f"{prediction_original:.2f}"
                    )
                except Exception as e:
                    st.error(f"Error predicting {dep_var}: {str(e)}")

        st.info("🔹 Adjust the sliders to see how changes in school funding impact student outcomes in real-time!")

    else:
        st.error("⚠️ CSV file must contain a 'county-year' column (e.g., 'Gwinnett-2019'). Please check your file format.")
else:
    st.info("📤 Please upload a CSV file to proceed.")
