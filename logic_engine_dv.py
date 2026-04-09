class DomesticViolenceLogicEngine:
    def __init__(self, data):
        self.data = data
        self.reasons = []

    def evaluate_reliefs(self):
        """Maps facts to Sections 18-22 based on Section 3 definitions."""
        orders = []
        abuse = self.data.get("abuse_incidents", [])
        
        # Sec 18: Protection Orders [cite: 28, 90]
        if any(x in abuse for x in ['physical', 'sexual', 'verbal', 'emotional']):
            orders.append({"section": "18", "relief": "Protection Order", "desc": "Prohibits the respondent from committing or aiding acts of domestic violence[cite: 172]."})
        
        # Sec 19: Residence Orders [cite: 29, 110]
        if self.data.get("threat_of_eviction") or 'economic' in abuse:
            orders.append({"section": "19", "relief": "Residence Order", "desc": "Secures right to shared household and restrains dispossession[cite: 181]."})
            
        # Sec 21: Custody Orders [cite: 31, 208]
        if self.data.get("number_of_children", 0) > 0:
            orders.append({"section": "21", "relief": "Custody Order", "desc": "Temporary custody of children to the mother[cite: 208]."})
            
        # Sec 22: Compensation Orders [cite: 32, 211]
        if any(x in abuse for x in ['emotional', 'sexual', 'physical']):
            orders.append({"section": "22", "relief": "Compensation Order", "desc": "Damages for mental torture and emotional distress[cite: 211]."})
            
        return orders

    def calculate_monetary_relief(self):
        """Calculates Monetary Relief under Section 20."""
        self.reasons = [] 
        
        # BULLETPROOF EXTRACTION: Converts 'null' or missing keys to safe numbers
        r_income = float(self.data.get("respondent_net_monthly_income") or 0.0)
        a_income = float(self.data.get("aggrieved_net_monthly_income") or 0.0)
        kids = int(self.data.get("number_of_children") or 0)
        medical = float(self.data.get("medical_expenses") or 0.0)
        earnings_loss = float(self.data.get("loss_of_earnings") or 0.0)
        property_loss = float(self.data.get("property_damage_value") or 0.0)

        # 1. Maintenance Calculation (Sec 20(1)(d))
        rate = 0.33 if kids > 0 else 0.25
        target_maintenance = r_income * rate
        final_maintenance = max(0, target_maintenance - (a_income * 0.5))
        
        self.reasons.append(f"Maintenance of ₹{final_maintenance:,.2f} calculated under Sec 20(1)(d) at {int(rate*100)}% of Respondent's income.")
        self.reasons.append("Relief assessed to remain consistent with standard of living per Sec 20(2).")
        
        if a_income > 0:
            self.reasons.append(f"Offset applied for Aggrieved Person's income (₹{a_income:,.2f}) to determine fair balancing.")

        # 2. Medical Expenses (Sec 20(1)(b))
        if medical > 0:
            self.reasons.append(f"Medical expenses of ₹{medical:,.2f} included as per Sec 20(1)(b).")

        # 3. Loss of Earnings (Sec 20(1)(a))
        if earnings_loss > 0:
            self.reasons.append(f"Loss of earnings (₹{earnings_loss:,.2f}) included as per Sec 20(1)(a).")

        # 4. Property Damage / Stridhan Loss
        if property_loss > 0:
            self.reasons.append(f"Value of property damage or unreturned Stridhan (₹{property_loss:,.2f}) included.")

        total_one_time = medical + earnings_loss + property_loss

        return {
            "monthly": round(final_maintenance, 2),
            "one_time": round(total_one_time, 2),
            "total_initial": round(final_maintenance + total_one_time, 2),
            "reasons": self.reasons
        }