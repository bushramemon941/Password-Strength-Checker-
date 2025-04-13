import streamlit as st
import random
import string

def check_password_strength(password):
    score = 0
    length = len(password)
    
    # Length score (up to 50 points)
    length_score = min(length * 2, 50)
    
    # Complexity score (up to 50 points)
    complexity_score = 0
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    
    criteria_met = sum([has_upper, has_lower, has_number, has_symbol])
    complexity_score = criteria_met * 12.5
    
    total_score = length_score + complexity_score
    return min(total_score, 100)

def generate_password(length=12, use_upper=True, use_lower=True, use_number=True, use_symbol=True):
    chars = []
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_number:
        chars += string.digits
    if use_symbol:
        chars += string.punctuation
    
    if not chars:
        return ''
    
    password = []
    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_number:
        password.append(random.choice(string.digits))
    if use_symbol:
        password.append(random.choice(string.punctuation))
    
    remaining_length = length - len(password)
    if remaining_length > 0:
        password += [random.choice(chars) for _ in range(remaining_length)]
    
    random.shuffle(password)
    return ''.join(password)

# Streamlit UI Configuration
st.set_page_config(
    page_title="Password Toolkit",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Session state initialization
if 'current_password' not in st.session_state:
    st.session_state.current_password = ''

# Main Interface
st.title("🔒 Password Strength Checker & Generator")
st.write("Enhance your account security with our password analysis and generation tools.")

# Password Input Section
col1, col2 = st.columns([4, 1])
with col1:
    password = st.text_input(
        "Enter password to analyze:",
        type="password",
        value=st.session_state.current_password,
        key="pw_input",
        placeholder="Type or generate a password..."
    )
with col2:
    st.write("\n")
    st.write("\n")
    if st.button("Generate"):
        generated_pw = generate_password()
        st.session_state.current_password = generated_pw
        st.rerun()

# Password Strength Analysis
if password:
    score = check_password_strength(password)
    st.progress(score / 100)
    
    if score < 40:
        st.error(f"Weak Password ❌ (Score: {score:.0f}/100)")
    elif score < 70:
        st.warning(f"Medium Password ⚠️ (Score: {score:.0f}/100)")
    else:
        st.success(f"Strong Password ✅ (Score: {score:.0f}/100)")
    
    # Password Details
    with st.expander("🔍 Password Analysis Details"):
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_number = any(c.isdigit() for c in password)
        has_symbol = any(c in string.punctuation for c in password)
        
        st.markdown("**Characteristics:**")
        st.write(f"• Length: {len(password)} characters")
        st.write(f"• Uppercase letters: {'✅' if has_upper else '❌'}")
        st.write(f"• Lowercase letters: {'✅' if has_lower else '❌'}")
        st.write(f"• Numbers: {'✅' if has_number else '❌'}")
        st.write(f"• Special symbols: {'✅' if has_symbol else '❌'}")

# Custom Password Generator
with st.expander("🔧 Custom Password Generator", expanded=False):
    st.subheader("Customize Your Password")
    col1, col2 = st.columns([3, 2])
    
    with col1:
        pw_length = st.slider(
            "Password length",
            min_value=8,
            max_value=32,
            value=16,
            help="Longer passwords are more secure"
        )
        
    with col2:
        st.write("\n")
        use_upper = st.checkbox("A-Z", value=True)
        use_lower = st.checkbox("a-z", value=True)
        use_number = st.checkbox("0-9", value=True)
        use_symbol = st.checkbox("!@#$", value=True)
    
    if st.button("Generate Custom Password", key="custom_gen"):
        generated_pw = generate_password(
            length=pw_length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_number=use_number,
            use_symbol=use_symbol
        )
        
        if generated_pw:
            st.session_state.current_password = generated_pw
            st.rerun()
        else:
            st.error("Please select at least one character type!")


# How to Run
st.sidebar.markdown("## How to Use:")
st.sidebar.markdown("""
1. **Check Password Strength:**
   - Type or generate a password
   - Get instant security feedback
   
2. **Generate Strong Passwords:**
   - Use quick generator (✨ button)
   - Customize with specific requirements
   - Copy generated password securely
""")

st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ By Bushra Memon")