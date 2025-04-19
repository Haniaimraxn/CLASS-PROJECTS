import streamlit as st
import random
import string

# Blacklist of common passwords
blacklist = ["password", "123456", "password123", "qwerty", "letmein", "admin", "welcome"]

# Special characters allowed
special_chars = "!@#$%^&*"

# Custom weights for scoring (max total: 5)
weights = {
    "length": 1,
    "lowercase": 1,
    "uppercase": 1,
    "digit": 1,
    "special": 1,
}

# Evaluate password strength
def evaluate_password(password):
    score = 0
    feedback = []

    # Blacklist check
    if password.lower() in blacklist:
        return 0, "Weak", ["Avoid using common or easily guessable passwords."]

    if len(password) >= 8:
        score += weights["length"]
    else:
        feedback.append("Use at least 8 characters.")

    if any(c.islower() for c in password):
        score += weights["lowercase"]
    else:
        feedback.append("Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += weights["uppercase"]
    else:
        feedback.append("Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += weights["digit"]
    else:
        feedback.append("Include at least one number.")

    if any(c in special_chars for c in password):
        score += weights["special"]
    else:
        feedback.append(f"Add special characters ({special_chars}).")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return score, strength, feedback

# Generate strong password
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + special_chars
    while True:
        pwd = ''.join(random.choice(characters) for _ in range(length))
        score, strength, _ = evaluate_password(pwd)
        if strength == "Strong":
            return pwd

# Streamlit UI
st.title("🔐 Password Strength Meter")
password = st.text_input("Enter your password", type="password")

if password:
    score, strength, feedback = evaluate_password(password)

    st.write(f"*Strength Score:* {score}/5")
    st.write(f"*Password Strength:* :{ 'red' if strength == 'Weak' else 'orange' if strength == 'Moderate' else 'green' }[{strength}]")

    if strength != "Strong":
        st.warning("Suggestions to improve your password:")
        for tip in feedback:
            st.markdown(f"- {tip}")
    else:
        st.success("Great! Your password is strong.")

st.markdown("---")
if st.button("Generate a Strong Password"):
    strong_pwd = generate_strong_password()
    st.text_input("Suggested Password", strong_pwd)