import os
import construct
import argparse
import wave

# Built for construct >= 2.8
# Version 2.8 was released on September, 2016.
# There are significant API and implementation changes.
# Fields are now name-less and operators / >> are used to construct Structs
# and Sequences.
# Most classes were redesigned and reimplemented. You should read the
# documentation again.
if 2 <= construct.version[0] and 8 > construct.version[1]:
    raise ValueError("Built for construct >= 2.8 only")

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

def createdir(dirname):
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)

#
# SFX filename & description
#
sfx_file_desc = construct.Struct(
    "id"                    / construct.Int16ul,
    "name"                  / construct.CString(encoding="utf8"),
    "description"           / construct.CString(encoding="utf8"),
)

#
#
#
sfx_file_entry = construct.Struct(
    "offset"                / construct.Int32ul,            # + 0x00
    "length"                / construct.Int32ul,            # + 0x04
    "unk_word_00"           / construct.Int16ul,            # + 0x08
    "unk_word_01"           / construct.Int16ul,            # + 0x0A
    construct.OnDemandPointer(lambda ctx: ctx.offset, "data"    / construct.String(lambda ctx: ctx.length))
)

#
# SFX file
#
sfx_file = construct.Struct(
    "signature"             / construct.Const("\x30\x58\x46\x53"),  # + 0x00
    "NS_version"            / construct.Int32ul,                    # + 0x04
    "offset_file_table"     / construct.Int32ul,                    # + 0x08
    "total_length_data"     / construct.Int32ul,                    # + 0x0C
    "length_file_table"     / construct.Int32ul,                    # + 0x10
    "offset_string_table"   / construct.Int32ul,                    # + 0x14
    "length_string_table"   / construct.Int32ul,                    # + 0x18
    "entry_table"           / construct.OnDemandPointer(lambda ctx: ctx.offset_file_table,
        construct.Array(lambda ctx: ctx.length_file_table / 0x0C, sfx_file_entry)),
    "string_table"          / construct.OnDemandPointer(lambda ctx: ctx.offset_string_table,
        construct.Array(lambda ctx: ctx.length_file_table / 0x0C, sfx_file_desc))
)

class SFX:
    def __init__(self, filename):
        self.stream = open(filename, "rb")
        self.sfx_file = sfx_file.parse_stream(self.stream)

    def extract_index(self, index):
        if index >= len(self.sfx_file.entry_table()):
            return ""
        entry = self.sfx_file.entry_table()[index]
        return entry.data()

    def extract_all(self, outdir):
        createdir(outdir)
        for nb, entry in enumerate(self.sfx_file.entry_table()):
            audio_data = entry.data()
            wave_output = wave.open(outdir + "/" + sfx.sfx_file.string_table()[nb].name + ".wav", "wb")
            # TODO add comment to wave
            wave_output.setparams((1, 2, 11025, 0, 'NONE', 'not compressed'))
            for i in xrange(0, len(audio_data), 2):
                wave_output.writeframes(audio_data[i:i+2])
            wave_output.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sfx extract launch options')
    parser.add_argument('sfx_file', action='store', default='', help='sfxfile to extract')
    parser.add_argument('-o', dest='output_directory', help="Output directory", required=True, metavar='output_directory')

    args = parser.parse_args()

    sfx = SFX(args.sfx_file)
    sfx.extract_all(args.output_directory)