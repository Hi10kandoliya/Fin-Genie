import streamlit as st
from utils.financial_data import products
from utils.ai_helper import generate_faq, personalize_content, fallback_faq

st.set_page_config(page_title="FinGenie - Financial FAQ Assistant", layout="centered")

# --- Sidebar ---
st.sidebar.image("logo.png", width=100) if False else st.sidebar.title("🧠 FinGenie")
st.sidebar.markdown("**Your AI Financial Guide**")
st.sidebar.markdown("---")
st.sidebar.info("This demo uses generative AI to create personalized FAQs and explanations for financial products.")

# --- Main UI ---
st.title("💡 Understand Financial Products with AI")
st.markdown("Select a product, tell us about yourself, and get tailored answers.")

# Step 1: Product Selection
product = st.selectbox("Choose a financial product:", list(products.keys()))

# Step 2: User Profile
col1, col2 = st.columns(2)
with col1:
    profile = st.selectbox("Your profile:", ["general", "student", "professional", "retiree"])
with col2:
    use_ai = st.checkbox("Use AI for personalized content", value=True)

# Step 3: Optional custom question
custom_question = st.text_input("Ask a specific question (optional):")

# Step 4: Generate content
if st.button("Generate FAQs & Explanation", type="primary"):
    with st.spinner("Generating personalized content..."):
        try:
            if use_ai:
                faq_content = generate_faq(product, profile)
            else:
                faq_content = fallback_faq(product, profile)
        except:
            faq_content = fallback_faq(product, profile)  # Fallback on error
        
        st.subheader(f"📋 FAQs for {product} ({profile.capitalize()})")
        st.markdown(faq_content)
        
        # Display product features
        st.subheader("✨ Key Features")
        for feature in products[product]["features"]:
            st.write(f"✅ {feature}")
        
        # Personalized explanation (AI-powered)
        if use_ai:
            st.subheader("🧑‍💼 Personalized Advice")
            user_info = {
                "age": st.session_state.get("age", 30),
                "income": st.session_state.get("income", "$50,000"),
                "goal": st.session_state.get("goal", "saving")
            }
            try:
                explanation = personalize_content(product, user_info)
                st.info(explanation)
            except:
                st.info(f"As a {profile}, {product} can help you achieve your financial goals. Contact us for personalized advice.")
        
        st.success("✅ Content generated successfully!")

# --- Interactive Demo: Ask a question ---
st.markdown("---")
st.subheader("💬 Quick Question")
quick_q = st.text_input("Type your question here:")
if quick_q:
    st.info(f"💡 *For '{product}':* {quick_q}")
    st.markdown("_In a full implementation, this would trigger a real-time AI response._")

# Footer
st.markdown("---")
st.caption("📌 University Project – Generative AI for Financial Literacy | IWU - 2026")
