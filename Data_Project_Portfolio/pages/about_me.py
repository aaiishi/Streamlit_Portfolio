import streamlit as st
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie


# -- CONTACT BUTTON & CV STATE --
if "show_contact" not in st.session_state:
    st.session_state["show_contact"] = False
if "show_cv" not in st.session_state:
    st.session_state["show_cv"] = False
    

# -- CONTACT BUTTON --
@st.dialog("Contact Me")
def show_contact_form():
    st.write("Feel free to reach out to me through the following channels :")
    st.markdown("📧 **Email :** [alexandre.poujol@efrei.net](mailto:alexandre.poujol@efrei.net)")
    st.markdown("📞 **Phone :** +33 6 63 42 86 75")
    st.markdown("🔗 **LinkedIn :** [linkedin.com/in/poujol-alexandre](https://www.linkedin.com/in/poujol-alexandre)")
    if st.button("Close", key="close_contact"):
        st.session_state["show_contact"] = False


# -- CV BUTTON --
@st.dialog("My CV")
def show_cv_download():
    st.write("Click the button below to download my CV :")
    st.download_button(
        label="📄 Alexandre Poujol's CV",
        data=open("./assets/CV.pdf", "rb").read(),
        file_name="CV_Alexandre_Poujol.pdf",
        mime="application/pdf",
    )
    if st.button("Close", key="close_cv"):
        st.session_state["show_cv"] = False


# -- ABOUT ME SECTION --
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile_picture.png", width=200)
with col2:
    st.title("Alexandre Poujol", anchor=False)
    st.write("Junior data enjoyer & student at Efrei Paris")
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        if st.button("💬 Contact Me", key="contact_button"):
            st.session_state["show_contact"] = True
    with button_col2:
        if st.button("📄 CV", key="cv_button"):
            st.session_state["show_cv"] = True
if st.session_state["show_contact"]:
    show_contact_form()
if st.session_state["show_cv"]:
    show_cv_download()


# -- LOOTTIE --
def load_lottieur(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_job = load_lottieur("https://lottie.host/8ae7ccc0-e844-42d5-bcf2-5aa1fa80fa92/4vUqQI9peO.json")
lottie_school = load_lottieur("https://lottie.host/94496657-d55c-4f85-b31e-a592829ff748/LZ3I1NshQV.json")
lottie_star = load_lottieur("https://lottie.host/3cbdea95-98eb-4aae-9c5e-0168ebd90425/kWrmautQbT.json")
lottie_home = load_lottieur("https://lottie.host/88c93d83-ce1d-4b67-946d-5d2e45615499/0Mv8FaIwfV.json")


# -- CONTAINER -- 
st.write("")
with st.container():
    selected = option_menu(
        menu_title = None,
        options = ["Home", "Experiences", "Qualifications", "Skills"],
        icons = ["house", "database", "award-fill", "check"],
        orientation = "horizontal"
    )

if selected == "Experiences":
    with st.container():
        col13, col14 = st.columns(2)
        with col14:
            st.write("##")
            st.subheader("I had two main professional experiences !")
            st.title("Here are these internships :")
        with col13:
            st.lottie(lottie_job)
    st.write("---")
    with st.container():
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("""
            THALES
            - Market Analyst
            - Security devices against war drones
            - Thales is a French electronics group specializing in aerospace, defense and security
            """)
        with col4:
            st.subheader("""
            BNP PARIBAS
            - Data Analyst
            - Mainly Power BI 
            - BNP Paribas is a French commercial bank operating in 65 countries
            """)

if selected == "Qualifications":
    with st.container():
        col5, col6 = st.columns(2)
        with col5:
            st.write("##")
            st.subheader("Since I almost finished my Efrei college ...")
            st.title("Here are my qualifications !")
        with col6:
            st.lottie(lottie_school)
    st.write("---")
    with st.container():
        col7, col8 = st.columns(2)
        with col7:
            st.subheader("""
            EFREI PARIS
            - Engineer school
            - Master in Data
            - Machine Learning, Big Data and Data Visualization courses
            - International semester in Poland (4 months)
            """)
        with col8:
            st.subheader("""
            LYCEE INTERNATIONAL DE SAINT GERMAIN EN LAYE
            - Primary, middle and high shcool
            - "Baccalauréat" in France
            - Maths, Physics & It
            - OIB : International Option (Portuguese)
            """)

if selected == "Skills":
    with st.container():
        col9, col10 = st.columns(2)
        with col10:
            st.write("##")
            st.subheader("Finally, here is an important part of me :")
            st.title("My skills !")
        with col9:
            st.lottie(lottie_star)
    st.write("---")
    with st.container():
        col11, col12 = st.columns(2)
        with col11:
            st.subheader("""
            HARD SKILLS
            - Python
            - SQL
            - Colab
            - Streamlit
            """)
        with col12:
            st.subheader("""
            SOFT SKILLS
            - Leadership
            - Communication
            - Problem Solver
            - Adaptabilty
            """)

if selected == "Home":
    with st.container():
        col15, col16 = st.columns(2)
        with col15:
            st.write("##")
            st.subheader("Here you can find some of my projects...")
            st.title("Welcome to my Porfolio !")
        with col16:
            st.lottie(lottie_home)
    st.write("---")