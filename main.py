import streamlit as st
from nlp_utils import extract_range
from calendar_service import create_event
from datetime import datetime
import dateutil.parser

st.title("💻CALENDAR - Smart Appointment Booking Bot")

user_input = st.text_input("💬 Enter your request (e.g., 'Book an appointment for Neha on Friday at 5pm'):")

if st.button("Book Appointment"):
    start_time, end_time = extract_range(user_input)

    if start_time and end_time:
        result = create_event(f"Appointment with", start_time, end_time)
        kl = dateutil.parser.isoparse(start_time)
        st.success(f"✅ Appointment booked for at {kl.strftime('%A, %d %B %Y at %I:%M %p')}")
    else:
        st.error("❌ Could not understand the input. Please try again.")