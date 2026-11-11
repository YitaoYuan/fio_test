#!/usr/bin/env bash
NUMJOBS=8
IODEPTH=8
BS=8m
SIZE=10G

fio --name=writeN --filename_format='test.$jobnum' --numjobs=${NUMJOBS} --rw=write --direct=1 --ioengine=libaio --iodepth=${IODEPTH} --bs=${BS} --falloc=truncate --scramble_buffers=0 --size=${SIZE}

fio --name=readN --filename_format='test.$jobnum' --numjobs=${NUMJOBS} --rw=read --direct=1 --ioengine=libaio --iodepth=${IODEPTH} --bs=${BS} --size=${SIZE}
