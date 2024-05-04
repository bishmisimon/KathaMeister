import mysql.connector
import streamlit as st
import welcome

import base64

# Set page configuration
st.set_page_config(layout="wide")

# Read the logo image as bytes and encode it to base64
with open("Logo.png", "rb") as f:
    image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode()

# Custom HTML/CSS for the banner and background
custom_html = f"""
<style>
    .banner {{
        text-align: center;
        margin-top: 2px;
    }}
</style>
<div class="banner">
    <img src="data:image/png;base64,{image_base64}" alt="Logo" style="max-width: 100%; height: auto;">
</div>
"""

# Display the custom HTML with the base64-encoded image
st.markdown(custom_html, unsafe_allow_html=True)

# Main content
st.markdown("<h1 style='text-align: center; color: #4169E1;'>Ihre Lieblings Deutsche Ausprache Bewerter</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-style: italic; font-family: cursive;'>Your German Pronunciation Feedback</h2>", unsafe_allow_html=True)
################

#conn = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="root",
#    database="katha_meister"
#)
conn = mysql.connector.connect(
    host="database-1.clsoq4mai7vi.ap-south-1.rds.amazonaws.com",
    user="kathameisterxp",
    password="CroCro123",
    database="kathameister"
)

cursor = conn.cursor()

# Function to register a new user
def register(username, email, f_name, l_name, password):
    try:
        # Check if username already exists
        cursor.execute("SELECT COUNT(*) FROM user_register WHERE user_name = %s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            st.error(f"Username '{username}' already exists. Registration failed.")
            return False

        # Insert new user into database
        cursor.execute("INSERT INTO user_register (user_name, email, f_name, l_name, password) VALUES (%s, %s, %s, %s, %s)",
                       (username, email, f_name, l_name, password))
        conn.commit()
        
        st.success(f"User '{username}' registered successfully.")
        return True  # Return True upon successful registration
    except Exception as e:
        st.error(f"Error registering user: {e}")
        return False  # Return False if registration fails

# Function to check if the provided credentials are valid
def is_valid_credentials(username, password):
    cursor.execute("SELECT COUNT(*) FROM user_register WHERE user_name = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    return result[0] > 0

# Function to display the registration form
def registration_form():
    with st.container():
        with st.container():
            st.title("User Registration")
            username = st.text_input("Username", key="username_input_reg")
            email = st.text_input("Email Address", key="email_input_reg")
            f_name = st.text_input("First Name", key="f_name_input_reg")
            l_name = st.text_input("Last Name", key="l_name_input_reg")
            password = st.text_input("Password", type="password", key="password_input_reg")
            if st.button("Register", key="register_btn"):
                if register(username, email, f_name, l_name, password):
                    st.success("Registration successful! Please proceed to login.")

# Function to display the login form
def login_form():
    with st.container():
        with st.container():
            st.title("User Login")
            username = st.text_input("Username", key="username_input_login")
            password = st.text_input("Password", type="password", key="password_input_login")
            if st.button("Login", key="login_btn"):
                if is_valid_credentials(username, password):
                    st.success(f"Welcome, {username}!")
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

def main():
    if st.session_state.get("logged_in"):
        st.success("Logged in successfully to the Dashboard!")
        st.write("Redirecting to welcome page...")
        welcome.main() # Display the welcome page
    else:
        st.markdown("<div class='centered' style='color: #4169E1;'><h1>User Authentication</h1></div>", unsafe_allow_html=True)
        st.markdown("<div class='centered'><p>Please login or register to access the application</p></div>", unsafe_allow_html=True)
        st.write("---")
        login_form()
        st.write("or")
        registration_form()

if __name__ == "__main__":
    main()
