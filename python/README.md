# Open Realms of the Haunting tools (python)

## Requirements

* [Python 2.7][python_2_7]
* [Python Construct >= 2.8][python_construct]

## gdv_parser.py

Extract audio and video from **G**remlin **D**igital **V**ideo file format.

| Decoder        | Status |
|----------------|--------|
| 0              | TODO   |
| 1              | TODO   |
| 3              | TODO   |
| 6              | TODO   |
| 8              | DONE   |

### Usage

    usage: gdv_parser.py [-h] [-o output_file] [-d] [-i] [-a] [-f] [-p] gdv_file
    
    gdv extract launch options
    
    positional arguments:
    gdv_file        gdv file to extract
    
    optional arguments:
    -h, --help      show this help message and exit
    -o output_file  Output WAV file
    -d              Enable debugging output
    -i              Print file information
    -a              Extract audio
    -f              Extract frames
    -p              Prefix PNG frame name

#### Extract audio

    gdv_parser.py -a -o out.wav HAWK02B.GDV
    
#### Extract all frames 

All frames will be extracted one by one to `DUMP_FRAME_<FILENAME>_XXXX.PNG`

    gdv_parser.py -f HAWK02B.GDV

[python_2_7]: http://www.python.org/getit/
[python_construct]: https://pypi.python.org/pypi/construct