# ⚖️ ALMA: Automated Legal Mapping & Analysis System
<img width="1907" height="741" alt="image" src="https://github.com/user-attachments/assets/2c6e79e9-ec08-41ec-ae4a-4c76638a63fd" />
<img width="1603" height="813" alt="image" src="https://github.com/user-attachments/assets/4dffca49-7249-49d7-9c28-c1aca0aa8a4d" />


**ALMA** is a Neuro-Symbolic AI expert system designed to provide deterministic legal assessments for Indian Statutory Laws. By decoupling semantic perception (LLM) from logical execution (Symbolic Math), ALMA eliminates the "hallucination" risks associated with pure generative AI in high-stakes legal domains.

---

##  Project Overview

ALMA introduces a **Neuro-Symbolic Architecture**:

-  **Neuro Layer (LLM - Llama-3):** Handles Natural Language Understanding  
-  **Symbolic Layer (Python Engine):** Executes legal logic deterministically  

This hybrid approach ensures:
- No mathematical hallucinations  
- 100% deterministic computation  
- ⚖️ Legally auditable outputs  

---

## 🔁 The Pipeline: How It Works

### **1️⃣ Semantic Perception (Neuro Layer)**
The system processes unstructured user input such as emotional or conversational legal narratives.

- Uses **Llama-3** for parsing
- Performs:
  - Named Entity Recognition (NER)
  - Relation Extraction
- Extracts:
  - Age, income, land size, injury, etc.
- Ignores emotional noise using rule-based filtering

---

### **2️⃣ Structured Representation (JSON Bridge)**
Extracted data is converted into a structured format.

- Output: **Typed JSON Dictionary**
- Acts as a **Data Contract**
- Ensures:
  - Transparency
  - Debugging capability
  - Auditability

---

### **3️⃣ Statutory Execution (Symbolic Layer)**
The JSON data is passed into a deterministic Python engine.

- Executes:
  - Mathematical formulas
  - Legal thresholds
  - Boolean logic rules

- Covers:
  - 🚗 Motor Vehicles Act (Sarla Verma Guidelines)
  - 🌱 West Bengal Land Reforms Act (WBLRA)
  - 🏠 Protection of Women from Domestic Violence Act (PWDVA)

 **Guarantee:** No hallucination — only rule-based computation

---

### **4️⃣ Explainable Output (Streamlit UI)**
Results are displayed through a user-friendly dashboard.

- 📊 Shows:
  - Final verdict (legal/compensation result)
  - Step-by-step reasoning trace
- 🧾 Provides:
  - Section-wise legal justification
  - Transparent calculation breakdown

---

## 📊 Key Results

| Module | Accuracy | Notes |
|--------|--------|------|
| 🚗 Motor Vehicles Act | 86% | 100% calculation precision |
| 🌱 Land Reforms (WBLRA) | 92% | Accurate land conversion logic |
| 🏠 PWDVA | 93% | Effective trauma-to-law mapping |

---

## 💡 Key Features

- 🔹 Neuro-Symbolic AI Architecture  
- 🔹 Deterministic Legal Computation  
- 🔹 Explainable AI (White-box reasoning)  
- 🔹 Multi-domain Legal Support  
- 🔹 Streamlit-based Interactive UI  

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **LLM:** Llama-3  
- **Architecture:** Neuro-Symbolic AI  
- **Data Format:** JSON  

---

