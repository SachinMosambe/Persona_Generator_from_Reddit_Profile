from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI

def generate_user_persona(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    llm = OpenAI(temperature=0.7)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    prompt = (
        "Create a concise Reddit user profile in the following format:\n\n"

        " **User Profile Card**\n"
        "------------------------\n"
        "**Username**: [Reddit username]\n"
        "**Profile Created**: [Account age]\n"
        "**Location**: [Based on post history]\n"
        "**Age Range**: [Estimated from content]\n"
        "**Occupation**: [If mentioned/implied]\n\n"

        " **Key Traits**\n"
        "----------------\n"
        "• Personality: [3 main characteristics]\n"
        "• Interests: [Main topics/hobbies]\n"
        "• Style: [Communication approach]\n\n"

        " **Activity Pattern**\n"
        "-------------------\n"
        "• Most Active In: [Top subreddits]\n"
        "• Peak Activity: [Time patterns]\n"
        "• Content Type: [Posts vs Comments]\n\n"

        " **Notable Characteristics**\n"
        "-------------------------\n"
        "• Unique Traits: [What makes them stand out]\n"
        "• Common Topics: [Frequently discussed]\n"
        "• Behavior Pattern: [How they interact]\n\n"

        "Support each point with a brief evidence quote [Source: URL]"
    )

    return qa_chain.run(prompt)

