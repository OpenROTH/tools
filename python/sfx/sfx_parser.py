import os
import argparse
import wave
from construct import *

import sys
sys.path.append(os.path.abspath(__file__ + "\..\.."))
from utils import hexdump, createdir

# Built for construct >= 2.8
# Version 2.8 was released on September, 2016.
# There are significant API and implementation changes.
# Fields are now name-less and operators / >> are used to construct Structs
# and Sequences.
# Most classes were redesigned and reimplemented. You should read the
# documentation again.
if 2 <= version[0] and 8 > version[1]:
    raise ValueError("Built for construct >= 2.8 only")

#
# SFX filename & description
#
sfx_file_desc_s = Struct(
    "id"                    / Int16ul,
    "name"                  / CString(encoding="utf8"),
    "description"           / CString(encoding="utf8"),
)

#
#
#
sfx_file_entry_s = Struct(
    "offset"                / Int32ul,            # + 0x00
    "length"                / Int32ul,            # + 0x04
    "id"                    / Int16ul,            # + 0x08
    "unk_word_01"           / Int16ul,            # + 0x0A
    OnDemandPointer(lambda ctx: ctx.offset, "data" / Bytes(lambda ctx: ctx.length))
)

#
# SFX file
#
sfx_file_s = Struct(
    "signature"             / Const("\x30\x58\x46\x53"),  # + 0x00
    "NS_version"            / Int32ul,                    # + 0x04
    "offset_file_table"     / Int32ul,                    # + 0x08
    "total_length_data"     / Int32ul,                    # + 0x0C
    "length_file_table"     / Int32ul,                    # + 0x10
    "offset_string_table"   / Int32ul,                    # + 0x14
    "length_string_table"   / Int32ul,                    # + 0x18
    "entry_table"           / OnDemandPointer(lambda ctx: ctx.offset_file_table,
        Array(lambda ctx: ctx.length_file_table / 0x0C, sfx_file_entry_s)),
    "string_table"          / OnDemandPointer(lambda ctx: ctx.offset_string_table,
        Array(lambda ctx: ctx.length_file_table / 0x0C, sfx_file_desc_s))
)

class SFXFile:
    def __init__(self, filename):
        self.stream = open(filename, "rb")
        self.sfx_file_c = sfx_file_s.parse_stream(self.stream)

    def extract_index(self, index):
        if index >= len(self.sfx_file_c.entry_table()):
            return ""
        entry = self.sfx_file_c.entry_table()[index]
        return entry.data()

    def extract_all(self, outdir):
        createdir(outdir)
        for nb, entry in enumerate(self.sfx_file_c.entry_table()):
            audio_data = entry.data()
            wave_output = wave.open(outdir + "/" + self.sfx_file_c.string_table()[nb].name + ".wav", "wb")
            # TODO add comment to wave
            wave_output.setparams((1, 2, 11025, 0, 'NONE', 'not compressed'))
            for i in xrange(0, len(audio_data), 2):
                wave_output.writeframes(audio_data[i:i + 2])
            wave_output.close()
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sfx extract launch options')
    parser.add_argument('sfx_file', action='store', default='', help='sfxfile to extract')
    parser.add_argument('-o', dest='output_directory', help="Output directory", required=True, metavar='output_directory')

    args = parser.parse_args()

    sfx = SFXFile(args.sfx_file)
    sfx.extract_all(args.output_directory)