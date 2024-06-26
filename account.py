
import re
import streamlit as st
import mysql.connector
from mysql.connector import Error
import base64

# Create database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',          # Replace with your host
            user='root',               # Replace with your MySQL username
            password='',               # Replace with your MySQL password
            database='bookflair'
        )
    except Error as e:
        st.error(f"Error: '{e}'")
    return connection

# User login
def login_user(email, password):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

# User sign up
def sign_up_user(email, password, username):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("INSERT INTO users (email, password, username) VALUES (%s, %s, %s)", (email, password, username))
    connection.commit()
    cursor.close()
    connection.close()

# Email validation
def is_email_valid(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Password validation
def is_password_valid(password):
    return len(password) >= 8

# Username uniqueness check
def is_username_unique(username):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is None

# Email uniqueness check
def is_email_unique(email):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is None

# Main app function
def app():
    st.title(":violet[Account] Sign in:violet[/]Sign out")

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_info = None

    # User is logged in
    if st.session_state.logged_in:
        st.success(f"{st.session_state.user_info['username']} logged in!")
        if st.button('Sign Out', key='signout_button'):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.experimental_rerun()

    # User is not logged in
    else:
        choice = st.selectbox('Login or Sign Up', ["Login", "Sign Up"], key='login_signup_choice')
        if choice == 'Login':
            email = st.text_input('Email Address', key='login_email')
            password = st.text_input('Password', type='password', key='login_password')

            if st.button('Login', key='login_button'):
                if not is_email_valid(email):
                    st.error("Invalid email format")
                else:
                    user = login_user(email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_info = user
                        st.success(f"Welcome {user['username']}!")
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect email or password")

        else:
            email = st.text_input('Email Address', key='signup_email')
            password = st.text_input('Password', type='password', key='signup_password')
            username = st.text_input('Enter a unique username', key='signup_username')

            if st.button('Sign Up', key='signup_button'):
                if not is_email_valid(email):
                    st.error("Invalid email format")
                elif not is_password_valid(password):
                    st.error("Password must be at least 8 characters long")
                elif not is_username_unique(username):
                    st.error("Username already taken")
                elif not is_email_unique(email):
                    st.error("Email already registered")
                else:
                    try:
                        sign_up_user(email, password, username)
                        st.success("Account created successfully!")
                    except Error as e:
                        st.error(f"Error: {e}")


    st.write("")
    """### gif from local file"""
    file_ = open("images/Laurel’s Guide to Grimoires.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<div style="text-align:center;"><img src="data:image/gif;base64,{data_url}" alt="cat gif"></div>',
        unsafe_allow_html=True,
    )


# Ensure to call the app function to run the application
if __name__ == '__main__':
    app()