import argparse
from PIL import Image
from construct import *

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

# Built for construct >= 2.8
# Version 2.8 was released on September, 2016.
# There are significant API and implementation changes.
# Fields are now name-less and operators / >> are used to construct Structs
# and Sequences.
# Most classes were redesigned and reimplemented. You should read the
# documentation again.
if 2 <= version[0] and 8 > version[1]:
    raise ValueError("Built for construct >= 2.8 only")

struct_00_s = "struct_00" / Struct(
    "value" / Int16ul,
)

default_struct_s = "default_struct" / Struct(
    "value" / Int16ul,
)

buffer_s = Struct(
    "length"    / Int16ul,
    "data"      / OnDemand(Bytes(lambda ctx: ctx.length))
)

screenshot_s = Struct(
    "length"            / Int16ul,
    "unk_dword_00"      / Int32ul,
    "width"             / Int16ul,
    "height"            / Int16ul,
    "data"              / OnDemand(Bytes(lambda ctx: ctx.length - 0x08)),
)

map_name_s = Struct(
    "length"    / Int16ul,
    "data"      / Bytes(lambda ctx: ctx.length)
)

tmp_name_s = Struct(
    "length"    / Int16ul,
    "data"      / Bytes(lambda ctx: ctx.length)
)

player_s = Struct(
    "pos_x"             / Int32sl,      # + 0x00
    "pos_z"             / Int32sl,      # + 0x04
    "pos_y"             / Int32sl,      # + 0x08
    "unk_word_00"       / Int16ul,      # + 0x0C    direction ?
    "unk_word_01"       / Int16ul,      # + 0x0E    direction ?
    "index_left_hand"   / Int32ul,      # + 0x10
    "index_right_hand"  / Int32ul,      # + 0x14
    "health_point"      / Int32ul,      # + 0x18
    "camera_tilt"       / Int32sl,      # + 0x1C
    "unk_dword_07"      / Int32ul,      # + 0x20
    "unk_dword_08"      / Int32ul,      # + 0x24
    "unk_word_02"       / Int16ul,      # + 0x28
    "unk_word_03"       / Int16ul,      # + 0x2A
    "unk_dword_10"      / Int32ul,      # + 0x2C
)

player_inventory_s = Struct(
    "length"    / Int16ul,
    "items"     / Array(lambda ctx: ctx.length / 0x04,
        Struct(
            "id"                / Int16ul,
            "quantity"          / Int16ul,
        )),
)

#
# type entry
#
"""
SAVE ENTRY by type
"""
save_entry_s = Struct(
    "type"              / Int16ul,
    "data"              / Switch(this.type,
        {
            #
            # 0x01 -> Value stored on a WORD ; if Value >= 3 all files present 
            # in folder "tmp\\*.tmp" will be deleted
            #
            0x01 : Int16ul,
            #
            # 0x02
            #
            0x02 : buffer_s,
            #
            # 0x03 -> Contains current savegame's map location
            #
            0x03 : map_name_s,
            #
            # 0x04
            #
            0x04 : buffer_s,
            #
            # 0x05
            #
            0x05 : buffer_s,
            #
            # 0x06
            #
            0x06 : buffer_s,
            #
            # 0x07 -> Player inventory
            #
            0x07 : player_inventory_s,
            #
            # 0x08
            #
            0x08 : tmp_name_s,
            #
            # 0x09
            #
            0x09 : buffer_s,
            #
            # 0x0A -> Contains savegame's name
            #
            0x0A : buffer_s,
            #
            # 0x0B -> Contains savegame's screenshot
            #
            0x0B : screenshot_s,
            #
            # 0x0C
            #
            0x0C : Pass,
            #
            # 0x0D
            #
            0x0D : buffer_s,
            #
            # 0x0E
            #
            0x0E : buffer_s,
        },
    ),
)

#
# SAVE file
#
save_file_s = Struct(
    "entries"           / GreedyRange(save_entry_s),
)

class SaveFile:
    def __init__(self, filename):
        self.stream = open(filename, "rb")
        self.save_file_c = save_file_s.parse_stream(self.stream)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SAVE extract launch options')
    parser.add_argument('save_file', action='store', default='', help='SAVE file to extract')
    parser.add_argument('-o', dest='output_directory', help="Output directory", required=False, metavar='output_directory')

    args = parser.parse_args()

    savef = SaveFile(args.save_file)
    #print savef.save_file_c
    
    
    for entr in savef.save_file_c.entries:
        if entr.type == 0x02:
            print hexdump(entr.data.data())
            print player_s.parse(entr.data.data())
        #if entr.type == 0x07:
        #    print entr.data
            
            
    #save8 = SaveFile("SAVE8.SAV")
    #save9 = SaveFile("SAVE9.SAV")
    #
    #f = [x for x in save8.save_file_c.entries if x.type == 0x02][0]
    #s = [x for x in save9.save_file_c.entries if x.type == 0x02][0]
    #diffhexdump(f.data.data(), s.data.data())