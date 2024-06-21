from pytube import YouTube
import os


class YouTubeDownloader:
    def downloadYouTubeVideo(video_url, path):

        yt = YouTube(video_url)
        yt = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        if not os.path.exists(path):
            os.makedirs(path)
        yt.download(path)

    def downloadYouTubeAudio(video_url, path):

        yt = YouTube(video_url)
        yt = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
        if not os.path.exists(path):
            os.makedirs(path)
        yt.download(path)

    def download_both(video_url, export_file_name):
        YouTubeDownloader.downloadYouTubeVideo(
            video_url,
            f"./temp_videos/{export_file_name}",
        )
        YouTubeDownloader.downloadYouTubeAudio(
            video_url,
            f"./temp_audio/{export_file_name}_audio",
        )


YouTubeDownloader.download_both(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley", "Rickroll"
)
