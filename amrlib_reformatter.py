import os

os.chdir('')

input_file = ""
output_file = ''

with open(input_file, 'r', encoding="utf-8") as infile, open(output_file, 'w', encoding="utf-8") as outfile:
    for line in infile:
        sent = line.split('\t')[0]
        all_graphs = line.split("\t")[1]
        doc_graph = all_graphs.split("DOCUMENT ")[1]
        sent_split = all_graphs.split("SENTENCE ")[1]
        sent_graph = sent_split.split("ALIGNMENT ")[0]
        align_split = sent_split.split("ALIGNMENT ")[1]
        align = align_split.split("DOCUMENT ")[0]
        output_string = f"# ::id \n# ::snt {sent}\n# ::save-date \n{sent_graph} {align} {doc_graph}\n"
        outfile.write(output_string) 
