import re

def combine_files(file_paths, output_path=None):
    """
    Combines multiple files containing numbered sentences and renumbers them sequentially.
    
    Args:
        file_paths (list): List of paths to input files
        output_path (str, optional): Path where the combined file should be saved
                                   If None, prints to console
    
    Returns:
        str: Combined content with updated numbering
    """
    combined_lines = []
    current_sent_num = 0
    
    try:
        for file_path in file_paths:
            print(f"Processing file: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                for line in lines:
                    line = line.strip()
                    
                    # Update sentence number
                    if line.startswith('# ::nsent'):
                        current_sent_num += 1
                        combined_lines.append(f'# ::nsent {current_sent_num}')
                        
                    # Copy other lines as is
                    else:
                        combined_lines.append(line)
        
        combined_content = '\n'.join(combined_lines)
        
        # Save to file if output path is provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as out_file:
                out_file.write(combined_content)
            print(f"Combined content saved to: {output_path}")
        
        return combined_content
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
        
# Example usage:
if __name__ == "__main__":
    input_files = [
        "eng_zho_doc_dev_spring.txt",
        "arp_doc_dev_spring.txt",
        "nav_doc_dev_spring.txt",
        "saa_doc_dev_spring.txt",
        "kuk_doc_dev_spring.txt",

    ]
    output_file = "all_doc_dev_spring.txt"
    
    result = combine_files(input_files, output_file)
