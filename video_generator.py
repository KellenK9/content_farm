import moviepy.editor as mpy
from moviepy.video.tools.segmenting import findObjects
import moviepy.video.fx.all as vfx


class VerticalVideoMaker:

    # Set global variables
    WHITE = (255, 255, 255)
    SCREEN_SIZE = (1080, 1920)
    VERTICAL_MARGIN = 120
    FOOTER_HEIGHT = 60
    max_chars_per_line = 30

    def add_logo():
        SB_LOGO_PATH = "./static/StackBuildersLogo.jpg"

        sb_logo = (
            mpy.ImageClip(SB_LOGO_PATH).set_position(("center", 0)).resize(width=200)
        )
        return sb_logo

    def split_text_into_lines(text):
        text_lines = []
        words = text.split()
        curr_phrase = ""
        for i in range(len(words)):
            if len(f"{curr_phrase} {words[i]}") < VerticalVideoMaker.max_chars_per_line:
                if len(curr_phrase) == 0:  # Gets rid of initial space
                    curr_phrase = f"{words[i]}"
                else:
                    curr_phrase = (
                        f"{curr_phrase} {words[i]}"  # Creates space between words
                    )
                if i == len(words) - 1:
                    text_lines.append(curr_phrase)
            else:
                text_lines.append(curr_phrase)
                if (
                    i == len(words) - 1
                ):  # Covers cases where the last word gets its own line
                    text_lines.append(words[i])
                else:
                    curr_phrase = f"{words[i]}"
        return text_lines

    def add_text(text, start_time, duration):
        text_lines = VerticalVideoMaker.split_text_into_lines(text)
        text_clips = []
        vertical_line_height = 100
        for i in range(len(text_lines)):
            text = text_lines[i]
            if len(text) > 0:
                txt_clip = (
                    mpy.TextClip(
                        text,
                        font="Charter-bold",
                        color="RoyalBlue4",
                        kerning=4,
                        fontsize=60,
                    )
                    .set_position(
                        (
                            "center",
                            VerticalVideoMaker.VERTICAL_MARGIN
                            + (vertical_line_height * i),
                        )
                    )
                    .set_duration(duration)
                    .set_start(start_time)
                )
                text_clips.append(txt_clip)
        return text_clips

    def concatenate_text_clips(list_of_text_tuples):
        # Each tuple should be formatted as (text, duration)
        text_clips = []
        current_start = 0
        buffer = 0
        for text_tuple in list_of_text_tuples:
            curr_text_clips = VerticalVideoMaker.add_text(
                text_tuple[0], current_start, text_tuple[1]
            )
            for text_clip in curr_text_clips:
                text_clips.append(text_clip)
            current_start = current_start + text_tuple[1] + buffer
        return text_clips

    def import_video_clip(file_location, start_time, duration):
        clip = mpy.VideoFileClip(file_location)
        clip = clip.subclip(start_time, start_time + duration)  # clipping by seconds
        clip = clip.volumex(0.8)  # Reduce the audio volume (volume x 0.8)
        clip = clip.fx(vfx.resize, width=1080)
        clip = clip.set_position(
            (
                "center",
                VerticalVideoMaker.SCREEN_SIZE[1]
                - clip.h
                - VerticalVideoMaker.FOOTER_HEIGHT,
            )
        )
        return clip

    def import_footer(file_location):
        clip = mpy.ImageClip(file_location)
        clip = clip.fx(vfx.resize, width=1080)
        clip = clip.set_position(
            (
                "center",
                VerticalVideoMaker.SCREEN_SIZE[1] - clip.h,
            )
        )
        return clip

    def compile_video(
        video_clip, footer_clip, text_clips, compiled_audio, total_duration
    ):
        clips = [video_clip, footer_clip]
        for text_clip in text_clips:
            clips.append(text_clip)
        final_clip = (
            mpy.CompositeVideoClip(
                clips=clips,
                size=VerticalVideoMaker.SCREEN_SIZE,
            )
            .on_color(color=VerticalVideoMaker.WHITE, col_opacity=1)
            .set_duration(total_duration)
            .set_audio(compiled_audio)
        )  # .set_audio(compiled_audio)
        return final_clip

    def export_video(final_clip):
        final_clip.write_videofile("video_with_python.mp4", fps=10)

    def create_audio_clip(audio_path):
        return mpy.AudioFileClip(f"temp_audio/{audio_path}.wav")

    def concatenate_audio(audio_tuple_list):  # Each tuple is (audio clip, duration)
        audio_array = []
        curr_start_time = 0
        for i in range(len(audio_tuple_list)):
            curr = audio_tuple_list[i][0]
            audio_array.append(curr.set_start(curr_start_time))
            curr_start_time += audio_tuple_list[i][1]
        mixed = mpy.CompositeAudioClip(audio_array)
        return mixed

    def main(list_of_text_tuples):  # Each tuple should be formatted as (text, duration)
        total_duration = 0
        audio_tuples_list = []  # Each tuple is (audio clip, duration)
        for i in range(len(list_of_text_tuples)):
            total_duration += list_of_text_tuples[i][1]
            curr_clip = VerticalVideoMaker.create_audio_clip(i)
            audio_tuples_list.append((curr_clip, list_of_text_tuples[i][1]))
        compiled_audio = VerticalVideoMaker.concatenate_audio(audio_tuples_list)
        imported_video = VerticalVideoMaker.import_video_clip(
            "videos_for_import/Tom and Jerry - 002 - Midnight Snack [1941].mp4",
            35,
            total_duration,
        )
        footer_clip = VerticalVideoMaker.import_footer("temp_footer.png")
        all_text_clips = VerticalVideoMaker.concatenate_text_clips(list_of_text_tuples)
        compilation = VerticalVideoMaker.compile_video(
            imported_video, footer_clip, all_text_clips, compiled_audio, total_duration
        )
        VerticalVideoMaker.export_video(compilation)


"""
VerticalVideoMaker.main(
    [
        ("Testing Kellen's super cool bot, gosh he's a beast", 10),
        ("Watching Tom and Jerry", 10),
    ]
)
"""
