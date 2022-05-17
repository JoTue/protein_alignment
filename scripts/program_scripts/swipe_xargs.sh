#!/bin/sh

# subprocess.run(f"scripts/program_scripts/swipe_xargs.sh {chunk_n} {threads_n} {query_file} {chunk_name} {db_file} {gapopen-gapextension} {gapextension} {matrix} {seq_n} {min_score} {name}", shell=True)    
qdir=$(dirname $3)
# copy input files in /tmp
TMPDIR=/tmp/tuechler
mkdir -p $TMPDIR
cp -r $qdir $TMPDIR
ls $TMPDIR/data

seq $1 | xargs -I[] --max-procs=$2 bash -c "echo start []; date; uptime; swipe -i $TMPDIR/data/$4/q_[] -d $TMPDIR/data/db.fasta -G $6 -E $7 -M /apps/emboss/6.6.0/emboss/data/E$8 -e 1000000 -b $9 -v $9 -c ${10} > /scratch/cube/tuechler/program_out/${11}/swipe_xargs/[].swipe_xargs ; echo end []; date; uptime"

rm -rf $TMPDIR