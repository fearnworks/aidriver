import asyncio
from loguru import logger
import gradio as gr
import os
import time
from dotenv import load_dotenv, find_dotenv
from chat import create_chat_interface


load_dotenv(find_dotenv())


def init_interface():
    title = "AI Driver Demo UI"
    interface = {}
    with gr.Blocks(analytics_enabled=False, title=title) as ui:
        with gr.Tab("Chat"):
            interface["chat"] = create_chat_interface()
        # with gr.Tab("Swarm"):
        #     interface["swarm_chat"] = create_swarm_chat_interface()
        # with gr.Tab("QA"):
        #     interface["qa"] = create_qa()
        # with gr.Tab("Vector Storage"):
        #     interface['vectorstorage'] = create_local_loader()
    ui.queue()

    ui.launch(
        prevent_thread_lock=True,
        server_name="0.0.0.0",
        server_port=18000,
        inbrowser=True,
    )


async def main():
    init_interface()
    while True:
        time.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())