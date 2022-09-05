import argparse
import os
import csv
import string
import re
import preprocessor as p


def save_data(data, file_name, mode):
    with open(os.path.join(pred_config.output_file, mode, file_name), "w") as fp:
        for d in data:
            fp.write("%s\n" % d)


def clean_data(text):
    text = p.clean(text)
    text = text.replace('\d+', '')
    text = text.lower()
    CLEANR = re.compile('<.*?>')
    text = re.sub(CLEANR, ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))

    return text.strip()


def read_save_data(args, mode):
    with open(os.path.join(args.input_file, mode, "replies.tsv"), encoding='ISO-8859-1') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        utterances = []
        bio = []
        intents = []
        next(rd)
        for row in rd:
            clean_utterance = clean_data(row[1])
            if clean_utterance == '':
                continue
            else:
                print(clean_utterance)

            utterances.append(clean_utterance)
            bio.append("O " * len(clean_utterance.split()))
            intents.append(row[2])

    save_data(intents, "label", mode)
    save_data(utterances, "seq.in", mode)
    save_data(bio, "seq.out", mode)


parser = argparse.ArgumentParser()
parser.add_argument("--input_file", default="youtube_data/UCz_cNcJzCy4asffzW5ERH1w", type=str, help="Input file for prediction")
parser.add_argument("--output_file", default="data/youtube", type=str, help="Input file for prediction")
pred_config = parser.parse_args()

if not os.path.isdir(pred_config.output_file):
    os.makedirs(os.path.join(pred_config.output_file, "train"))
    os.makedirs(os.path.join(pred_config.output_file, "test"))
    os.makedirs(os.path.join(pred_config.output_file, "dev"))


read_save_data(pred_config, "train")
read_save_data(pred_config, "test")
read_save_data(pred_config, "dev")







