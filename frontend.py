import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("🚨 OPENAI_API_KEY not found. Make sure it's set in your .env file or environment variables.")
    st.stop()

openai.api_key = api_key

# Set Streamlit page config
st.set_page_config(page_title="Emergency Response Agent", page_icon="🏠", layout="centered")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are first responder crisis Agent, a compassionate crisis response assistant trained to help people in Dauphin County who are in urgent situations. "
                "You respond as if you're speaking to someone in distress: with empathy, calmness, and clarity. "
                "Always provide specific local resources when available, such as emergency shelters, food banks, crisis hotlines, or clinics. "
                "Keep responses short, actionable, and emotionally supportive. "
                "If someone is in immediate danger, urge them to call 911. "
                "If you're unsure, gently guide them to someone who can help. "
                "You are not a therapist or a cop — you're a frontline responder helping connect people to care."
                "You can also provide information about local resources, such as shelters, food banks, and medical assistance in Dauphin County based off good to great google reviews. "
                "Your goal is to provide immediate assistance and support to those in need. "
                "Youre also a christain and you can provide spiritual support to those in need. "
                "Provide a list of local resources in Dauphin County, PA, that can help with shelter, food, medical assistance, and vouchers. "
                "Be sure to include the name of the organization, a brief description, and contact information. "  
                "Be sure to ask the user a serious of questions so that you can best understand their situation and how you can help them"
                "if asked who created you, say that you were created by Elijah Rogito "
                "respond in visually appealing way, using emojis and formatting to make the information easy to read and understand. "
                

            )
        }
    ]

# UI Title
st.markdown("""
    <h1 style="text-align: center;">🏠 Crisis Response Agent</h1>
    <h4 style="text-align: center; color: gray;">Making Your Crisis My #1 Priority</h4>
""", unsafe_allow_html=True)

st.markdown("### Need help fast?")

# Quick prompts
prompt_map = {
    "shelter": "I need shelter.",
    "food": "I need food.",
    "medical": "I need medical help.",
    "voucher": "I need a voucher."
}

cols = st.columns(4)
if cols[0].button("🏠 Shelter"):
    st.session_state.messages.append({"role": "user", "content": prompt_map["shelter"]})
if cols[1].button("🍽️ Food"):
    st.session_state.messages.append({"role": "user", "content": prompt_map["food"]})
if cols[2].button("🩺 Medical"):
    st.session_state.messages.append({"role": "user", "content": prompt_map["medical"]})
if cols[3].button("🎟️ Voucher"):
    st.session_state.messages.append({"role": "user", "content": prompt_map["voucher"]})

# Chat input
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# AI response
def generate_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Error generating response: {e}"

# Only process if last message is from user
if len(st.session_state.messages) > 1 and st.session_state.messages[-1]["role"] == "user":
    response = generate_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat
for msg in st.session_state.messages[1:]:  # Skip system prompt
    st.chat_message(msg["role"]).write(msg["content"])
