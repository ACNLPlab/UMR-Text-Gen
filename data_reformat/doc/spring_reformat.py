import re

def transform_umr_to_structured(input_file, output_file):
    """Transform UMR format file to structured format."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sentences = content.split('# ::id')[1:]  
    output = []
    sentence_count = 1
    
    for sentence in sentences:
        lines = sentence.strip().split('\n')
        current_entry = []
        
        current_entry.append(f'# ::nsent {sentence_count}')
        sentence_count += 1
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('# ::save-date'):
                continue
                
            if line.startswith('# ::snt'):
                current_entry.append(line)
                continue
                
            if line.startswith('SENTENCE '):
                parts = re.split(' ALIGNMENT | DOCUMENT ', line[9:])
                
                # add AMR part
                current_entry.append(parts[0].strip())
                
                # add alignment information
                if len(parts) > 1:
                    current_entry.append('# ::alignment ' + parts[1].strip())
                
                # add document information if it exists
                if len(parts) > 2:
                    current_entry.append('# ::document ' + parts[2].strip())
        
        if current_entry:
            output.extend(current_entry)

    # write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
        f.write('\n()')

# use the function
transform_umr_to_structured('arp_doc_dev_amrlib.txt', 'arp_doc_dev_spring.txt')
