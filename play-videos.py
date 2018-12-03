#!/usr/bin/env python
import argparse
import itertools
import sys
import collections
import re

import cv2


__description__ = '''
Play videos synchronously with automatic window placement.

Keymap:

    b) freeze the videos;
    c) continue playing the videos;
    g) show progress on console;
    h) show help on console;
    l) go to the earliest frame within the rewind limit;
    n) go to next frame;
    p) go to previous frame;
    r) go to the latest frame.
'''

_description = re.sub(r'[^\n ]\+', ' ', __description__)


def make_parser():
    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument('videos', metavar='VIDEO', nargs='+')
    parser.add_argument('--fps', type=float, default=6.0,
                        help='the frame-per-second; default to %(default)s')
    parser.add_argument('-c', '--color', choices=['r', 'g'], default='r',
                        help='(r)gb video or (g)ray video')
    parser.add_argument('-s', '--scale', type=float, default=1.0,
                        help='to what scale to downsample the frames')
    parser.add_argument('--hw', '--frame-size', dest='hw', nargs=2, type=int,
                        default=(480, 704), metavar=('HEIGHT', 'WIDTH'),
                        help='height and width of the videos; '
                             'default to %(default)s')
    parser.add_argument('-b', '--freeze-once-start', dest='freeze_once_start',
                        action='store_true',
                        help='to freeze the videos once started')
    parser.add_argument('-n', '--cache-size', type=int, default=10,
                        dest='cache',
                        help='how many number of frames the video player is '
                             'able to rewind; should be no less than 1; '
                             'default to %(default)s. '
                             'There is a limit because the '
                             'program cache last CACHE frames on the run. The '
                             'reason why ffmpeg backend is not used because '
                             'it is not reliable (see '
                             'https://github.com/opencv/opencv/issues/9053).')
    return parser


def window_placement(n, size, nrows=None, ncols=None, zero=(0, 0)):
    w0, h0 = zero
    w, h = size
    if nrows is None:
        nrows = int(n / ncols + 0.5)
    else:
        ncols = int(n / nrows + 0.5)
    locations = []
    for k in range(n):
        i, j = k // ncols, k % ncols
        locations.append((h0 + h * i, w0 + w * j))
    return locations


def proc_frame(scale: float, rgb: bool, frame):
    if not rgb:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (0, 0), fx=1./scale, fy=1./scale)
    return frame


def get_frameno(cap):
    return int(cap.get(cv2.CAP_PROP_POS_FRAMES))


def play_video(filenames, fps: float, scale: float, rgb: bool,
               cache_size: int, frame_hw, freeze_once_start):
    T = int(1000 / fps)
    _caps = list(map(cv2.VideoCapture, filenames))
    open_failures = [i for i in range(len(_caps))
                     if not _caps[i].isOpened()]
    filename_caps = [(f, c) for i, (f, c) in enumerate(zip(filenames, _caps))
                     if i not in open_failures]
    window_locations = window_placement(len(filename_caps), tuple(frame_hw),
                                        nrows=2, zero=(0, 100))
    cache = collections.deque(maxlen=max(1, cache_size))

    try:
        for l, (f, _) in zip(window_locations, filename_caps):
            cv2.namedWindow(f)
            cv2.moveWindow(f, *l)

        frozen = False
        melting = False
        one_step_more = False
        while True:
            if not (frozen or melting) or one_step_more:
                to_show = []
                for f, c in filename_caps:
                    r, im = c.read()
                    if r:
                        im = proc_frame(scale, rgb, im)
                        to_show.append((f, im))
                for f, im in to_show:
                    cv2.imshow(f, im)
                cache.append(tuple(to_show))
            elif frozen and not one_step_more:
                for f, im in cache[rewind]:
                    cv2.imshow(f, im)
            elif not frozen and melting:
                rewind += 1
                print('melting: {}'.format(rewind))
                for f, im in cache[rewind]:
                    cv2.imshow(f, im)
                if rewind == -1:
                    melting = False
                    del rewind
            one_step_more = False

            if freeze_once_start:
                freeze_once_start = False
                frozen = True
                rewind = -1
            key = (cv2.waitKey(T) & 0xFF)
            if key == ord('q'):
                break
            elif key == ord('b'):
                if frozen:
                    print('Already frozen')
                else:
                    frozen = True
                    if not melting:
                        rewind = -1
            elif key == ord('n'):
                if not frozen:
                    print('Press `b\' to freeze the frame first')
                else:
                    if rewind + 1 >= 0:
                        print('One step more')
                        one_step_more = True
                    else:
                        rewind += 1
            elif key == ord('r'):
                if not frozen:
                    print('Press `b\' to freeze the frame first')
                else:
                    if rewind + 1 >= 0:
                        print('Already at the latest frame')
                    else:
                        rewind = -1
            elif key == ord('p'):
                if not frozen:
                    print('Press `b\' to freeze the frame first')
                else:
                    if rewind == -len(cache):
                        print('Cannot rewind anymore')
                    else:
                        rewind -= 1
            elif key == ord('l'):
                if not frozen:
                    print('Press `b\' to freeze the frame first')
                else:
                    if rewind == -len(cache):
                        print('Already at the earliest frame')
                    else:
                        rewind = -len(cache)
            elif key == ord('c'):
                frozen = False
                try:
                    if rewind < -1:
                        melting = True
                    else:
                        del rewind
                except NameError:
                    pass
            elif key == ord('h'):
                print(__description__.strip())
            elif key == ord('g'):
                print('|'.join(map(
                    str, iter(get_frameno(c)
                              for _, c in filename_caps))))
    finally:
        for c in iter(x[1] for x in filename_caps):
            c.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    args = make_parser().parse_args()
    if (len(args.videos) == 1 and args.videos[0] == '-'
            and not sys.stdin.isatty()):
        args.videos = list(map(str.strip, sys.stdin.readlines()))
    play_video(args.videos, args.fps, args.scale, args.color == 'r',
               args.cache, args.hw, args.freeze_once_start)
