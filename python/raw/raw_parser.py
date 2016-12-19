import os
import construct
import argparse
from PIL import Image

# Built for construct >= 2.8
# Version 2.8 was released on September, 2016.
# There are significant API and implementation changes.
# Fields are now name-less and operators / >> are used to construct Structs
# and Sequences.
# Most classes were redesigned and reimplemented. You should read the
# documentation again.
if 2 <= construct.version[0] and 8 > construct.version[1]:
    raise ValueError("Built for construct >= 2.8 only")
    
palette = [
(0x00, 0x00, 0x00),(0x00, 0x00, 0x00),(0x04, 0x44, 0x20),(0x48, 0x6C, 0x50),
(0x00, 0x50, 0x28),(0x34, 0x64, 0x40),(0x08, 0x3C, 0x1C),(0x00, 0x00, 0x00),
(0x44, 0x30, 0x30),(0x00, 0x00, 0x00),(0x3C, 0x28, 0x24),(0x00, 0x00, 0x00),
(0xBC, 0x80, 0x48),(0x00, 0x00, 0x00),(0x20, 0x10, 0x14),(0x00, 0x00, 0x00),
(0x2C, 0x80, 0x5C),(0x00, 0x00, 0x00),(0x3C, 0x2C, 0x64),(0x00, 0x00, 0x00),
(0x54, 0x2C, 0x0C),(0x00, 0x00, 0x00),(0x64, 0x78, 0x9C),(0x00, 0x00, 0x00),
(0x34, 0x88, 0x5C),(0x00, 0x00, 0x00),(0x44, 0x24, 0x10),(0x00, 0x00, 0x00),
(0x40, 0x3C, 0x38),(0x00, 0x00, 0x00),(0xDC, 0xAC, 0x84),(0x00, 0x00, 0x00),
(0xFC, 0xB0, 0x64),(0xC8, 0x8C, 0x4C),(0x94, 0x68, 0x38),(0x60, 0x44, 0x24),
(0x30, 0x20, 0x10),(0x00, 0x00, 0x00),(0xD0, 0x70, 0x30),(0xB8, 0x60, 0x28),
(0xA0, 0x54, 0x24),(0x88, 0x48, 0x1C),(0x70, 0x3C, 0x18),(0x58, 0x30, 0x10),
(0x40, 0x20, 0x0C),(0x2C, 0x14, 0x08),(0x14, 0x08, 0x04),(0x00, 0x00, 0x00),
(0xAC, 0xC4, 0xE8),(0x40, 0x2C, 0x5C),(0xB4, 0xCC, 0xF0),(0x2C, 0x24, 0x50),
(0x3C, 0x3C, 0x50),(0x1C, 0x1C, 0x28),(0x00, 0x00, 0x00),(0x70, 0x50, 0xBC),
(0x60, 0x44, 0xA4),(0x50, 0x38, 0x8C),(0x44, 0x30, 0x74),(0x34, 0x24, 0x5C),
(0x28, 0x1C, 0x44),(0x18, 0x10, 0x2C),(0x08, 0x04, 0x14),(0x00, 0x00, 0x00),
(0xFC, 0xFC, 0xFC),(0xE8, 0xE8, 0xE8),(0xD8, 0xD8, 0xD8),(0xC8, 0xC8, 0xC8),
(0xB8, 0xB8, 0xB8),(0xA4, 0xA4, 0xA4),(0x94, 0x94, 0x94),(0x84, 0x84, 0x84),
(0x74, 0x74, 0x74),(0x60, 0x60, 0x60),(0x50, 0x50, 0x50),(0x40, 0x40, 0x40),
(0x30, 0x30, 0x30),(0x1C, 0x1C, 0x1C),(0x0C, 0x0C, 0x0C),(0x00, 0x00, 0x00),
(0xBC, 0xD4, 0xF8),(0x00, 0x00, 0x00),(0x9C, 0xB8, 0xEC),(0x00, 0x00, 0x00),
(0xFC, 0xFC, 0x00),(0xE4, 0xE4, 0x00),(0xCC, 0xCC, 0x00),(0xB4, 0xB4, 0x00),
(0x9C, 0x9C, 0x00),(0x88, 0x88, 0x00),(0x70, 0x70, 0x00),(0x58, 0x58, 0x00),
(0x40, 0x40, 0x00),(0x28, 0x28, 0x00),(0x14, 0x14, 0x00),(0x00, 0x00, 0x00),
(0xFC, 0xE0, 0xBC),(0x84, 0x74, 0x64),(0xFC, 0xF0, 0xCC),(0x70, 0x68, 0x60),
(0xF4, 0xCC, 0xA0),(0x00, 0x00, 0x00),(0x00, 0x00, 0x00),(0xFC, 0x00, 0x00),
(0xDC, 0x00, 0x00),(0xBC, 0x00, 0x00),(0x9C, 0x00, 0x00),(0x7C, 0x00, 0x00),
(0x5C, 0x00, 0x00),(0x3C, 0x00, 0x00),(0x1C, 0x00, 0x00),(0x00, 0x00, 0x00),
(0xE8, 0xB8, 0x90),(0xCC, 0xA0, 0x80),(0xB4, 0x8C, 0x70),(0x98, 0x78, 0x5C),
(0x80, 0x64, 0x4C),(0x64, 0x50, 0x3C),(0x48, 0x38, 0x2C),(0x30, 0x24, 0x1C),
(0x14, 0x10, 0x0C),(0x00, 0x00, 0x00),(0xD4, 0x80, 0x6C),(0x68, 0x3C, 0x34),
(0x00, 0x00, 0x00),(0xF4, 0x54, 0x00),(0xD4, 0x48, 0x00),(0xB4, 0x3C, 0x00),
(0x94, 0x30, 0x00),(0x78, 0x28, 0x00),(0x58, 0x1C, 0x00),(0x38, 0x10, 0x00),
(0x1C, 0x04, 0x00),(0x00, 0x00, 0x00),(0x00, 0xAC, 0x5C),(0x00, 0x98, 0x50),
(0x00, 0x84, 0x44),(0x00, 0x70, 0x3C),(0x00, 0x5C, 0x30),(0x00, 0x48, 0x24),
(0x00, 0x34, 0x1C),(0x00, 0x24, 0x10),(0x00, 0x10, 0x04),(0x00, 0x00, 0x00),
(0x38, 0x1C, 0x0C),(0x38, 0x74, 0x58),(0x4C, 0x28, 0x0C),(0x2C, 0x80, 0x5C),
(0x00, 0x20, 0x34),(0x38, 0x84, 0x5C),(0x80, 0x38, 0x14),(0x34, 0x88, 0x5C),
(0xC0, 0x98, 0x7C),(0xDC, 0xAC, 0x84),(0x64, 0x38, 0x10),(0x50, 0x2C, 0x64),
(0x4C, 0x14, 0x00),(0x60, 0x3C, 0x8C),(0x3C, 0x30, 0x24),(0x58, 0x18, 0x84),
(0x54, 0x44, 0x30),(0x6C, 0x44, 0x94),(0x70, 0x5C, 0x44),(0x74, 0x4C, 0x9C),
(0x08, 0x2C, 0x18),(0x84, 0x58, 0xA4),(0x6C, 0x20, 0x00),(0x8C, 0x60, 0xB0),
(0x10, 0x08, 0x24),(0x30, 0x28, 0x50),(0x24, 0x18, 0x30),(0x38, 0x28, 0x4C),
(0x20, 0x14, 0x3C),(0x30, 0x2C, 0x48),(0x3C, 0x38, 0x3C),(0x24, 0x24, 0x24),
(0x60, 0x4C, 0x2C),(0x2C, 0x2C, 0x2C),(0x68, 0x54, 0x3C),(0x18, 0x18, 0x18),
(0x28, 0x10, 0x08),(0x78, 0x60, 0x48),(0x30, 0x18, 0x0C),(0x58, 0x48, 0x40),
(0x8C, 0x70, 0x54),(0x38, 0x2C, 0x40),(0xA4, 0x84, 0x60),(0x2C, 0x28, 0x3C),
(0x54, 0x3C, 0x28),(0x24, 0x28, 0x3C),(0x48, 0x48, 0x44),(0x3C, 0x30, 0x48),
(0x58, 0x58, 0x58),(0x3C, 0x2C, 0x44),(0x34, 0x34, 0x34),(0x50, 0xAC, 0x90),
(0x38, 0x28, 0x24),(0x34, 0x94, 0x88),(0x60, 0x24, 0x04),(0x4C, 0x9C, 0x84),
(0x50, 0x18, 0x00),(0x44, 0x34, 0x80),(0x44, 0x10, 0x00),(0x5C, 0x38, 0x98),
(0x34, 0x18, 0x0C),(0x90, 0x50, 0x24),(0x00, 0x40, 0x20),(0xB0, 0x58, 0x20),
(0x2C, 0x28, 0x44),(0x00, 0x00, 0x7C),(0x80, 0x60, 0x34),(0x80, 0x6C, 0xE4),
(0x78, 0x54, 0x28),(0x8C, 0x80, 0xE8),(0xA8, 0x74, 0x40),(0x8C, 0x9C, 0xF8),
(0xBC, 0xB8, 0xDC),(0x00, 0x00, 0x00),(0x8C, 0xAC, 0xDC),(0x00, 0x00, 0x00),
(0x80, 0xA0, 0xD4),(0x00, 0x00, 0x00),(0x70, 0x8C, 0xD0),(0x00, 0x00, 0x00),
(0x78, 0x90, 0xAC),(0x64, 0x78, 0x9C),(0x00, 0x54, 0x28),(0xA0, 0xE8, 0x54),
(0x30, 0x60, 0x34),(0x10, 0x70, 0x5C),(0x58, 0x68, 0x8C),(0x54, 0x54, 0x90),
(0x50, 0x54, 0x88),(0x54, 0x58, 0x94),(0x44, 0x44, 0x80),(0x60, 0x70, 0x8C),
(0xE8, 0x9C, 0x50),(0xF8, 0xD8, 0x00),(0x18, 0xC8, 0x5C),(0xFC, 0xE4, 0x00),
(0x50, 0xDC, 0x44),(0x14, 0x04, 0x00),(0xF8, 0xC4, 0x24),(0x00, 0x00, 0x00),
(0xE4, 0x84, 0x28),(0x00, 0x00, 0x00),(0xF4, 0x7C, 0x1C),(0x00, 0x00, 0x00),
(0xFC, 0xC8, 0x50),(0x00, 0x00, 0x00),(0xFC, 0xA8, 0x3C),(0x00, 0x00, 0x00),
(0xC0, 0x88, 0x30),(0x00, 0x00, 0x00),(0x48, 0x54, 0x68),(0x70, 0x00, 0xC8)]
    
def align_4(x):
    return ((((x) + 3) >> 2) << 2)
    
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
# RAW file
#
raw_file = construct.Struct(
    "flag"          / construct.Int16ul,
    "unk_word_00"   / construct.Int16ul,
    "width"         / construct.Int16ul,
    "height"        / construct.Int16ul,
    "data"          / construct.GreedyBytes
)

# cseg01:0002F528 66 81 7A 0E 57 52                       cmp     word ptr [edx+0Eh], 5257h
# cseg01:0002F52E 0F 85 A3 01 00 00                       jnz     loc_2F6D7
# cseg01:0002F534 66 C7 05 0C 9F 08 00 0D+                mov     error_num, 0Dh
# cseg01:0002F53D 66 83 7A 02 70                          cmp     word ptr [edx+2], 70h ; 'p
raw_file_2 = construct.Struct(
    "unk_word_00"           / construct.Int16ul,                    # + 0x00
    "version"               / construct.Int16ul,                    # + 0x02
    "ns_offset_00"          / construct.Int16ul,                    # + 0x04
    "ns_offset_01"          / construct.Int16ul,                    # + 0x06
    "ns_offset_02"          / construct.Int16ul,                    # + 0x08
    "field_A"               / construct.Int16ul,
    "field_C"               / construct.Int16ul,
    "signature"             / construct.Const("\x57\x52"),
    "field_10"              / construct.Int16ul,
    "field_12"              / construct.Int16ul,
    "field_14"              / construct.Int16ul,                    # // length
    "field_16"              / construct.Int16ul,
    "field_18"              / construct.Int16ul,
    "field_1A"              / construct.Int16ul
)

obj_00 = construct.Struct(
    "unk_field_00"           / construct.Int16ul,                    # + 0x00
    "unk_field_02"           / construct.Int16ul,                    # + 0x02
    "unk_field_04"           / construct.Int16ul,                    # + 0x04
    "index_texture_up"       / construct.Int16ul,                    # + 0x06
    "index_texture_down"     / construct.Int16ul,                    # + 0x08
    "unk_field_0A"           / construct.Int16ul,                    # + 0x0A
    "unk_field_0C"           / construct.Int8ul,                     # + 0x0C
    "unk_field_0D"           / construct.Int8ul,                     # + 0x0D
    "offset_2_obj_XX"        / construct.Int16ul,                    # + 0x0E       // offset absolute
    "unk_field_10"           / construct.Int16ul,                    # + 0x10
    "unk_field_12"           / construct.Int16ul,                    # + 0x12
    "unk_field_14"           / construct.Int16ul,                    # + 0x14
    "unk_field_16"           / construct.Int16ul,                    # + 0x16
    "unk_field_18"           / construct.Int16ul,                    # + 0x18
)

obj_01 = construct.Struct(
    "unk_field_00"           / construct.Int16ul,                    # + 0x00
    "unk_field_02"           / construct.Int16ul,                    # + 0x02
    "unk_field_04"           / construct.Int16ul,                    # + 0x04
    "offset_2_obj_00"        / construct.Int16ul,                    # + 0x06
    "unk_field_08"           / construct.Int16ul,                    # + 0x08
    "unk_field_0A"           / construct.Int16ul,                    # + 0x0A
)

fu_obj_XX = construct.Struct(
    "offset_obj_01"          / construct.Int16ul,                    # + 0x00       // offset relatif
    "offset_obj_02"          / construct.Int16ul,                    # + 0x02       // offset relatif
    "unk_field_04"           / construct.Int16ul,                    # + 0x04
    "offset_obj_00"          / construct.Int16ul,                    # + 0x06
    "unk_field_08"           / construct.Int16ul,                    # + 0x08
    "NS_flag"                / construct.Int16ul,                    # + 0x0A
)

def uncomp(buf, size):
    res_buf = ""
    pos = 0x00
    while size > 0:
        while True:
            if size == 0:
                return res_buf
            r = buf[pos : pos+1]
            pos = pos + 1
            if ord(r) >= 0xF1:
                break
            res_buf += r
            size = size - 1
        nb = (ord(r) + 0x10) & 0xFF
        res_buf += ((buf[pos:pos + 1]) * nb)
        pos = pos + 1
        size = size - nb
    return res_buf
    
class RawF:
    def __init__(self, filename):
        self.stream = open(filename, "rb")
        #self.raw_file = raw_file.parse_stream(self.stream)
        self.raw_file = raw_file_2.parse_stream(self.stream)
        
    def extract_it(self, outfile):
        pixels = uncomp(self.raw_file.data, self.raw_file.width * self.raw_file.height)
        img_data = ""
        for i in xrange(0, len(pixels)):
            img_data += chr(palette[ord(pixels[i])][0]) + chr(palette[ord(pixels[i])][1]) + chr(palette[ord(pixels[i])][2])
        i = Image.frombuffer("RGB", (self.raw_file.width, self.raw_file.height), img_data)
        i = i.transpose(Image.FLIP_TOP_BOTTOM)
        i.save(outfile)
    
obj_ns_off_01 = construct.Struct(
    "offset_obj_01"          / construct.Int16ul,                    # + 0x00       // offset relatif
    "offset_obj_02"          / construct.Int16ul,                    # + 0x02       // offset relatif
    "unk_field_04"           / construct.Int16ul,                    # + 0x04
    "offset_obj_00"          / construct.Int16ul,                    # + 0x06
    "unk_field_08"           / construct.Int16ul,                    # + 0x08
    "NS_flag"                / construct.Int16ul,                    # + 0x0A
)

obj_vec = construct.Struct(
    "unk_field_00"           / construct.Int16ul,                    # + 0x00
    "unk_field_02"           / construct.Int16ul,                    # + 0x02
    "unk_field_04"           / construct.Int16ul,                    # + 0x04
    "unk_field_06"           / construct.Int16ul,                    # + 0x06
    "position_X"             / construct.Int16ul,                    # + 0x08
    "position_Y"             / construct.Int16ul,                    # + 0x0A
)

def get_z1_z2(stream, offset):
    saved = stream.tell()
    stream.seek(offset, 0x00)
    obj = obj_00.parse(stream.read(0x1A))
    stream.seek(saved, 0x00)
    return obj.unk_field_00, obj.unk_field_02

def get_obj_vec(rawf, offset):
    saved = rawf.stream.tell()
    rawf.stream.seek(offset, 0x00)
    obj = obj_vec.parse_stream(rawf.stream)
    rawf.stream.seek(saved, 0x00)
    return (obj.position_X, obj.position_Y)

def get_obj_off_01(rawf, offset):
    saved = rawf.stream.tell()
    rawf.stream.seek(offset, 0x00)
    obj = obj_ns_off_01.parse_stream(rawf.stream)
    x_1, y_1 = get_obj_vec(rawf, rawf.raw_file.unk_word_00 + obj.offset_obj_01)
    x_2, y_2 = get_obj_vec(rawf, rawf.raw_file.unk_word_00 + obj.offset_obj_02)
    z_1, z_2 = get_z1_z2(rawf.stream, obj.offset_obj_00)
    rawf.stream.seek(saved, 0x00)
    return x_1, y_1, x_2, y_2, z_1, z_2

def test_magic(rawf):
    fobj = None
    print "#" * 20
    print "#" * 20
    print "#" * 20
    print ""
    print "[+] Entering test_magic"
    rawf.stream.seek(rawf.raw_file.ns_offset_01, 0x00)
    buf = rawf.stream.read(rawf.raw_file.ns_offset_02 - rawf.raw_file.ns_offset_01 - 0x02)
    actual_v = 1
    fd_out = open("test3.obj", "wb")
    for i in xrange(0, len(buf), 0x0C):
        fobj_ns_off_01 = obj_ns_off_01.parse(buf[i:i+0x0C])
        print "[+] Current offset in buf : 0x%04X, in file : 0x%04X" % (i, i + rawf.raw_file.ns_offset_01)
        
        if fobj_ns_off_01.unk_field_08 != 0xFFFF:
            continue

        print "[NS_OFFSET_01] offset_obj_01        : 0x%04X (%d)" % (fobj_ns_off_01.offset_obj_01, fobj_ns_off_01.offset_obj_01)
        rawf.stream.seek(rawf.raw_file.unk_word_00 + fobj_ns_off_01.offset_obj_01)
        robj_00 = obj_vec.parse(rawf.stream.read(0x0C))
        print "    unk_field_00         : 0x%04X (%d)" % (robj_00.unk_field_00, robj_00.unk_field_00)
        print "    unk_field_02         : 0x%04X (%d)" % (robj_00.unk_field_02, robj_00.unk_field_02)
        print "    unk_field_04         : 0x%04X (%d)" % (robj_00.unk_field_04, robj_00.unk_field_04)
        print "    unk_field_06         : 0x%04X (%d)" % (robj_00.unk_field_06, robj_00.unk_field_06)
        print "    position_X           : 0x%04X (%d)" % (robj_00.position_X, robj_00.position_X)
        print "    position_Y           : 0x%04X (%d)" % (robj_00.position_Y, robj_00.position_Y)
        
        print "[NS_OFFSET_01] offset_obj_02        : 0x%04X (%d)" % (fobj_ns_off_01.offset_obj_02, fobj_ns_off_01.offset_obj_02)
        rawf.stream.seek(rawf.raw_file.unk_word_00 + fobj_ns_off_01.offset_obj_02)
        robj = obj_vec.parse(rawf.stream.read(0x0C))
        print "    unk_field_00         : 0x%04X (%d)" % (robj.unk_field_00, robj.unk_field_00)
        print "    unk_field_02         : 0x%04X (%d)" % (robj.unk_field_02, robj.unk_field_02)
        print "    unk_field_04         : 0x%04X (%d)" % (robj.unk_field_04, robj.unk_field_04)
        print "    unk_field_06         : 0x%04X (%d)" % (robj.unk_field_06, robj.unk_field_06)
        print "    position_X           : 0x%04X (%d)" % (robj.position_X, robj.position_X)
        print "    position_Y           : 0x%04X (%d)" % (robj.position_Y, robj.position_Y)
        
        z1, z2 = get_z1_z2(rawf.stream, fobj_ns_off_01.offset_obj_00)
        
        print "[NS_OFFSET_01] unk_field_04         : 0x%04X (%d)" % (fobj_ns_off_01.unk_field_04, fobj_ns_off_01.unk_field_04)
        # TODO FIX 0x0A + 0x4 if & 0x80
        rawf.stream.seek(fobj_ns_off_01.unk_field_04)
        robj4 = fu_obj_2.parse(rawf.stream.read(0x0C))
        print "            unk_field_00         : 0x%04X (%05d)" % (robj4.unk_field_00, robj4.unk_field_00)
        print "            unk_field_02         : 0x%04X (%05d)       # index texture ?" % (robj4.unk_field_02, robj4.unk_field_02)               # INDEX TEXTURE
        print "            unk_field_04         : 0x%04X (%05d)" % (robj4.unk_field_04, robj4.unk_field_04)
        print "            unk_field_06         : 0x%04X (%05d)       # index texture ?" % (robj4.unk_field_06, robj4.unk_field_06)               # INDEX TEXTURE
        print "            unk_field_08         : 0x%04X (%05d)       # Stretching ?" % (robj4.unk_field_08, robj4.unk_field_08)                  # Stretching ?
        print "            unk_field_0A         : 0x%04X (%05d)" % (robj4.unk_field_0A, robj4.unk_field_0A)
        
        
        print "[NS_OFFSET_01] offset_obj_00        : 0x%04X (%d)" % (fobj_ns_off_01.offset_obj_00, fobj_ns_off_01.offset_obj_00)
        print "[NS_OFFSET_01] unk_field_08         : 0x%04X (%d)      # NS_OFFSET_01 offset?" % (fobj_ns_off_01.unk_field_08, fobj_ns_off_01.unk_field_08)
        print "[NS_OFFSET_01] NS_flag              : 0x%04X (%d)" % (fobj_ns_off_01.NS_flag, fobj_ns_off_01.NS_flag)
        
        #if not (robj_00.position_X >= 0xF000 and robj_00.position_X <= 0xF180 or robj.position_X >= 0xF000 and robj.position_X <= 0xF180):
        #    continue
        
        #if fobj_ns_off_01.unk_field_08 != 0xFFFF:
        #    x_1, y_1, x_2, y_2, z_1, z_2 = get_obj_off_01(rawf, fobj_ns_off_01.unk_field_08)
        #    
        #    fd_out.write("v %f %f %f\n" % (float(robj_00.position_X) / 100., float(robj_00.position_Y) / 100., float(z1) / 100.))  # - 8
        #    fd_out.write("v %f %f %f\n" % (float(robj.position_X) / 100., float(robj.position_Y) / 100., float(z1) / 100.))        # - 7
        #    fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
        #    actual_v += 2
        #    fd_out.write("v %f %f %f\n" % (float(robj_00.position_X) / 100., float(robj_00.position_Y) / 100., float(z2) / 100.))  # - 6
        #    fd_out.write("v %f %f %f\n" % (float(robj.position_X) / 100., float(robj.position_Y) / 100., float(z2) / 100.))        # - 5
        #    fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
        #    actual_v += 2
        #    fd_out.write("v %f %f %f\n" % (float(x_1) / 100., float(y_1) / 100., float(z_1) / 100.))                               # - 4
        #    fd_out.write("v %f %f %f\n" % (float(x_2) / 100., float(y_2) / 100., float(z_1) / 100.))                               # - 3
        #    fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
        #    actual_v += 2
        #    fd_out.write("v %f %f %f\n" % (float(x_1) / 100., float(y_1) / 100., float(z_2) / 100.))                               # - 2
        #    fd_out.write("v %f %f %f\n" % (float(x_2) / 100., float(y_2) / 100., float(z_2) / 100.))                               # - 1
        #    fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
        #    actual_v += 2
        #    
        #    #fd_out.write("l %d %d\n" % (actual_v - 8, actual_v - 4))
        #    #fd_out.write("l %d %d\n" % (actual_v - 7, actual_v - 3))
        #    #fd_out.write("l %d %d\n" % (actual_v - 6, actual_v - 2))
        #    #fd_out.write("l %d %d\n" % (actual_v - 5, actual_v - 1))
            
        if fobj_ns_off_01.unk_field_08 == 0xFFFF:
            fd_out.write("v %f %f %f\n" % (float(robj_00.position_X) / 100., float(robj_00.position_Y) / 100., float(z1) / 100.))  # - 4
            fd_out.write("v %f %f %f\n" % (float(robj.position_X) / 100., float(robj.position_Y) / 100., float(z1) / 100.))        # - 3
            fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
            actual_v += 2
            fd_out.write("v %f %f %f\n" % (float(robj_00.position_X) / 100., float(robj_00.position_Y) / 100., float(z2) / 100.))  # - 2
            fd_out.write("v %f %f %f\n" % (float(robj.position_X) / 100., float(robj.position_Y) / 100., float(z2) / 100.))        # - 1
            fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
            actual_v += 2

        print "-" * 20
    fd_out.close()
    exit(0)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='raw extract launch options')
    parser.add_argument('raw_file', action='store', default='', help='raw file to extract')
    parser.add_argument('-o', dest='output_file', help="Output file", required=True, metavar='output_file')
    
    args = parser.parse_args()
    
    rawf = RawF(args.raw_file)
    print rawf.raw_file
    
    print "unk_word_00      : 0x%04X" % rawf.raw_file.unk_word_00
    print "version          : 0x%04X" % rawf.raw_file.version
    print "ns_offset_00     : 0x%04X" % rawf.raw_file.ns_offset_00      # sizeof (obj) == 0x1A
    print "ns_offset_01     : 0x%04X" % rawf.raw_file.ns_offset_01      # sizeof (obj) == 0x0C
    print "ns_offset_02     : 0x%04X" % rawf.raw_file.ns_offset_02
    print "field_A          : 0x%04X" % rawf.raw_file.field_A
    print "field_C          : 0x%04X" % rawf.raw_file.field_C
    print "field_10         : 0x%04X" % rawf.raw_file.field_10
    print "field_12         : 0x%04X" % rawf.raw_file.field_12
    print "field_14         : 0x%04X" % rawf.raw_file.field_14
    print "field_16         : 0x%04X" % rawf.raw_file.field_16
    print "field_18         : 0x%04X" % rawf.raw_file.field_18
    print "field_1A         : 0x%04X" % rawf.raw_file.field_1A
    
    print "field_12 + field_1A : 0x%04X" % (rawf.raw_file.field_12 + rawf.raw_file.field_1A)
    
    total = 0x1C + (rawf.raw_file.field_12 + rawf.raw_file.field_1A) + rawf.raw_file.field_16 + rawf.raw_file.field_18
    
    print "total : 0x%04X" % total
    
    
    t = (rawf.raw_file.unk_word_00 + rawf.raw_file.field_12 + rawf.raw_file.field_14 + rawf.raw_file.field_16 + rawf.raw_file.field_1A + rawf.raw_file.field_18)
    
    print "total : 0x%04X" % (t)
    
    # SECOND READ!
    t2 = (rawf.raw_file.unk_word_00 + rawf.raw_file.field_12 + rawf.raw_file.field_14 + rawf.raw_file.field_1A) - 0x1C
    print "total : 0x%04X" % (t2)
    
    #rawf.stream.seek(0x1C, 0x00)
    #buf = rawf.stream.read(t2)
    #print hexdump(buf)
    
    fd_out = open("test_2.obj", "wb")
    
    actual_v = 1
    
    rawf.stream.seek(rawf.raw_file.ns_offset_00, 0x00)
    buf = rawf.stream.read(rawf.raw_file.ns_offset_01 - rawf.raw_file.ns_offset_00 - 0x02)
    for i in xrange(0, len(buf), 0x1A):
        print hexdump(buf[i:i+0x1A], 0x1A)
        obj = obj_00.parse(buf[i:i+0x1A])
        #print obj
        
        print "[MM] Current offset in file : 0x%04X" % (rawf.raw_file.ns_offset_00 + i)
        
        print "    unk_field_00       : 0x%04X (%d)" % (obj.unk_field_00, obj.unk_field_00)
        print "    unk_field_02       : 0x%04X (%d)" % (obj.unk_field_02, obj.unk_field_02)
        print "    unk_field_04       : 0x%04X (%d)" % (obj.unk_field_04, obj.unk_field_04)
        print "    index_texture_up   : 0x%04X (%d)" % (obj.index_texture_up, obj.index_texture_up)
        print "    index_texture_down : 0x%04X (%d)" % (obj.index_texture_down, obj.index_texture_down)
        print "    unk_field_0A       : 0x%04X (%d)" % (obj.unk_field_0A, obj.unk_field_0A)
        print "    unk_field_0C       : 0x%02X (%d)" % (obj.unk_field_0C, obj.unk_field_0C)
        print "    unk_field_0D       : 0x%02X (%d)" % (obj.unk_field_0D, obj.unk_field_0D)
        print "    offset_2_obj_XX    : 0x%04X (%d)" % (obj.offset_2_obj_XX, obj.offset_2_obj_XX)
        
        rawf.stream.seek(obj.offset_2_obj_XX)
        obj1 = obj_01.parse(rawf.stream.read(0x0C))
        
        fu_obj = construct.Struct(
            "unk_field_00"           / construct.Int16ul,                    # + 0x00       // offset relatif
            "unk_field_02"           / construct.Int16ul,                    # + 0x02
            "unk_field_04"           / construct.Int16ul,                    # + 0x04
            "unk_field_06"           / construct.Int16ul,                    # + 0x06
            "position_X"             / construct.Int16ul,                    # + 0x08
            "position_Y"           / construct.Int16ul,                      # + 0x0A
        )
        
        fu_obj_2 = construct.Struct(
            "unk_field_00"           / construct.Int16ul,                    # + 0x00
            "unk_field_02"           / construct.Int16ul,                    # + 0x02
            "unk_field_04"           / construct.Int16ul,                    # + 0x04
            "unk_field_06"           / construct.Int16ul,                    # + 0x06
            "unk_field_08"           / construct.Int16ul,                    # + 0x08
            "unk_field_0A"           / construct.Int16ul,                    # + 0x0A
        )
        
        print "        unk_field_00         : 0x%04X (%d)" % (obj1.unk_field_00, obj1.unk_field_00)
        rawf.stream.seek(rawf.raw_file.unk_word_00 + obj1.unk_field_00)
        fobj = fu_obj.parse(rawf.stream.read(0x0C))
        print "            unk_field_00         : 0x%04X (%d)" % (fobj.unk_field_00, fobj.unk_field_00)
        print "            unk_field_02         : 0x%04X (%d)" % (fobj.unk_field_02, fobj.unk_field_02)
        print "            unk_field_04         : 0x%04X (%d)" % (fobj.unk_field_04, fobj.unk_field_04)
        print "            unk_field_06         : 0x%04X (%d)" % (fobj.unk_field_06, fobj.unk_field_06)
        print "            position_X           : 0x%04X (%d)" % (fobj.position_X, fobj.position_X)
        print "            position_Y           : 0x%04X (%d)" % (fobj.position_Y, fobj.position_Y)
        fd_out.write("v %f %f %f\n" % (float(fobj.position_X) / 100., float(fobj.position_Y) / 100., 0x00))
        print "        unk_field_02         : 0x%04X (%d)" % (obj1.unk_field_02, obj1.unk_field_02)
        rawf.stream.seek(rawf.raw_file.unk_word_00 + obj1.unk_field_02)
        fobj = fu_obj.parse(rawf.stream.read(0x0C))
        print "            unk_field_00         : 0x%04X (%d)" % (fobj.unk_field_00, fobj.unk_field_00)
        print "            unk_field_02         : 0x%04X (%d)" % (fobj.unk_field_02, fobj.unk_field_02)
        print "            unk_field_04         : 0x%04X (%d)" % (fobj.unk_field_04, fobj.unk_field_04)
        print "            unk_field_06         : 0x%04X (%d)" % (fobj.unk_field_06, fobj.unk_field_06)
        print "            position_X           : 0x%04X (%d)" % (fobj.position_X, fobj.position_X)
        print "            position_Y           : 0x%04X (%d)" % (fobj.position_Y, fobj.position_Y)
        fd_out.write("v %f %f %f\n" % (float(fobj.position_X) / 100., float(fobj.position_Y) / 100., 0x00))
        print "        unk_field_04         : 0x%04X (%d)" % (obj1.unk_field_04, obj1.unk_field_04)
        
        fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
        actual_v += 2
        
        # TODO FIX
        rawf.stream.seek(obj1.unk_field_04)
        fobj = fu_obj_2.parse(rawf.stream.read(0x0C))
        print "            unk_field_00         : 0x%04X (%d)" % (fobj.unk_field_00, fobj.unk_field_00)
        print "            unk_field_02         : 0x%04X (%d)" % (fobj.unk_field_02, fobj.unk_field_02)
        print "            unk_field_04         : 0x%04X (%d)" % (fobj.unk_field_04, fobj.unk_field_04)
        print "            unk_field_06         : 0x%04X (%d)" % (fobj.unk_field_06, fobj.unk_field_06)
        print "            unk_field_08         : 0x%04X (%d)" % (fobj.unk_field_08, fobj.unk_field_08)
        #print "            unk_field_0A         : 0x%04X (%d)" % (fobj.unk_field_0A, fobj.unk_field_0A)
        print "        offset_2_obj_00      : 0x%04X (%d)" % (obj1.offset_2_obj_00, obj1.offset_2_obj_00)
        print "        unk_field_08         : 0x%04X (%d)" % (obj1.unk_field_08, obj1.unk_field_08)
        print "        unk_field_0A         : 0x%08X (%d)" % (obj1.unk_field_0A, obj1.unk_field_0A)
        
        print "    unk_field_10         : 0x%04X (%d)" % (obj.unk_field_10, obj.unk_field_10)
        print "    unk_field_12         : 0x%04X (%d)" % (obj.unk_field_12, obj.unk_field_12)
        print "    unk_field_14         : 0x%04X (%d)" % (obj.unk_field_14, obj.unk_field_14)
        print "    unk_field_16         : 0x%04X (%d)" % (obj.unk_field_16, obj.unk_field_16)
        print "    unk_field_18         : 0x%04X (%d)" % (obj.unk_field_18, obj.unk_field_18)
        
        
        #print hexdump()
        #print "-" * 20
        
        
        
        # .. 0x06 [WORD]
        # .. 0x08 [WORD]
        # .. 0x0D [BYTE]
        # .. 0x0E [WORD] : OFFSET !?
        # ..
        # .. 0x14 [WORD] : NS_ID
        # .. 0x16 [WORD] : ???? &= 0xFBu;
        # .. 0x18 [WORD] : OFFSET !?
    fd_out.close()
    #exit(0)
    print "-" * 20
    
    rawf.stream.seek(rawf.raw_file.ns_offset_01, 0x00)
    buf = rawf.stream.read(rawf.raw_file.ns_offset_02 - rawf.raw_file.ns_offset_01 - 0x02)
    
    actual_v = 1
    
    fd_out = open("test.obj", "wb")
    
    for i in xrange(0, len(buf), 0x0C):
        #print hexdump(buf[i:i+0x0C], 0x0C)
        print "[+] Current offset in file : 0x%04X | 0x%04X" % (i, i + rawf.raw_file.ns_offset_01)
        fobj = fu_obj_XX.parse(buf[i:i+0x0C])
        print "[NNNS_OFFSET_01] offset_obj_01        : 0x%04X (%d)" % (fobj.offset_obj_01, fobj.offset_obj_01)
        rawf.stream.seek(rawf.raw_file.unk_word_00 + fobj.offset_obj_01)
        robj_00 = fu_obj.parse(rawf.stream.read(0x0C))
        print "    unk_field_00         : 0x%04X (%d)" % (robj_00.unk_field_00, robj_00.unk_field_00)
        print "    unk_field_02         : 0x%04X (%d)" % (robj_00.unk_field_02, robj_00.unk_field_02)
        print "    unk_field_04         : 0x%04X (%d)" % (robj_00.unk_field_04, robj_00.unk_field_04)
        print "    unk_field_06         : 0x%04X (%d)" % (robj_00.unk_field_06, robj_00.unk_field_06)
        print "    position_X           : 0x%04X (%d)" % (robj_00.position_X, robj_00.position_X)
        print "    position_Y           : 0x%04X (%d)" % (robj_00.position_Y, robj_00.position_Y)
        
        print "[NNNS_OFFSET_01] offset_obj_02        : 0x%04X (%d)" % (fobj.offset_obj_02, fobj.offset_obj_02)
        rawf.stream.seek(rawf.raw_file.unk_word_00 + fobj.offset_obj_02)
        robj = fu_obj.parse(rawf.stream.read(0x0C))
        print "    unk_field_00         : 0x%04X (%d)" % (robj.unk_field_00, robj.unk_field_00)
        print "    unk_field_02         : 0x%04X (%d)" % (robj.unk_field_02, robj.unk_field_02)
        print "    unk_field_04         : 0x%04X (%d)" % (robj.unk_field_04, robj.unk_field_04)
        print "    unk_field_06         : 0x%04X (%d)" % (robj.unk_field_06, robj.unk_field_06)
        print "    position_X           : 0x%04X (%d)" % (robj.position_X, robj.position_X)
        print "    position_Y           : 0x%04X (%d)" % (robj.position_Y, robj.position_Y)
        
        z1, z2 = get_z1_z2(rawf.stream, fobj.offset_obj_00)
        
        #if not(robj_00.position_X >= 0xF000 and robj_00.position_X <= 0xF180 or robj.position_X >= 0xF000 and robj.position_X <= 0xF180):
        #if (robj_00.position_X >= 0xF000 and robj_00.position_X <= 0xF180 or robj.position_X >= 0xF000 and robj.position_X <= 0xF180):
        #    #continue
        fd_out.write("v %f %f %f\n" % (float(robj_00.position_X) / 100., float(robj_00.position_Y) / 100., float(z1) / 100.))
        fd_out.write("v %f %f %f\n" % (float(robj.position_X) / 100., float(robj.position_Y) / 100., float(z1) / 100.))
        fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
        actual_v += 2
        fd_out.write("v %f %f %f\n" % (float(robj_00.position_X) / 100., float(robj_00.position_Y) / 100., float(z2) / 100.))
        fd_out.write("v %f %f %f\n" % (float(robj.position_X) / 100., float(robj.position_Y) / 100., float(z2) / 100.))
        fd_out.write("l %d %d\n" % (actual_v, actual_v + 1))
        actual_v += 2
        
        #fd_out.write("f %d %d %d %d\n" % (actual_v - 4, actual_v - 2, actual_v - 1, actual_v - 3))
        
        print "[NNNS_OFFSET_01] unk_field_04         : 0x%04X (%d)" % (fobj.unk_field_04, fobj.unk_field_04)
        # TODO FIX 0x0A + 0x4 if & 0x80
        rawf.stream.seek(fobj.unk_field_04)
        robj4 = fu_obj_2.parse(rawf.stream.read(0x0C))
        print "            unk_field_00         : 0x%04X (%05d)" % (robj4.unk_field_00, robj4.unk_field_00)
        print "            unk_field_02         : 0x%04X (%05d)       # index texture ?" % (robj4.unk_field_02, robj4.unk_field_02)               # INDEX TEXTURE
        print "            unk_field_04         : 0x%04X (%05d)" % (robj4.unk_field_04, robj4.unk_field_04)
        print "            unk_field_06         : 0x%04X (%05d)       # index texture ?" % (robj4.unk_field_06, robj4.unk_field_06)               # INDEX TEXTURE
        print "            unk_field_08         : 0x%04X (%05d)       # Stretching ?" % (robj4.unk_field_08, robj4.unk_field_08)                  # Stretching ?
        print "            unk_field_0A         : 0x%04X (%05d)" % (robj4.unk_field_0A, robj4.unk_field_0A)
        
        
        print "[NNNS_OFFSET_01] offset_obj_00        : 0x%04X (%d)" % (fobj.offset_obj_00, fobj.offset_obj_00)
        print "[NNNS_OFFSET_01] unk_field_08         : 0x%04X (%d)      # NS_OFFSET_01 offset?" % (fobj.unk_field_08, fobj.unk_field_08)
        print "[NNNS_OFFSET_01] NS_flag              : 0x%04X (%d)" % (fobj.NS_flag, fobj.NS_flag)
        
        print "-" * 80
        
        # + 0x00 [WORD] 
        # + 0x02 [WORD]
        # + 0x04 [WORD] : NS_ID ?!
        # ..
        # + 0x0A [BYTE] : ???
    
    fd_out.close()
    
    print "-" * 20
    
    test_magic(rawf)
    exit(0)
    
    rawf.stream.seek(rawf.raw_file.ns_offset_02, 0x00)
    buf = rawf.stream.read(rawf.raw_file.field_A - rawf.raw_file.ns_offset_02 - 0x02)
    i = 0
    pos = 0
    while pos < len(buf):
        if ord(buf[pos + 1:pos + 2]) & 0x80 != 0:
            print hexdump(buf[pos:pos+0x0A+0x04])
            pos = pos + 0x0A + 4
        else:
            print hexdump(buf[pos:pos+0x0A])
            pos = pos + 0x0A
        i = i + 1
    print "i : %X" % i
    
    
    obj_unk_00 = construct.Struct(
        "unk_field_00"           / construct.Int16ul,                    # + 0x00
        "unk_field_02"           / construct.Int16ul,                    # + 0x02
        "unk_field_04"           / construct.Int16ul,                    # + 0x04
        "unk_field_06"           / construct.Int16ul,                    # + 0x06
        "entries"                / construct.Array(lambda ctx: ctx.unk_field_06,
            construct.Struct(
                "unk_field_00"           / construct.Int16ul,                    # + 0x00
                "unk_field_02"           / construct.Int16ul,                    # + 0x02
                "unk_field_04"           / construct.Int16ul,                    # + 0x04
                "unk_field_06"           / construct.Int16ul,                    # + 0x06
                "unk_field_08"           / construct.Int16ul,                    # + 0x08
                "unk_field_0A"           / construct.Int16ul,                    # + 0x0A
            )
        )
    )
    
    rawf.stream.seek(rawf.raw_file.field_C, 0x00)
    o = obj_unk_00.parse_stream(rawf.stream)
    print o
    
    # unk_word_00      : 0x18C4
    # field_12         : 0x024C
    # field_14         : 0x0614
    # field_16         : 0x026A
    # field_18         : 0x0008
    # field_1A         : 0x04BC
    rawf.stream.seek(rawf.raw_file.unk_word_00 + rawf.raw_file.field_14, 0x00)
    #b = rawf.stream.read(rawf.raw_file.field_1A)
    
    obj_unk_01 = construct.Struct(
        "unk_field_00"           / construct.Int16ul,                    # + 0x00
        "unk_field_02"           / construct.Int16ul,                    # + 0x02
        "unk_offset_00"          / construct.Int16ul,                    # + 0x04
        "unk_nb_00"              / construct.Int16ul,                    # + 0x06
        
        "unk_offset_01"          / construct.Int16ul,                    # + 0x08
        "unk_nb_01"              / construct.Int16ul,                    # + 0x0A
        
        "unk_offset_02"          / construct.Int16ul,                    # + 0x0C
        "unk_nb_02"              / construct.Int16ul,                    # + 0x0E
       
        "unk_offset_03"          / construct.Int16ul,                    # + 0x10
        "unk_nb_03"              / construct.Int16ul,                    # + 0x12
        
        "unk_offset_04"          / construct.Int16ul,                    # + 0x14
        "unk_nb_04"              / construct.Int16ul,                    # + 0x16
        
        "unk_offset_05"          / construct.Int16ul,                    # + 0x18
        "unk_nb_05"              / construct.Int16ul,                    # + 0x1A
        
        "unk_offset_06"          / construct.Int16ul,                    # + 0x1C
        "unk_nb_06"              / construct.Int16ul,                    # + 0x1E
        
        "unk_offset_07"          / construct.Int16ul,                    # + 0x20
        "unk_nb_07"              / construct.Int16ul,                    # + 0x22
        
        "unk_offset_08"          / construct.Int16ul,                    # + 0x24
        "unk_nb_08"              / construct.Int16ul,                    # + 0x26
        
        "unk_offset_09"          / construct.Int16ul,                    # + 0x28
        "unk_nb_09"              / construct.Int16ul,                    # + 0x2A
        
        "unk_offset_10"          / construct.Int16ul,                    # + 0x2C
        "unk_nb_10"              / construct.Int16ul,                    # + 0x2E
        
        "unk_offset_11"          / construct.Int16ul,                    # + 0x30
        "unk_nb_11"              / construct.Int16ul,                    # + 0x32
        
        "unk_offset_12"          / construct.Int16ul,                    # + 0x34
        "unk_nb_12"              / construct.Int16ul,                    # + 0x36
        
        "unk_offset_13"          / construct.Int16ul,                    # + 0x38
        "unk_nb_13"              / construct.Int16ul,                    # + 0x3A
        
        "unk_offset_14"          / construct.Int16ul,                    # + 0x3C
        "unk_nb_14"              / construct.Int16ul,                    # + 0x3E
        
        "entries"                / construct.OnDemandPointer(lambda ctx: rawf.raw_file.unk_word_00 + rawf.raw_file.field_14 + ctx.unk_offset_00,
            construct.Array(lambda ctx: ctx.unk_nb_00,
                construct.Struct(
                    "length"     / construct.Int16ul,
                    "data"       / construct.String(lambda ctx: ctx.length - 0x02)
                )
            )
        )
    )
    o = obj_unk_01.parse_stream(rawf.stream)
    print o
    
    import struct
    for entry in o.entries():
        #print hexdump(struct.pack("<H", entry.length) + entry.data, 0x20)
        print hexdump(entry.data, 0x20)
        
        # /!\ SIZE BEFORE
        # + 0x00 : ????
        # + 0x01 : TYPE 
        #
        
        # Type
        #   - 0x1B          : FIELD_08 => WORD
        #   - 0x30          : FIELD_08 => WORD
        #   - 0x39          : FIELD_08 => WORD
        
    
    #for i in xrange(0, len(buf), 0x0C):
    #    print hexdump(buf[i:i+0x0C], 0x0C)
        
        # + 0x00
        # + 0x01        // flag if & 0x80 sizeof == 0x0E => 0x0A + 0x04
        
    # THIRD READ!
    #t3 = t2 + rawf.raw_file.field_16
    #print "total : 0x%04X" % (t3)
    #
    #buf = rawf.stream.read(rawf.raw_file.field_16)
    #print hexdump(buf)
    #
    ## THIRD READ!
    #t4 = t3 + rawf.raw_file.field_18
    #print "total : 0x%04X" % (t4)
    #
    #buf = rawf.stream.read(rawf.raw_file.field_18)
    #print hexdump(buf)
    
    #rawf.extract_it(args.output_file)