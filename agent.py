import ollama
from search_tool import search_web

def ask_agent(prompt):

    if "search" in prompt.lower():
        info = search_web(prompt)
        prompt = f"Use this information to answer:\n{info}\nQuestion:{prompt}"

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]