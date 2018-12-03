# syncvideos

Play videos synchronously with automatic window placement by arranging windows in grid.

# Usage

## Command line argument

```plain
usage: play-videos.py [-h] [--fps FPS] [-c {r,g}] [-s SCALE]
                      [--hw HEIGHT WIDTH] [-b] [-n CACHE]
                      VIDEO [VIDEO ...]

Play videos synchronously with automatic window placement. Keymaps: b) freeze
the videos; c) continue playing the videos; g) show progress on console; h)
show help on console; l) go to the earliest frame within the rewind limit; n)
go to next frame; p) go to previous frame; r) go to the latest frame.

positional arguments:
  VIDEO

optional arguments:
  -h, --help            show this help message and exit
  --fps FPS             the frame-per-second; default to 6.0
  -c {r,g}, --color {r,g}
                        (r)gb video or (g)ray video
  -s SCALE, --scale SCALE
                        to what scale to downsample the frames
  --hw HEIGHT WIDTH, --frame-size HEIGHT WIDTH
                        height and width of the videos; default to (480, 704)
  -b, --freeze-once-start
                        to freeze the videos once started
  -n CACHE, --cache-size CACHE
                        how many number of frames the video player is able to
                        rewind; should be no less than 1; default to 10. There
                        is a limit because the program cache last CACHE frames
                        on the run. The reason why ffmpeg backend is not used
                        because it is not reliable (see
                        https://github.com/opencv/opencv/issues/9053).
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
