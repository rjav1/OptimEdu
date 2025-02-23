import streamlit as st
import pandas as pd


st.set_page_config(page_title="OptimEdu Data Uploader", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

        /* Apply Montserrat font globally */
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

        /* Styling for subheaders */
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


with st.container():
    st.markdown("""
        <div class='title-container'>
            <h1 style="margin: 0;">📊 OptimEdu Data Uploader</h1>
            <h3>Empowering Schools with Data-Driven Budget Decisions 📚✨</h3>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<h2 class='custom-subheader'>📌 CSV Formatting Instructions</h2>", unsafe_allow_html=True)


st.markdown("""
To ensure your file is uploaded correctly to the **OptimEdu Data Uploader**, format your CSV file as follows:
""")


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


st.markdown("<h3 class='custom-subheader'>✅ Upload Instructions</h3>", unsafe_allow_html=True)

st.markdown("""
1. Save the file as `.csv` with **comma-separated values**.
2. Ensure **column names match exactly** as shown.
3. Click **Upload CSV File** in the Budget Forecaster.
""")

st.success("Follow these steps to ensure a smooth upload! 🚀")



uploaded_file = st.file_uploader("Upload a .csv file", type=["csv"])

if uploaded_file is not None:
   
    df = pd.read_csv(uploaded_file)

    
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    if "county-year" in df.columns:
        df["county"] = df["county-year"].str.extract(r'^(.*?)-\d{4}$')  
        df["year"] = df["county-year"].str.extract(r'-(\d{4})$') 
        df["year"] = pd.to_numeric(df["year"], errors="coerce")  


        df.dropna(subset=["year"], inplace=True)
        df["year"] = df["year"].astype(int)

     
        if df["county"].isna().all() or df["year"].isna().all():
            st.error("⚠️ Could not extract 'county' or 'year' from 'county-year'. Ensure format is 'CountyName-YYYY' (e.g., 'Gwinnett-2019').")
        else:
           
            county_list = sorted(df["county"].unique())
            selected_county = st.selectbox("Select a County", county_list)

           
            year_list = sorted(df["year"].unique(), reverse=True)
            selected_year = st.selectbox("Select a Year", year_list)

          
            filtered_data = df[(df["county"] == selected_county) & (df["year"] == selected_year)]

            if not filtered_data.empty:
                st.markdown(f"<h3 class='custom-subheader'>📊 Data for {selected_county} in {selected_year}</h3>", unsafe_allow_html=True)

               
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
