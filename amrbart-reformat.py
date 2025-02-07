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
# See paper: 
'''
@inproceedings{bai-etal-2022-graph,
    title = "Graph Pre-training for {AMR} Parsing and Generation",
    author = "Bai, Xuefeng  and
      Chen, Yulong  and
      Zhang, Yue",
    booktitle = "Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = may,
    year = "2022",
    address = "Dublin, Ireland",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.acl-long.415",
    pages = "6001--6015"
}
'''
