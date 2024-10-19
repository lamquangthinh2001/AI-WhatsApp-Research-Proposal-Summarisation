from fastapi import FastAPI, Request, Form
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = "https://thinh-m2ej7j6c-westeurope.openai.azure.com/"
openai.api_version = "19/10/2024"  # Adjust according to your version

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    body = await request.form()
    user_message = body.get('Body')

    # Generate response using Azure OpenAI
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_message,
        max_tokens=150
    )

    reply = response.choices[0].text.strip()

    # Create a Twilio MessagingResponse to send the reply back
    twilio_response = MessagingResponse()
    twilio_response.message(reply)

    return str(twilio_response)
