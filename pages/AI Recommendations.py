import streamlit as st
import openai

# Set page configuration
st.set_page_config(
    page_title="School Budget Simulation",
    layout="wide"
)

# Apply custom CSS for background and text color
st.markdown(
    """
    <style>

        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
        
        {
            font-family: 'Montserrat', sans-serif;
        }
        
        body {
            background-color: #E3F2FD; /* Light blue background */
            color: #0D47A1; /* Dark blue text */
        }
        .stTextInput>div>div>input {
            background-color: #FFFFFF; /* White input fields */
            color: #0D47A1;
        }
        .stSelectbox>div>div>div {
            color: #0D47A1;
        }
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

# Retrieve OpenAI API key from Streamlit secrets
openai_key = st.secrets.get("openai_key")

if not openai_key:
    st.error("🚨 Missing OpenAI API key! Please set 'openai_key' in Streamlit secrets.")
    st.stop()

# Configure OpenAI API key
client = openai.OpenAI(api_key=openai_key)  # ✅ Use OpenAI's new client method

# Store chatbot state
if "recommendation" not in st.session_state:
    st.session_state.recommendation = ""
if "chat_response" not in st.session_state:
    st.session_state.chat_response = ""

def generate_recommendations():
    metric = st.selectbox(
        "What area would you like to modify?",
        ["Choose an option", "Spending Per Student", "Student-Teacher Ratio", "Per-Pupil Instructional Spending"],
    )

    change = st.selectbox(
        "Would you like to increase or decrease?",
        ["Choose an option", "Increase", "Decrease"],
    )

    if st.button("Simulate Recommendations"):
        if metric != "Choose an option" and change != "Choose an option":
            prompt = f"A school wants to {change.lower()} its {metric.lower()}. Provide specific recommendations on how they can achieve this goal while maintaining educational quality."
            
            # Display a loading message while waiting for response
            with st.status("⏳ Generating recommendations, please wait..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "system", "content": prompt}]
                    )
                    st.session_state.recommendation = response.choices[0].message.content
                    st.success("✅ Recommendations generated successfully!")
                    st.write(f"**Generated Recommendations:**\n\n{st.session_state.recommendation}")
                except Exception as e:
                    st.error(f"Error generating recommendations: {e}")

    if st.session_state.recommendation:
        st.header("Ask Questions About the Recommendations")
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
                    st.write(f"**Chatbot Response:** {st.session_state.chat_response}")
                except Exception as e:
                    st.error(f"Error generating chatbot response: {e}")

st.title("📚 School Budget Simulation and AI Recommendations")
generate_recommendations()
