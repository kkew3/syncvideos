# syncvideos

Play videos synchronously with automatic window placement by arranging windows in grid.

# Usage

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


## Detailed help

> Copied from `play-videos.py --help`

```plain
usage: play-videos.py [-h] [-f VIDEO] [-L NROWS NCOLS] [-l X Y] [--fps FPS]
                      [-c {rgb,gray}] [-r FILE] [-b] [-n CACHE] [-g FRAME_ID]
                      [-q]

Play videos synchronously with automatic window placement.

Keymaps
-------

    b) freeze the videos;
    c) continue playing the videos;
    g) show progress on console;
    h) show help on console;
    l) go to the earliest frame within the rewind limit;
    n) go to next frame;
    p) go to previous frame already played;
    r) go to the latest frame.

Example
-------

Play `video1' and `video1' side-by-side:

    python playvideos.py -f video1 -l 0 0 -f video2 -l 0 1;

Arrange all AVI videos in two rows:

    find . -name '*.avi' -print | python playvideos.py -f- -L 2 x

Custom frame preprocessing routine
----------------------------------

Routines can be injected at runtime by giving python files defining them.
The routines will be chained such that the result from the ith routine
will be fed as input into the (i+1)th routine. Each file defines one and
only one routine.

Each file defining a routine must contain a function named `frame_processor`
that expects no argument and returns a callable object, denoted as `fp`. The
callable object should behave the same as the following function signature:

    def fp(cl_frames: List[Tuple[Tuple[int, int], Optional[numpy.ndarray]]]) \
            -> List[Tuple[Tuple[int, int], Optional[numpy.ndarray]]]:
        ...

`cl_frames' is a list of tuples (cell_location, frame).
For example,

    [((0,0),frame1), ((0,1),frame2), ((1,0),frame3)]

means frame1 at upper left, frame2 at upper right, frame3 at lower left,
nothing (blank) at lower right. If `frame' is `None', then the cell
located at `cell_location' is empty. For example,

    [((0,0),frame1), ((0,1),frame2), ((1,0),frame3)]

is equivalent to

    [((0,0),frame1), ((0,1),frame2), ((1,0),frame3), ((1,1),None)]

The returned value is of the same format
as the input list, but does not necessarily maintain the same length.
For example, given the input list

    [((0,0),frame1), ((0,1),frame2)]

the returned list can be

    [((0,0),frame1'), ((0,1),frame2'), ((1,0),frame1), ((1,1),frame2)]

                      == End of description ==

optional arguments:
  -h, --help            show this help message and exit
  -f VIDEO, --video-file VIDEO
                        the video(s) to play at sync; or `-' to read video
                        filenames from stdin, one per line

Layout specification:
  -L NROWS NCOLS, --grid-shape NROWS NCOLS
                        the grid shape, default to 1 1, where at least one of
                        NROWS and NCOLS should be a positive integer; the one
                        that's not a positive integer will be regarded as
                        undefined dimension; this option will be ignored
                        unless `-l X Y' is not specified
  -l X Y, --location X Y
                        the ith location corresponds to the ith VIDEO

Video specification:
  --fps FPS             the frame-per-second; default to 6.0
  -c {rgb,gray}, --color {rgb,gray}
                        rgb video or gray video; default to gray

Frame processors:
  -r FILE, --routine FILE
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

# Dependencies

Developed under `Python 3.6.5`.

Python package dependency:

- `opencv-python`

Optional dependency:

- `tqdm`
