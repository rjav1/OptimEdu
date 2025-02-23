import streamlit as st

st.set_page_config(
    page_title="OptimEdu | Empowering Schools",
    page_icon="💰",
    layout="wide"
)

st.markdown(
    """
    <style>
        /* Ensure uniform image size & border radius */
        .team-img {
            border-radius: 2px !important; /* Apply 2px border radius */
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #544B6A, #268AD6);
                    padding: 2.5rem;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                    margin-bottom: 20px;">
            <h1 style="margin: 0;">📊 OptimEdu 💰</h1>
            <h3>Empowering Schools with Data-Driven Budget Decisions 📚✨</h3>
        </div>
    """, unsafe_allow_html=True)

st.divider()

st.markdown("<h2 style='text-align: center;'>🤝 Meet the Team</h2>", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns(3)

    team_members = [
        {"name": "Mahika Batra", "role": "CS @ Georgia Tech", "image": "images/mahika.png"},
        {"name": "Rahil Javid", "role": "Mathematics @ Georgia Tech", "image": "images/rahil.png"},
        {"name": "Aryan Vaidya", "role": "Industrial Engineering @ Georgia Tech", "image": "images/aryan.png"},
    ]

    for col, member in zip([col1, col2, col3], team_members):
        with col:
            st.image(member["image"], use_container_width=True) 
            st.markdown(f"""
                <div style="text-align: center; margin-top: 10px;">
                    <h3 style="margin: 5px 0 3px;">{member['name']}</h3>
                    <p style="color: #bbb; font-size: 16px; font-weight: bold;">{member['role']}</p>
                </div>
            """, unsafe_allow_html=True)

st.divider()

st.markdown("<h2 style='text-align: center;'>📌 Project Overview</h2>", unsafe_allow_html=True)

st.markdown("""
    <p style="text-align: center; font-size: 18px;">
        🏫 The <b>Budget Forecaster</b> leverages <b>AI and data analytics</b> to provide schools 
        with <b>smart financial insights</b>, ensuring <b>better resource allocation</b> 📊 and 
        <b>optimized student outcomes</b> 🎯.
    </p>
    <p style="text-align: center; font-size: 18px;">
        💡 <b>Our goal</b> is to make <b>data-driven decision-making</b> accessible to 
        <b>every educational institution</b>, enabling smarter <b>budget planning</b> 💰.
    </p>
""", unsafe_allow_html=True)
