# AutoFix AI — Intelligent Autocorrect System

AutoFix AI is a hybrid autocorrect engine built using:

- **SymSpell** → Ultra-fast typo correction  
- **T5 Transformer** → Contextual grammar & spelling correction  
- **Streamlit UI** → Beautiful web interface  

This project automatically fixes:

- Spelling mistakes  
- Grammar errors  
- Missing words  
- Contextual confusion (“ther” → “their”, “there”)  

---

## Live Demo
Click **Run** to launch the Streamlit app.

---

## Technology Stack
- Python
- Streamlit
- SymSpellPy
- HuggingFace Transformers
- T5 Grammar Correction Model

---

## How It Works
### 1. SymSpell Stage  
Finds nearest word with 1–2 character edits.

### 2. T5 Transformer Stage  
Understands context and produces the best corrected sentence.

---

## 📚 Example
Input:
