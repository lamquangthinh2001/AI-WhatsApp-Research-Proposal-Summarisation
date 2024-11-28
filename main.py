from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse

from twilio.twiml.messaging_response import MessagingResponse
import openai
from credentials import *
import os

app = FastAPI()

openai = openai.AzureOpenAI(
    azure_endpoint=openai_api_url,
    api_key=openai_api_key,
    api_version="2024-02-01",
)

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    body = await request.form()
    user_message = body.get('Body')

    # Generate response using Azure OpenAI
    response = openai.chat.completions.create(
        model="gpt-35-turbo",
    messages=[
            {
        "role": "system",
        "content": "Extract and summarize information from a student's research proposal into a concise report with clearly defined sections. Ensure the summary follows this structured format:\n\n---\n\n**Steps:**\n\n1. **Identify Key Sections**: Locate the student's name, research topic, introduction, background information, and research design sections within the proposal.\n2. **Summarize Content**: For each identified section, distill the information into a brief and precise summary that captures the essence of the content.\n3. **Organize Report**: Arrange the summaries into clearly labeled sections, ensuring each section is distinct and easy to navigate.\n\n---\n\n**Output Format:**\n\n- **Name**: [Student's Name]  \n  *(Include the full name of the student as listed in the proposal.)*  \n\n- **Topic**: [Research Topic]  \n  *(Provide the full title of the research proposal topic.)*  \n\n- **Introduction**:  \n  *(Summarize the key points from the introduction, including the purpose and significance of the research.)*  \n\n- **Background**:  \n  *(Provide a concise summary of the background information, focusing on the context and rationale for the research.)*  \n\n- **Research Design**:  \n  *(Outline the main elements of the research design, such as the methods, participants, data collection, and analysis approach.)*  \n\n---\n\n**Notes:**\n\n- Ensure all sections are summarized objectively and concisely, maintaining the original intent and content of the proposal.\n- Use professional and clear language to make the summary accessible and informative.\n- Avoid excessive detail; focus on the most critical information for each section.\n"
    },
        {
            "role": "user",
            "content": "Tell me about the research of Elizabeth Blessing",
        },
        {
            "role": "assistant",
            "content": "## In-domain response\n- **Name**: Elizabeth Blessing\n- **Topic**: Knowledge, Attitudes, and Practices Among Pharmacy Interns and Pharmacists Regarding Legal Obligations When Handling, Dispensing and Supplying Medicines in Namibia: A Cross-Sectional Descriptive Study\n- **Introduction**: The research aims to analyze the existing understanding, attitude, and behaviors of pharmacy interns and registered pharmacists in Namibia regarding legal obligations when handling, dispensing, and supplying medicines. The study is important due to the potential negative consequences of lack of knowledge, negative attitude, and non-compliance practice by pharmacy professionals on patient health outcomes.\n- **Background**: The study is conducted in Namibia, where pharmaceutical products are highly regulated to ensure rational use and handling, as well as mitigate risks posed by substandard, adulterated, counterfeit medicines, or those otherwise not meeting quality, safety, and efficacy standards. Pharmacists are expected to comply with the requirements set out in the Medicines and Related Substances Control Act No.13 2003. Compliance with regulations has been found to be higher in pharmacist-run pharmacies than in nurse-run clinic dispensaries.\n- **Research Design**: The study is a cross-sectional descriptive study. The data was collected through a google form survey, and the participants were pharmacy interns and pharmacists. The data was validated before being transferred into the final online survey, which summarized the information gathered from the participants. The data was organized and stored securely on google drive with a password only known by the researcher. The data was anonymized, and no name of the participant appeared. The data was entered into the SPSS version 28 database, where it was cleaned and used. Data was finalized, then it was tabled and summarized in graphs. The study adhered to all the research ethics and code of conduct as required by NUST and the MoHSS.",
        },
        {
            "role": "user",
            "content": user_message,
        },
    ],
    
    extra_body={
        "data_sources":[
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": azure_ai_search_endpoint,
                    "index_name": azure_ai_search_index,
                    "authentication": {
                        "type": "api_key",
                        "key": azure_ai_search_api_key,
                    }
                }
            }
        ],
    },
    max_tokens= 100
    )
    reply = response.choices[0].message.content.strip()

    # Create a Twilio MessagingResponse to send the reply back
    twilio_response = MessagingResponse()
    twilio_response.message(reply)

    return PlainTextResponse(str(twilio_response), media_type="application/xml")


