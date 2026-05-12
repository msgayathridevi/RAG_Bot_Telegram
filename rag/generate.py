import ollama
from rag.retriever import retrieve


def answer_question(query):
    # Get relevant context
    retrieved_docs = retrieve(query)

    context = "\n\n".join(
        [doc[0] for doc in retrieved_docs]
    )

    prompt = f"""
        Use ONLY the provided context.

        If the answer exists in the context,
        answer briefly and directly.

        If it does not exist, say:
        I couldn't find that information.

        Context:
        {context}

        Question:
        {query}

        Answer:
        """

    response = ollama.chat(
        model="qwen2.5:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    while True:
        q = input("\nAsk: ")

        if q.lower() == "exit":
            break

        answer = answer_question(q)

        print("\nAnswer:")
        print(answer)