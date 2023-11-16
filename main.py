import streamlit as st
import json
import dotenv
import os
import requests
dotenv.load_dotenv()
import openai
import networkx as nx
import matplotlib.pyplot as plt
from prompts import OLOG_EXAMPLE


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


def get_openai_completions(prompt):
    messages = [
        {"role": "system", "content": "You are a helpfull assistant to help with misinforamtion reserach. Bespicific and keep you answers short"}
    ]
    messages.append({"role": "user", "content": prompt})
    
    completion = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages
    )
    
    assistant_message = completion.choices[0].message['content']
    messages.append({"role": "assistant", "content": assistant_message})

    return assistant_message

def create_olog_graph(data):
    G = nx.DiGraph()

    for node in data["olog"]["nodes"]:
        G.add_node(node["id"], label=node["text"])

    for edge in data["olog"]["edges"]:
        G.add_edge(edge["source"], edge["target"], label=edge["relation"])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'))
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    return G


# Placeholder function for data analysis
def analyze_claim(link, claim):
    # Placeholder data
    try:
        data_needed = get_openai_completions(f"What data is needed to find if this claim: {claim} is true or false?")
    except Exception as e:
        data_needed = f"Error: {e}"

    try:
        data_sources  = get_openai_completions(f"Where to find this data: {data_needed}? Just output the short list of data sources.")
    except Exception as e:
        data_sources = f"Error: {e}"
    try:
        search_results = get_ai_snippets_for_query(data_needed)
    except Exception as e:
        search_results = f"Error: {e}"

    return {
        "data_needed": data_needed,
        "data_source": data_sources,
        "found_data": search_results
    }


# Main application
def main():
    st.title("Graph neural networks to spot false information")

    # Input section
    link = st.text_input("Enter the link to the claim:")
    claim = st.text_area("Enter the claim:")
    
    if st.button("Analyze Claim"):
        if link and claim:
            # Analyzing the claim
            analysis = analyze_claim(link, claim)

            # Displaying results
            st.subheader("1. Data Needed to Debunk the Claim")
            st.markdown(analysis["data_needed"])

            st.subheader("2. Where to Find the Data")
            st.markdown(analysis["data_source"])

            st.subheader("3. What Data Was Found")
            st.markdown(analysis["found_data"])

            # JSON log
            st.subheader("4. OLOG of the Claim")
            json_olog_str = get_openai_completions(f"Return a json of an OLOG of this claim:{claim}. Return just the json and dont say `Certainly` or anything. Follow the sctructe of thjis example: {OLOG_EXAMPLE}")
            st.markdown(json_olog_str)
            json_olog = json.loads(json_olog_str[7:-3])
            G = create_olog_graph(json_olog)
            # Display the graph
            st.pyplot(plt)

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
