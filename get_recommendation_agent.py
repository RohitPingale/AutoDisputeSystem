from openai import OpenAI
import json
import os
from typing import Dict, Any

def get_chatgpt_recommendation( dispute,category, priority, team, unique_ref) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    url = "https://api.openai.com/v1/chat/completions"
    
    personas = {
        "fraud_team": "You are an experienced fraud investigation specialist with deep knowledge of financial regulations and fraud patterns.",
        "billing_team": "You are a billing dispute resolution expert with experience in transaction reconciliation and merchant communications.",
        "customer_service": "You are a customer-focused dispute resolution specialist who prioritizes customer satisfaction.",
        "escalation_team": "You are a senior dispute resolution manager who handles complex and high-priority cases."
    }

    persona = personas.get(team, personas["customer_service"])
    

    prompt = f"""
        {persona}

        Please provide detailed step-by-step instructions to resolve the following transaction dispute:

        DISPUTE DETAILS:
        - Category: {dispute.category}
        - Priority Level: {priority}
        - Transaction Amount: ${dispute.amount}
        - Customer Description: "{dispute.description}"
        - Customer Account Age: {dispute.acc_opened_years} years
        - Previous Disputes: {dispute.previous_disputes}
        - Premium Customer: {"Yes" if dispute.is_premium else "No"}

        Provide a detailed recommendation with:
        1. Initial assessment steps
        2. Required documentation and technical help
        3. Communication approach with the customer
        4. Verification procedures.

        Reponse should without any markdown sysntax excpet for "\n"
        """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a banking dispute resolution assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        recommendation = response.choices[0].message.content
        return str(recommendation)
        
    except Exception as e:
        print(f"Error calling API: {e}")
        return "Unable to get detailed recommendation at this time. try LLMAPI as False and register dispute."