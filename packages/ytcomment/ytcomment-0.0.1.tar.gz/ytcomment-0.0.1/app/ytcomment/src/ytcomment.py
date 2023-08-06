import requests
import json
import googleapiclient.discovery



GOOGLE_KEY = "AIzaSyBZdHYAp2WWgm413pasORoGG2nJ179DYVg"
MAX_COMMENT = 10000

def youtubescrapper(link):

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=GOOGLE_KEY)
    try:
        video_id = link.split("v=")[-1]
        video_id = video_id.split("&")[0]
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        resposne = request.execute()
        title = resposne["items"][0]["snippet"]["title"]
    except Exception as err:
        print(str(err))
        return ["Please provide a correct youtube video"], None

    comments = []
    flag = 1
    next_page = None
    while flag:
        try:
            if next_page:
                request = youtube.commentThreads().list(
                    part="snippet,replies",
                    pageToken=next_page,
                    videoId = video_id
                )
            else:
                request = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId = video_id
                )
            res = request.execute()
            next_page = res.get("nextPageToken")
            count = 0
            for item in res["items"]:
                try:
                    iii = comments.index(item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
                    count += 1
                except:
                    comments.append(item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
            if count == len(res["items"]) or len(comments) >= MAX_COMMENT:
                flag = 0
        except:
            comments= ["No comments Available"]

    return comments, title

