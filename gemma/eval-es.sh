#!/bin/bash

python -u test_eng_sent.py \
    --model_name_or_path  /home/common/ACNLP/gemma-llama-finetune/eng_sent_gemma \
    --do_predict \
    --task graph2text \
    --validation_file /home/common/ACNLP/gemma-llama-finetune/val.csv \
    --output_dir /home/common/ACNLP/gemma-llama-finetune/outputs \
    --per_device_eval_batch_size=1 \
    --max_source_length=1024 \
    --max_target_length=1024 \
    --val_max_target_length=1024 \
    --predict_with_generate \
    --save_steps 10000 \
    --max_val_samples 1000 \
    --evaluation_strategy="no" \
    --save_strategy 'no'\
    --eval_steps 10000 \
    --load_best_model_at_end \
    --metric_for_best_model bleu \
    --save_total_limit 1 \
    --adafactor \
    --num_beams 5 \
    --fp16
