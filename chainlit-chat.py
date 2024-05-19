import chainlit as cl
from chainlit.input_widget import Switch, Select
import torch

from aitana_bot import AitanaBot

available_llm = AitanaBot.get_available_llm()
available_RAG = AitanaBot.get_available_RAG_engine()
max_new_tokens = 250
RAG_search_k = 4

@cl.on_settings_update
async def setup_agent(settings):
    # Update the RAG search flag
    rag = settings["RAG_is_working"]
    cl.user_session.set("RAG_is_working", rag)

    # Clear the cache and set the new LLM model
    rag_engine = settings["CurrentRAG"]
    current_LLM = settings["CurrentLLM"]

    print(f'RAG Engine: {rag_engine}, LLM Model: {current_LLM}')

    old_bot = cl.user_session.get("aitana_bot")
    if old_bot:
        del old_bot
    torch.cuda.empty_cache()

    aitana_bot = AitanaBot(current_LLM, rag_engine)
    cl.user_session.set("aitana_bot", aitana_bot)

    # Update the settings
    print("on_settings_update", settings)


@cl.on_chat_start
async def on_chat_start():
    aitana_bot = AitanaBot()
    cl.user_session.set("aitana_bot", aitana_bot)

    hello_msg = ("¡Hola! Estoy listo para responder preguntas sobre el sitio web de la Universidad de Alicante.\n" +
                 "Puedes hacer preguntas. Por ejemplo:\n" +
                 "1. ¿Cuánto cuesta la matrícula en el máster de Inteligencia Artificial?\n" +
                 "2. ¿Cuánto cuesta la matrícula en el grado de Inteligencia Artificial?\n" +
                 "3. ¿Cuántas plazas están disponibles para la admisión en el Máster de Inteligencia Artificial?\n" +
                 "4. ¿Quién es el coordinador del máster Universitario en Inteligencia Artificial?\n" +
                 "--------------------------------------\n" +
                 "5. ¿Cuántas estrellas hay en el cielo?")

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
                id="CurrentRAG",
                label="Current RAG Engine",
                values=available_RAG,
                initial_index=0,
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
        RAG_context = await cl.make_async(aitana_bot.search_in_faiss_index)(message.content, RAG_search_k)

        print("RAG_context Count:")
        print(len(RAG_context))

        content_list = [f'{item["content"]}' for item in RAG_context]
        context_str = "\n----------\n".join(content_list)

        context += "\n\nSite content:\n"
        context += "\n\n" + context_str + "\n"

    final_prompt = (f"Summarize the key details from the context, retaining only the most crucial information, " +
                    f"and answer the question concisely in a language of the question.\n\n" +
                    f"CONTEXT:\n{context}\n\nQUESTION:\n{message.content}")

    #print(final_prompt)
    output = await cl.make_async(aitana_bot.get_answer)(final_prompt, max_new_tokens)

    response = []

    response.append("\n " + output + "\n")

    if RAG_context is not None and "The provided text does not contain" not in output:
        response.append("\n More info:")
        for context in RAG_context:
            response.append("\n" + context['url'])

    msg.content = "".join(response)

    await msg.update()
