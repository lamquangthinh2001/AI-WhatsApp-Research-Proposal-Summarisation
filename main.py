from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse

from twilio.twiml.messaging_response import MessagingResponse
from openai import AzureOpenAI
import os

app = FastAPI()



openai = AzureOpenAI(
    api_key="af03a0d3abe7436cb18ced1b5b7d2f8f",  
    api_version="2024-02-01",
    azure_endpoint = "https://thinh-m2ej7j6c-westeurope.openai.azure.com/"
    )

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    body = await request.form()
    user_message = body.get('Body')

    # Generate response using Azure OpenAI
    response = openai.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "you must give answers in bullet points and should not exceed 50 words"},
            {"role": "user", "content": user_message}
        ],
            max_tokens = 50
    )
    reply = response.choices[0].message.content.strip()

    # Create a Twilio MessagingResponse to send the reply back
    twilio_response = MessagingResponse()
    twilio_response.message(reply)

    return PlainTextResponse(str(twilio_response), media_type="application/xml")


