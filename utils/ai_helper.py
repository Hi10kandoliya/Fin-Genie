
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_faq(product_name, user_profile="general"):
    """Generate personalized FAQ based on product and user profile."""
    profile_context = {
        "student": "You are a college student looking for low-cost options.",
        "professional": "You are a working professional seeking premium benefits.",
        "retiree": "You are a retiree focused on safety and fixed returns.",
        "general": "You are a general customer."
    }
    
    prompt = f"""
    You are a financial advisor. A {profile_context.get(user_profile, 'general customer')} is interested in {product_name}.
    
    Generate 3 frequently asked questions and answers about {product_name} that are:
    - Easy to understand for a beginner
    - Tailored to the user's profile: {user_profile}
    - Include one practical example
    
    Format as:
    Q1: [Question]
    A1: [Answer]
    Q2: [Question]
    A2: [Answer]
    Q3: [Question]
    A3: [Answer]
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content

def personalize_content(product_name, user_info):
    """Generate personalized product explanation based on user details."""
    prompt = f"""
    User details:
    - Age: {user_info.get('age', '30')}
    - Income: {user_info.get('income', '$50,000')}
    - Goal: {user_info.get('goal', 'saving for future')}
    
    Explain the {product_name} in simple terms. Highlight:
    1. Why this product fits the user's situation
    2. One key benefit they should care about
    3. One thing they should watch out for
    
    Keep it under 150 words. Use friendly, non-technical language.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.8
    )
    
    return response.choices[0].message.content

# For offline demo (no API key), use fallback:
def fallback_faq(product_name, user_profile="general"):
    from financial_data import products
    data = products.get(product_name, {})
    questions = data.get("common_questions", ["What is this product?"])
    answers = [
        f"This product offers {', '.join(data.get('features', ['various benefits']))}.",
        f"Check with your bank for {user_profile}-specific options.",
        "Contact customer support for detailed information."
    ]
    return "
".join([f"Q{i+1}: {q}
A{i+1}: {a}" for i, (q, a) in enumerate(zip(questions[:3], answers))])
