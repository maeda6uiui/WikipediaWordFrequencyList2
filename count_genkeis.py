import argparse
from collections import Counter
from pathlib import Path
from tqdm import tqdm

def main(args):
    input_dirname:str=args.input_dirname
    output_dirname:str=args.output_dirname

    input_dir=Path(input_dirname)
    input_files=list(input_dir.glob("*.txt"))

    output_dir=Path(output_dirname)
    output_dir.mkdir(exist_ok=True,parents=True)

    for input_file in tqdm(input_files):
        with input_file.open("r") as r:
            genkeis=r.read().splitlines()

        counter=Counter(genkeis)

        output_file=output_dir.joinpath(input_file.name)
        with output_file.open("w") as w:
            for genkei,freq in counter.most_common():
                w.write(f"{genkei}\t{freq}\n")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input_dirname",type=str)
    parser.add_argument("-o","--output_dirname",type=str)
    args=parser.parse_args()

    main(args)
