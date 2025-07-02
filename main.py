import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

# Tool functions
def get_weather(location: str, unit: str = "C") -> str:
    return f"The weather in {location} is 22 degrees {unit}."

def student_finder(student_roll: int) -> str:
    data = {1: "Qasim", 2: "Sir Zia", 3: "Daniyal"}
    return data.get(student_roll, "Not Found")

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message("Hello, I'm Basit Ali — a programmer. How can I help you today?").send()

@cl.on_message
async def on_message(message: cl.Message):
    content = message.content.lower()

    # Simulated tool calls
    if "weather" in content:
        await cl.Message(get_weather("Karachi")).send()
        return
    if "piaic" in content or "student" in content:
        await cl.Message(student_finder(2)).send()
        return

    # Fallback to Gemini
    response = model.generate_content(message.content)
    await cl.Message(response.text).send()
