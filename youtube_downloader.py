from pytube import YouTube
import os


class YouTubeDownloader:
    @staticmethod
    def resolve_output_path(path):
        if os.path.isabs(path):
            return path

        normalized_path = os.path.normpath(path.replace("\\", "/"))
        if normalized_path == ".":
            normalized_path = ""
        if normalized_path == "generated_content" or normalized_path.startswith(
            "generated_content/"
        ):
            return os.path.join(os.path.dirname(__file__), normalized_path)

        return os.path.join(
            os.path.dirname(__file__),
            "generated_content",
            normalized_path.lstrip("./"),
        )

    def downloadYouTubeVideo(video_url, path):

        yt = YouTube(video_url)
        yt = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        output_path = YouTubeDownloader.resolve_output_path(path)
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
        yt.download(output_path)

    def downloadYouTubeAudio(video_url, path):

        yt = YouTube(video_url)
        yt = (
            yt.streams.filter(only_audio=True, file_extension="mp4")
            .order_by("abr")
            .desc()
            .first()
        )
        output_path = YouTubeDownloader.resolve_output_path(path)
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
        yt.download(output_path)

    def download_both(video_url, export_file_name):
        YouTubeDownloader.downloadYouTubeVideo(
            video_url,
            f"./temp_videos/{export_file_name}",
        )
        YouTubeDownloader.downloadYouTubeAudio(
            video_url,
            f"./temp_audio/{export_file_name}_audio",
        )


"""
YouTubeDownloader.download_both(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley", "Rickroll"
)
"""
