import json
# folder_input='./sql-chat/'
folder_input='./chatbot-chat/'
# folder_output='./sql-text/'
folder_output='./chatbot-text/'
names=['test', 'train', 'valid']
for name in names:
    with open(folder_input + name + '.jsonl', 'r') as json_file:
        json_list = list(json_file)
    with open(folder_output + name + '.jsonl', 'w') as outfile:
        for json_str in json_list:
            result = json.loads(json_str)
            message = result['messages']
            entry = {
                "text": message[0]['content'] + '\nUser:' + message[1]['content'] + '\nAssistant:' + message[2]['content']
            }
            json.dump(entry, outfile)
            outfile.write('\n')