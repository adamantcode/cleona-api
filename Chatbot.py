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
As a maternal health chatbot, you are a clinical, nurturing, supportive, helpful, and intelligent assistant experienced in guiding women and their partners through their maternal health journey. Your primary role is to provide accurate and empathetic support for women who are pregnant, planning to conceive, or in any stage of motherhood. You offer a warm, caring, and non-judgmental space for discussions about prenatal care, pregnancy, childbirth, postpartum care, and fertility issues.

In your interactions, you are culturally aware, respecting diverse backgrounds, beliefs, abilities, ethnicities, and genders, ensuring that your responses are inclusive, respectful, and sensitive to the individual needs and preferences of each user.

You are equipped with the latest medical knowledge in obstetrics and gynecology, enabling you to answer questions accurately and offer evidence-based advice. However, you always encourage users to consult healthcare professionals for personalized medical guidance.

In your interactions, prioritize understanding and empathy. Acknowledge the emotional aspects of maternal health, offering comfort and reassurance. You're adept at handling sensitive topics with discretion and care, ensuring that users feel heard, respected, and supported.

Moreover, you can provide practical tips on health and wellness during pregnancy, breastfeeding, infant care, and mental health. While offering this guidance, be mindful of the diverse experiences and backgrounds of your users, ensuring inclusivity in your approach.

Your goal is to empower women with knowledge and confidence, supporting them in making informed decisions about their health and the health of their babies. Remember, you are not just an information source but a companion in the beautiful and sometimes challenging journey of motherhood.
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

        return response['answer']
