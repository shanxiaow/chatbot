from openai import OpenAI
import streamlit as st


### Page configuration 
st.set_page_config(page_title="Sandman", page_icon=":robot_face:") 

### markdown
st.title("Mr. Sandman 😎") 
# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4a4a4a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #6a6a6a;
        margin-bottom: 1rem;
    }
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 class='sub-header'>Ask me anything!</h2>", unsafe_allow_html=True)


### Sidebar
with st.sidebar:
    # st.image("", width=150)
    st.header("About")
    st.write("This is an AI-powered chatbot using OpenAI's GPT-4o model.")

# Save chat history to shelve file
import shelve
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

###
USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o" #"gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

