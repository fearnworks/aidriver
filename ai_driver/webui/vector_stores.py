import gradio as gr
import httpx
from loguru import logger
from auth import auth_service

timeout = httpx.Timeout(3600.0)
import asyncio


async def endpoint_test(dir: str):
    task1 = asyncio.create_task(make_request(dir, "local_download_pipeline"))

    response = await asyncio.gather(task1)
    logger.info(response)
    if response.status_code == 200:
        print("Server for pinecone is up and running!")
    else:
        print("Server for pinecone is not responding.")

    return response


async def make_request(dir, endpoint):
    async with httpx.AsyncClient(timeout=timeout) as client:
        client = auth_service.add_auth_headers(client)
        logger.info(f"Making request to {endpoint} with query {dir}")
        request = {"directory_path": dir}
        response = await client.post(
            f"http://ai_driver:28001/api/v1/retrieval/{endpoint}",
            json=request,
        )
        logger.debug(response.text)
        return response


def create_local_loader() -> gr.Blocks:
    with gr.Blocks() as loader_tab:
        with gr.Row():
            with gr.Column():
                directory = gr.Textbox(label="Directory", value="/data")
                button = gr.Button("Load Local Directory")
            with gr.Column():
                docs = gr.Textbox(label="Chunked Documents")
        button.click(
            fn=endpoint_test, inputs=[directory], outputs=[docs]
        )
    return loader_tab
