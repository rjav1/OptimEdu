import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Budget Forecaster", layout="wide")

# Custom CSS for Montserrat Font and Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
        
        /* Apply Montserrat font globally */
        * {
            font-family: 'Montserrat', sans-serif;
        }

        /* Styling for titles and headers */
        .custom-title {
            font-weight: 700;
            font-size: 48px;
            text-align: center;
            color: #FFFFFF;
            margin-bottom: 10px;
        }

        .custom-subheader {
            font-weight: 600;
            font-size: 28px;
            text-align: center;
            color: #FFFFFF;
            margin-bottom: 20px;
        }

        /* Tables */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }

        /* Success and Info Messages */
        .stSuccess, .stInfo, .stWarning, .stError {
            font-weight: 500;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Title (Now using HTML to ensure Montserrat applies)
st.markdown("<h1 class='custom-title'>Budget Forecaster</h1>", unsafe_allow_html=True)

st.markdown("<h2 class='custom-subheader'>📌 CSV Formatting Instructions</h2>", unsafe_allow_html=True)

# Instructions
st.markdown("""
To ensure your file is uploaded correctly to the **Budget Forecaster**, format your CSV file as follows:
""")

# Required Columns Table
st.markdown("<h3 class='custom-subheader'>✅ Required Columns</h3>", unsafe_allow_html=True)

columns_data = {
    "Column Name": [
        "county-year", "spending_per_student", "student_teacher_ratio", 
        "per_pupil_instructional_spending", "math_score", "reading_score",
        "graduation_rate", "higher_education_pursuit_rate"
    ],
    "Description": [
        "County and year (e.g., Gwinnett-2019).",
        "Amount spent per student in USD.",
        "Student-to-teacher ratio.",
        "Instructional spending per student.",
        "Average math score.",
        "Average reading score.",
        "High school graduation rate (%).",
        "Higher education pursuit rate (%)."
    ]
}
st.table(pd.DataFrame(columns_data))

# Example CSV Format
st.markdown("<h3 class='custom-subheader'>✅ Example CSV Format</h3>", unsafe_allow_html=True)

sample_data = {
    "county-year": ["Gwinnett-2019", "Fulton-2020", "Cobb-2021"],
    "spending_per_student": [11500, 12000, 11000],
    "student_teacher_ratio": [16, 15, 17],
    "math_score": [275, 280, 270],
    "reading_score": [280, 285, 275],
    "graduation_rate": [87, 89, 85]
}
st.table(pd.DataFrame(sample_data))

# Upload Instructions
st.markdown("<h3 class='custom-subheader'>✅ Upload Instructions</h3>", unsafe_allow_html=True)

st.markdown("""
1. Save the file as `.csv` with **comma-separated values**.
2. Ensure **column names match exactly** as shown.
3. Click **Upload CSV File** in the Budget Forecaster.
""")

st.success("Follow these steps to ensure a smooth upload! 🚀")


# File Upload Section
uploaded_file = st.file_uploader("Upload a .csv file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Standardize column names (convert to lowercase and replace spaces with underscores)
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Ensure 'county-year' exists
    if "county-year" in df.columns:
        # Extract county name (without year) and create a new 'county' column
        df["county"] = df["county-year"].str.extract(r'^(.*?)-\d{4}$')  # Extracts only the county name
        df["year"] = df["county-year"].str.extract(r'-(\d{4})$')  # Extracts the 4-digit year
        df["year"] = pd.to_numeric(df["year"], errors="coerce")  # Convert year to integer

        # Drop rows with invalid year values
        df.dropna(subset=["year"], inplace=True)
        df["year"] = df["year"].astype(int)

        # Ensure extraction was successful
        if df["county"].isna().all() or df["year"].isna().all():
            st.error("⚠️ Could not extract 'county' or 'year' from 'county-year'. Ensure format is 'CountyName-YYYY' (e.g., 'Gwinnett-2019').")
        else:
            # Dropdown for selecting a county (only names, no year)
            county_list = sorted(df["county"].unique())
            selected_county = st.selectbox("Select a County", county_list)

            # Dropdown for selecting a year (only years, no county-year mix)
            year_list = sorted(df["year"].unique(), reverse=True)
            selected_year = st.selectbox("Select a Year", year_list)

            # Filter data based on selected county and year
            filtered_data = df[(df["county"] == selected_county) & (df["year"] == selected_year)]

            if not filtered_data.empty:
                st.markdown(f"<h3 class='custom-subheader'>📊 Data for {selected_county} in {selected_year}</h3>", unsafe_allow_html=True)

                # Display relevant data
                fields = [
                    "spending_per_student", "student_teacher_ratio", 
                    "per_pupil_instructional_spending", "math_score", "reading_score", 
                    "graduation_rate", "higher_education_pursuit_rate"
                ]

                for field in fields:
                    value = filtered_data[field].values[0] if field in filtered_data.columns else "N/A"
                    st.markdown(f"**{field.replace('_', ' ').title()}:** {value}")

            else:
                st.warning(f"⚠️ No data available for {selected_county} in {selected_year}.")
    else:
        st.error("CSV file must contain a 'county-year' column with format 'CountyName-YYYY' (e.g., 'Gwinnett-2019').")

else:
    st.info("📤 Please upload a CSV file to proceed.")
