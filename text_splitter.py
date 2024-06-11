# This function is meant to split large blocks of texts that may or may not be split into paragraphs into
# smaller chunks with times assigned of how long they should stay on screen

# step 1: split each paragraph into sentences delimited by periods.
# Step 2: For each sentence determine its length of chars.
# Step 3: If adding the next sentence would keep this under the on-screen limit, combine them into 1 slide.
# Step 4: If length of a single sentence exceeds the on-screen limit, get creative, start by splitting on : ;
# Step 5: Determine length of time each slide would take to read with text to speech.
# By feeding each slide of text into text 2 speech individually, we wind up with many short audio clips so we'll know just how long they last


class TextSplitter:  # TODO: Needs tests

    # Define Global Variables
    on_screen_char_limit = 270  # = max_chars_per_line * lines on screen

    def text_splitter(list_of_paragraphs):
        final_list = []
        list_of_sentences = []
        for paragraph in list_of_paragraphs:
            list_of_sentences = TextSplitter.paragraph_splitter(paragraph)
            for i in range(len(list_of_sentences)):
                if len(list_of_sentences[i]) > TextSplitter.on_screen_char_limit:
                    split_sentences = TextSplitter.sentence_splitter(
                        list_of_sentences[i]
                    )
                    for sentence_piece in split_sentences:
                        final_list.append(sentence_piece)
                elif len(final_list) > 0:
                    if (
                        len(list_of_sentences[i]) + len(final_list[-1])
                        < TextSplitter.on_screen_char_limit
                    ):
                        final_list[-1] = (
                            f"{final_list[len(final_list) - 1]}{list_of_sentences[i]}"
                        )
                else:
                    final_list.append(list_of_sentences[i])
        return final_list

    def paragraph_splitter(paragraph):
        list_of_sentences = paragraph.split(".")
        return list_of_sentences

    def sentence_splitter(sentence):  # TODO: Needs a lot of work
        final_splits = []
        still_splitting = [sentence]
        splitting_characters = ["!", ";", ":", " "]

        for char in splitting_characters:
            for chunk in still_splitting:
                sentence_split = chunk.split(char)

            still_splitting = []

            for split in sentence_split:
                if len(split) < TextSplitter.on_screen_char_limit:
                    final_splits.append(split)
                else:
                    still_splitting.append(split)

        return final_splits
