# fbro

`fbro` is an interactive console file browser for AWS S3.

## Installation

```bash
pip install fbro
```

Please note that this tool will not work on Windows, because Windows does not support curses.


## Usage

You can start it with `fbro`. Then a list of all your AWS S3 buckets will be
shown. You can use the arrow keys (<kbd>↑</kbd> / <kbd>↓</kbd>) and select one
by going to the <kbd>→</kbd>. You can go back by pressing <kbd>←</kbd>.

```
s3://martin-thoma/
- enzado/
- correlation.jpg
- testfile.txt
```
