# SFX

## Requirements

* [Python 2.7][python_2_7]
* [Python Construct >= 2.8][python_construct]

## sfx_parser.py

Extract sound from .SFX file format

### Usage

    usage: sfx_parser.py [-h] -o output_directory sfx_file
    
    sfx extract launch options
    
    positional arguments:
        sfx_file             sfxfile to extract
    
    optional arguments:
        -h, --help           show this help message and exit
        -o output_directory  Output directory

#### Extract all sounds

    > sfx_parser.py "FX22.SFX" -o out_dir
    
## Files

| Filename       | MD5                              |
| -------------- | -------------------------------- |
| FX22.SFX       | 3999135D197890CE4AAD9895112EBC91 |
| FXSCRIPT.SFX   | 6391D983DC94A976F6D20BC5C421043B |


[python_2_7]: http://www.python.org/getit/
[python_construct]: https://pypi.python.org/pypi/construct