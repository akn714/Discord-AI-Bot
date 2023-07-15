# for storing chat histories for individual chats:

from langchain.memory import ConversationBufferMemory

# key -> unique chat id
# value -> chat history for that chat
history = dict()


# chat history
def chat_history(key):
    global history
    try:
        return history[key]
    except:
        history[key] = ConversationBufferMemory()
        return history[key]
