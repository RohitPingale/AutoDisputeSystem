
class disputeAssignment:
    def __init__(self, DisputeCategory, PriorityLevel, TeamAssignment):
        self.DisputeCategory = DisputeCategory
        self.PriorityLevel = PriorityLevel
        self.TeamAssignment = TeamAssignment

    def assign_priority(self, category, dispute):
  
        if category == self.DisputeCategory.UNAUTHORIZED and dispute.amount > 10000:
            return self.PriorityLevel.URGENT

        if category == self.DisputeCategory.UNAUTHORIZED and dispute.amount > 1000:
            return self.PriorityLevel.MEDIUM
        

        if dispute.previous_disputes > 5:
            return self.PriorityLevel.HIGH
        

        if dispute.amount > 100000:
            return self.PriorityLevel.HIGH
        elif dispute.amount > 5000:
            return self.PriorityLevel.MEDIUM
        

        if dispute.is_premium:
            return self.PriorityLevel.HIGH
    
        return self.PriorityLevel.LOW


    def assign_team(self,category,priority):
        if category == self.DisputeCategory.UNAUTHORIZED:
            return self.TeamAssignment.FRAUD

        elif category == self.DisputeCategory.DUPLICATE or category == self.DisputeCategory.WRONG_AMOUNT:
            return self.TeamAssignment.BILLING

        elif priority == self.PriorityLevel.URGENT or priority == self.PriorityLevel.HIGH:
            return self.TeamAssignment.ESCALATION
        else:
            return self.TeamAssignment.CUSTOMER_SERVICE


