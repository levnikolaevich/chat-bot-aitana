import chainlit as cl
from chainlit.input_widget import Switch, Select

from aitana_bot import AitanaBot

available_llm = ["google/gemma-1.1-2b-it", "google/gemma-1.1-7b-it"]
current_LLM = "google/gemma-1.1-7b-it"
max_new_tokens = 250
RAG_search_k = 2

@cl.on_settings_update
async def setup_agent(settings):
    rag = settings["RAG_is_working"]
    cl.user_session.set("RAG_is_working", rag)

    current_LLM = settings["CurrentLLM"]
    aitana_bot = AitanaBot(current_LLM)
    cl.user_session.set("aitana_bot", aitana_bot)

    print("on_settings_update", settings)


@cl.on_chat_start
async def on_chat_start():
    aitana_bot = AitanaBot(current_LLM)
    cl.user_session.set("aitana_bot", aitana_bot)

    hello_msg = ("¡Hola! Estoy listo para responder preguntas sobre el sitio web de la Universidad de Alicante.\n" +
                 "Puedes hacer preguntas. Por ejemplo:\n" +
                 "1. ¿Cuánto cuesta la matrícula en Inteligencia Artificial?\n" +
                 "2. ¿Cuáles son los plazos de admisión para la facultad de Inteligencia Artificial?\n" +
                 "3. ¿Quién es el coordinador del máster Universitario en Inteligencia Artificial?")

    await cl.Message(
        content=hello_msg,
        #elements=elements
    ).send()

    rag_initial = True
    await cl.ChatSettings(
        [
            Switch(
                id="RAG_is_working",
                label="RAG Search",
                initial=rag_initial
            ),
            Select(
                id="CurrentLLM",
                label="Current model",
                values=available_llm,
                initial_index=0,
            ),
        ]
    ).send()

    cl.user_session.set("RAG_is_working", rag_initial)


@cl.on_message
async def on_message(message: cl.Message):
    aitana_bot = cl.user_session.get("aitana_bot")
    msg = cl.Message(content="")
    await msg.send()

    context = ""
    RAG_context = None

    if cl.user_session.get("RAG_is_working"):
        _, _, RAG_context = await cl.make_async(aitana_bot.search_in_faiss_index)(message.content, RAG_search_k)

        content_list = [item["content"] for item in RAG_context]
        context_str = "\n".join(content_list)

        context += "\n\nSite content:\n"
        context += "\n\n" + context_str + "\n"

    final_prompt = (f"Summarize the key details from the context, retaining only the most crucial information, " +
                    f"and answer the question concisely.\n\n" +
                    f"CONTEXT:\n{context}\n\nQUESTION:\n{message.content}")

    print(final_prompt)
    output = await cl.make_async(aitana_bot.get_answer)(final_prompt, max_new_tokens)

    response = []

    response.append("\n " + output + "\n")

    if RAG_context is not None:
        response.append("\n More info:")
        response.append("\n" + RAG_context[0]['url'])

    msg.content = "".join(response)

    await msg.update()
