import gradio as gr
import os 
import json 
import requests

#Streaming endpoint 
API_URL = "http://127.0.0.1:8100/v1/chat/completions" #os.getenv("API_URL") + "/generate_stream"

#Inferenec function


def predict(system_msg, inputs, top_p, temperature, chat_counter, chatbot=[], history=[]):  

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_gpt4_key}"  #Users will provide their own OPENAI_API_KEY 
    }
    print(f"system message is ^^ {system_msg}")
    if system_msg.strip() == '':
        initial_message = [{"role": "user", "content": f"{inputs}"},]
        multi_turn_message = []
    else:
        initial_message= [{"role": "system", "content": system_msg},
                   {"role": "user", "content": f"{inputs}"},]
        multi_turn_message = [{"role": "system", "content": system_msg},]
        
    if chat_counter == 0 :
        payload = {
        "model": model['id'],
        "messages": initial_message , 
        "temperature" : 1.0,
        "top_p":1.0,
        "n" : 1,
        "stream": True,
        "presence_penalty":0,
        "frequency_penalty":0,
        }
        print(f"chat_counter - {chat_counter}")
    else: #if chat_counter != 0 :
        messages=multi_turn_message # Of the type of - [{"role": "system", "content": system_msg},]
        for data in chatbot:
          user = {}
          user["role"] = "user" 
          user["content"] = data[0] 
          assistant = {}
          assistant["role"] = "assistant" 
          assistant["content"] = data[1]
          messages.append(user)
          messages.append(assistant)
        temp = {}
        temp["role"] = "user" 
        temp["content"] = inputs
        messages.append(temp)
        #messages
        payload = {
        "model": model['id'],
        "messages": messages, # Of the type of [{"role": "user", "content": f"{inputs}"}],
        "temperature" : temperature, #1.0,
        "top_p": top_p, #1.0,
        "n" : 1,
        "stream": True,
        "presence_penalty":0,
        "frequency_penalty":0,}

    chat_counter+=1

    history.append(inputs)
    print(f"Logging : payload is - {payload}")
    # make a POST request to the API endpoint using the requests.post method, passing in stream=True
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)
    print(f"Logging : response code - {response}")
    token_counter = 0 
    partial_words = "" 

    counter=0
    for chunk in response.iter_lines():
        #Skipping first chunk
        if counter == 0:
          counter+=1
          continue
        # check whether each line is non-empty
        if chunk.decode() :
          chunk = chunk.decode()
          # decode each line as response data is in bytes
          if len(chunk) > 12 and "content" in json.loads(chunk[6:])['choices'][0]['delta']:
              partial_words = partial_words + json.loads(chunk[6:])['choices'][0]["delta"]["content"]
              if token_counter == 0:
                history.append(" " + partial_words)
              else:
                history[-1] = partial_words
              chat = [(history[i], history[i + 1]) for i in range(0, len(history) - 1, 2) ]  # convert to tuples of list
              token_counter+=1
              yield chat, history, chat_counter, response  # resembles {chatbot: chat, state: history}  
                   
#Resetting to blank
def reset_textbox():
    return gr.update(value='')

#to set a component as visible=False
def set_visible_false():
    return gr.update(visible=False)

#to set a component as visible=True
def set_visible_true():
    return gr.update(visible=True)

#Using info to add additional information about System message in GPT4
system_msg_info = """You are an AI programming assistant.
        
                - Follow the user's requirements carefully and to the letter.
                - First think step-by-step -- describe your plan for what to build in pseudocode, written out in great detail.
                - Then output the code in a single code block.
                - Minimize any other prose."""
      

with gr.Blocks(css = """#col_container { margin-left: auto; margin-right: auto;} #chatbot {height: 1520px; overflow: auto;}""",) as demo:
    with gr.Column(elem_id = "col_container"):
        #Users need to provide their own GPT4 API key, it is no longer provided by Huggingface 
        with gr.Row():
            openai_gpt4_key = ""
            with gr.Accordion(label="System message:", open=False):
                system_msg = gr.Textbox(label="Instruct the AI Assistant to set its beaviour", info = system_msg_info, value="",placeholder="Type here..")
                accordion_msg = gr.HTML(value="🚧 To set System message you will have to refresh the app", visible=False)
                          
        chatbot = gr.Chatbot(label='GPT4', elem_id="chatbot")
        inputs = gr.Textbox(placeholder= "Hi there!", label= "Type an input and press Enter")
        state = gr.State([]) 
        with gr.Row():
            with gr.Column(scale=7):
                b1 = gr.Button().style(full_width=True)
            with gr.Column(scale=3):
                server_status_code = gr.Textbox(label="Status code from OpenAI server", )
    
        #top_p, temperature
        with gr.Accordion("Parameters", open=False):
            top_p = gr.Slider( minimum=-0, maximum=1.0, value=1.0, step=0.05, interactive=True, label="Top-p (nucleus sampling)",)
            temperature = gr.Slider( minimum=-0, maximum=5.0, value=1.0, step=0.1, interactive=True, label="Temperature",)
            chat_counter = gr.Number(value=0, visible=False, precision=0)

    #Event handling
    inputs.submit( predict, [system_msg, inputs, top_p, temperature, chat_counter, chatbot, state], [chatbot, state, chat_counter, server_status_code],)  #openai_api_key
    b1.click( predict, [system_msg, inputs, top_p, temperature, chat_counter, chatbot, state], [chatbot, state, chat_counter, server_status_code],)  #openai_api_key
    
    inputs.submit(set_visible_false, [], [system_msg])
    b1.click(set_visible_false, [], [system_msg])
    inputs.submit(set_visible_true, [], [accordion_msg])
    b1.click(set_visible_true, [], [accordion_msg])
    
    b1.click(reset_textbox, [], [inputs])
    inputs.submit(reset_textbox, [], [inputs])

demo.queue(max_size=99, concurrency_count=20).launch(debug=True)