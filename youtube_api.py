import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json

class youtube_api:

    def __init__(self, client_secrets_path):
        self.client_secrets = client_secrets_path
        self.youtube = None

    def load_credentials(self):
        credentials = None

        if os.path.exists('token.pickle'):
            print("Loading Credentials From File...")
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print("Refreshing Access Token...")
                credentials.refresh(Request())
            else:
                print("Fetching New Tokens...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json',
                    scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
                )

                flow.run_local_server(port=8080, prompt='consent')

                credentials = flow.credentials

                with open('token.pickle', 'wb') as f:
                    print("Saving Credentials for Future Use...")
                    pickle.dump(credentials, f)

        self.youtube = build("youtube", "v3", credentials=credentials)

    def get_comments(self, videoId):
        request = self.youtube.commentThreads().list(
        part="id,replies,snippet",
        order="relevance",
        videoId=videoId,
        #pageToken="QURTSl9pMGFOUl9pUjQyYmpfMzNiUnhWQlJzbXZxaVF0SlY4TDZHZjRZVUJnZ1BlLXgyYnJaS2poeFRRamcyUmttaDAzYnhIdldlckZ6MnVScUlheV9EQnBBQkNnc19sSXc1OVlpY2FLOTdRM0xtMFlpWmRiSXV0NC1FY3hMYUNmUHF3M21aVFNZcG9KcXFQZlZRMXF4b042YnROVVA0c0Z0bEZZM21zQk1Ta1MtWjFNNkZ6Xy11ZlRwY2NPMTFrU1Jsa2JvNTVLSzlXTjg1eDI0cW8xU01uNWVlYkowWXIxYS0tT1BMbFJGaU9jS1puRDdkNFhFRHpyd3pBZjhla0xvd0ZsYUx2MEdpYkFsYjI0QnZQZ2RjVkVpYl80Um5RdkVKVEEtMEV0U3lRUXFvOUgtWnhKcFB1Slp4dmJDampyUjAyS3RCRmRVdw=="
        )

        response = request.execute()

        comment_dict = {}

        for comment in response['items']:
            comment_dict[comment['snippet']['topLevelComment']['id']] = comment['snippet']['topLevelComment']['snippet']['textDisplay']

        while response.get('nextPageToken', None):
            request = self.youtube.commentThreads().list(
                part="id,replies,snippet",
                order="relevance",
                videoId=videoId,
                pageToken=response['nextPageToken']
            )

            response = request.execute()

            for comment in response['items']:
                comment_dict[comment['snippet']['topLevelComment']['id']] = \
                comment['snippet']['topLevelComment']['snippet']['textDisplay']

        #print(json.dumps(response))
        return comment_dict

    def get_playlist_video(self):
        request = self.youtube.playlistItems().list(
            part="status",
            playlistId="PLpAqSYsFkgvufrorQgA6kmT-PO_okSyzk"
        )

        response = request.execute()

        return response

    def add_comments(self, comment, videoId):
        request = self.youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": videoId,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment
                        }
                    }
                }
            }
        ).execute()

        return request

    def delete_comments(self, commentId):
        request = self.youtube.comments().setModerationStatus(
            id=commentId,
            moderationStatus="rejected"
        )
        request.execute()
