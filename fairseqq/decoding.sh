set -e


cmd="python generate.py data-bin/wmt14_en_de  
--path checkpoints/fconv_wmt_en_de/checkpoint_best.pt
--beam 5 
--remove-bpe
"
CUDA_VISIBLE_DEVICES=3 $cmd
