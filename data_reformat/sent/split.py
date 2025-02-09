import random

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
        f.write(f"# ::source {source_name}\n")
        
        for i, (sentence, graph) in enumerate(pairs, 1):
            f.write(f"# ::nsent {i}\n")
            f.write(f"# ::snt {sentence}\n")
            f.write(f"{graph}\n")

random.seed(42)

with open('eng_sent_train.txt', 'r', encoding='utf-8') as f:
    input_text = f.read()


DEV_NUM = 113
pairs = parse_and_format(input_text)
dev_pairs = random.sample(pairs, DEV_NUM)
train_pairs = [pair for pair in pairs if pair not in dev_pairs]

write_formatted_file(train_pairs, 'eng_sent_train_full_spring.txt', 'eng_sent_train.txt')
write_formatted_file(dev_pairs, 'fake.txt', 'eng_sent_train.txt')

print(f"Split completed successfully!")
print(f"Training set: {len(train_pairs)} examples")
print(f"Development set: {len(dev_pairs)} examples")
