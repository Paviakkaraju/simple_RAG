import streamlit as st
from ui.chat_logic import model, get_relevant_chunks, generate_response
from sentence_transformers import SentenceTransformer
embed_model = SentenceTransformer("all-MiniLM-L6-v2", device='cpu')

st.title("Codework Chatbot")
st.write("Welcome to the Codework Chatbot. Ask any question about codework!")

user_query = st.text_input("Your question:")

if st.button("Submit") and user_query:
    st.write("🔍 Retrieving relevant information...")
    
    # Retrieve relevant chunks from ChromaDB based on user query
    results = get_relevant_chunks(user_query, embed_model,top_k=3)
    retrieved_docs = results.get("documents", [])
    
    st.write("ℹ️ Retrieved context:")
    for doc in retrieved_docs:
        st.write(f"- {doc}")
    
    st.write("🤖 Generating response...")
    # Generate the final answer using the retrieved context and user query
    answer = generate_response(user_query, model, retrieved_docs)
    st.write("**Answer:**")
    st.write(answer)
