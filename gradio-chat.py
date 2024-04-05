import gradio as gr
import tracemalloc
import time

from aitana_bot import AitanaBot

tracemalloc.start()

K_MAX_RESULTS = 1

global aitana_bot
aitana_bot = None

def initialize_global_variables():
    global aitana_bot

    if aitana_bot is None:
        print("initialize aitana_bot started")
        aitana_bot = AitanaBot()
        print("initialize aitana_bot finished")


def chat_with_ai(query):
    global aitana_bot
    context = ""

    D, I, RAG_context = aitana_bot.search_in_faiss_index(query, k=K_MAX_RESULTS)
    content_list = [item["content"] for item in RAG_context]
    context_str = "\n".join(content_list)

    context += "\n\nSite content:\n"
    context += "\n\n" + context_str + "\n"

    final_prompt = (f"Summarize the key details from a context, ensuring to retain the most crucial information " +
                    f"and answer to the question:\n\nCONTEXT:\n{context}\n\nQUESTION:\n{query}")

    start_time = time.time()
    response = aitana_bot.get_answer(final_prompt, 200)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to get the response: {elapsed_time} seconds")

    new_chat_history_item = []

    new_chat_history_item.append("\n Q: " + query)
    new_chat_history_item.append("\n A: " + response)
    new_chat_history_item.append("\n More info:")

    for sentence in RAG_context:
        new_chat_history_item.append("\n" + sentence['url'])
    new_chat_history_item.append("\n ------------------------")

    aitana_bot.update_chat_history(new_chat_history_item)

    print(aitana_bot.get_chat_history())
    output = ''
    for sentence in aitana_bot.get_chat_history():
        output += sentence

    print("output:")
    print(output)
    print("final_prompt:")
    print(final_prompt)
    return output, final_prompt

def main():
    with gr.Blocks() as buscador:
        gr.Markdown("Chat with Website Content")
        with gr.Row():
            with gr.Column():
                query = gr.Textbox(label="Enter your query:")
                submit_button = gr.Button("To ask")
                gr.Markdown("Chat History:")
                responseOutput = gr.Textbox(label="", interactive=False, lines=10)
                gr.Markdown("Final Prompt:")
                FinalPromptOutput = gr.Textbox(label="", interactive=False, lines=10)
                # Process the user query when the submit button is clicked.
                submit_button.click(fn=chat_with_ai, inputs=[query], outputs=[responseOutput, FinalPromptOutput])

    buscador.launch()


if __name__ == '__main__':
    initialize_global_variables()
    main()
