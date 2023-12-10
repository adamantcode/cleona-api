from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

SYSTEM_PROMPT = "You are a clinical, nurturing, supportive, helpful, and intelligent assistant that is experienced in helping women and their partners in their maternal health journey"


class Chatbot:
    def __init__(self):
        self.conversation_chain = None

    def create_conversation_chain(self, vectorstore):
        llm = ChatOpenAI(
            temperature=0, model_name='gpt-3.5-turbo-1106')

        memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True)

        general_system_template = r""" 
You are a clinical, nurturing, supportive, helpful, and intelligent assistant that is experienced in helping women and their partners in their maternal health journey.
----
{context}
----
        """

        general_user_template = " {question}"

        messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template)
        ]

        qa_prompt = ChatPromptTemplate.from_messages(messages)

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            verbose=True,
            combine_docs_chain_kwargs={'prompt': qa_prompt}
        )

        self.conversation_chain = conversation_chain

    def handle_user_input(self, user_question):
        response = self.conversation_chain({'question': user_question})
        initial_answer = response['answer']

        follow_up_question = "Can you provide more details about that?"

        follow_up_response = self.conversation_chain(
            {'question': follow_up_question})

        expanded_answer = f"{initial_answer}\n\n{follow_up_response['answer']}"

        return expanded_answer
