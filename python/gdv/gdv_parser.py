import os
import construct
import argparse
import wave
from PIL import Image
import struct
import StringIO

# Built for construct >= 2.8
# Version 2.8 was released on September, 2016.
# There are significant API and implementation changes.
# Fields are now name-less and operators / >> are used to construct Structs
# and Sequences.
# Most classes were redesigned and reimplemented. You should read the
# documentation again.
if 2 <= construct.version[0] and 8 > construct.version[1]:
    raise ValueError("Built for construct >= 2.8 only")

##########################
#
# HELPER
#
##########################

def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines).rstrip('\n')

#
# (playback_frequency / framerate) * (number_of_channels) * (bits_per_sample / 8) * (isCompressed + 1)
#
def get_length_audio_data(gs):
    amount = 0x00
    if gs.sound_flags.audio_present["AUDIO_NOT_PRESENT"] == True:
        return 0x00
    amount = gs.playback_frequency / gs.framerate
    if gs.sound_flags.audio_channels["STEREO"] == True:
        amount = amount + amount
    if gs.sound_flags.sample_width["BIT_16"] == True:
        amount = amount + amount
    if gs.sound_flags.audio_coding["DPCM"] == True:
        amount = amount >> 1
    return amount

#
# cseg01:0005BB62                         build_delta_table proc near
# cseg01:0005BB62 83 3D 6C 19 09 00 00      cmp     delta_table_modulation+0C8h, 0
# cseg01:0005BB69 75 45                     jnz     short locret_5BBB0
# cseg01:0005BB6B 60                        pusha
# cseg01:0005BB6C B8 40 00 00 00            mov     eax, 40h ; '@'
# cseg01:0005BB71 BA 2D 00 00 00            mov     edx, 2Dh ; '-'
# cseg01:0005BB76 29 C9                     sub     ecx, ecx
# cseg01:0005BB78 BF A4 18 09 00            mov     edi, offset delta_table_modulation
# cseg01:0005BB7D C7 07 00 00 00 00         mov     dword ptr [edi], 0
# cseg01:0005BB83 83 C7 04                  add     edi, 4
# cseg01:0005BB86                       loc_5BB86:
# cseg01:0005BB86 89 C5                     mov     ebp, eax
# cseg01:0005BB88 C1 ED 05                  shr     ebp, 5
# cseg01:0005BB8B 01 E9                     add     ecx, ebp
# cseg01:0005BB8D 01 D0                     add     eax, edx
# cseg01:0005BB8F 83 C2 02                  add     edx, 2
# cseg01:0005BB92 89 0F                     mov     [edi], ecx
# cseg01:0005BB94 89 CE                     mov     esi, ecx
# cseg01:0005BB96 F7 DE                     neg     esi
# cseg01:0005BB98 89 77 04                  mov     [edi+4], esi
# cseg01:0005BB9B 83 C7 08                  add     edi, 8
# cseg01:0005BB9E 81 FF A0 1C 09 00         cmp     edi, (offset delta_table_modulation+3FCh)
# cseg01:0005BBA4 7C E0                     jl      short loc_5BB86
# cseg01:0005BBA6 89 C5                     mov     ebp, eax
# cseg01:0005BBA8 C1 ED 05                  shr     ebp, 5
# cseg01:0005BBAB 01 E9                     add     ecx, ebp
# cseg01:0005BBAD 89 0F                     mov     [edi], ecx
# cseg01:0005BBAF 61                        popa
# cseg01:0005BBB0                       locret_5BBB0:
# cseg01:0005BBB0 C3                                      retn
# cseg01:0005BBB0                         build_delta_table endp
#
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

##########################
#
# Construct declaration
#
##########################

#
# Sound Flags
#
gdv_soundflags = construct.BitStruct(
    construct.Padding(4),
    construct.FlagsEnum("audio_coding"      / construct.BitsInteger(1), PCM = 0x00, DPCM = 0x01),
    construct.FlagsEnum("sample_width"      / construct.BitsInteger(1), BIT_8 = 0x00, BIT_16 = 0x01),
    construct.FlagsEnum("audio_channels"    / construct.BitsInteger(1), MONO = 0x00, STEREO = 0x01),
    construct.FlagsEnum("audio_present"     / construct.BitsInteger(1), AUDIO_NOT_PRESENT = 0x00, AUDIO_PRESENT = 0x01),
    construct.Padding(8),
)

#
# Image type
#
gdv_imagetype = construct.BitStruct(
    construct.Padding(5),
    construct.Enum("video_depth"            / construct.BitsInteger(3),
        PIXEL_8_BITS        = 0x01,
        PIXEL_15_BITS       = 0x02,
        PIXEL_16_BITS       = 0x03,
        PIXEL_24_BITS       = 0x04,
    ),
    construct.Padding(8),
)

#
# VideoFrame header
#
gdv_video_frame_header = construct.Struct(
    "signature"             / construct.Const("\x05\x13"),                      # + 0x00
    "length"                / construct.Int16ul,                                # + 0x02
    "type_flags"            / construct.BitStruct(                              # + 0x04
        "unk_00"               / construct.BitsInteger(1),
        "unk_01"               / construct.BitsInteger(1),
        "half_resolution_mode" / construct.BitsInteger(1),
        "unk_03"               / construct.BitsInteger(1),
        construct.Enum("coding_method"            / construct.BitsInteger(4),
            METHOD_00       = 0x00,
            METHOD_01       = 0x01,
            METHOD_02       = 0x02,
            METHOD_03       = 0x03,
            METHOD_04       = 0x04,
            METHOD_05       = 0x05,
            METHOD_06       = 0x06,
            METHOD_07       = 0x07,
            METHOD_08       = 0x08),
        "stream_start"      / construct.BitsInteger(24, swapped=True)),
)

#
# VideoFrame
#
gdv_video_frame = construct.Struct(
    "frame_header" / gdv_video_frame_header,
    construct.OnDemand(construct.Array(lambda ctx: ctx.frame_header.length, "data" / construct.Byte))
)

#
# Chunk
#
gdv_chunk = construct.Struct(
    "audio_data"        /   construct.If(lambda ctx: ctx._.gdv_header.sound_flags.audio_present["AUDIO_PRESENT"] == True,
        construct.OnDemand(construct.Array(lambda ctx: get_length_audio_data(ctx._.gdv_header), "audio_data" / construct.Int8ul))),
    "video"             / construct.If(lambda ctx: ctx._.gdv_header.frame_size != 0x00,
        gdv_video_frame)
)

#
# GDV header
#
gdv_header = construct.Struct(
    "start_gdv_header"      / construct.Tell,
    "signature"             / construct.Const("\x94\x19\x11\x29"),                          # + 0x00
    "size_id"               / construct.Int16ul,                                            # + 0x04
    "nb_frames"             / construct.Int16ul,                                            # + 0x06
    "framerate"             / construct.Int16ul,                                            # + 0x08
    "sound_flags"           / gdv_soundflags,                                               # + 0x0A
    "playback_frequency"    / construct.Int16ul,                                            # + 0x0C
    "image_type"            / gdv_imagetype,                                                # + 0x0E
    "frame_size"            / construct.Int16ul,                                            # + 0x10
    "unk_byte_00"           / construct.Int8ul,                                             # + 0x12
    "lossyness"             / construct.Int8ul,                                             # + 0x13
    "frame_width"           / construct.Int16ul,                                            # + 0x14
    "frame_height"          / construct.Int16ul,                                            # + 0x16
    "end_gdv_header"        / construct.Tell,
)

#
# GDV file
#
gdv_file = construct.Struct(
    "gdv_header"            / gdv_header,
    # 768-byte palette if the video is palettized (image type indicates 8 bits/pixel)
    "palette"               / construct.If(lambda ctx: ctx.gdv_header.image_type.video_depth == "PIXEL_8_BITS",
                                construct.OnDemandPointer(lambda ctx: ctx.gdv_header.end_gdv_header,
                                    construct.Array(0x300, "palette" / construct.Int8ul))),
    "start_chunks"          / construct.IfThenElse(lambda ctx: ctx.gdv_header.image_type.video_depth == "PIXEL_8_BITS",
                                construct.Computed(lambda ctx: ctx.gdv_header.end_gdv_header + 0x300),
                                construct.Computed(lambda ctx: ctx.gdv_header.end_gdv_header)),
    "chunks"                / construct.OnDemandPointer(lambda ctx: ctx.start_chunks,
        construct.Array(lambda ctx: ctx.gdv_header.nb_frames, gdv_chunk)
        ),
)

##########################
#
# Video decoder
#
##########################

#
# 32-bit bit queue & stream reader
#
class BitReader:
    def __init__(self, bytes):
        if len(bytes) == 0:
            return
        self.bytes = ''.join(chr(x) for x in bytes)
        self.pos = 0
        self.queue = struct.unpack("<I", self.bytes[0x00:0x04])[0]
        self.pos += 4
        self.size = 16

    def get_bits(self, num):
        val = self.queue & ((1 << num) - 1)
        self.queue = self.queue >> num
        self.size = self.size - num
        if self.size <= 0:
            self.size = self.size + 16
            self.queue = self.queue | ((struct.unpack("<H", self.bytes[self.pos:self.pos+2])[0]) << self.size)
            self.pos += 2
        return val

    def get_bit(self):
        return self.get_bits(1)

    def get_byte(self):
        val = self.bytes[self.pos:self.pos+1]
        self.pos = self.pos + 1
        return val

#
#
#
class FrameDecoder:
    def __init__(self, frame_width, frame_height, frame_header, bytes, pos, prev_frame=None):
        #print frame_header
        self.reader = BitReader(bytes)
        self.pixels = StringIO.StringIO()
        self.frame_header = frame_header

        # Used when the offset used by copy pixel is greater
        # than the file position indicator
        #self.inv_offset = ""
        for i in xrange(0, 256):
            #self.inv_offset += chr(i) * 8
            self.pixels.write(chr(i) * 8)
        for i in xrange(0, 256):
            #self.inv_offset += chr(i) * 8
            self.pixels.write(chr(i) * 8)

        #if frame_header.type_flags.half_resolution_mode != 1:
        #    raise ValueError("FrameDecoder - half_resolution_mode : TODO")
        if prev_frame == None:
            #self.pixels.write("\x00" * int((frame_width * frame_height) * 0.5))
            self.pixels.write("\x00" * int((frame_width * frame_height)))
        else:
            self.pixels.write(prev_frame)
        self.pixels.seek(pos + 4096, 0x00)
        self.decoding = {"METHOD_01" : self.decode_method_01,
                         "METHOD_02" : self.decode_method_02,
                         "METHOD_03" : self.decode_method_03,
                         "METHOD_04" : self.decode_method_04,
                         "METHOD_05" : self.decode_method_05,
                         "METHOD_06" : self.decode_method_06,
                         "METHOD_07" : self.decode_method_07,
                         "METHOD_08" : self.decode_method_08}

        self.subdecoding_method_08 = {0 : self.method_08_tag_00,
                                      1 : self.method_08_tag_01,
                                      2 : self.method_08_tag_02,
                                      3 : self.method_08_tag_03}

    def get_bits(self, num):
        return self.reader.get_bits(num)

    def get_bit(self):
        return self.reader.get_bit()

    def get_byte(self):
        return self.reader.get_byte()

    def copy_pixels(self, offset, length):
        saved = self.pixels.tell()
        self.pixels.seek(offset, 0x01)
        pix = self.pixels.read(length)
        self.pixels.seek(saved)
        self.pixels.write(pix)

    def get_pixel(self, offset):
        saved = self.pixels.tell()
        self.pixels.seek(offset, 0x01)
        pix = self.pixels.read(0x01)
        self.pixels.seek(saved)
        return pix

    def get_pixels(self):
        self.pixels.seek(0x00 + 4096, 0x00)
        return self.pixels.read()

    def decode(self):
        self.decoding[self.frame_header.type_flags.coding_method]()

    def decode_method_01(self):
        raise ValueError("[TODO] decode_method_01")

    def decode_method_02(self):
        raise ValueError("[TODO] decode_method_02")

    def decode_method_03(self):
        # do nothing
        pass

    def decode_method_04(self):
        raise ValueError("[TODO] decode_method_04")

    def decode_method_05(self):
        raise ValueError("[TODO] decode_method_05")

    def decode_method_06(self):
        raise ValueError("[TODO] decode_method_06")

    def decode_method_07(self):
        raise ValueError("[TODO] decode_method_07")

    def decode_method_08(self):
        while True:
            tag = self.get_bits(2)
            #print "[+] tag : %d" % tag
            if self.subdecoding_method_08[tag]() == False:
                break

    def method_08_tag_00(self):
        if self.get_bits(1) == 0x00:
            self.pixels.write(self.get_byte())
            return True
        length = 2
        count = 0
        while True:
            count = count + 1
            step = self.get_bits(count)
            length = length + step
            if (step != ((1 << count) - 1)):
                break
        for i in xrange(0, length):
            self.pixels.write(self.get_byte())
        return True

    # cseg01:000141E5                 and     al, 1
    # cseg01:000141E7                 jz      short loc_1420F
    # cseg01:000141E9                 sub     eax, eax
    # cseg01:000141EB                 mov     al, [esi]
    # cseg01:000141ED                 inc     esi
    # cseg01:000141EE                 or      al, al
    # cseg01:000141F0                 js      short loc_141FB
    # cseg01:000141F2                 lea     edi, [edi+eax+12h]
    # cseg01:000141F6                 jmp     loc_14071
    # cseg01:000141FB ; ---------------------------------------------------------------------------
    # cseg01:000141FB
    # cseg01:000141FB loc_141FB:                              ; CODE XREF: METHOD_08+1A0
    # cseg01:000141FB                 add     al, al
    # cseg01:000141FD                 shl     eax, 7
    # cseg01:00014200                 mov     al, [esi]
    # cseg01:00014202                 inc     esi
    # cseg01:00014203                 lea     edi, [edi+eax+92h]
    # cseg01:0001420A                 jmp     loc_14071
    def method_08_tag_01(self):
        if self.get_bits(1) == 0x00:
            self.pixels.seek(self.get_bits(4) + 2, 0x01)
            return True
        length = ord(self.get_byte())
        if length & 0x80 == 0:
            self.pixels.seek(length + 0x12, 0x01)
            return True
        self.pixels.seek((((length & 0x7F) << 8) | ord(self.get_byte())) + 0x92, 0x01)
        return True

    def method_08_tag_02(self):
        sub_tag = self.get_bits(0x02)
        #print "[+] sub_tag : 0x%02X" % sub_tag
        if sub_tag == 0x03:
            offset = ord(self.get_byte())
            length = 2 + int((offset & 0x80) == 0x80)
            offset = offset & 0x7F
            if offset == 0:
                if self.pixels.tell() == 0x00:
                    self.pixels.write("\xFF" * length)
                else:
                    self.pixels.write(self.get_pixel(-1) * length)
                return True
            else:
                offset = offset + 1
                #if offset > self.pixels.tell():
                #    v = 4096 - offset - self.pixels.tell()
                #    self.pixels.write(self.inv_offset[-v:-v + length])
                #else:
                self.copy_pixels(-offset, length)
                return True
        next_4 = self.get_bits(0x04)
        next_byte = ord(self.get_byte())
        offset = (next_4 << 0x08) | next_byte
        if sub_tag == 0x00 and offset == 0xFFF:
            return False
        #print "offset : 0x%04X (%d)" % (offset, offset)
        if sub_tag == 0x00 and offset > 0xF80:
            length = (offset & 0x0F) + 2
            offset = (offset >> 4) & 7
            #print "[+] offset %d" % offset
            px1 = self.get_pixel(-(offset + 1))
            px2 = self.get_pixel(-offset)
            for i in xrange(0, length):
                self.pixels.write(px1)
                self.pixels.write(px2)
            return True
        length = sub_tag + 3
        if offset == 0xFFF:
            if self.pixels.tell() == 0x00:
                self.pixels.write("\xFF" * length)
            else:
                self.pixels.write(self.get_pixel(-1) * length)
            return True
        offset = 4096 - offset
        #if offset > self.pixels.tell():
        #    v = offset - self.pixels.tell()
        #    self.pixels.write(self.inv_offset[-v:-v + length])
        #    return True
        self.copy_pixels(-offset, length)
        return True

    def method_08_tag_03(self):
        first_byte = ord(self.get_byte())
        if first_byte & 0xC0 == 0xC0:
            top_4 = self.get_bits(0x04)
            next_byte = ord(self.get_byte())
            length = (first_byte & 0x3F) + 0x08
            offset = (top_4 << 0x08) | next_byte
            self.copy_pixels(offset + 1, length)
            return True
        if first_byte & 0x80 == 0x00:
            bits_6_to_4 = first_byte >> 4
            bits_3_to_0 = first_byte & 0x0F
            next_byte = ord(self.get_byte())
            length = bits_6_to_4 + 6
            offset = (bits_3_to_0 << 8) | next_byte
        else:
            top_4 = self.get_bits(0x04)
            next_byte = ord(self.get_byte())
            length = 14 + (first_byte & 0x3F)
            offset = (top_4 << 8) | next_byte
        #print "[+] offset : 0x%X" % offset
        if offset == 0xFFF:
            if self.pixels.tell() == 0x00:
                self.pixels.write("\xFF" * length)
            else:
                self.pixels.write(self.get_pixel(-1) * length)
            return True
        offset = 4096 - offset
        #if offset > self.pixels.tell():
        #    v = offset - self.pixels.tell()
        #    #self.pixels.write(self.inv_offset[-v:-v + length])
        #    return True
        self.copy_pixels(-offset, length)
        return True

class GDV:
    def __init__(self, filename):
        self.stream = open(filename, "rb")
        self.gdv_file = gdv_file.parse_stream(self.stream)
        self.table_delta_mod = compute_delta_modulation()

    def __str__(self):
        b  = "[+] size_id               : 0x%04X (%d)\n" % (self.gdv_file.gdv_header.size_id, self.gdv_file.gdv_header.size_id)
        b += "[+] nb_frames             : 0x%04X (%d)\n" % (self.gdv_file.gdv_header.nb_frames, self.gdv_file.gdv_header.nb_frames)
        b += "[+] framerate             : 0x%04X (%d)\n" % (self.gdv_file.gdv_header.framerate, self.gdv_file.gdv_header.framerate)
        b += "[+] playback_frequency    : 0x%04X (%d)\n" % (self.gdv_file.gdv_header.playback_frequency, self.gdv_file.gdv_header.playback_frequency)
        b += "[+] frame_size            : 0x%04X (%d)\n" % (self.gdv_file.gdv_header.frame_size, self.gdv_file.gdv_header.frame_size)
        b += "[+] lossyness             : 0x%02X   (%d)\n" % (self.gdv_file.gdv_header.lossyness, self.gdv_file.gdv_header.lossyness)
        b += "[+] frame_width           : 0x%04X (%d)\n" % (self.gdv_file.gdv_header.frame_width, self.gdv_file.gdv_header.frame_width)
        b += "[+] frame_height          : 0x%04X (%d)\n" % (self.gdv_file.gdv_header.frame_height, self.gdv_file.gdv_header.frame_height)
        return b

    def get_palette(self):
        if self.gdv_file.palette != None:
            # palette components is a 6-bit VGA
            pal_0 = self.gdv_file.palette()
            palette = []
            for i in xrange(0, len(pal_0), 3):
                # scale
                palette.append(((((pal_0[i]) * 255) / 63), (((pal_0[i + 1]) * 255) / 63), (((pal_0[i + 2]) * 255) / 63)))
            return palette
        return ""

    def convert_to_wave(self, filename="test.wav"):
        if self.gdv_file.gdv_header.sound_flags.audio_present["AUDIO_PRESENT"] != True:
            print "[-] File doesn't contain audio data"
            return
        wave_output = wave.open(filename, "wb")
        left_state = 0x00
        right_state = 0x00
        # (nchannels, sampwidth, framerate, nframes, comptype, compname)
        wave_output.setparams((2, 2, self.gdv_file.gdv_header.playback_frequency, 0, 'NONE', 'not compressed'))
        for frame_num in xrange(0, self.gdv_file.gdv_header.nb_frames):
            audio_data = self.gdv_file.chunks()[frame_num].audio_data()
            for i in xrange(0, len(audio_data), 2):
                left_state = (left_state + self.table_delta_mod[audio_data[i]])
                right_state = (right_state + self.table_delta_mod[audio_data[i + 1]])
                wave_output.writeframes(struct.pack("<H", (left_state & 0xFFFF)))
                wave_output.writeframes(struct.pack("<H", (right_state& 0xFFFF)))
        wave_output.close()

    def extract_frames(self, prefix):
        if self.gdv_file.gdv_header.frame_size == 0x00:
            print "[-] File doesn't contain video data"
            return
        prev_frame = None
        for frame_num in xrange(0, self.gdv_file.gdv_header.nb_frames):
            print "[+] Working on %d" % frame_num
            video = self.gdv_file.chunks()[frame_num].video
            frame = FrameDecoder(self.gdv_file.gdv_header.frame_width,
                        self.gdv_file.gdv_header.frame_height,
                        video.frame_header,
                        video.data(),
                        video.frame_header.type_flags.stream_start,
                        prev_frame)
            frame.decode()
            pixels = frame.get_pixels()
            palette = self.get_palette()
            img_data = ""
            for i in xrange(0, len(pixels)):
                img_data += chr(palette[ord(pixels[i])][0]) + chr(palette[ord(pixels[i])][1]) + chr(palette[ord(pixels[i])][2])
            # In case half/quarter resolution
            img_data += "\x00" * (((self.gdv_file.gdv_header.frame_width * self.gdv_file.gdv_header.frame_height) - (len(img_data) / 3)) * 3)
            i = Image.frombuffer("RGB", (self.gdv_file.gdv_header.frame_width, self.gdv_file.gdv_header.frame_height), img_data)
            i = i.transpose(Image.FLIP_TOP_BOTTOM)
            i.save(prefix + "%05d.png" % frame_num)
            prev_frame = pixels

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gdv extract launch options')
    parser.add_argument('gdv_file', action='store', default='', help='gdv file to extract')
    parser.add_argument('-o', dest='output_file', help="Output WAV file", required=False, metavar='output_file')
    parser.add_argument('-d', dest='debug', action="store_const", const=True, help="Enable debugging output", default=False)
    parser.add_argument('-i', dest='info', action="store_const", const=True, help="Print file information", default=False)
    parser.add_argument('-a', dest='audio', action="store_const", const=True, help="Extract audio", default=False)
    parser.add_argument('-f', dest='frame', action="store_const", const=True, help="Extract frames", default=False)
    parser.add_argument('-p', dest='prefix', action="store_const", const=True, help="Prefix PNG frame name", default=False)
    args = parser.parse_args()

    gdv = GDV(args.gdv_file)
    if args.info == True:
        print gdv
    if args.audio == True:
        if not args.output_file:
            parser.error('-o is required when -a is set')
        gdv.convert_to_wave(args.output_file)
    if args.frame == True:
        if not args.prefix:
            names_png = "DUMP_FRAME_%s_" % os.path.basename(args.gdv_file)
        else:
            names_png = args.prefix
        gdv.extract_frames(names_png)
        print "Try running : ffmpeg -f image2 -r " + str(gdv.gdv_file.gdv_header.framerate) + " -i " + names_png + "%05d.png -vcodec mpeg4 -y movie.mp4"