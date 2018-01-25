# Daylio export to Year in Pixels

Small python tool to convert from Daylio formatted data into [Year in Pixels](http://year-in-pixels.glitch.me) formatted data.

## Usage

    python3 daylio2yearinpixels.py daylio_export.csv yearinpixels.txt

Then simply copy the contents of `yearinpixels.txt` into the Import window in [Year in Pixels](http://year-in-pixels.glitch.me).

## Requires

The script uses pandas and numpy, both of which can be installed (if not already available) with a:

    pip install --user pandas numpy


