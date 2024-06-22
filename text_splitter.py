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
    on_screen_char_limit = 180  # = max_chars_per_line (30) * (lines on screen (7) - 1)

    def text_splitter(list_of_paragraphs):
        final_list = []
        final_list_no_empty_strings = []
        for paragraph in list_of_paragraphs:
            if len(paragraph) > TextSplitter.on_screen_char_limit:
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
                            final_list[-1] = f"{final_list[-1]} {list_of_sentences[i]}"
                        else:
                            final_list.append(list_of_sentences[i])
                    else:
                        final_list.append(list_of_sentences[i])
            else:
                final_list.append(paragraph)
        for final in final_list:
            if len(final) > 1:
                final_list_no_empty_strings.append(final)
        return final_list_no_empty_strings

    def paragraph_splitter(paragraph):
        list_of_sentences = paragraph.split(".")
        for i in range(len(list_of_sentences)):
            list_of_sentences[i] = f"{list_of_sentences[i]}."
        return list_of_sentences

    def sentence_splitter(sentence):  # TODO: Needs a lot of work.
        final_splits = []
        still_splitting = [sentence]
        splitting_characters = ["!", ";", ":", " "]
        still_splitting_temp = []

        for char in splitting_characters:
            if len(still_splitting) > 0:
                for chunk in still_splitting:
                    if len(chunk) > TextSplitter.on_screen_char_limit:
                        if char in chunk:
                            sentence_split = chunk.split(char)
                            for i in range(len(sentence_split)):
                                sentence_split[i] = f"{sentence_split[i]}{char}"
                            for split in sentence_split:
                                if len(split) < TextSplitter.on_screen_char_limit:
                                    final_splits.append(split)
                                else:
                                    still_splitting_temp.append(split)
                    else:  # Do we ever even hit this??
                        final_splits.append(chunk)
                still_splitting = still_splitting_temp
                still_splitting_temp = []

        return final_splits

    def lyric_text_splitter(
        list_of_lines, max_chars_per_line, max_lines_on_screen
    ):  # Key difference for lyrics is that lines are coming in instead of paragraphs
        list_of_text_pages = []  # Each element in list is a list of sentences
        curr_text_page = []
        for line in list_of_lines:
            if len(line) <= max_chars_per_line:
                if len(curr_text_page) == max_lines_on_screen:
                    list_of_text_pages.append(curr_text_page)
                    curr_text_page = []
                curr_text_page.append(line)
            else:
                split_lines = TextSplitter.sentence_splitter(line)
                if len(curr_text_page) + len(split_lines) >= max_lines_on_screen:
                    list_of_text_pages.append(curr_text_page)
                    curr_text_page = []
                for split in split_lines:
                    curr_text_page.append(split)
        if len(curr_text_page) > 0:
            list_of_text_pages.append(curr_text_page)
        return list_of_text_pages

    def test_sentence_splitter():
        test_input = [
            "Here is the first paragraph. It's made up of a few sentences, but should still be less than the on-screen limit of 190 characters.",
            "Here is a second short paragraph."
            "Here is a third short paragraph."
            "Here is the fourth paragraph and boy is it a doozy. We want this paragraph to exceed the 190 character limit set for a single page. This will help test how it splits such paragraphs. This last sentence is what will pass the limit; can't wait to see the result",
        ]
        output_generated = TextSplitter.text_splitter(test_input)
        for page_of_text in output_generated:
            print(page_of_text)
        print(len(output_generated))
        # Try testing multiple periods in a row
        # Change () to have higher importance than .
        # Check logic for paragraphs that are too large with not breaking chars getting omitted
