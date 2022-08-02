import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from youtube_api import youtube_api
import pandas as pd
import json

credentials = None


def save_data(id, seq_in, mode=''):

    save_dir = 'data/kor_hate'

    label = len(seq_in) * ['none']

    seq_out = []

    for i in seq_in:
        seq_out.append(len(i.split()) * 'O ')

    if not os.path.isdir(os.path.join(save_dir, mode)):
        os.makedirs(os.path.join(save_dir, mode))

    with open(os.path.join(save_dir, mode, 'label'), 'w') as fp:
        fp.write('\n'.join(label))

    with open(os.path.join(save_dir, mode, 'seq.in'), 'w') as fp:
        fp.write('\n'.join(seq_in))

    with open(os.path.join(save_dir, mode, 'seq.out'), 'w') as fp:
        fp.write('\n'.join(seq_out))

    with open(os.path.join(save_dir, mode, 'id'), 'w') as fp:
        fp.write('\n'.join(id))


def get_comments(api, videoId):
    comments = api.get_comments(videoId)
    save_data(list(comments.keys()), list(comments.values()), 'test')
    print("Comments saved")

    return list(comments.keys())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    api = youtube_api("client_secrets.json")
    api.load_credentials()

    id = get_comments(api, "9gUWVBeXKBM")

    # df = pd.read_csv("kor_hate_model/preds.csv")
    #
    # print(df)
    #
    # for idx, row in df.iterrows():
    #     if row['intent_hyp'] == 'hate':
    #         print("Deleted:", row['utterance'])
    #         api.delete_comments(id[idx])


    # playlist = api.get_playlist_video()
    # api.add_comments("Example 2", "9gUWVBeXKBM")


