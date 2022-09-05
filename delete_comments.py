import argparse
from inference import inference
from youtube_api import youtube_api
import re
import preprocessor as p
import string

parser = argparse.ArgumentParser()

parser.add_argument("--input_file", default="sample_pred_in.txt", type=str, help="Input file for prediction")
parser.add_argument("--output_file", default="sample_pred_out.txt", type=str, help="Output file for prediction")
parser.add_argument("--model_dir", default="youtube_model", type=str, help="Path to save, load model")
parser.add_argument("--batch_size", default=32, type=int, help="Batch size for prediction")
parser.add_argument("--no_cuda", action="store_true", help="Avoid using CUDA when available")

parser.add_argument("--channel_id", default="youtube_model", type=str, help="Path to save, load model")
parser.add_argument("--video_id", default=None, type=str, help="Path to save, load model")
parser.add_argument("--use_channel_id", default=True)

pred_config = parser.parse_args()

def clean_data(text):
    text = p.clean(text)
    text = text.replace('\d+', '')
    text = text.lower()
    CLEANR = re.compile('<.*?>')
    text = re.sub(CLEANR, ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

api = youtube_api("client_secrets.json")
api.load_credentials()
channel_id = "UCz_cNcJzCy4asffzW5ERH1w"
video_ids = api.get_video_ids(channel_id, 1)
comments, replies = api.get_comments(video_ids[0], get_all=False, max_results=100)
infer = inference(pred_config)

for reply_id, reply in replies.items():
    clean_comment = clean_data(reply)
    intent = infer.predict(clean_comment)
    print(intent, clean_comment)
    if intent == "TRUE":
        api.delete_comments(reply_id)