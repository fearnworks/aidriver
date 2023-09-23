import gradio as gr
import httpx
from loguru import logger
import secrets
from auth import auth_service
from ai_driver.cloud_llm.swarm import get_swarm_output
from ai_driver.cloud_llm.OAISettings import OAIModels, default_swarm_config

timeout = httpx.Timeout(600.0)


async def make_request(prompt, session_id, endpoint):
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Call add_auth_headers to include the authentication token in the headers
        client = auth_service.add_auth_headers(client)

        logger.info(f"Making request to {endpoint} with query {prompt}")
        request = {"query": prompt, "session_id": session_id}
        response = await client.post(
            f"http://ai_driver:28001/api/v1/chat/{endpoint}",
            json=request,
        )
        logger.debug(response.text)
        return response


def refresh_session_list():
    with httpx.Client(timeout=timeout) as client:
        # Call add_auth_headers to include the authentication token in the headers
        client = auth_service.add_auth_headers(client)

        logger.info(f"Making request to sessions")
        response = client.post(
            f"http://ai_driver:28001/api/v1/chat/sessions",
            json={},
        )
        logger.debug(response.json())
        sessions = response.json()
        return sessions


async def get_history(session_id: str):
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Call add_auth_headers to include the authentication token in the headers
        client = auth_service.add_auth_headers(client)

        logger.info(f"Making request to history with session {session_id}")
        request = {"session_id": session_id}
        response = await client.post(
            f"http://ai_driver:28001/api/v1/chat/history",
            json=request,
        )
        logger.debug(response.text)
        history_pairs = response.json()["history"]
        history = []
        for pair in history_pairs:
            history.append((pair["human"], pair["ai"]))

        return history


def create_swarm_chat_interface() -> gr.Blocks:
    config = default_swarm_config
    CSS = """
    .contain { display: flex; flex-direction: column; }
    .gradio-container { height: 100vh !important; }
    #component-0 { height: 100%; }
    #component-1 { height: 100%; }
    #iteration_chat {height: 100% !important; overflow: auto;}
    #base_chat {height: 100% !important; overflow: auto;}
    #chat_column {height: 95vh; overflow: auto;}
    #output_column {height: 95vh; overflow: auto;}
    #iter_column {height: 95vh; overflow: auto;}
    """
    session_id = secrets.randbits(32)
    session_options = [str(session_id)]
    chat_display = None
    with gr.Blocks(css=CSS) as chat_tab:
        with gr.Row():
            with gr.Column(elem_id="chat_column"):
                with gr.Tab("Output", elem_id="output_column"):
                    base_chat_display = gr.Chatbot([], height=700, elem_id="base_chat")
                with gr.Tab("Iterations", elem_id="iter_column"):
                    iteration_chat_display = gr.Chatbot(
                        [], height=700, elem_id="iteration_chat"
                    )
                with gr.Row():
                    chat_input = gr.Textbox("")

            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        # Config settings widgets
                        system_messages_slider = gr.Slider(
                            minimum=1,
                            maximum=10,
                            step=1,
                            value=config.num_agents,
                            label="How many system messages",
                        )
                        token_length_slider = gr.Slider(
                            minimum=100,
                            maximum=16000,
                            value=config.max_response_tokens,
                            label="Response Token Length",
                        )
                        feedback_rounds_slider = gr.Slider(
                            minimum=1,
                            maximum=5,
                            step=1,
                            value=config.iterations,
                            label="Feedback Rounds",
                        )
                        temperature = gr.Slider(
                            minimum=0,
                            maximum=1.2,
                            step=0.1,
                            value=config.temperature,
                            label="Temperature",
                        )
                    with gr.Column():
                        model_for_system_messages_dropdown = gr.Dropdown(
                            list(OAIModels),
                            label="Model for System Messages",
                            value=config.system_message_model.value,
                        )
                        model_for_answer_generation_dropdown = gr.Dropdown(
                            list(OAIModels),
                            label="Model for Answer Generation",
                            value=config.answer_generation_model.value,
                        )
                        model_for_answer_iteration_dropdown = gr.Dropdown(
                            list(OAIModels),
                            label="Model for Answer Iteration",
                            value=config.answer_iteration_model.value,
                        )
                        model_for_synthesizing_dropdown = gr.Dropdown(
                            list(OAIModels),
                            label="Model for Synthesizing Final Response",
                            value=config.response_aggregation_model.value,
                        )
                with gr.Accordion("Session Management"):
                    with gr.Column():
                        session_id_label = gr.Textbox(session_id, label="Session ID")

                        refresh_button = gr.Button("🔄")

                    with gr.Column():
                        session_id_labels = gr.Textbox("", label="Session ID List")
                        refresh_session_button = gr.Button("🔄")

    refresh_button.click(
        get_history, inputs=[session_id_label], outputs=[base_chat_display]
    )
    refresh_session_button.click(
        refresh_session_list, inputs=[], outputs=[session_id_labels]
    )
    chat_input.submit(
        get_swarm_output,  # This function needs to be modified to accept the new inputs
        inputs=[
            base_chat_display,
            iteration_chat_display,
            chat_input,
            system_messages_slider,
            temperature,
            token_length_slider,
            feedback_rounds_slider,
            model_for_system_messages_dropdown,
            model_for_answer_generation_dropdown,
            model_for_answer_iteration_dropdown,
            model_for_synthesizing_dropdown,
        ],
        outputs=[base_chat_display, iteration_chat_display],
    )
    return chat_tab
