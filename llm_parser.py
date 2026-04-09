import json
import ollama
import re

def normalize_family_size(data):
    """
    Safety Layer: Converts common words to numbers if the AI forgets.
    """
    # 1. Handle explicit word-to-number cases for family size
    fam = str(data.get('family_size', 1)).lower()
    
    word_map = {
        "single": 1, "sole": 1, "myself": 1, "one": 1,
        "couple": 2, "two": 2, "wife": 2, "husband": 2,
        "three": 3, "four": 4, "five": 5, "six": 6, 
        "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    
    # Check if the value is in our map (e.g., "single" -> 1)
    if fam in word_map:
        data['family_size'] = word_map[fam]
    else:
        # Try to force convert "5" (string) to 5 (int)
        try:
            data['family_size'] = int(fam)
        except:
            # Fallback default
            data['family_size'] = 1
            
    return data

def parse_query(user_text):
    """
    Extracts ALL legal parameters from a single natural language query.
    """
    
    # 1. The Super-Prompt (Updated with "Single" instructions)
    prompt = f"""
    You are a Legal Data Extraction Engine. 
    Extract parameters into strict JSON.
    
    RULES FOR 'FAMILY_SIZE':
    - If user says "single", "myself", "sole", or "only me" -> output 1.
    - If user says "couple", "me and my wife" -> output 2.
    - Convert number words ("five") to integers (5).
    
    DEFAULTS (if missing):
    - current_holding_acres: 0.0
    - current_land_type: "non-irrigated"
    - family_size: 1
    
    SCHEMA:
    {{
      "family_size": (int) ALWAYS output an integer (e.g., 1, 5),
      "current_holding_acres": (float) convert to acres,
      "current_land_type": (string) 'irrigated', 'non-irrigated', 'orchard', 'homestead',
      "intent": (string) 'buy', 'sell', 'inherit',
      "new_amount_acres": (float) convert to acres,
      "new_land_type": (string) 'irrigated', 'non-irrigated', 'orchard', 'homestead'
    }}

    EXAMPLES:
    Input: "I am a single person buying 2 acres of Shali."
    Output: {{ "family_size": 1, "current_holding_acres": 0.0, "current_land_type": "non-irrigated", "intent": "buy", "new_amount_acres": 2.0, "new_land_type": "irrigated" }}

    Input: "Me and my wife want to buy 5 acres. We have no land."
    Output: {{ "family_size": 2, "current_holding_acres": 0.0, "current_land_type": "non-irrigated", "intent": "buy", "new_amount_acres": 5.0, "new_land_type": "non-irrigated" }}

    Input: "Family of three owning 10 bighas of orchard."
    Output: {{ "family_size": 3, "current_holding_acres": 3.3, "current_land_type": "orchard", "intent": "buy", "new_amount_acres": 0.0, "new_land_type": "non-irrigated" }}

    CURRENT QUERY: "{user_text}"
    OUTPUT JSON ONLY:
    """

    try:
        # 2. Call Ollama
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': "Output JSON only. No text."},
            {'role': 'user', 'content': prompt},
        ])
        
        raw_text = response['message']['content']
        
        # 3. Clean & Parse
        clean_text = re.sub(r'```json\s*', '', raw_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'```', '', clean_text)
        
        start = clean_text.find('{')
        end = clean_text.rfind('}') + 1
        
        if start != -1 and end != -1:
            json_str = clean_text[start:end]
            data = json.loads(json_str)
            
            # 4. Apply the Safety Layer (The Fix)
            data = normalize_family_size(data)
            
            return data
        else:
            return {"error": "Invalid JSON from AI", "raw": raw_text}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the fix immediately
    print(parse_query("I am a single person"))

# Add this to the bottom of your llm_parser.py

import json
import ollama
import re

def parse_mv_query(user_text):
    """
    Extracts parameters for the Motor Vehicles Act.
    """
    # Notice the DOUBLE BRACES {{ }} used around the JSON objects in this f-string
    prompt = f"""
    You are a strictly literal Data Extraction Engine. 
    Extract the EXACT numbers from the text into strict JSON.
    DO NOT apply legal knowledge. DO NOT do any math. DO NOT divide or multiply.
    
    SCHEMA:
    {{
      "age": (int) victim's age,
      "monthly_income": (float) Exact income. Do not do math,
      "dependents": (int) number of dependents,
      "marital_status": (string) 'single' or 'married',
      "employment_type": (string) 'permanent' or 'self-employed',
      "medical_bills": (float) Medical expenses. Default 0.0,
      "claim_type": (string) If text says 'hit and run', output 'hit-and-run'. If it says 'no fault' or 'section 164', output 'no-fault'. Otherwise output 'fault',
      "outcome": (string) If victim died, output 'death'. If survived/injured, output 'injury',
      "disability_percent": (float) Percentage of permanent disability (e.g., 40.0). Default 0.0,
      "hospital_days": (int) Number of days spent in hospital. Default 0
    }}

    EXAMPLES:
    Input: "A hit and run case where a 30 year old died."
    Output: {{ "age": 30, "monthly_income": 0.0, "dependents": 0, "marital_status": "single", "employment_type": "self-employed", "medical_bills": 0.0, "claim_type": "hit-and-run", "outcome": "death", "disability_percent": 0.0, "hospital_days": 0 }}

    Input: "A 35 year old man making 40000 a month survived a crash but suffered 45 percent permanent disability. He was in the hospital for 20 days with 1 lakh in medical bills."
    Output: {{ "age": 35, "monthly_income": 40000.0, "dependents": 0, "marital_status": "single", "employment_type": "self-employed", "medical_bills": 100000.0, "claim_type": "fault", "outcome": "injury", "disability_percent": 45.0, "hospital_days": 20 }}

    CURRENT QUERY: "{user_text}"
    OUTPUT JSON ONLY:
    """

    try:
        # Standard dictionary syntax here, no double braces needed since it's not an f-string
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': "Output JSON only. No text."},
            {'role': 'user', 'content': prompt},
        ])
        
        raw_text = response['message']['content']
        clean_text = re.sub(r'```json\s*', '', raw_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'```', '', clean_text)
        
        # Searching for single braces in the final string
        start = clean_text.find('{')
        end = clean_text.rfind('}') + 1
        
        if start != -1 and end != -1:
            return json.loads(clean_text[start:end])
        else:
            return {"error": "Invalid JSON"}

    except Exception as e:
        return {"error": str(e)}
    

def parse_dv_query(user_text):
    """
    Precise extraction engine for the PWDVA 2005.
    Only outputs child count if explicitly mentioned as a number.
    """
    
    system_instruction = (
        "You are a specialized Legal Data Extraction Bot for the Domestic Violence Act. "
        "Your ONLY job is to convert natural language into valid JSON. "
        "STRICT RULES: "
        "1. DO NOT add conversational text. "
        "2. DO NOT infer the number of children; if no number is mentioned, output 0. "
        "3. Convert word-numbers (e.g., 'two') to integers (2). "
        "4. Categorize abuse based strictly on Section 3 definitions."
    )

    prompt = f"""
    ### DATA ANCHOR RULES:
    1. 'EARNS' or 'MAKES' -> Map strictly to respondent_net_monthly_income.
    2. 'WORTH' or 'VALUED AT' -> Map strictly to property_damage_value.
    3. 'SALARY' or 'WAGES' (if lost) -> Map strictly to loss_of_earnings.
    4. 'HOSPITAL' or 'SURGERY' -> Map strictly to medical_expenses.

    ### SCHEMA (ALL KEYS REQUIRED):
    {{
      "respondent_net_monthly_income": (float) Default: 0.0,
      "aggrieved_net_monthly_income": (float) Default: 0.0,
      "number_of_children": (int) Default: 0,
      "threat_of_eviction": (bool) Default: false,
      "medical_expenses": (float) Default: 0.0,
      "loss_of_earnings": (float) MUST extract any amount linked to 'salary', 'wages', or 'lost'. Default: 0.0,
      "property_damage_value": (float) Default: 0.0,
      "abuse_incidents": (list) Choose from: ['physical', 'sexual', 'verbal', 'emotional', 'economic']
    }}

    ### TEST CASE FIXES:
    Input: "Husband earns 50,000. He took jewelry worth 1,00,000."
    Output: {{ "respondent_net_monthly_income": 50000.0, "aggrieved_net_monthly_income": 0.0, "number_of_children": 0, "threat_of_eviction": false, "medical_expenses": 0.0, "loss_of_earnings": 0.0, "property_damage_value": 100000.0, "abuse_incidents": ["economic"] }}

    Input: "Husband earns 80,000. I had surgery for 30,000 and lost 10,000 in salary."
    Output: {{ "respondent_net_monthly_income": 80000.0, "aggrieved_net_monthly_income": 0.0, "number_of_children": 0, "threat_of_eviction": false, "medical_expenses": 30000.0, "loss_of_earnings": 10000.0, "property_damage_value": 0.0, "abuse_incidents": ["physical", "economic"] }}

    QUERY: "{user_text}"
    JSON ONLY:
    """

    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': system_instruction},
            {'role': 'user', 'content': prompt},
        ])
        
        raw_text = response['message']['content']
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return {"error": "Invalid JSON"}
    except Exception as e:
        return {"error": str(e)}