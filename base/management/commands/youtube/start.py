# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/code-samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os
from pathlib import Path

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload


api_key = "AIzaSyBvtkgLraKOaYl0lKT6k4ytewc9L3xjWZA"
scopes = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]
o_auth_clinet_key = "79071197269-3d5fo2cknh3js043a850s01v6t972if6.apps.googleusercontent.com"

file_name = f"client_secret_{o_auth_clinet_key}.json"
foldor_path = Path(os.getcwd()).joinpath("data")
# def upload_dir(dir_path: Path, youtube):

#     lista = os.listdir(dir_path)
#     print(lista)
#     res = []
#     for el in lista:
#         file_name = name_of_file(el)

#         request = youtube.videos().insert(
#             body={"snippet": {"title": f"{file_name}", "description": f"{file_name}", "tags": [], "defaultLanguage": "ar"}},
#             part="snippet",
#             # TODO: For this request to work, you must replace "YOUR_FILE"
#             #       with a pointer to the actual file you are uploading.
#             media_body=MediaFileUpload(foldor_path.joinpath(el)),
#         )
#         res.append(request)
#     return res


def insert_play_list(youtube, title, desc):
    tags = title.split(" ")
    request = youtube.playlists().insert(
        part="snippet",
        body={
            "snippet": {
                "title": f"{title}",
                "description": f"{desc}",
                "tags": tags,
                "defaultLanguage": "ar",
            },
        },
    )

    return request.execute()


def upload_list(lista, name, desc):

    global file_name
    global scopes
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = file_name
    file = Path(__file__).parent.joinpath(f"{client_secrets_file}")

    # # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(file, scopes)

    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    playlist = insert_play_list(youtube, name, desc)
    print(f"playlist:{playlist}")

    for el in lista:
        session = el["session"]
        video_upload_request = youtube.videos().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": f"{session.title}",
                    "description": f"{session.title} {desc}",
                    "tags": name.split(" / "),
                    "defaultLanguage": "ar",
                },
                "status": {
                    "publicStatsViewable": True,
                    "madeForKids": False,
                },
            },
            # TODO: For this request to work, you must replace "YOUR_FILE"
            #       with a pointer to the actual file you are uploading.
            media_body=MediaFileUpload(el["file"]),
        )
        video_upload_res = video_upload_request.execute()

        print(f"video_upload_res :{video_upload_res}")

        playlistItems_request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist.get("id"),
                    "resourceId": video_upload_res.get("id"),
                    # "title": f"{session.title}",
                    # "description": f"{session.title} {desc}",
                    "tags": name.split(" / "),
                    "defaultLanguage": "ar",
                },
            },
        )

        # res = reques / youtube / v3 / docs / playlistItems / listt.execute()
        playlistItems_res = playlistItems_request.execute()
        print(f"playlistItems_res : {playlistItems_res}")
        url = playlistItems_res.get("snippet").get("thumbnails").get("key").get("url")

        session.video_url = url
        session.save()
    # for el in lista:
    #     file_name = name_of_file(el)

    #     request = youtube.videos().insert(
    #         body={"snippet": {"title": f"{file_name}", "description": f"{file_name}", "tags": [], "defaultLanguage": "ar"}},
    #         part="snippet",
    #         # TODO: For this request to work, you must replace "YOUR_FILE"
    #         #       with a pointer to the actual file you are uploading.
    #         media_body=MediaFileUpload(foldor_path.joinpath(el)),
    #     )
    #     res.append(request)
    # return res


def name_of_file(file):

    # dir = Path(file).resolve()
    return os.path.basename(file).rsplit(".", 1)[0]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = file_name

    # # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    # # credentials = flow.run_console()
    # flow.fetch_token(code = credentials)

    # youtube = googleapiclient.discovery.build(
    #     api_service_name, api_version, credentials=credentials)

    # ===

    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    req_list = upload_dir(foldor_path, youtube)
    res_list = []
    for request in req_list:
        response = request.execute()
        res_list.append(response)


if __name__ == "__main__":
    main()
# upload_dir(Path(__file__).resolve(), None)
