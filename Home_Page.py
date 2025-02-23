import streamlit as st

# Page Configuration
st.set_page_config(page_title="Home | Budget Forecaster", layout="wide")

# Custom CSS for Centering & Modern Design with Montserrat Font
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
        
        /* Apply Montserrat font to entire page */
        * {
            font-family: 'Montserrat', sans-serif;
        }

        /* Full-width centered gradient title section */
        .title-box {
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 36px;
            background: linear-gradient(to right, #1E3A5F, #567C8D);
            color: #FFFFFF;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
            margin-bottom: 20px;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .subtext {
            text-align: center;
            font-size: 22px;
            font-weight: 600;
            color: #FFFFFF;
        }



        /* Full-width Team Member Cards */


        /* Circular Image with Full-Width Scaling */
        .image-box img {
            width: 200px;
            height: 200px;
            border-radius: 50%; /* Fully Circular */
            object-fit: cover;
            display: block;
            margin: auto;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }

        /* Name & Description */
        .name {
            font-size: 24px;
            font-weight: 700;
            color: #FFFFFF;
            margin-top: 15px;
        }

        .description {
            font-size: 18px;
            font-weight: 400;
            color: #DDE6F0;
            margin-top: 5px;
        }

        /* Center Content */
        .center-content {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)

# Title Section with Gradient Background
st.markdown("<div class='title-box'>📊 Budget Forecaster 💰</div>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Empowering Schools with Data-Driven Decisions 📚✨</p>", unsafe_allow_html=True)

# Meet the Team Section
st.divider()
st.markdown("<h2 class='center-text'>🤝 Meet the Team</h2>", unsafe_allow_html=True)

# Full-Width Centered Team Members
st.markdown('<div class="section-bg center-content">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown('<div class="team-box">', unsafe_allow_html=True)
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.image("images/mahika.png")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<p class='name'>🏭 <b>Mahika Batra</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='description'>CS @ Georgia Tech</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="team-box">', unsafe_allow_html=True)
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.image("images/rahil.png")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<p class='name'>🔢 <b>Rahil Javid</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Mathematics @ Georgia Tech</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="team-box">', unsafe_allow_html=True)
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.image("images/aryan.png")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<p class='name'>💾 <b>Aryan Vaidya</b></p>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Industrial Engineering @ Georgia Tech</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Project Overview Section with Background Color
st.divider()
st.markdown("<h2 class='center-text'>📌 Project Overview</h2>", unsafe_allow_html=True)

st.markdown("""
    <div class="section-bg center-content">
        <p class='description'>
            🏫 The <b>Budget Forecaster</b> project leverages AI to provide schools 
            with smart insights into optimizing their budgets 💡, ensuring better 
            student outcomes 📈 while maximizing efficiency. 
        </p>
        <p class='description'>
            🎯 Our goal is to make data-driven decisions accessible, so every 
            institution can plan smarter and improve their financial strategies! 💰📊
        </p>
    </div>
""", unsafe_allow_html=True)
