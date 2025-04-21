import streamlit as st
from cryptography.fernet import Fernet
import hashlib
import base64

# Initialize session state
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "authenticated" not in st.session_state:
    st.session_state.authenticated = True

# Generate a consistent Fernet key
def generate_key(passkey: str):
    hashed = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])

# Encrypt using Fernet
def encrypt_data(text: str, passkey: str):
    key = generate_key(passkey)
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

# Decrypt using Fernet
def decrypt_data(cipher_text: str, passkey: str):
    try:
        key = generate_key(passkey)
        f = Fernet(key)
        return f.decrypt(cipher_text.encode()).decode()
    except Exception:
        return None

# Hash passkey for storage
def hash_passkey(passkey: str):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Login page
def login_page():
    st.title("Reauthorization Required")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.authenticated = True
            st.session_state.failed_attempts = 0
            st.success("Login successful!")
        else:
            st.error("Incorrect credentials.")

# Insert data
def insert_data():
    st.title("Store New Data")
    username = st.text_input("Enter a unique username")
    text = st.text_area("Enter the text to encrypt")
    passkey = st.text_input("Enter a passkey", type="password")

    if st.button("Encrypt & Store"):
        if username and text and passkey:
            encrypted_text = encrypt_data(text, passkey)
            st.session_state.stored_data[username] = {
                "encrypted_text": encrypted_text,
                "passkey": hash_passkey(passkey)
            }
            st.success("Data stored securely!")
        else:
            st.warning("All fields are required.")

# Retrieve data
def retrieve_data():
    st.title("Retrieve Data")
    username = st.text_input("Enter your username")
    passkey = st.text_input("Enter your passkey", type="password")

    if st.button("Decrypt"):
        if username in st.session_state.stored_data:
            stored = st.session_state.stored_data[username]
            if hash_passkey(passkey) == stored["passkey"]:
                decrypted = decrypt_data(stored["encrypted_text"], passkey)
                st.success(f"Decrypted Data: {decrypted}")
                st.session_state.failed_attempts = 0
            else:
                st.session_state.failed_attempts += 1
                st.error(f"Incorrect passkey! Attempts: {st.session_state.failed_attempts}/3")
        else:
            st.warning("Username not found!")

        if st.session_state.failed_attempts >= 3:
            st.session_state.authenticated = False

# Main navigation
def main():
    st.sidebar.title("Secure Data App")
    page = st.sidebar.radio("Navigate", ["Home", "Insert Data", "Retrieve Data"])

    if not st.session_state.authenticated:
        login_page()
    else:
        if page == "Home":
            st.title("Welcome to the Secure Data Encryption App")
            st.write("Choose an option from the sidebar to continue.")
        elif page == "Insert Data":
            insert_data()
        elif page == "Retrieve Data":
            retrieve_data()

if __name__ == "__main__":
   main ()
