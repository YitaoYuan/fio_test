#!/usr/bin/env bash
config_name=tmp

cat > ./${config_name}.fio <<EOF
[global]
ioengine=io_uring
direct=1
rw=read
bs=4m
iodepth=32
group_reporting=1
loops=3
EOF

for i in $(seq -w 1 64); do
  cat >> ./${config_name}.fio <<EOF
[f${i}]
filename=/models/preset/deepseek-ai/DeepSeek-R1-0528/v1.0/model-000${i}-of-000163.safetensors
numjobs=1
EOF
  echo >> ./${config_name}.fio
done

