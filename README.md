
# Tools used:
1. ChatGPT API  
2. FastAPI  
3. Python  
4. Pydantic  
5. SQLite  

---

## Implemented API:  
**POST** `/disputes/`  

---

## Implementation:
```bash
pip install -r requirements.txt
```

Install SQLite DB or view it using **DB Browser** (DBvear).  

```bash
python main.py
```

or to run the main app in a loop for dispute addition:  
```bash
uvicorn main:app --reload
```

Check implemented API docs:  
- [http://localhost:8000/docs](http://localhost:8000/docs)  
- [http://localhost:8000/docs#/default/create_dispute_disputes__post](http://localhost:8000/docs#/default/create_dispute_disputes__post)  


## results:
1. Sample query:
   ![Sample query](https://github.com/user-attachments/assets/cd722bc9-6a8e-4458-a1ac-7b49845a0752)
2. Sample_response_using_CHATGPT_API
   ![Sample_response_using_CHATGPT_API](https://github.com/user-attachments/assets/9d27a087-fedf-4ea4-906f-e42bc15d916b)
3. Storing in DB for future improvements in AIML models
   ![Storing in DB for future improvements in AIML models](https://github.com/user-attachments/assets/882a7c45-9634-48e0-8003-f254a49d23d4)


---

## Workflow:

### 1. Take input:
Sample input:
```json
{
    "transaction_id": "123456",
    "amount": 1500.00,
    "description": "I don't recognize this transaction on my bank account, it's unauthorized and I have not initiated it",
    "customer_id": "ABCD123",
    "acc_opened_years": 3,
    "previous_disputes": 1,
    "is_premium": true,
    "acc_balance": 100000.00,
    "LLMAPI": true
}
```
- The last 4 attributes (`acc_opened_years`, `previous_disputes`, `is_premium`, `acc_balance`) are historical attributes of the user. These attributes help in understanding the user’s relationship with the bank and allow prioritization to avoid customer loss.  

---

### 2. Uses AI to classify disputes:
- Since there is no data for training a machine learning model, a **rule-based system** is used for classification.  
- If an API key is available, the ChatGPT API is used to generate recommended actions dynamically.  
- If the API key is unavailable, a static rule-based response is generated.  

---

### 3. Routes the dispute to the right team:
- A team assignment and priority tag is added in the database.  
- Routing is based on this tag, which allows the next system to query the DB and fetch disputes based on team and priority.  
- This helps create better in-house AI/ML models specific to the bank or client.  

**Goal:**  
- Create a DB that stores all fields of the sample input.  
- Add three new columns: **Team assignment**, **Priority**, and **Recommended actions**.  

---

## File Structure:

### `main.py`:
- Implements the basic API for `create_dispute`.  
- After receiving the dispute input, two classes are called:  
    - `classifyDisputes` (from `classify_disputes.py`)  
    - `disputeAssignment` (from `dispute_assignment.py`)  
- Uses **Pydantic** for input consistency.  
- Uses enums for categorization of team, dispute category, and priority to avoid hardcoding and improve readability.  

---

### `classify_disputes.py`:
**class `classifyDisputes`**  
- **Purpose:** Classifies the dispute and generates recommended actions.  
- **Methods:**  
    - `classify_dispute_AI()` – Placeholder for AI-based classification using LLM.  
    - `classify_dispute_rule_based()` –  
        - Uses a rule-based system for classification based on keywords in the description.  
        - Categories:  
            - `UNAUTHORIZED` – if the description contains "unauthorized", "not me", "fraud".  
            - `DUPLICATE` – if the description contains "twice", "double", "duplicate".  
            - `WRONG_AMOUNT` – if the description contains "wrong amount", "incorrect amount".  
            - `OTHER` – for all other cases.  

    - `generate_rulebased_recommendation(category)` –  
        - Generates static rule-based recommendations based on the category.  
        - Sample recommendations:  
            - **UNAUTHORIZED** – "Recommendation: sample Rule based recommendation for UNAUTHORIZED"  
            - **DUPLICATE** – "Recommendation: sample Rule based recommendation for DUPLICATE"  
            - **WRONG_AMOUNT** – "Recommendation: sample Rule based recommendation for WRONG_AMOUNT"  
            - **OTHER** – "Recommendation: sample Rule based recommendation for OTHER"  

---

### `dispute_assignment.py`:
**class `disputeAssignment`**  
- **Purpose:** Assigns a priority and team to the dispute based on category and dispute details.  
- **Methods:**  
    - `assign_priority(category, dispute)` –  
        - Assigns priority based on:  
            - **URGENT** – Unauthorized disputes over $10,000.  
            - **MEDIUM** – Unauthorized disputes over $1,000.  
            - **HIGH** – Previous disputes > 5 or amount > $100,000 or premium user.  
            - **LOW** – Default for other cases.  

    - `assign_team(category, priority)` –  
        - Assigns the dispute to the appropriate team:  
            - **FRAUD** – If category is `UNAUTHORIZED`.  
            - **BILLING** – If category is `DUPLICATE` or `WRONG_AMOUNT`.  
            - **ESCALATION** – If priority is `URGENT` or `HIGH`.  
            - **CUSTOMER_SERVICE** – Default for other cases.  

---

### `db_ops.py`:
- Handles database operations for storing dispute details and fetching them when needed.  

---

### `get_recommendation_agent.py`:
- Handles AI-based classification and recommendation using ChatGPT API (if API key is available).  

---

## Further Tasks:
Error handling based on LLM API failures.  
Async processing for faster classification and recommendations.  
More complex rule-based classification.  

---
