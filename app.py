from __future__ import annotations

import gradio as gr

from query import ask


def handle_query(question: str):
    result = ask(question)
    sources = "\n".join(f"• {source}" for source in result["sources"]) or "No sources retrieved."
    return result["answer"], sources


with gr.Blocks() as demo:
    gr.Markdown("# Solo Travel RAG")
    gr.Markdown("Ask a question about solo travel tips, destinations, and planning.")

    with gr.Row():
        inp = gr.Textbox(label="Your question", placeholder="How should I choose where to travel?")

    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.queue().launch()