import gradio as gr
import httpx
from loguru import logger
import secrets
from api_utils import openai_generate
timeout = httpx.Timeout(600.0)



async def make_request(
    prompt, session_id, endpoint, model_dropdown, temperature, max_tokens
):
    from api_models import get_models, ModelListResponse,ModelPermission,Model
    response: ModelListResponse = await get_models()
    model: Model = response.data[0]
    response = openai_generate(model, prompt)
    # async with httpx.AsyncClient(timeout=timeout) as client:
    #     # Call add_auth_headers to include the authentication token in the headers
    #     client = auth_service.add_auth_headers(client)

    #     logger.info(f"Making request to {endpoint} with query {prompt}")
    #     request = {
    #         "query": prompt,
    #         "session_id": session_id,
    #         "model": model_dropdown,
    #         "temperature": temperature,
    #         "max_tokens": max_tokens,
    #     }
    #     response = await client.post(
    #         f"http://ai_driver:28001/api/v1/chat/{endpoint}",
    #         json=request,
    #     )
    #     logger.debug(response.text)
    return response


async def chat(
    chat_history,
    message: str,
    session_id: str,
    model_dropdown: str,
    temperature: float,
    token_length_slider: int,
):
    logger.info(f"Chatbot received message: {message}")
    logger.info(
        f"Model: {model_dropdown}, Temperature: {temperature}, Token Length: {token_length_slider}"
    )

    response = await make_request(
        message,
        session_id,
        "cloudllm",
        model_dropdown,
        temperature,
        token_length_slider,
    )
    response = response.json()
    history = chat_history + [(message, response["result"])]
    return history


# def refresh_session_list():
#     with httpx.Client(timeout=timeout) as client:
#         # Call add_auth_headers to include the authentication token in the headers
#         client = auth_service.add_auth_headers(client)

#         logger.info(f"Making request to sessions")
#         response = client.post(
#             f"http://ai_driver:28001/api/v1/chat/sessions",
#             json={},
#         )
#         logger.debug(response.json())
#         sessions = response.json()
#         return sessions


# async def get_history(session_id: str):
#     async with httpx.AsyncClient(timeout=timeout) as client:
#         # Call add_auth_headers to include the authentication token in the headers
#         client = auth_service.add_auth_headers(client)

#         logger.info(f"Making request to history with session {session_id}")
#         request = {"session_id": session_id}
#         response = await client.post(
#             f"http://ai_driver:28001/api/v1/chat/history",
#             json=request,
#         )
#         logger.debug(response.text)
#         history_pairs = response.json()["history"]
#         history = []
#         for pair in history_pairs:
#             history.append((pair["human"], pair["ai"]))

#         return history


def create_chat_interface() -> gr.Blocks:
    CSS = """
    .contain { display: flex; flex-direction: column; }
    .gradio-container { height: 100vh !important; }
    #component-0 { height: 100%; }
    #component-1 { height: 100%; }
    #chat {height: 100% !important; overflow: auto;}
    #base_chat {height: 100% !important; overflow: auto;}
    #chat_column {height: 95vh; overflow: auto;}
    """
    session_id = secrets.randbits(32)
    session_options = [str(session_id)]
    chat_display = None
    with gr.Blocks(css=CSS) as chat_tab:
        with gr.Row():
            with gr.Column(elem_id="chat_column"):
                with gr.Tab("Output", elem_id="output_column"):
                    chat_history = []
                    chat_display = gr.Chatbot([], height=700, elem_id="base_chat")
                with gr.Row():
                    chat_input = gr.Textbox("")

            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        token_length_slider = gr.Slider(
                            minimum=100,
                            maximum=16000,
                            value=8000,
                            label="Response Token Length",
                        )
                        temperature = gr.Slider(
                            minimum=0,
                            maximum=1.2,
                            step=0.1,
                            value=0.4,
                            label="Temperature",
                        )
                    with gr.Column():
                        model_dropdown = gr.Dropdown(
                            ["local", "cloud"],
                            label="Model",
                            value="cloud",
                        )
                with gr.Accordion("Session Management"):
                    with gr.Column():
                        session_id_label = gr.Textbox(session_id, label="Session ID")

                        refresh_button = gr.Button("🔄")

                    with gr.Column():
                        session_id_labels = gr.Textbox("", label="Session ID List")
                        refresh_session_button = gr.Button("🔄")

    # refresh_button.click(get_history, inputs=[session_id_label], outputs=[chat_display])
    # refresh_session_button.click(
    #     refresh_session_list, inputs=[], outputs=[session_id_labels]
    # )
    chat_input.submit(
        chat,  # This function needs to be modified to accept the new inputs
        inputs=[
            chat_display,
            chat_input,
            session_id_label,
            model_dropdown,
            temperature,
            token_length_slider,
        ],
        outputs=[chat_display],
    )
    return chat_tab
