# UMR-Text-Gen
This repository includes relevant code from the paper "Generating Text from Uniform Meaning Representation."


Our model checkpoints are available at the following link:
https://drive.google.com/drive/folders/1aOsoBFJsnzJNjPE_EQNdHtXqD7ZClcuX?usp=sharing


*amrbart-reformat.py* rewrites a file containing linearized graphs, with each graph on a separate line, into the desired output format and returns it in a .jsonl file

*text-extractor.py* is a compilation of methods to help extract and reformat UMR data from its original format into these categories: sentences, sentence-level graphs, alignment, and document-level graphs. Then you can reformat them into your desired format by using the method "combine" and changing the variable "combined". Examples of how to get desired format for UMR-to-AMR conversion or AMRlib are in comments at the bottom of the file.

*umr-to-amr-conv.py* converts a file containing linearized UMR graphs, with each graph on a separate line, to be their AMR equivalent. 
