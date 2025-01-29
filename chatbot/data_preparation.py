import json
import os 
def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json_str = json.dumps(data, ensure_ascii=False)
        f.write(json_str + '\n')

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# input_data = load_json(os.getcwd() + '/chatbot/chatbot/train.json')
# output_data = os.getcwd() + '/chatbot/data/train.jsonl'

system_message = "Eres un asistente virtual para una página web de reservas de campos de fútbol. Tu objetivo es brindar respuestas claras, precisas y amables en español, ayudando a los usuarios a gestionar sus reservas, conocer disponibilidad, tarifas y resolver cualquier duda sobre el servicio. Mantén siempre un tono cordial y accesible."

def convert_to_jsonl(input_data, output_file, output_file_1):
    with open(input_data, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'w', encoding='utf-8') as f:
        messages = data['messages']
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                conversation = {
                    "messages": [
                        # {"role": "system", "content": system_message},
                        {"content": system_message, "role": "system"},
                        {"content": messages[i]["content"], "role": "user"},
                        # { "role": "user", "content": messages[i]["content"]},
                        {"content": messages[i+1]["content"], "role": "assistant"}  
                        # {"role": "assistant", "content": messages[i+1]["content"], }  
                    ]
                }
                    
                    
                json_line = json.dumps(conversation, ensure_ascii=False)
                f.write(json_line + '\n')

    # with open(output_file, 'r', encoding='utf-8') as f:
    #     data = json.load(f)          

    with open(output_file_1, 'w', encoding='utf-8') as f:
        messages = data['messages']
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                conversation = {
                    
                    "prompt":    messages[i]["content"],
                       "completion" : messages[i+1]["content"]
                    
                }
                json_line = json.dumps(conversation, ensure_ascii=False)
                f.write(json_line + '\n')

input_file = os.getcwd() + '/chatbot/train.json'
output_file = os.getcwd() + '/chatbot-chat/train.jsonl'
output_file_1 = os.getcwd() + '/test/train.jsonl'
convert_to_jsonl(input_file, output_file, output_file_1)



# print(a.keys())