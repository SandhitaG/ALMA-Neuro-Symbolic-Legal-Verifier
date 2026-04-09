# logic_engine_mv.py 
# Master MACT Engine (Sections 161, 164, 166)
# Incorporates Sarla Verma, Pranay Sethi, Raj Kumar, and Notional Income Precedents

def get_multiplier(age):
    """Returns statutory multiplier based on age (Sarla Verma)."""
    if age <= 15: return 15
    elif 16 <= age <= 25: return 18
    elif 26 <= age <= 30: return 17
    elif 31 <= age <= 35: return 16
    elif 36 <= age <= 40: return 15
    elif 41 <= age <= 45: return 14
    elif 46 <= age <= 50: return 13
    elif 51 <= age <= 55: return 11
    elif 56 <= age <= 60: return 9
    elif 61 <= age <= 65: return 7
    else: return 5

def get_personal_expense_deduction(marital_status, dependents):
    """Calculates deduction fraction for personal expenses."""
    marital_status = str(marital_status).lower()
    if "single" in marital_status or "unmarried" in marital_status: 
        return 0.50
    else:
        if dependents <= 3: return 1/3
        elif 4 <= dependents <= 5: return 1/4
        else: return 1/5

def get_future_prospects(age, employment_type):
    """Adds a percentage to income based on age and job security (Pranay Sethi)."""
    job = str(employment_type).lower()
    is_permanent = "permanent" in job or "salaried" in job
    
    if age < 40: return 0.50 if is_permanent else 0.40
    elif 40 <= age <= 50: return 0.30 if is_permanent else 0.25
    elif 51 <= age <= 60: return 0.15 if is_permanent else 0.10
    else: return 0.00

def calculate_compensation(age, monthly_income, dependents, marital_status, employment_type="self-employed", medical_bills=0.0, claim_type="fault", outcome="death", disability_percent=0.0, hospital_days=0):
    """
    Master MACT Calculator. Routes to Section 161, 164, or 166 based on parameters.
    """
    claim_type = str(claim_type).lower()
    outcome = str(outcome).lower()
    
    # ==========================================
    # ROUTE 1: Section 161 (Hit and Run)
    # ==========================================
    if claim_type == "hit-and-run":
        if outcome == "death":
            return True, "✅ **HIT-AND-RUN (Sec 161) DEATH CLAIM: ₹2,00,000**\n\nUnder Section 161 of the Motor Vehicles Act, the fixed compensation for death in a hit-and-run case (where the identity of the vehicle is untraceable) is ₹2 Lakhs. No multiplier math is required."
        else:
            return True, "✅ **HIT-AND-RUN (Sec 161) INJURY CLAIM: ₹50,000**\n\nUnder Section 161, the fixed compensation for grievous hurt in a hit-and-run case is ₹50,000."

    # ==========================================
    # ROUTE 2: Section 164 (No-Fault Liability)
    # ==========================================
    elif claim_type == "no-fault":
        if outcome == "death":
            return True, "✅ **NO-FAULT LIABILITY (Sec 164) DEATH CLAIM: ₹5,00,000**\n\nUnder Section 164 (2019 Amendment), you do not need to prove negligence. The fixed statutory payout for death is ₹5 Lakhs."
        else:
            return True, "✅ **NO-FAULT LIABILITY (Sec 164) INJURY CLAIM: ₹2,50,000**\n\nUnder Section 164, the fixed statutory payout for grievous hurt without proving negligence is ₹2.5 Lakhs."

    # ==========================================
    # ROUTE 3: Section 166 (Fault-Based)
    # ==========================================
    else: 
        if age <= 0:
            return False, "🚫 MISSING DATA: The victim's age is mandatory to determine the legal multiplier."

        # --- NOTIONAL INCOME LOGIC (For Minors, Homemakers, Unemployed) ---
        is_notional = False
        if monthly_income <= 0:
            is_notional = True
            # Apply standard Supreme Court notional income for non-earning members
            if age <= 15:
                monthly_income = 2500.0  # ₹30,000 annually for minors
            else:
                monthly_income = 3500.0  # ₹42,000 annually for homemakers/unemployed adults

        # Core Math
        base_annual_income = monthly_income * 12
        fp_percentage = get_future_prospects(age, employment_type)
        fp_amount = base_annual_income * fp_percentage
        gross_annual_income = base_annual_income + fp_amount
        multiplier = get_multiplier(age)

        # --- PATH A: DEATH CLAIM (Sarla Verma) ---
        if outcome == "death":
            deduction_fraction = get_personal_expense_deduction(marital_status, dependents)
            personal_expenses = gross_annual_income * deduction_fraction
            net_annual_dependency = gross_annual_income - personal_expenses
            loss_of_dependency = net_annual_dependency * multiplier
            
            conventional_heads = 15000 + 15000 + (40000 * dependents)
            grand_total = loss_of_dependency + conventional_heads + medical_bills
            
            notional_warning = "*(⚠️ Court-Assigned Notional Income Applied)*\n" if is_notional else ""
            
            breakdown = (
                f"✅ **SEC 166 DEATH COMPENSATION: ₹{grand_total:,.2f}**\n\n"
                f"**1. Income & Dependency:**\n{notional_warning}"
                f"- Base Annual Income: ₹{base_annual_income:,.2f} (₹{monthly_income:,.2f}/mo)\n"
                f"- Future Prospects Added ({fp_percentage*100:.0f}% for {employment_type}): +₹{fp_amount:,.2f}\n"
                f"- Gross Annual Income: ₹{gross_annual_income:,.2f}\n"
                f"- Personal Expenses Deducted: -₹{personal_expenses:,.2f}\n"
                f"- Net Annual Dependency: ₹{net_annual_dependency:,.2f}\n"
                f"- Multiplier: {multiplier} (Age {age})\n"
                f"- **Total Loss of Dependency: ₹{loss_of_dependency:,.2f}**\n\n"
                f"**2. Damages:**\n"
                f"- Conventional Heads (Estate, Funeral, Consortium): ₹{conventional_heads:,.2f}\n"
                f"- Medical Bills: ₹{medical_bills:,.2f}\n"
            )
            return True, breakdown
        
        # --- PATH B: INJURY & DISABILITY CLAIM (Raj Kumar v. Ajay Kumar) ---
        else:
            if disability_percent <= 0:
                return False, "🚫 MISSING DATA: For an injury claim under Sec 166, you must provide the Percentage of Permanent Disability (e.g., 'suffered 40% disability')."
            
            # 1. Loss of Future Earnings (No personal deduction for survivors)
            loss_of_earning_capacity = gross_annual_income * multiplier * (disability_percent / 100.0)
            
            # 2. Non-Pecuniary Damages
            pain_and_suffering = disability_percent * 1500.0 
            loss_of_amenities = disability_percent * 1000.0
            
            # 3. Special Damages
            special_diet_and_attendant = hospital_days * 1000.0
            
            grand_total = loss_of_earning_capacity + pain_and_suffering + loss_of_amenities + special_diet_and_attendant + medical_bills
            
            notional_warning = "*(⚠️ Court-Assigned Notional Income Applied)*\n" if is_notional else ""

            breakdown = (
                f"✅ **SEC 166 INJURY COMPENSATION: ₹{grand_total:,.2f}**\n\n"
                f"**1. Loss of Future Earning Capacity:**\n{notional_warning}"
                f"- Base Annual Income: ₹{base_annual_income:,.2f} (₹{monthly_income:,.2f}/mo)\n"
                f"- Gross Annual (with {fp_percentage*100:.0f}% Future Prospects): ₹{gross_annual_income:,.2f}\n"
                f"- Permanent Disability: {disability_percent}%\n"
                f"- Multiplier: {multiplier} (Age {age})\n"
                f"- **Total Earning Loss: ₹{loss_of_earning_capacity:,.2f}**\n\n"
                f"**2. Non-Pecuniary & Special Damages:**\n"
                f"- Pain & Suffering: ₹{pain_and_suffering:,.2f}\n"
                f"- Loss of Amenities: ₹{loss_of_amenities:,.2f}\n"
                f"- Attendant & Special Diet ({hospital_days} days): ₹{special_diet_and_attendant:,.2f}\n"
                f"- Medical Bills: ₹{medical_bills:,.2f}\n"
            )
            return True, breakdown