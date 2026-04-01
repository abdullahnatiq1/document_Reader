from config import client, collection


def llm(prompt):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role" : "user", "content" : prompt}]
    )
    return response.choices[0].message.content.strip()

def isChunkRelevant(query, chunk):
    return "YES" in llm (f"Is this chunk useful to answer the question? \n Question : {query} \n Chunk : {chunk} \n Reply YES or NO only").upper()

def isAnswerRelevant(answer, context):
    return "YES" in llm (f"IS this answer based on the context? \n Context : {context} \n  Answer : {answer} \n Reply YES or NO only").upper()

def selfRagRetrieve(query):
    results = collection.query(query_texts=[query], n_results=5)
    chunks = results ["documents"][0]

    usefulChunks = [c for c in chunks if isChunkRelevant(query,c)]
    print(f"Self RAG is implemented so Total Chunk : {len(chunks)}, useful Chunks : {(usefulChunks)}")
    return "\n\n".join (usefulChunks) if usefulChunks else "\n\n".join(chunks)

def selfRagVerify(answer, context):
    if isAnswerRelevant(answer, context):
        print("Answer is Relevant")
    else:
        print("Answer is not relevant")