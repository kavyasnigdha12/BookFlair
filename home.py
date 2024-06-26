import streamlit as st
from streamlit_carousel import carousel
import account


def app():
    
    st.markdown("<h1 style='text-align: center; color: white;'>----- 𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣 -----</h1>", unsafe_allow_html=True)
    # Hero Section
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/wont_be.jpg", width=300)
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.header('Discover Your Next Favorite Book!', divider='rainbow')
        st.subheader("Get personalized recommendations based on your interests",divider='rainbow')
        st.button("Sign In Now")
        

    # Call to Action Bar
    st.write("---")
    st.success("Sign up for a free trial and unlock unlimited recommendations!")

    #pip install streamlit-carousel

    # Implementing carousel (ensure to have `streamlit_carousel` installed)
    # book_covers = [
    #     {"title": "Book 1", "image": "images/book1.jpg"},
    #     {"title": "Book 2", "image": "images/book2.jpg"},
    #     {"title": "Book 3", "image": "images/book3.jpg"}
    # ]
    # carousel(book_covers)

    # Footer (optional - uncomment to display)
    st.write("---")
    st.markdown("<p style='text-align: center; color: white;'>© 2024 𝔹𝕠𝕠𝕜𝔽𝕝𝕒𝕚𝕣. All rights reserved.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Contact us at: support@bookflair.com</p>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
  app()
