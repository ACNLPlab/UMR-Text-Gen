import random
import json

def parse_and_format(input_text):

    lines = input_text.strip().split('\n')
    
    pairs = []
    for line in lines:
        line = line.strip()
        if not line or '\t' not in line:
            continue
        
        sentence, graph = line.split('\t')
        pairs.append((sentence.strip(), graph.strip()))
    
    return pairs

def write_formatted_file(pairs, filename, source_name):
    with open(filename, 'w', encoding='utf-8') as f:
        for sentence, graph in pairs:
            data = {"sentence": sentence, "graph": graph}
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

random.seed(42)

with open('zho_sent_train.txt', 'r', encoding='utf-8') as f:
    input_text = f.read()

DEV_NUM = 40
pairs = parse_and_format(input_text)
dev_pairs = random.sample(pairs, DEV_NUM)
train_pairs = [pair for pair in pairs if pair not in dev_pairs]

write_formatted_file(train_pairs, 'zho_sent_tr_ft.txt', 'zho_sent_train.txt')
write_formatted_file(dev_pairs, 'zho_sent_dev_ft.txt', 'zho_sent_train.txt')

print(f"Split completed successfully!")
print(f"Training set: {len(train_pairs)} examples")
print(f"Development set: {len(dev_pairs)} examples")
