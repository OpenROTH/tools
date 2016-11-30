import os
import construct
import argparse
import re
import wave
import struct

#
# > strings.exe DBASE500.DAT | grep "WAVEfmt " | wc -l
# 1467 ; 0x5bb
#

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
    
def align_8(x):
    return (((x) + 8 - 1) & ~(8 - 1))
    
def createdir(dirname):
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)
    
def compute_delta_modulation():
    delta_table = []
    delta_table.append(0)
    delta = 0
    code = 0x40
    step = 0x2D
    for i in xrange(0, 256 - 2, 2):
        delta = delta + (code >> 5)
        code = code + step
        step = step + 2
        delta_table.append(delta)
        delta_table.append((-delta) & 0xFFFFFFFF)
    delta_table.append((delta + (code >> 5)))
    return delta_table

dbase500_entry = construct.Struct(
    "chunk_id"                  / construct.Const("FFIR"),                                                  # + 0x00
    "chunk_length"              / construct.Int32ul,                                                        # + 0x04
    "format"                    / construct.Const("WAVE"),                                                  # + 0x08
    "sub_chunk_1_id"            / construct.Const("fmt "),                                                  # + 0x0C
    "sub_chunk_1_size"          / construct.Int32ul,                                                        # + 0x10
    "audio_format"              / construct.Int16ul,                                                        # + 0x14
    "num_channel"               / construct.Int16ul,                                                        # + 0x16
    "sample_rate"               / construct.Int32ul,                                                        # + 0x18
    "byte_rate"                 / construct.Int32ul,                                                        # + 0x1C
    "block_align"               / construct.Int16ul,                                                        # + 0x20
    "bit_per_sample"            / construct.Int16ul,                                                        # + 0x22
    "sub_chunk_2_id"            / construct.Const("data"),                                                  # + 0x24
    "sub_chunk_2_size"          / construct.Int32ul,                                                        # + 0x28
    "data"                      / construct.OnDemand(construct.String(lambda ctx: ctx.sub_chunk_2_size)),   # + 0x2C
    construct.Padding(lambda ctx: align_8(ctx.sub_chunk_2_size + 0x2C) - (ctx.sub_chunk_2_size + 0x2C)),
)

dbase500_file = construct.Struct(
    "signature"                  / construct.Const("DBASE500"),                                             # + 0x00
    "entries"                    / construct.GreedyRange(dbase500_entry)
)

class DBase500:
    def __init__(self, filename):
        self.stream = open(filename, "rb")
        self.db500_file = dbase500_file.parse_stream(self.stream)
        self.table_delta_mod = compute_delta_modulation()

    def get_nb_entry(self):
        return len(self.db500_file.entries)
        
    def extract_index(self, index, filename):
        if index >= len(self.db500_file.entries):
            return ""
        self.extract_audio(self.db500_file.entries[index])
            
    def extract_offset(self, offset, filename):
        saved = self.stream.tell()
        self.stream.seek(offset, 0x00)
        entry = dbase500_entry.parse_stream(self.stream)
        self.stream.seek(saved)
        self.extract_audio(entry)
            
    def extract_audio(self, entry, filename):
        audio_data = entry.data()
        wave_output = wave.open(filename, "wb")
        wave_output.setparams((entry.num_channel, 2, entry.sample_rate, 0, 'NONE', 'not compressed'))
        state = 0x00
        for i in xrange(0, len(audio_data)):
            state = (state + self.table_delta_mod[ord(audio_data[i])])
            wave_output.writeframes(struct.pack("<H", state & 0xFFFF))
        wave_output.close()
        
    def extract_all(self, outdir):
        createdir(outdir)
        for nb, entry in enumerate(self.db500_file.entries):
            self.extract_audio(entry, outdir + "/" + str(nb) + ".wav")

    def print_dbase500_info(off=None, dd=None):
        if off == None and dd == None:
            print "| %-25s | %-20s | %-20s | %-20s | %-20s | %-20s | %-20s |" % ("OFFSET", "AUDIO FORMAT", "NUM CHANNEL", "SAMPLE RATE", "BYTE RATE", "LENGTH DATA", "DURATION")
            print "| %-25s | %-20s | %-20s | %-20s | %-20s | %-20s | %-20s |" % ("-" * 25, "-" * 20, "-" * 20, "-" * 20, "-" * 20, "-" * 20, "-" * 20)
        else:
            duration = dd.sub_chunk_2_size / float(dd.sample_rate * dd.num_channel * dd.bit_per_sample / 8)
            print "| %-25s | %-20s | %-20s | %-20s | %-20s | %-20s | %-20s |" % ("0x%08X (%d)" % (off, off), "0x%08X (%d)" % (dd.audio_format, dd.audio_format), "0x%08X (%d)" % (dd.num_channel, dd.num_channel), "0x%08X (%d)" % (dd.sample_rate, dd.sample_rate), "0x%08X (%d)" % (dd.byte_rate, dd.byte_rate), "0x%08X (%d)" % (dd.sub_chunk_2_size, dd.sub_chunk_2_size), str(duration))

def check_dbase500():
    fd = open("DBASE500.DAT", "rb")
    buf = fd.read()
    total_length = 0x08 # SIGNATURE
    for off in [m.start() for m in re.finditer('WAVEfmt ', buf)]:
        fd.seek(off - 0x08, 0x00)
        dentry = dbase500_entry.parse_stream(fd)
        total_length += align_8(0x2C + dentry.sub_chunk_2_size)
    if os.path.getsize("DBASE500.DAT") != total_length:
        raise ValueError("[-] DBASE500 not entirely parsed!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dbase500 extract launch options')
    parser.add_argument('dbase_file', action='store', default='', help='dbase500 file to extract')
    parser.add_argument('-o', dest='output_directory', help="Output directory", required=True, metavar='output_directory')
    args = parser.parse_args()
    
    db = DBase500(args.dbase_file)
    db.extract_all(args.output_directory)