# syncvideos

Play videos synchronously with automatic window placement by arranging windows in grid.

# Usage

## Command line argument

```plain
usage: play-videos.py [-h] [-f VIDEO] [-l X Y] [--fps FPS] [-c {rgb,gray}]
                      [-r ROUTINE] [-b] [-n CACHE] [-g FRAME_ID] [-q]

Play videos synchronously with automatic window placement. Keymaps: b) freeze
the videos; c) continue playing the videos; g) show progress on console; h)
show help on console; l) go to the earliest frame within the rewind limit; n)
go to next frame; p) go to previous frame already played; r) go to the latest
frame. Example: 1. python playvideos.py -f video1 -l 0 0 -f video2 -l 0 1; 2.
find python playvideos.py -f - -l 2 x;

optional arguments:
  -h, --help            show this help message and exit
  -f VIDEO, --video-file VIDEO
                        the video(s) to play at sync; or "-" to read video
                        filenames from stdin, one per line
  -l X Y, --location X Y
                        the ith location corresponds to the ith VIDEO; if
                        VIDEO is specified as a single '-', then the first X Y
                        pair will be interpreted as the grid dimension NROWS
                        NCOLS, where at least one of the NROWS NCOLS must be
                        integer, and 'X' is interpreted as undefined dimension

Video specification:
  --fps FPS             the frame-per-second; default to 6.0
  -c {rgb,gray}, --color {rgb,gray}
                        rgb video or gray video

Frame processors:
  -r ROUTINE, --routine ROUTINE
                        file that defines a custom frame processor

Runtime behavior:
  -b, --freeze-once-start
                        to freeze the videos once started
  -n CACHE, --cache-size CACHE
                        how many number of frames the video player is able to
                        rewind; should be no less than 1; default to 100.
                        There is a limit because the program cache last CACHE
                        frames on the run. The reason why ffmpeg backend is
                        not used because it is not reliable (see
                        https://github.com/opencv/opencv/issues/9053).
  -g FRAME_ID, --goto FRAME_ID
                        Start the videos at frame FRAME_ID
  -q, --quiet
```

Example:

Start `video1` and `video2` at the 100th frame (0-indexed), and have the two videos side-by-side:

```bash
play-videos.py -f video1 -l 0 0 -f video2 -l 0 1 -g100
```

Start a number of videos arranged in two columns and played in grayscale:

```bash
find . -name '*.avi' -print | play-videos.py -f- -l X 2 -c gray
```


## Runtime keymaps

- **b**: freeze the videos;
- **c**: continue playing the videos;
- **g**: show progress on console;
- **h**: show help on console;
- **l**: go to the earliest frame within the rewind limit;
- **n**: go to next frame;
- **p**: go to previous frame;
- **r**: go to the latest frame.

To interact using above keymaps, the window focus should be on one of the opencv video windows rather than the console.

# Dependency

Developed under `Python 3.6.5`.

Python package dependencies:

- `opencv-python`
