import streamlit as st


# -- PAGE SETUP --
about_page = st.Page(
    page="pages/about_me.py",
    title="About me",
    icon="👨‍💻",
    default=True,
)
museum_page= st.Page(
    page="pages/museum_data.py",
    title="French museums",
    icon="📊",
)
chatbot_page = st.Page(
    page="pages/chatbot.py",
    title="Chatbot",
    icon="🗣️",
)
datacamp_page = st.Page(
    page="pages/datacamp_pages/datacamp.py",
    title="Datacamp",
    icon="🎓",
)
face_detector_page = st.Page(
    page="pages/face_detector.py",
    title="Face Detector",
    icon="👁‍🗨",
)


# -- NAVIGATION SETUP [WITH SECTIONS] --
pg = st.navigation(
    {
        "Home page": [about_page, chatbot_page],
        "Projects": [museum_page, datacamp_page, face_detector_page],
    }
)


# -- RUN NAVIGATION --
pg.run()


# -- SHARED ON ALL PAGES --
st.logo("assets/earth_logo.png")
st.sidebar.text("© 2024 Poujol")