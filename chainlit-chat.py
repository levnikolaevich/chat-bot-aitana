import chainlit as cl

from aitana_bot import AitanaBot


@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)


@cl.on_chat_start
async def on_chat_start():
    aitana_bot = AitanaBot()
    cl.user_session.set("aitana_bot", aitana_bot)

    hello_msg = ("¡Hola! Estoy listo para responder preguntas sobre el sitio web de la Universidad de Alicante.\n" +
                 "Puedes hacer preguntas. Por ejemplo:\n" +
                 "1. ¿Cuánto cuesta la matrícula en Inteligencia Artificial?\n" +
                 "2. ¿Cuáles son los plazos de admisión para la facultad de Inteligencia Artificial?")

    await cl.Message(
        content=hello_msg,
        #elements=elements
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    aitana_bot = cl.user_session.get("aitana_bot")
    msg = cl.Message(content="")
    await msg.send()

    context = ""

    _, _, RAG_context = await cl.make_async(aitana_bot.search_in_faiss_index)(message.content, 1)

    content_list = [item["content"] for item in RAG_context]
    context_str = "\n".join(content_list)

    context += "\n\nSite content:\n"
    context += "\n\n" + context_str + "\n"

    final_prompt = (f"Summarize the key details from a context, ensuring to retain the most crucial information " +
                    f"and answer to the question:\n\nCONTEXT:\n{context}\n\nQUESTION:\n{message.content}")

    print(final_prompt)
    output = await cl.make_async(aitana_bot.get_answer)(final_prompt, 200)

    response = []

    response.append("\n " + output)
    response.append("\n More info:")

    for sentence in RAG_context:
        response.append("\n" + sentence['url'])

    msg.content = "".join(response)

    await msg.update()
