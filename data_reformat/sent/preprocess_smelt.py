import re
import json

def format_text(input_text):
    pattern = r'\w+\s*/\s*'
    cleaned_text = re.sub(pattern, '', input_text)
    cleaned_text = re.sub(r'\((?!\s)', '( ', cleaned_text)
    cleaned_text = re.sub(r'(?<!\s)\)', ' )', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        current_sentence = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('# ::snt'):
                current_sentence = line.replace('# ::snt', '').strip()
            elif line.startswith('(') and current_sentence is not None:
                formatted_graph = format_text(line)
                result = {
                    "source": formatted_graph,
                    "target": current_sentence
                }
                f.write(json.dumps(result, ensure_ascii=False) + '\n')
                current_sentence = None

# process the file
process_file('all_sent_dev_spring.txt', 'all_sent_dev_smelt.json')