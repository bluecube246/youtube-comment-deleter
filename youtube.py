import os
from youtube_api import youtube_api
import csv
import argparse

credentials = None


def get_comments(api, videoId):
    comments, replies = api.get_comments(videoId, get_all=True, max_results=100)
    #save_data(list(comments.keys()), list(comments.values()), 'test')
    print("Comments saved")

    return comments, replies


def save_youtube_data(video_ids, api, channel_id, mode=None):
    output_columns = ['id', 'comment', 'spam']

    if not os.path.exists(os.path.join("youtube_data_raw", channel_id, mode)):
        os.makedirs(os.path.join("youtube_data_raw", channel_id, mode))

    if isinstance(video_ids, str):
        video_ids = [video_ids]

    for video_id in video_ids:
        comments, replies = get_comments(api, video_id)
        comment_data = zip(list(comments.keys()), list(comments.values()))
        reply_data = zip(list(replies.keys()), list(replies.values()))

        with open(os.path.join("youtube_data_raw", channel_id, mode, video_id + "_comments.tsv"), 'w', newline='') as csvfile:
            tsv_output = csv.writer(csvfile, delimiter='\t')
            tsv_output.writerow(output_columns)
            for id, val in comment_data:
                tsv_output.writerow([id, val, False])

        with open(os.path.join("youtube_data_raw", channel_id, mode, video_id + "_replies.tsv"), 'w', newline='') as csvfile:
            tsv_output = csv.writer(csvfile, delimiter='\t')
            tsv_output.writerow(output_columns)
            for id, val in reply_data:
                tsv_output.writerow([id, val, False])


def create_combine_data(comment_type, mode, channel_id):
    import glob

    data_files = glob.glob(os.path.join("youtube_data_raw", channel_id, mode, "*_" + comment_type + ".tsv"))

    data = ""

    for file in data_files:
        with open(file) as fp:
            header = fp.readline()
            data_temp = fp.read()

        data += data_temp

    data = header + data
    with open(os.path.join("youtube_data", channel_id, mode, comment_type + ".tsv"), 'w') as fp:
        fp.write(data)


def combine_youtube_data(channel_id, mode):

    if not os.path.exists(os.path.join("youtube_data", channel_id, mode)):
        os.makedirs(os.path.join("youtube_data", channel_id, mode))

    create_combine_data("comments", mode, channel_id)
    create_combine_data("replies", mode, channel_id)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--channel_id", default="UC4Bf1QwmVtSyZHmxi4gIuQw", type=str, help="channel id to gather data")
    parser.add_argument("--n", default=4, type=int, help="Number of video's to extract comments")
    args = parser.parse_args()

    api = youtube_api("client_secrets.json")
    api.load_credentials()

    video_ids = api.get_video_ids(args.channel_id, 4)

    save_youtube_data(video_ids[0], api, channel_id=args.channel_id, mode="test")
    save_youtube_data(video_ids[1], api, channel_id=args.channel_id, mode="dev")
    save_youtube_data(video_ids[2:], api, channel_id=args.channel_id, mode="train")

    combine_youtube_data(args.channel_id, mode="test")
    combine_youtube_data(args.channel_id, mode="dev")
    combine_youtube_data(args.channel_id, mode="train")
