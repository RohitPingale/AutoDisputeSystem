
class classifyDisputes:
    def __init__(self, dispute, DisputeCategory):
        self.dispute = dispute
        self.DisputeCategory = DisputeCategory
    
    def classify_dispute_AI(self):
        return None
    
    def classify_dispute_rule_based(self):
        """
        A Automated system require  data and NLP to train ML models
        """

        description = self.dispute.description.lower()
        
        if "unauthorized" in description or "not me" in description or "fraud" in description:
            return self.DisputeCategory.UNAUTHORIZED
        elif "twice" in description or "double" in description or "duplicate" in description:
            return self.DisputeCategory.DUPLICATE
        elif "wrong amount" in description or "incorrect amount" in description:
            return self.DisputeCategory.WRONG_AMOUNT
        else:
            return self.DisputeCategory.OTHER
       
        return None

    def generate_rulebased_recommendation(self, catgory):
        ##imporvement : we can keep this an asyc function to contiously  generating recommendation using in caseof LLM API specfically  and sperate 
        # from the create_dispute process(based on the unqiue of dispute retireve unsolved disputes ant passing those LLM API to  generate the recommendation). 
            if catgory == self.DisputeCategory.UNAUTHORIZED:
                    return "Recommendation: sample Rule based recommendation for UNAUTHORIZED"
            if catgory == self.DisputeCategory.DUPLICATE :
                    return "Recommendation: sample Rule based recommendation for DUPLICATE"
            if catgory == self.DisputeCategory.WRONG_AMOUNT :
                    return "Recommendation: sample Rule based recommendation for WRONG_AMOUNT"
            if catgory == self.DisputeCategory.OTHER :
                    return "Recommendation: sample Rule based recommendation for OTHER"
        