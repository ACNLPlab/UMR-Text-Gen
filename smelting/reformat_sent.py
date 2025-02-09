import re

def format_text(input_text):
    pattern = r'\w+\s*/\s*'
    cleaned_text = re.sub(pattern, '', input_text)
    cleaned_text = re.sub(r'\((?!\s)', '( ', cleaned_text)
    cleaned_text = re.sub(r'(?<!\s)\)', ' )', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def process_file(input_file, output_file):
   try:
       with open(input_file, 'r') as f:
           lines = f.readlines()
       
       formatted_lines = [format_text(line) for line in lines]
       
       with open(output_file, 'w') as f:
           f.write('\n'.join(formatted_lines))
           
       print(f"Successfully processed {input_file} to {output_file}")
           
   except Exception as e:
       print(f"Error processing file: {str(e)}")

# reformat the file
input_file = "/home/common/ACNLP/umr-to-amr/zho_sent_test_umr2amr.txt"  
output_file = "zho_sent_test_umr2amr_smelt.txt"
process_file(input_file, output_file)

