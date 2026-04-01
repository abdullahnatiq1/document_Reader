import openai
from dotenv import load_dotenv
import os
import chromadb
from selfrag import selfRagRetrieve, selfRagVerify
from config import client, collection
from chunking import indexPDF

load_dotenv()

indexPDF("book.pdf")

history = []
lastContext = ""

while True:
    query = input("You : ")
    if query.lower() == "exit":
        break

    if any (word in query.lower() for word in ["further", "explain", "more", "describe", "elaborate"]):   # query.lower is liya use kiya hai ta k further or Futher model same assume kara
        retrievedContext = lastContext
    else:
        retrievedContext = selfRagRetrieve(query)     # [0] 1 query enter krna k liya use kr raha 2 queries k liya hum phir 1 use krna 
                                                                    # humne yahan pa \n\n.join is liya lagaye hai ta k 2 lines ko alagh rakha then .join kara ye usko list banana sa bacha rahi hai 
                                                                    # \n\n.join as an splitter kam kr raha hai 
        lastContext = retrievedContext


    prompt = f"""
Answer the following based only on the context provided         
Context : {retrievedContext},                                                  
Question : {query}                                        
"""
# baghair context k model ko pata hi nai chalaga k hum kiski baat kr raha

    history.append({"role" : "user", "content" : prompt})

    response = client.chat.completions.create(                 # ye Generation hai
        model="llama-3.3-70b-versatile",                       # ye humari prompt model ko bhej raha hai or uska role user bata raha 
        temperature = 0.5,
        messages = history,
        stream = True
    )
    print ("Assistant : ", end = "", flush = True)
    fullResponse = ""

    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end = "", flush=True)
            fullResponse += content

    print("\n")
    history.append({"role" : "assistant", "content" : fullResponse})
    selfRagVerify(fullResponse, retrievedContext)
