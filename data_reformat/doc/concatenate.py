import os
def concatenate_files(input_files, output_file):
    """
    Concatenate multiple files into a single output file.
    
    Args:
        input_files (list): List of input file paths
        output_file (str): Path for the output file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_path in input_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        #outfile.write(f"\n\n--- Content from {file_path} ---\n\n")
                        outfile.write(infile.read())
                else:
                    print(f"Warning: File '{file_path}' not found. Skipping.")
        print(f"Successfully created {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

input_files = [
        "eng_zho_doc_train_amrlib.txt",
        "arp_doc_train_amrlib.txt",
        "nav_doc_train_amrlib.txt",
        "saa_doc_train_amrlib.txt",
        "kuk_doc_train_amrlib.txt",

    ]

output_file = 'all_doc_train_amrlib_new.txt'
concatenate_files(input_files, output_file)