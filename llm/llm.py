from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import threading

model_lock = threading.Lock()

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def generate_response(query: str, context: str = ""):

    input_text = f"""
You are a high-quality assistant in a distributed systems project.

Use the context to answer accurately.

Context:
{context}

Question:
{query}

Rules:
- Answer in 3 to 6 lines
- Be technical and clear
- Do not repeat the question
- Use context if available

Answer:
"""

    inputs = tokenizer(input_text, return_tensors="pt", truncation=True)

    with model_lock:
        outputs = model.generate(**inputs, max_new_tokens=80)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)