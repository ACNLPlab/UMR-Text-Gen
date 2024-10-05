import re
import os

# Extracts the sentence from the given text files and return it in a list
def sentence_extractor(files, lang, keyword):
    sentences = []
    for file in files:
        with open(file, "r", encoding="utf-8") as infile:
            for line in infile:
                if keyword in line:
                    info = line.split(keyword, 1)[1].strip()
                    if lang == "eng" or lang == "zho":
                        sentence = re.sub(r'^\d+\s+', '', info)
                    else:
                        sentence = re.sub(r'\s+', ' ', info).strip()
                    sentences.append(sentence)
    return sentences

# Extracts the sentence level UMR graph for the sentence from the given text files and return it in a list
def sentence_umr_extractor(files):
    umr_graphs = []
    for file in files:
        with open(file, "r", encoding="utf-8") as infile:
            content = infile.read()
            matches = re.findall(r'# sentence level graph:?:\s*([\s\S]*?)(?=#|$)', content)
            for match in matches:
                combined_lines = ' '.join(line.strip() for line in match.strip().splitlines() if line.strip())
                if combined_lines:  
                    umr_graphs.append(combined_lines)
    return umr_graphs

# Extracts the alignment for the sentence from the given text file and return it in a list
def alignment_extractor(files): 
    alignments = []
    for file in files:
        with open(file, "r", encoding="utf-8") as infile:
            content = infile.read()
            matches = re.findall(r'# alignments?:\s*([\s\S]*?)(?=#|$)', content)
            for match in matches:
                combined_lines = ' '.join(line.strip() for line in match.strip().splitlines() if line.strip())
                if combined_lines:
                    alignments.append(combined_lines)
                else: 
                    alignments.append("") 
    return alignments

# Extracts the document level UMR graph for the sentence from the given text file and return it in a list
def doc_level_extractor(files):
    umr_graphs = []
    for file in files:
        with open(file, "r", encoding="utf-8") as infile:
            content = infile.read()
            matches = re.findall(r'# document level annotation:\s*([\s\S]*?)(?=\n\s*\n|#|$)', content)
            for match in matches:
                combined_lines = ' '.join(line.strip() for line in match.strip().splitlines() if line.strip())
                if combined_lines:  
                    umr_graphs.append(combined_lines)
    return umr_graphs

# Combines two files in the order given
def combine_files(files, output):
    with open(output, 'w', encoding="utf-8") as outfile:
        for file in files:
            with open(file, 'r', encoding="utf-8") as infile:
                for line in infile:
                    outfile.write(line)

# Combines the first lines of the given dictionaries in the format set to variable "combines"
def combine(sentences, sentence_graphs, alignments, document_graphs, output):
    with open(output, 'w', encoding="utf-8") as outfile:
        for sentence, sentgraph, align, docgraph in zip(sentences, sentence_graphs, alignments, document_graphs):
            combined = sentence + '\tSENTENCE ' + sentgraph + ' ALIGNMENT ' + align + ' DOCUMENT ' + docgraph + '\n'
            outfile.write(combined)

# Given a list and output file, writes list item by item and returns afetr each item
def write_to_file(list, output):
    with open(output, 'w', encoding="utf-8") as outfile:
        for item in list:
                outfile.write(item + '\n')






