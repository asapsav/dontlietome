import streamlit as st
import json
import dotenv
import os
import requests
dotenv.load_dotenv()
import openai


YOUDOTCOM_API_KEY = os.getenv("YOUDOTCOM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
OPENAI_MODEL = "gpt-4-1106-preview"

def get_ai_snippets_for_query(query):
    headers = {"X-API-Key": YOUDOTCOM_API_KEY}
    params = {"query": query}
    return requests.get(
        f"https://api.ydc-index.io/search?query={query}",
        params=params,
        headers=headers,
    ).json()

messages = [
        {"role": "system", "content": "You are a helpfull assistant."}
    ]
def get_openai_completions(prompt, messages):

    messages.append({"role": "user", "content": prompt})
    
    completion = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages
    )
    
    assistant_message = completion.choices[0].message['content']
    messages.append({"role": "assistant", "content": assistant_message})

    return assistant_message, messages

# Placeholder function for data analysis
def analyze_claim(link, claim):
    # Placeholder data
    try:
        data_needed = get_openai_completions(f"What data is needed to find if this claim: {claim} is true or false?", messages)
    except Exception as e:
        data_needed = f"Error: {e}"
    try:
        search_results = get_ai_snippets_for_query(data_needed)
    except Exception as e:
        search_results = f"Error: {e}"

    return {
        "data_needed": data_needed,
        "data_source": "Sources of data",
        "found_data": search_results
    }


# Main application
def main():
    st.title("Claim Analysis Tool")

    # Input section
    link = st.text_input("Enter the link to the claim:")
    claim = st.text_area("Enter the claim:")
    
    if st.button("Analyze Claim"):
        if link and claim:
            # Analyzing the claim
            analysis = analyze_claim(link, claim)

            # Displaying results
            st.subheader("1. Data Needed to Debunk the Claim")
            st.write(analysis["data_needed"])

            st.subheader("2. Where to Find the Data")
            st.write(analysis["data_source"])

            st.subheader("3. What Data Was Found")
            st.write(analysis["found_data"])

            # JSON log
            st.subheader("4. OLOG of the Claim and Data Found")
            json_log = {
                "claim": claim,
                "analysis": analysis
            }
            st.json(json_log)

            # Placeholder for ULTRA Model Embeddings
            st.subheader("5. ULTRA Embeddings")
            st.image("word_embeddings_colah.png", caption="Placeholder for ULTRA Model Embeddings")

            # Description of Embeddings
            st.subheader("6. Description of ULTRA Model Embeddings")
            st.write("This is a placeholder description for the ULTRA model embeddings.")

        else:
            st.error("Please enter both the link and the claim.")

if __name__ == "__main__":
    main()
