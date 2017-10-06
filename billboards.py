#!/usr/bin/env python3

debug = False


def print_debug(*args):
    """Only print if in debug mode"""

    if debug:
        print(*args)


def try_layout(w, h, text, size):
    """Tries to layout the text in rectangle, using text size"""

    # List of lines of text
    layout = []

    for i, word in enumerate(text.split(" ")):
        # Initialize first line with first word
        if i == 0:
            layout = [word]
        # Check if we can add a new word on current line
        elif (len(layout[-1]) + len(word) + 1) * size <= w:
            layout[-1] += " " + word
        else:
            # Start new line
            layout.append(word)

    return layout


def max_font_size(w, h, text):
    """Find max font size for given box size and text"""

    # Size has to be smaller than width and height
    size = min(w, h)
    # Try decreasing font sizes until text fits in rectangle
    while size > 0:
        print_debug("\nTrying size of", size)
        layout = try_layout(w, h, text, size)

        for line in layout:
            print_debug(line)

        max_char = max(len(line) for line in layout)

        if max_char * size > w:
            # If lines are still too big, compress characters to fit
            size = w // max_char
        elif len(layout) * size > h:
            # Otherwise just keep decreasing
            size -= 1
        else:
            # We found a working solution
            break

    return size


def process_file(filename):
    """
    Read a text file formatted as described,
    finds max font size for each line, and prints it
    """
    try:
        with open(filename) as f:
            lines = f.readlines()
            try:
                num_tests = int(lines[0])
                assert len(lines) >= num_tests + 1, "not enough lines"
                for i, line in enumerate(lines[1:num_tests+1]):
                    # Python 3 syntactic sugar
                    width, height, *text = line.split(" ")
                    width = int(width)
                    height = int(height)
                    text = ' '.join(text)
                    size = max_font_size(width, height, text)
                    print("Case #{}: {}".format(i+1, size))
            except (IndexError, ValueError, AssertionError) as e:
                print("Badly formatted file:", e)
    except EnvironmentError as e:
        print("Cannot open file:", e)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("Usage: billboards.py [filename]")
