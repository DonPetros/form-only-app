import streamlit as st
import os
import json

st.title("📝 Respond to a Survey")

# Load form files
form_dir = "forms"
if not os.path.exists(form_dir):
    st.warning("No forms found.")
    st.stop()

form_files = [f for f in os.listdir(form_dir) if f.endswith(".json")]
if not form_files:
    st.warning("No available forms.")
    st.stop()

selected_form = st.selectbox("Select a form to complete:", form_files)

with open(os.path.join(form_dir, selected_form), "r") as f:
    form_data = json.load(f)

st.header(form_data["title"])
responses = []

for q in form_data["questions"]:
    if q["type"] == "Text":
        response = st.text_input(q["text"])
    elif q["type"] == "Scale (1–5)":
        response = st.slider(q["text"], 1, 5, 3)
    elif q["type"] == "Multiple Choice":
        response = st.radio(q["text"], q["options"])
    else:
        response = "Unsupported question type"
    responses.append({"question": q["text"], "response": response})

# Save responses
if st.button("Submit"):
    os.makedirs("responses", exist_ok=True)
    response_file = f"responses/{selected_form.replace('.json','')}_responses.json"

    if os.path.exists(response_file):
        with open(response_file, "r") as f:
            all_responses = json.load(f)
    else:
        all_responses = []

    all_responses.append(responses)

    with open(response_file, "w") as f:
        json.dump(all_responses, f, indent=4)

    st.success("✅ Response submitted! Thank you.")
