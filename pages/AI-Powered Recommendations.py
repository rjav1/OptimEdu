import streamlit as st
import openai


st.set_page_config(
    page_title="AI-Powered Recommendations",
    layout="wide"
)


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

        /* Select Boxes - Apply Tan Color to Placeholder */
        div[data-baseweb="select"] > div {
            color: #F5E0B7 !important;  /* Tan color for 'Choose an option' */
        }


    </style>
    """,
    unsafe_allow_html=True
)


with st.container():
    st.markdown("""
        <div class='title-container'>
            <h1 style="margin: 0;">📚 AI-Powered Recommendations</h1>
            <h3>AI-Based Recommendations for Smarter Educational Spending 💰</h3>
        </div>
    """, unsafe_allow_html=True)


openai_key = st.secrets.get("openai_key")

if not openai_key:
    st.error("🚨 Missing OpenAI API key! Please set 'openai_key' in Streamlit secrets.")
    st.stop()


client = openai.OpenAI(api_key=openai_key)  # ✅ Use OpenAI's new client method


if "recommendation" not in st.session_state:
    st.session_state.recommendation = ""
if "chat_response" not in st.session_state:
    st.session_state.chat_response = ""

def generate_recommendations():
    st.markdown("<h2 style='text-align: center; color: white;'>📊 Choose Budget Modification Area</h2>", unsafe_allow_html=True)

    metric = st.selectbox(
        "What area would you like to modify?",
        ["Choose an option", "Spending Per Student", "Student-Teacher Ratio", "Per-Pupil Instructional Spending"],
    )

    change = st.selectbox(
        "Would you like to increase or decrease?",
        ["Choose an option", "Increase", "Decrease"],
    )

    if st.button("🚀 Simulate Recommendations"):
        if metric != "Choose an option" and change != "Choose an option":
            prompt = f"A school wants to {change.lower()} its {metric.lower()}. Provide specific recommendations on how they can achieve this goal while maintaining educational quality."
            
            with st.status("⏳ Generating recommendations, please wait..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "system", "content": prompt}]
                    )
                    st.session_state.recommendation = response.choices[0].message.content
                    st.success("✅ Recommendations generated successfully!")
                    st.markdown(f"<h3 style='color: #0D47A1;'>📌 Generated Recommendations:</h3>", unsafe_allow_html=True)
                    st.write(st.session_state.recommendation)
                except Exception as e:
                    st.error(f"Error generating recommendations: {e}")

    if st.session_state.recommendation:
        st.markdown("<h2 style='text-align: center; color: #0D47A1;'>💬 Ask Questions About the Recommendations</h2>", unsafe_allow_html=True)
        user_question = st.text_input("Enter your question about the recommendations:")
        if user_question:
            with st.status("⏳ Generating response..."):
                try:
                    chat_response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": f"Based on these recommendations: {st.session_state.recommendation}, answer this question: {user_question}"}
                        ]
                    )
                    st.session_state.chat_response = chat_response.choices[0].message.content
                    st.success("✅ Response generated successfully!")
                    st.markdown(f"<h3 style='color: #0D47A1;'>🤖 Chatbot Response:</h3>", unsafe_allow_html=True)
                    st.write(st.session_state.chat_response)
                except Exception as e:
                    st.error(f"Error generating chatbot response: {e}")

generate_recommendations()
