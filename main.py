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

# Function to connect to MySQL database
def connect_to_database():
    conn = mysql.connector.connect(
        host="database-1.clsoq4mai7vi.ap-south-1.rds.amazonaws.com",
        user="kathameisterxp",
        password="CroCro123",
        database="kathameister"
    )
    return conn

# Function to check if the provided credentials are valid
def is_valid_credentials(username, password, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user_register WHERE user_name = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    return result[0] > 0

# Function to display the login form
def login_form(conn):
    with st.container():
        with st.container():
            st.title("User Login")
            username = st.text_input("Username", key="username_input_login")
            password = st.text_input("Password", type="password", key="password_input_login")
            if st.button("Login", key="login_btn"):
                if is_valid_credentials(username, password, conn):
                    st.session_state.logged_in = True
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password.")

def main():
    conn = connect_to_database()
    if st.session_state.get("logged_in"):
        st.success("Logged in successfully to the Dashboard!")
        st.write("Redirecting to welcome page...")
        welcome.main() # Display the welcome page
    else:
        st.markdown("<div class='centered' style='color: #4169E1;'><h1>User Authentication</h1></div>", unsafe_allow_html=True)
        st.markdown("<div class='centered'><p>Please login or register to access the application</p></div>", unsafe_allow_html=True)
        st.write("---")
        login_form(conn)

if __name__ == "__main__":
    main()
