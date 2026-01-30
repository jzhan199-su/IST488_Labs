
import streamlit as st
from openai import OpenAI,  AuthenticationError, APIConnectionError
from PyPDF2 import PdfReader



def read_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Show title and description.
st.title("My Document Summary GPT App")
st.write(
    "Upload a document below and choose a type of summary to generate a result using OpenAI's GPT models.")


# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

#1. Initialize the OpenAI client with the API key from Streamlit secrets.
openai_api_key = st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
        st.error("OpenAI API key not found. Please set it in Streamlit secrets.")
        st.stop()


try:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # 2. Lightweight API key verification
    client.models.list()

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .pdf)", type=("txt", "pdf")
    )

    summary_type = st.sidebar.radio(
        "Choose summary type:",
        [
            "Summarize in 100 words",
            "Summarize in 2 connecting paragraphs",
            "Summarize in 5 bullet points",
            "用中文总结为100字",
            "用中文总结为2段连贯的文字",
            "用中文总结为5个要点"
        ]
    )

    use_advanced = st.sidebar.checkbox("Use advanced model")

    if use_advanced:
        model = "gpt-5.1-chat-latest" 
        st.sidebar.info("Using: GPT-5.1 Chat Latest")
    else:
        model = "gpt-3.5-turbo" 
        st.sidebar.info("Using: GPT-3.5-Turbo")




    if uploaded_file and summary_type and use_advanced is not None:

        #read different types of files
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension == 'txt':
            document = uploaded_file.read().decode()
        elif file_extension == 'pdf':
            document = read_pdf(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()


        # Process the uploaded file and question.
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {summary_type}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)

except AuthenticationError:
    st.error("Invalid OpenAI API key. Please check and try again.")

except APIConnectionError:
    st.error("Network error. Unable to connect to OpenAI servers.")

except Exception as e:
    st.error(f"Unexpected error: {e}")
