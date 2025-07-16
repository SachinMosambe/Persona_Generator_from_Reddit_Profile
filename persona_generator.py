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
        "Analyze the Reddit user's content and generate a detailed, structured user persona. "
        "Include the following characteristics if possible:\n"
        "- Username\n"
        "- Interests\n"
        "- Personality Traits\n"
        "- Hobbies\n"
        "- Profession or Background (if guessable)\n"
        "- Writing Style\n"
        "- Beliefs or Opinions\n"
        "- Political/Social leanings\n"
        "- Age or Gender (if inferable)\n\n"
        "For each characteristic, include a citation in square brackets referencing the original source "
        "(e.g., [Source: <URL>])."
    )

    return qa_chain.run(prompt)
