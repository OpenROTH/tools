import os
from PIL import Image, ImageDraw

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

def diffhexdump(src_00, src_01, length=16):
    import colorama
    colorama.init(autoreset=True)
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src_00), length):
        chars_00 = src_00[c:c + length]
        chars_01 = src_01[c:c + length]
        hex = []
        printable = ''
        nb_total = 0x00
        for i, x in enumerate(chars_00):
            if x != chars_01[i]:
                hex.append(colorama.Fore.RED + ("%02x" % ord(x)) + colorama.Style.RESET_ALL)
                nb_total += 4
            else:
                hex.append("%02x" % ord(x))
                nb_total += 1
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars_00])
        lines.append("%04x  %-*s  %s\n" % (c, nb_total * 3, ' '.join(hex), printable))
    print ''.join(lines).rstrip('\n')

def createdir(dirname):
    try:
        os.stat(dirname)
    except:
        os.mkdir(dirname)

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

def build_palette(palette, out="out.png"):
    im = Image.new("P", (512, 512), 0)
    im.putpalette(palette)
    d = ImageDraw.ImageDraw(im)
    x = 0
    y = 0
    for i in xrange(0, 256):
        d.rectangle((x, y, x + 32, y + 32), i)
        x = (x + 32)
        if x % 512 == 0:
            y = (y + 32)
            x = 0
    im.save(out)

# Take a 768 byte table of int
def conv_build_palette(palette, out="out.png"):
    if len(palette) != 768:
        return
    new_palette = []
    for i in xrange(0, len(palette), 3):
        new_palette.append((palette[i] * 255) / 63)
        new_palette.append((palette[i + 1] * 255) / 63)
        new_palette.append((palette[i + 2] * 255) / 63)
    build_palette(new_palette, out)