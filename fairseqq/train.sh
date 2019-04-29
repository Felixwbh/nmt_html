#! /usr/bin/bash
set -e

#device=0,1,2,3,4,5,6,7
#device=0
device=3

#task=iwslt-de2en
task=wmt-en2de

# must set this tag
tag=test_long

if [ $task == "iwslt-de2en" ]; then
	arch=transformer_iwslt_de_en
	share_embedding=0
	dropout=0.3
	lr=0.0005
	warmup=4000
	update_freq=1
	weight_decay=0.0001
	saved_checkpoint_num=10
	max_epoch=
	max_update=50000
	data_dir=iwslt14.tokenized.de-en
	src_lang=de
	tgt_lang=en
elif [ $task == "wmt-en2de" ]; then
	arch=transformer_wmt_en_de
	share_embedding=0
	lr=0.0007
	warmup=4000
        max_tokens=4096
	update_freq=2
	weight_decay=0.0
	saved_checkpoint_num=5
	max_epoch=20
	max_update=
	data_dir=180w.c-e
	src_lang=c
	tgt_lang=e

elif [ $task == "wmt19_en2zh" ]; then
        arch=transformer_t2t_wmt_en_de
        share_embedding=0
        share_decoder_input_output_embed=1
        lr=0.001
        warmup=8000
        max_tokens=4096
        update_freq=1
        weight_decay=0.0
        saved_checkpoint_num=20
        max_epoch=15
        max_update=
        data_dir=wmt19_en2zh
        src_lang=en
        tgt_lang=zh

elif [ $task == "ldc" ]; then
        arch=transformer_t2t_wmt_en_de
        share_embedding=0
        share_decoder_input_output_embed=1
        lr=0.0007
        warmup=4000
        max_tokens=4096
        update_freq=1
        weight_decay=0.0
        saved_checkpoint_num=20
        max_epoch=15
        max_update=
        data_dir=LDC_180W
        src_lang=zh
        tgt_lang=en
else
	echo "unknown task=$task"
	exit
fi

save_dir=checkpoints/$task/$tag

if [ ! -d $save_dir ]; then
	mkdir -p $save_dir
fi
cp ${BASH_SOURCE[0]} $save_dir/train.sh

gpu_num=`echo "$device" | awk '{split($0,arr,",");print length(arr)}'`

cmd="python3 -u train.py data-bin/$data_dir
  --distributed-world-size $gpu_num -s $src_lang -t $tgt_lang
  --arch $arch
  --optimizer adam --clip-norm 0.0
  --lr-scheduler inverse_sqrt --warmup-init-lr 1e-07 --warmup-updates $warmup
  --lr $lr --min-lr 1e-09
  --weight-decay $weight_decay
  --criterion label_smoothed_cross_entropy --label-smoothing 0.1
  --max-tokens $max_tokens
  --update-freq $update_freq
  --no-progress-bar
  --log-interval 100
  --save-dir $save_dir"
#  --keep-interval-updates $saved_checkpoint_num
#  --save-last-checkpoints $saved_checkpoint_num"

adam_betas="'(0.9, 0.997)'"
cmd=${cmd}" --adam-betas "${adam_betas}
if [ $share_embedding -eq 1 ]; then
cmd=${cmd}" --share-all-embeddings "
fi
#if [ $share_decoder_input_output_embed -eq 1 ]; then
#cmd=${cmd}" --share-decoder-input-output-embed "
#fi
if [ -n "$max_epoch" ]; then
cmd=${cmd}" --max-epoch "${max_epoch}
fi
if [ -n "$max_update" ]; then
cmd=${cmd}" --max-update "${max_update}
fi
if [ -n "$dropout" ]; then
cmd=${cmd}" --dropout "${dropout}
fi

#echo $cmd
#eval $cmd
#cmd=$(eval $cmd)
#nohup $cmd exec 1> $save_dir/train.log exec 2>&1 &
#tail -f $save_dir/train.log

export CUDA_VISIBLE_DEVICES=$device
cmd="nohup "${cmd}" > $save_dir/train.log 2>&1 &"
eval $cmd
tail -f $save_dir/train.log

