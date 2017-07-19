import os

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