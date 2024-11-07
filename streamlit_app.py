import streamlit as st

# Page Configuration
st.set_page_config(page_title="MathGPT", page_icon="📐")

# Sidebar
with st.sidebar:
    st.markdown("### We stand on the side of peace ✌️ 🕊️ ✨")
    st.button("Login with Google")
    st.button("Subscribe now!")
    st.markdown("""
    Do you need human-level intelligence? Send us your problem in [this link](#).
    Cost of assistance depending on complexity, starting EE from $10 USD
    """)

# Main Content
st.title("MathGPT")
st.subheader("Use GPT to solve math problems")
st.markdown("Follow [Twitter](#)  |  Contact: [mathgpt.app@gmail.com](mailto:mathgpt.app@gmail.com)")

# Information Section
st.info("Dear user, to use the app you need to login and subscribe.", icon="📦")

# Blog Link
st.markdown("#### Blog 👉 [📘](#)")
