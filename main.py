from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
import random

from classify_dispute import classifyDisputes
from dispute_assignment import  disputeAssignment

from db_ops import dispute_to_db,init_database
from get_recommendation_agent import get_chatgpt_recommendation

# from classify_dispute.classifyInput import classify_dispute, generate_recommendation
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Auto Transaction Dispute API")

class DisputeCategory(str, Enum):
    UNAUTHORIZED = "unauthorized_payment"
    DUPLICATE = "duplicate_payment"
    NOT_RECEIVED = "payment_not_received"
    WRONG_AMOUNT = "wrong_amount"
    OTHER = "other"

class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TeamAssignment(str, Enum):
    FRAUD = "fraud_team"
    BILLING = "billing_team"
    CUSTOMER_SERVICE = "customer_service"
    ESCALATION = "escalation_team"

class DisputeRequest(BaseModel):
    transaction_id: str
    amount: float
    description: str
    customer_id: str
    acc_opened_years: float
    previous_disputes: int
    is_premium: bool
    acc_balance: float
    LLMAPI: bool
    category: Optional[DisputeCategory] = None
    reference_number: Optional[str] = None

class DisputeResponse(BaseModel):
    transaction_id: str
    assigned_category: str
    priority: PriorityLevel
    assigned_team: TeamAssignment
    recommendation: str
    reference_number: str




db_conn = init_database("FraudTransactions")


@app.post("/disputes/", response_model=DisputeResponse)
async def create_dispute(dispute: DisputeRequest):
 
    clf_dispute = classifyDisputes(dispute,DisputeCategory)
    assign_dispute = disputeAssignment(DisputeCategory, PriorityLevel, TeamAssignment)


     
    category = clf_dispute.classify_dispute_rule_based()
    ##TODO we can use the ML model to classify the disputes but we need data.Implemntation at classify_disput.py >classify_dispute_AI 
        

    priority = assign_dispute.assign_priority(category, dispute)
    
    team = assign_dispute.assign_team(category, priority)

    unique_ref  = dispute.transaction_id + dispute.customer_id +str(random.randint(1,1000))

    if dispute.LLMAPI: 
        recommendation = get_chatgpt_recommendation( dispute,category, priority, team, unique_ref)
    else:
        recommendation = clf_dispute.generate_rulebased_recommendation(category)
    
    dispute_to_db(db_conn, dispute,category, priority, team, unique_ref, recommendation)


    response = DisputeResponse(
        transaction_id=dispute.transaction_id,
        assigned_category=category,
        priority=priority,
        assigned_team=team,
        reference_number=unique_ref,
        recommendation=recommendation
    )
    
    return response


if __name__ == "__main__":
    
    uvicorn.run(app, host = "0.0.0.0", port= 8000)