import re

# Extracts the full raw sentence from the given text file
def sentence_extractor(file, output):
    keyword = "Words"
    with open(file, "r") as infile, open(output, "w") as outfile:
            for line in infile:
                if keyword in line:
                    info = line.split(keyword, 1)[1].strip()
                    sentence = re.sub(r'\s+', ' ', info).strip()
                    outfile.write(sentence + "\n")

# Extracts the sentence level UMR graph for the sentence from the given text file
def sentence_UMR_extractor(file, output):
    keyword = "# sentence level graph:"
    with open(file, "r") as infile, open(output, "w") as outfile:
        write_graph = False
        for line in infile:
            if keyword in line:
                write_graph = True
                continue
            if write_graph:
                if line.strip() and not line.startswith("#"):
                    outfile.write(line.strip() + " ")
                else:
                    write_graph = False
                    outfile.write("\n")

# Extracts the alignment for the sentence from the given text file
def alignment_extractor(file, output):
    keyword = "# alignment:"
    with open(file, "r") as infile, open(output, "w") as outfile:
        write_graph = False
        for line in infile:
            if keyword in line:
                write_graph = True
                continue
            if write_graph:
                if line.strip() and not line.startswith("#"):
                    outfile.write(line.strip() + " ")
                else:
                    write_graph = False
                    outfile.write("\n")

# Extracts the document level UMR graph for the sentence from the given text file
def doc_level_extractor(file, output):
    keyword = "# document level annotation:"
    with open(file, "r") as infile, open(output, "w") as outfile:
        write_graph = False
        for line in infile:
            if keyword in line:
                write_graph = True
                continue
            if write_graph:
                if line.strip() and not line.startswith("#"):
                    outfile.write(line.strip() + " ")
                else:
                    write_graph = False
                    outfile.write("\n")

# Combines just the raw sentence and the sentence level UMR graph in the form: (sentence) \t (sentence level UMR graph) \n
def first_combine(sentence_file, sentence_UMR_file, output_file):
    with open(sentence_file, "r") as infile1, open(sentence_UMR_file, "r") as infile2, open(output_file, "w") as outfile:
        sentences = infile1.readlines()
        umr_graphs = infile2.readlines()
        
        min_length = min(len(sentences), len(umr_graphs))
        
        for i in range(min_length):
            sentence = sentences[i].strip()
            umr_graph = umr_graphs[i].strip()
            outfile.write(f"{sentence}\t{umr_graph}\n")

# Combines the raw sentence, sentence level UMR graph, alignment, document level UMR graph in the form: (sentence) \tSENTENCE (sentence level UMR graph) ALIGNMENT (alignment) DOCUMENT (document) \n
def all_combine(sentence_file, sentence_UMR_file, alignment_file, document_level_file, output_file):
    with open(sentence_file, "r") as infile1, open(sentence_UMR_file, "r") as infile2, open(alignment_file, "r") as infile3, open(document_level_file, "r") as infile4, open(output_file, "w") as outfile:
        sentences = infile1.readlines()
        umr_graphs = infile2.readlines()
        alignments = infile3.readlines()
        documents = infile4.readlines()
        
        min_length = min(len(sentences), len(umr_graphs), len(alignments), len(documents))
        
        for i in range(min_length):
            sentence = sentences[i].strip()
            umr_graph = umr_graphs[i].strip()
            alignment = alignments[i].strip()
            document = documents[i].strip()
            outfile.write(f"{sentence}\tSENTENCE {umr_graph} ALIGNMENT {alignment} DOCUMENT {document}\n")

sentence_extractor("input.txt", "sentence-output.txt") # creates a file of just the raw sentences
sentence_UMR_extractor("input.txt", "sentence-graph-output.txt") # creates a file of only the sentence level UMR graphs
alignment_extractor("input.txt", "alignment-output.txt") # creates a file of only the alignment of the sentences
doc_level_extractor("input.txt", "doc-graph-output.txt") # creates a file of only the sentences' document level UMR graphs
first_combine("sentence-output.txt", "sentence-graph-output.txt", "first-output.txt") # combines the sentences and sentences UMR graphs
# creates a text file with the sentence, sentence level UMR graph, alignment, and the document level UMR graph
all_combine("sentence-output.txt", "sentence-graph-output.txt", "alignment-output.txt", "doc-graph-output.txt", "full-OUTPUT.txt") 
