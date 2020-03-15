# coding=utf8
from Tuner import Tuner, openStream
from music import Note
from argparse import Namespace

flags = Namespace(
    lowest_note=Note.C(2),   # До контроктавы
    highest_note=Note.C(8),  # До четвёртой октавы
    rate=44100,
)


def main():
    stream = openStream(flags.rate)
    tuner = Tuner(stream=stream,
                  rate=flags.rate,
                  lowest=flags.lowest_note,
                  highest=flags.highest_note)
    tuner.exec()


if __name__ == '__main__':
    main()
