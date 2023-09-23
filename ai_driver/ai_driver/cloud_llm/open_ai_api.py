import openai
from ai_driver.core.generation_config import LLMGenerationConfig
import json


class OpenAIApiCaller:
    def __init__(self, config: LLMGenerationConfig):
        self.config = config

    def call_api(
        self,
        model,
        messages,
        temperature,
        max_tokens,
        functions=None,
        function_call=None,
    ):
        gpt_call_parameters = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        if functions:
            gpt_call_parameters["functions"] = functions

        if function_call:
            gpt_call_parameters["function_call"] = function_call

        try:
            response = openai.ChatCompletion.create(**gpt_call_parameters)
            responses = ""
            for chunk in response:
                if function_call:
                    if chunk["choices"][0]["delta"].get("function_call"):
                        chunk = chunk["choices"][0]["delta"]
                        arguments_chunk = chunk["function_call"]["arguments"]
                        print(arguments_chunk, end="", flush=True)
                        responses += arguments_chunk
                else:
                    response_content = (
                        chunk.get("choices", [{}])[0].get("delta", {}).get("content")
                    )
                    if response_content:
                        responses += response_content
            return responses
        except Exception as e:
            print(f"Error during API call: {e}")
            print(
                f"Payload: {json.dumps(gpt_call_parameters, indent=4)}"
            )  # Print the payload for debugging.
            return None
