import streamlit as st
import bcrypt
import yaml
import os

# Paths to store credentials and chat history
CREDENTIALS_FILE = "credentials.yaml"
CHAT_HISTORY_FILE = "user_chats.yaml"

def load_yaml(file_path):
    """Load data from a YAML file."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return yaml.safe_load(file) or {}

def save_yaml(file_path, data):
    """Save data to a YAML file."""
    with open(file_path, "w") as file:
        yaml.safe_dump(data, file)

def load_credentials():
    """Load user credentials."""
    return load_yaml(CREDENTIALS_FILE)

def save_credentials(credentials):
    """Save user credentials."""
    save_yaml(CREDENTIALS_FILE, credentials)

def load_chat_history(username):
    """Load a specific user's chat history."""
    chat_history = load_yaml(CHAT_HISTORY_FILE)
    return chat_history.get(username, [])

def save_chat_history(username, messages):
    """Save a user's chat history."""
    chat_history = load_yaml(CHAT_HISTORY_FILE)
    chat_history[username] = messages
    save_yaml(CHAT_HISTORY_FILE, chat_history)

def hash_password(password):
    """Hash the password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    """Verify password against the hashed version."""
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register():
    """User registration interface."""
    st.subheader("🔐 Register")

    if "register_username" in st.session_state:
        del st.session_state["register_username"]

    username = st.text_input("Username", key="reg_username")
    password = st.text_input("Password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
    
    if st.button("Sign Up"):
        if not username or not password:
            st.error("❌ Please enter a username and password!")
            return
        
        if password != confirm_password:
            st.error("❌ Passwords do not match!")
            return
        
        credentials = load_credentials()
        if username in credentials:
            st.error("❌ Username already exists! Try another.")
        else:
            credentials[username] = hash_password(password)
            save_credentials(credentials)
            st.success("✅ Registration successful! Please login.")
            st.session_state.page = "login"
            st.rerun()

def login():
    """User login interface."""
    st.subheader("🔑 Login")

    if "reg_username" in st.session_state:
        del st.session_state["reg_username"]

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        credentials = load_credentials()
        if username not in credentials:
            st.error("❌ Username not found!")
        elif not check_password(password, credentials[username]):
            st.error("❌ Incorrect password!")
        else:
            st.session_state.username = username  # Store the logged-in user
            st.session_state.chat_history = load_chat_history(username)  # Load user's chat history
            st.success(f"✅ Welcome, {username}!")
            st.session_state.page = "main"
            st.rerun()

def logout():
    """Logout function to clear session state."""
    st.session_state.clear()
    st.success("✅ Logged out successfully!")
    st.session_state.page = "login"
    st.rerun()

def auth():
    """Handle authentication for the app."""
    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    if "username" not in st.session_state:
        if st.session_state.page == "login":
            login()
            if st.button("Don't have an account? Register here."):
                st.session_state.page = "register"
                st.rerun()
        else:
            register()
            if st.button("Already have an account? Login here."):
                st.session_state.page = "login"
                st.rerun()
        return False
    return True

def main():
    """Main app function."""
    if not auth():
        return

    st.subheader(f"Welcome, {st.session_state.username}!")
    st.write("This is the main page.")

    # Logout Button
    if st.button("Logout"):
        logout()



if __name__ == "__main__":
    main()