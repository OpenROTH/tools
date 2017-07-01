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
    "unk_dword_12"              / Int32ul,
    "dbase400_cutscene_offset"  / Int32ul,
    "unk_dword_13"              / Int32ul
)

# FIXME: There counts only first DBASE400 entry, but they can be more
dbase100_inventory_entry = Struct(
    "length"                    / Int16ul,
    "unk_byte_01"               / Int8ul,
    "unk_byte_02"               / Int8ul,
    "unk_dword_01"              / Int32ul,
    "unk_dword_02"              / Int32ul,
    "unk_dword_03"              / Int32ul,
    "dbase400_inventory_offset" / Int32ul,
    "unk_dword_04"              / Int32ul,
    "unk_bytes_01"              / Bytes(lambda ctx: ctx.length - 20)
)

dbase100_inventory_offset = Struct(
    "offset"                    / Int32ul,
    "entry"                     / Pointer(lambda ctx: ctx.offset, dbase100_inventory_entry)
)

dbase100_file = Struct(
    "signature"                 / Const("DBASE100"),     # + 0x00
    "filesize"                  / Int32ul,               # + 0x08
    "unk_dword_02"              / Int32ul,               # + 0x0C
    "nb_dbase100_inventory"     / Int32ul,               # + 0x10
    "dbase100_table_offset_inventory"   / Int32ul,       # + 0x14        // offset
    "unk_dword_05"              / Int32ul,               # + 0x18
    "ns_offset_01"              / Int32ul,               # + 0x1C        // offset
    "nb_dbase400_cutscene"      / Int32ul,               # + 0x20        // nb * 0x14
    "dbase400_table_offset_cutscene"    / Int32ul,       # + 0x24        // offset
    "nb_dbase400_interface"     / Int32ul,               # + 0x28        // nb * 0x04
    "dbase400_table_offset_interface"   / Int32ul,       # + 0x2C        // offset
    "unk_dword_11"              / Int32ul,               # + 0x30

    "dbase100_offset_inventory" / Pointer(lambda ctx: ctx.dbase100_table_offset_inventory, Array(lambda ctx: ctx.nb_dbase100_inventory, dbase100_inventory_offset)),
    "dbase400_offset_cutscene"  / OnDemandPointer(lambda ctx: ctx.dbase400_table_offset_cutscene, Array(lambda ctx: ctx.nb_dbase400_cutscene, dbase100_cutscene_entry)),
    "dbase400_offset_interface" / OnDemandPointer(lambda ctx: ctx.dbase400_table_offset_interface, Array(lambda ctx: ctx.nb_dbase400_interface, Int32ul)),
    "dbase100_offset_01"        / OnDemandPointer(lambda ctx: ctx.ns_offset_01, Array(lambda ctx: ctx.unk_dword_05, Int32ul))
)

dbase400_subtitle = Struct(
    "length"                / Int16ul,
    "unk_word_00"           / Int16ul,        # duration?
    "font_color"            / Int8ul,
    "string"                / Aligned(4, String(lambda ctx: ctx.length - 5))    # FIXME what about zero-length string?
)

dbase400_entry = Struct(
    "unk_dword_00"          / Int32ul,                        # + 0x00
    "length"                / Int16ul,                        # + 0x04
    "font_color"            / Int16ul,                        # + 0x06
    "string"                / Aligned(4, String(lambda ctx: ctx.length))  # + 0x08
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
        db400_stream.seek(db400_offset.entry.dbase400_inventory_offset, 0x00)
        db400_entry = dbase400_entry.parse_stream(db400_stream)
        print "db400 inventory: " + str(db400_entry)

    for db400_offset in dbfile.dbase400_offset_cutscene():
        db400_stream.seek(db400_offset.dbase400_cutscene_offset, 0x00)
        db400_entry = dbase400_entry.parse_stream(db400_stream)
        print "db400 cutscene: " + str(db400_entry)

    for db400_offset in dbfile.dbase400_offset_interface():
        db400_stream.seek(db400_offset, 0x00)
        db400_entry = dbase400_entry.parse_stream(db400_stream)
        print "db400 interface: " + str(db400_entry)
    
    #print "[+] unk_dword_03 : 0x%08X" % dbfile.unk_dword_03
    #print "[+] ns_offset_00 : 0x%08X" % dbfile.ns_offset_00
    #stream.seek(dbfile.ns_offset_00, 0x00)
    #print hexdump(stream.read(0x20))
    
    print "[+] unk_dword_05 : 0x%08X" % dbfile.unk_dword_05
    print "[+] ns_offset_01 : 0x%08X" % dbfile.ns_offset_01
    stream.seek(dbfile.ns_offset_01, 0x00)
    print hexdump(stream.read(0x20))
    
#    for db100_offset in dbfile.dbase100_offset_inventory():   # sizeof == +0x18
#
#        # + 0x10 // ???
#        # + 0x14 // SFX INDEX
#
#        if (db100_offset >= 0x69A0 and (db100_offset + 0x18) <= 0x69A0):
#            print hex(db100_offset)
#            print "FUUU!!"
#            exit(0)
#
#        stream.seek(db100_offset + 0x10, 0x00)
#        v = Int32ul.parse(stream.read(4))
#        db400_stream.seek(v, 0x00)
#        db400_entry = dbase400_entry.parse_stream(db400_stream)
#        print "db400 sec. stream: " + str(db400_entry)
        
    i = []
    for db100_offset in dbfile.dbase100_offset_01():   # sizeof == +0x18
        i.append(db100_offset)
        #if db100_offset == 0x00:
            #continue
        #stream.seek(db100_offset, 0x00)
        #import struct
        #v = struct.unpack("<I", stream.read(4))[0]
        #print v
        #db400_stream.seek(db100_offset, 0x00)
        #db400_entry = dbase400_entry.parse_stream(db400_stream)
        #print db400_entry
    print sorted(i)
    #stream.seek(dbfile.dbase400_table_offset, 0x00)
    #print hexdump(stream.read(0x20))
    
    #sfx = SFX(args.sfx_file)
    #sfx.extract_all(args.output_directory)
