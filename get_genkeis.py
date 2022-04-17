import argparse
import MeCab
import os
import re
import unicodedata
from pathlib import Path
from pyknp import Juman
from tqdm import tqdm
from typing import List

def get_input_dir_basenames(index_filepath:str)->List[str]:
    ids=[]
    with open(index_filepath,"r") as r:
        for line in r:
            id,title=line.replace("\n","").split("\t")
            ids.append(id)

    return ids

def main(args):
    input_root_dirname:str=args.input_root_dirname
    index_filepath:str=args.index_filepath
    output_dirname:str=args.output_dirname
    engine_name:str=args.engine_name

    if engine_name not in ["mecab","jumanpp"]:
        raise RuntimeError(f"サポートされていないエンジン名が指定されました: {engine_name}")

    input_root_dir=Path(input_root_dirname)
    input_dir_basenames=get_input_dir_basenames(index_filepath)

    output_dir=Path(output_dirname)
    output_dir.mkdir(exist_ok=True,parents=True)

    r1=re.compile("[、。]")
    r2=re.compile(r"\d+")
    r3=re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％※]')

    tagger=MeCab.Tagger()
    jumanpp=Juman()

    for input_dir_basename in tqdm(input_dir_basenames):
        input_file=input_root_dir.joinpath(input_dir_basename,"text.txt")

        with input_file.open("r") as r:
            text=r.read().replace("\n","")

        sentences=r1.split(text)

        genkeis=[]
        for sentence in sentences:
            normalized_sentence=unicodedata.normalize("NFKC",sentence)
            replaced_sentence=r2.sub("",normalized_sentence)
            replaced_sentence=r3.sub("",replaced_sentence)

            if engine_name=="mecab":
                node=tagger.parseToNode(replaced_sentence)
                while node:
                    genkei=node.feature.split(",")[6]
                    if genkei!="*":
                        genkeis.append(genkei)

                    node=node.next
            
            elif engine_name=="jumanpp":
                result=jumanpp.analysis(replaced_sentence)
                for mrph in result.mrph_list():
                    if mrph.genkei!="　":
                        genkeis.append(mrph.genkei)

        output_filename=input_file.parent.name+".txt"
        output_file=output_dir.joinpath(output_filename)

        with output_file.open("w") as w:
            for genkei in genkeis:
                w.write(f"{genkei}\n")

if __name__=="__main__":
    os.environ["MECABRC"]="/etc/mecabrc"

    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input_root_dirname",type=str)
    parser.add_argument("-x","--index_filepath",type=str)
    parser.add_argument("-o","--output_dirname",type=str)
    parser.add_argument("-e","--engine_name",type=str,default="mecab")
    args=parser.parse_args()

    main(args)
