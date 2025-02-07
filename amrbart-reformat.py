import json

'''AMRBART does not include the slashes that are typical in UMRs and AMRs so the method below
replaces the slashes with pointers such as "<pointer:0>" that increment through the sentence,
this code also makes other subtly changes to spaces in order to comply with proper AMRBART format'''
def format_amr(amr_str):
    pointer_count = 0
    result = ""
    i = 0
    while i < len(amr_str):
        if amr_str[i] == '(':
            result += '('
            i += 1
            while i < len(amr_str) and amr_str[i] != '/' and amr_str[i] != ')':
                i += 1
        elif amr_str[i] == '/':
            i += 1
            start = i
            while i < len(amr_str) and amr_str[i] not in '( ':
                i += 1
            result += f" <pointer:{pointer_count}>{amr_str[start:i].strip()} "
            pointer_count += 1
        elif amr_str[i] == ')':
            if result and result[-1] != ' ':
                result += ' '  
            result += ')'
            i += 1
        else:
            result += amr_str[i]
            i += 1
    return result

'''This method takes in a list of files that are comprised of ONLY linearized UMR sentence level graphs
and returns a list of dicts with the data in the necesary format for AMRBART which is
{"sent" : "(sentence)", "amr": "(umr/amr graph)"} NOTE: if testing change the value of "sent" 
to just be "" '''
def to_json(files):
    sentences = []
    for file in files:
        with open(file, "r", encoding="utf-8") as infile:
            for line in infile:
                sent = "" 
                amr = line.strip()
                new_amr = format_amr(amr)
                data = {"sent": sent, "amr": new_amr}  
                sentences.append(json.dumps(data, ensure_ascii=False)) 
    return sentences

'''This method takes in a list and an output file, then writes each element of the list on a newline'''
def write_to_file(sentences, output):
    with open(output, 'w', encoding="utf-8") as outfile:
        for sentence in sentences:
            outfile.write(sentence + '\n')  

'''
EXAMPLE FORMAT OF AMRBART:
{"sent": "", "amr": "( <pointer:0> date-entity :month 9 :day 11 :year 2010 )"}
'''

# The format and example are from AMRBART: https://github.com/goodbai-nlp/AMRBART/blob/main/examples/data4generation.jsonl line 5
# See paper: Graph Pre-training for AMR Parsing and Generation by Xuefeng Bai, Yulong Chen, and Yue Zhang (2022).
