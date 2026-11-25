"""Emit a single remembered sentence to a chosen destination.

This little program has exactly one job: place one specific
sentence into a file, byte for byte, with no extra newline
tacked onto the end.  Everything else here exists only to
make sure that job is done carefully.
"""

import os
import sys

# The sentence is assembled from a pair of fragments so the
# wording stays easy to proof-read in the source.  Joined
# together they form the complete statement.
FRAGMENT_A = "Nine years I swept this shop's floor before the keys were mine; "
FRAGMENT_B = "the broom still hangs by the door, and I dust it like a trophy."
SENTENCE = FRAGMENT_A + FRAGMENT_B

# Where the sentence lands when the caller supplies nothing.
FALLBACK_TARGET = "/output/entry.txt"


def check_sentence(text):
    """Refuse to proceed unless *text* fits the one-line rules.

    Each rule gets its own check so a failure message points at
    the exact problem instead of lumping the rules together.
    """
    for marker, label in (("\n", "newline"), ("\r", "carriage return")):
        assert marker not in text, (
            "sentence must occupy a single line, "
            "but it contains a %s character" % label
        )
    assert len(text) >= 1, "sentence must not be empty"
    assert len(text) <= 200, (
        "sentence is %d characters long, over the 200 character limit"
        % len(text)
    )


def destination_from_args(arguments):
    """Pick the output path: first argument wins, otherwise the fallback."""
    if len(arguments) > 1:
        return arguments[1]
    return FALLBACK_TARGET


def store_sentence(target, text):
    """Write *text* to *target*, creating folders and fixing the mode."""
    folder = os.path.dirname(os.path.abspath(target))
    if folder and not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)

    # Binary mode keeps the bytes exactly as given; nothing is
    # translated and no terminator is appended by this code.
    handle = open(target, "wb")
    try:
        handle.write(text.encode("utf-8"))
    finally:
        handle.close()

    # The reader may be a different account, so grant explicit
    # read access for everyone while keeping write access private.
    os.chmod(target, 0o644)


def run():
    check_sentence(SENTENCE)
    store_sentence(destination_from_args(sys.argv), SENTENCE)


if __name__ == "__main__":
    run()
