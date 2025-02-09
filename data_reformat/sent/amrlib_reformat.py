def reformat_data(input_text):
    lines = input_text.strip().split('\n')
    formatted_data = []
    current_snt = None
    current_graph = None
    for line in lines:
        line = line.strip()
        if line.startswith("# ::snt"):
            current_snt = line.split(" ", 2)[2]
        elif line.startswith("("):
            current_graph = line
            if current_snt and current_graph:
                formatted_data.append(f"# ::id\n# ::snt {current_snt}\n# ::save-date\n{current_graph}\n")
                current_snt = None
                current_graph = None
    return "\n".join(formatted_data)

input_file = "/home/common/ACNLP/umr_data/train/sent/zho_sent_train_spring.txt"
output_file = "/home/common/ACNLP/amrlib/amrlib/data/zho-train/sent/train.txt"

with open(input_file, 'r', encoding='utf-8') as infile:
    input_data = infile.read()

output_data = reformat_data(input_data)

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write(output_data)

print(f"Reformatted data written to {output_file}")

