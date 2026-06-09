from __future__ import annotations

from typing import Iterable

from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL


SYSTEM_PROMPT = """You are a solo travel assistant.

You must answer using only the provided context.
Do not use outside knowledge.
Do not guess, infer facts not present, or invent details.

If the context does not contain enough information to answer the question, you must respond with exactly:
I don't have enough information on that.

Return only the answer text. Each Answer must include at least 1 source citation in the answer.
"""


def format_context(chunks: Iterable[dict]) -> str:
    parts = []
    for chunk in chunks:
        parts.append(f"[Source: {chunk['file_name']}]\n{chunk['text']}")
    return "\n\n".join(parts)


def build_user_prompt(query: str, context: str) -> str:
    return f"""Answer the question using only the information in the provided documents.
If the documents don't contain enough information to answer, say: I don't have enough information on that.

Question: {query}

Documents:
{context}
"""


def generate_answer(query: str, chunks: Iterable[dict]) -> str:
    chunk_list = list(chunks)
    if not chunk_list:
        return "I don't have enough information on that."

    client = Groq(api_key=GROQ_API_KEY)
    context = format_context(chunk_list)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(query, context)},
    ]
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content.strip()