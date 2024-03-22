import gradio as gr
from rag import RagFAISS
from chat_llm import Chat
import tracemalloc
import time

tracemalloc.start()

K_MAX_RESULTS = 1

global rag_faiss, chat_llm, chat_history, isInited
rag_faiss = None
chat_llm = None
chat_history = []
isInited = False

def initialize_global_variables():
    print("initialize_global_variables started")
    global rag_faiss, chat_llm

    if rag_faiss is None:
        rag_faiss = initialize_text_processing()

    if chat_llm is None:
        chat_llm = Chat(model_id="google/gemma-2b-it")

    print("initialize_global_variables finished")


def initialize_text_processing(modelST_id='avsolatorio/GIST-small-Embedding-v0'):
    """
    Initializes text processing by creating a FAISS index from PDF files in the given folder.

    Args:
        modelST_id (str): name of the model for SentenceTransformer

    Returns:
        RagFAISS: An initialized instance of the RagFAISS class.
    """
    rag_faiss_db = RagFAISS(modelST_id)
    text2vec = rag_faiss_db.extract_text_to_paragraphs()
    rag_faiss_db.read_or_create_faiss_index(text2vec)
    return rag_faiss_db


def execute_text(rag_faiss_db, query):
    """
    Executes a text query using the given RagFAISS instance.

    Args:
        rag_faiss_db (RagFAISS): The initialized RagFAISS instance.
        query (str): The text query to process.
    """
    D, I, RAG_context = rag_faiss_db.search(query)
    print(I)
    print(D)
    print(RAG_context)

def chat_with_ai(query):
    global rag_faiss, chat_llm, chat_history
    context = ""

    D, I, RAG_context = rag_faiss.search(query, k=K_MAX_RESULTS)
    content_list = [item["content"] for item in RAG_context]
    context_str = "\n".join(content_list)

    context += "\n\nSite content:\n"
    context += "\n\n" + context_str + "\n"

    final_prompt = (f"Summarize the key details from a context, ensuring to retain the most crucial information " +
                    f"and answer to the question:\n\nCONTEXT:\n{context}\n\nQUESTION:\n{query}")
    print("final_prompt:")
    print(final_prompt)
    start_time = time.time()
    response = chat_llm.get_answer(final_prompt, 200)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to get the response: {elapsed_time} seconds")

    chat_history.append("\n Q: " + query)
    chat_history.append("\n A: " + response)
    chat_history.append("\n More info:")
    for sentence in RAG_context:
        chat_history.append("\n" + sentence['url'])
    chat_history.append("\n ------------------------")

    output = ''
    for sentence in chat_history:
        output += sentence
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
    if not isInited:
        initialize_global_variables()
        isInited = True

    main()
