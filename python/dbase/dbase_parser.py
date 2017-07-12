import os
from construct import *
import argparse

# Built for construct >= 2.8
# Version 2.8 was released on September, 2016.
# There are significant API and implementation changes.
# Fields are now name-less and operators / >> are used to construct Structs
# and Sequences.
# Most classes were redesigned and reimplemented. You should read the
# documentation again.
if 2 <= version[0] and 8 > version[1]:
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

dbase100_cutscene_entry = Struct(
    "name"                      / String(8),
    "unk_word_01"               / Int16ul,          # Always 0 (Padding?)
    "length_subtitles"          / Int16ul,          # Zero if no subtitles
    "offset_dbase400"           / Int32ul,
    "offset_dbase400_subtitles" / Int32ul           # Zero if no subtitles
)

dbase400_subtitle = Aligned(2, Struct(
    "length_str"            / Int16ul,
    "unk_word_00"           / Int16ul,        # duration?
    "font_color"            / Int8ul,
    "string"                / String(lambda ctx: ctx.length_str - 5)
)
                            )
dbase400_subtitle_sequence = Struct(
    "dbase400_subtitle"     / GreedyRange(dbase400_subtitle),
    "end_of_subtitle"       / Const(b"\x00\x00\xff\xff")
)

# FIXME: There counts only first DBASE400 entry, but they can be more
# item_type:
# 0x00 - generic
# 0x01 - weapon
# 0x02 - characters and important info
# 0x03 - magic items (?)
# 0x04 - books, notes, letters etc.
# 0x12 - Adam Randall, protagonist
# 0x20 - coin
# 0x21 - ammo
# 0x40 - interactive items
# 0x43 - consumable or wearable items
dbase100_inventory_entry = Struct(
    "length"                    / Int16ul,
    "unk_word_01"               / Int16ul,
    "closeup_type"              / Int8ul,       # 0x00 - simple object (infinitive looping), 0x09 - play once
    "item_type"                 / Int8ul,
    "unk_byte_02"               / Int8ul,       # always 0
    "unk_byte_03"               / Int8ul,       # always 0
    "closeup_image"             / Int32ul,      # animated image in inventory
    "inventory_image"           / Int32ul,      # image in inventory
    "offset_dbase400"           / Int32ul,
    "add_length"                / Int16ul,
    "unk_byte_04"               / Int8ul,       # always 0
    "unk_byte_05"               / Int8ul,
    "unk_dword_04"              / Int32ul,
    "unk_bytes_01"              / Bytes(lambda ctx: ctx.add_length)
)

dbase100_inventory_offset = Struct(
    "offset"                    / Int32ul,
    "entry"                     / Pointer(lambda ctx: ctx.offset, dbase100_inventory_entry)
)

dbase100_opcode = Struct(
    "value"                     / BytesInteger(3, False, True),
    "command"                   / Int8ul
)

dbase100_action_entry = Struct(
    "length"                    / Int16ul,
    "unk_word_00"               / Int16ul,
    "opcodes"                   / If(lambda ctx: ctx.length != 0, Array(lambda ctx: ctx.length / 4 - 1, dbase100_opcode))
)

dbase100_action_offset = Struct(
    "offset"                    / Int32ul,
    "entry"                     / If(lambda ctx: ctx.offset != 0, Pointer(lambda ctx: ctx.offset, dbase100_action_entry))
)

dbase100_file = Struct(
    "signature"                 / Const("DBASE100"),     # + 0x00
    "filesize"                  / Int32ul,               # + 0x08
    "unk_dword_02"              / Int32ul,               # + 0x0C
    "nb_dbase100_inventory"     / Int32ul,               # + 0x10
    "dbase100_table_inventory"  / Int32ul,               # + 0x14        // offset
    "nb_dbase100_action"        / Int32ul,               # + 0x18
    "dbase100_table_action"     / Int32ul,               # + 0x1C        // offset
    "nb_dbase400_cutscene"      / Int32ul,               # + 0x20        // nb * 0x14
    "dbase400_table_cutscene"   / Int32ul,               # + 0x24        // offset
    "nb_dbase400_interface"     / Int32ul,               # + 0x28        // nb * 0x04
    "dbase400_table_interface"  / Int32ul,               # + 0x2C        // offset
    "unk_dword_11"              / Int32ul,               # + 0x30

    "dbase100_offset_inventory" / Pointer(lambda ctx: ctx.dbase100_table_inventory, Array(lambda ctx: ctx.nb_dbase100_inventory, dbase100_inventory_offset)),
    "dbase400_offset_cutscene"  / Pointer(lambda ctx: ctx.dbase400_table_cutscene, Array(lambda ctx: ctx.nb_dbase400_cutscene, dbase100_cutscene_entry)),
    "dbase400_offset_interface" / Pointer(lambda ctx: ctx.dbase400_table_interface, Array(lambda ctx: ctx.nb_dbase400_interface, Int32ul)),
    "dbase100_offset_01"        / Pointer(lambda ctx: ctx.dbase100_table_action, Array(lambda ctx: ctx.nb_dbase100_action, dbase100_action_offset))
)

dbase400_entry = Aligned(4, Struct(
    "offset_dbase500"       / Int32ul,                        # + 0x00
    "length_str"            / Int16ul,                        # + 0x04
    "font_color"            / Int16ul,                        # + 0x06
    "string"                / String(lambda ctx: ctx.length_str)  # + 0x08
)
)

dbase400_file = Struct(
    "signature"          / Const("DBASE400"),     # + 0x00
    "all"                / Array(2, dbase400_entry)
)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dbase extract launch options')
    parser.add_argument('dbase_file', action='store', default='', help='dbase file to extract')
    parser.add_argument('-o', dest='output_directory', help="Output directory", required=True, metavar='output_directory')

    args = parser.parse_args()

    stream = open(args.dbase_file)
    #dbfile = dbase400_file.parse_stream
    #print dbfile
    dbfile = dbase100_file.parse_stream(stream)
    print dbfile

    db400_file = os.path.join(os.path.dirname(args.dbase_file), "DBASE400.DAT")
    db400_stream = open(db400_file, "rb")

    for db400_offset in dbfile.dbase100_offset_inventory:
        db400_stream.seek(db400_offset.entry.offset_dbase400, 0x00)
        db400_entry = dbase400_entry.parse_stream(db400_stream)
        print "db400 inventory: " + str(db400_entry)

    for db400_offset in dbfile.dbase400_offset_cutscene:
        db400_stream.seek(db400_offset.offset_dbase400, 0x00)
        db400_entry = dbase400_entry.parse_stream(db400_stream)
        print "db400 cutscene: " + str(db400_entry)

        if db400_offset.offset_dbase400_subtitles != 0:
            db400_stream.seek(db400_offset.offset_dbase400_subtitles, 0x00)
            db400_entry = dbase400_subtitle_sequence.parse_stream(db400_stream)
            print "db400 subtitles: " + str(db400_entry)

    for db400_offset in dbfile.dbase400_offset_interface:
        db400_stream.seek(db400_offset, 0x00)
        db400_entry = dbase400_entry.parse_stream(db400_stream)
        print "db400 interface: " + str(db400_entry)

    #sfx = SFX(args.sfx_file)
    #sfx.extract_all(args.output_directory)
