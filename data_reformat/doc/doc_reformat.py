def transform_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            parts = line.strip().split('\t', 1)
            if len(parts) != 2:
                continue
                
            sentence, remainder = parts
            output = f"# ::id\n# ::snt {sentence}\n# ::save-date\n{remainder}\n\n"
            outfile.write(output)

input_file = "saa_doc_train.txt"
output_file = "saa_doc_train_clean.txt"
transform_file(input_file, output_file)