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
        current_graph = []
        
        for line in lines:
            line = line.strip()
            if not line:
                # When we hit an empty line, process the collected graph if we have both parts
                if current_sentence and current_graph:
                    # join the graph lines and format them
                    full_graph = ' '.join(current_graph)
                    formatted_graph = format_text(full_graph)
                    result = {
                        "source": formatted_graph,
                        "target": current_sentence
                    }
                    f.write(json.dumps(result, ensure_ascii=False) + '\n')
                current_sentence = None
                current_graph = []
                continue
                
            if line.startswith('# ::snt'):
                current_sentence = line.replace('# ::snt', '').strip()
            elif line.startswith('SENTENCE'):
                current_graph.append(line)

# process the file
## convert amrlib to smelt format
process_file('eng_doc_dev_amrlib.txt', 'eng_doc_dev_smelt.json')