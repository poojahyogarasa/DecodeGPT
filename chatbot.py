from groq import Groq

from config import GROQ_API_KEY
from prompts import SYSTEM_PROMPT
from database import get_recent_messages

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_response(
    user_message,
    pdf_text=""
):

    history = get_recent_messages(10)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add PDF Context
    if pdf_text:

        messages.append(
            {
                "role": "system",
                "content": f"""
You have access to an uploaded PDF.

Rules:

1. If the user asks for a summary,
   provide a concise summary.

2. If the user asks a question,
   answer only using relevant parts
   of the PDF.

3. Do NOT dump the entire document.

4. Keep answers clear and structured.

5. If information is not found in the PDF,
   say so clearly.

PDF CONTENT:

{pdf_text[:12000]}

Use the PDF content to answer questions
related to the uploaded document.

If the answer exists in the PDF,
prioritize the PDF over general knowledge.

PDF CONTENT:

{pdf_text[:12000]}
"""
            }
        )

    # Add Previous Chat History
    for role, message in history:

        messages.append(
            {
                "role": role,
                "content": message
            }
        )

    # Add Current User Message
    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=messages,

        temperature=0.4,

        max_tokens=1500

    )

    response = (
        completion
        .choices[0]
        .message
        .content
    )

    return response