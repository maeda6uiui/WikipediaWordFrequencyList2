import argparse
from pathlib import Path
from tqdm import tqdm

def main(args):
    input_dirname:str=args.input_dirname
    output_filepath:str=args.output_filepath

    input_dir=Path(input_dirname)
    input_files=list(input_dir.glob("*.txt"))

    genkei_freqs={}
    for input_file in tqdm(input_files):
        with input_file.open("r") as r:
            lines=r.read().splitlines()

        for line in lines:
            genkei,freq=line.split("\t")
            freq=int(freq)

            if genkei in genkei_freqs:
                genkei_freqs[genkei]+=freq
            else:
                genkei_freqs[genkei]=freq

    genkei_freqs=dict(sorted(genkei_freqs.items(),key=lambda x:x[1],reverse=True))

    with open(output_filepath,"w") as w:
        for genkei,freq in genkei_freqs.items():
            w.write(f"{genkei}\t{freq}\n")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input_dirname",type=str)
    parser.add_argument("-o","--output_filepath",type=str)
    args=parser.parse_args()

    main(args)
