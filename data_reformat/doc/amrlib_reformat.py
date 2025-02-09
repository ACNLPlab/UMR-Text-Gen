import re

def process_data(file_path, output_path):
    with open(file_path, 'r') as infile:
        data = infile.read()
    
    # Add newline after '# ::save-date' if it's not followed by a newline
    data = re.sub(r'(# ::save-date)(\()', r'\1\n\2', data)
    
    # Remove SENTENCE, ALIGNMENT, and DOCUMENT markers
    clean_data = re.sub(r'SENTENCE ', '', data)
    cleaned_data = re.sub(r'\s*(ALIGNMENT|DOCUMENT)\s*', ' ', clean_data)
    
    with open(output_path, 'w') as outfile:
        outfile.write(cleaned_data)

tr_infile = "/home/common/ACNLP/umr_data/train/doc/eng_zho_doc_train_amrlib.txt"
tr_outfile = "/home/common/ACNLP/amrlib/amrlib/data/eng-zho-train/doc/train.txt"
dev_infile = "/home/common/ACNLP/umr_data/train/doc/eng_zho_doc_dev_amrlib.txt"
dev_outfile = "/home/common/ACNLP/amrlib/amrlib/data/eng-zho-train/doc/dev.txt"

process_data(tr_infile, tr_outfile)
process_data(dev_infile, dev_outfile)
print("data sent to: " + tr_outfile)
print("data sent to: " + dev_outfile)
