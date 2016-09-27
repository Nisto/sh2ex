import os
import sys
import struct
import zlib

def get_u8(buf, offset):
    return struct.unpack("B", buf[offset:offset+1])[0]

def get_u32_le(buf, offset):
    return struct.unpack("<I", buf[offset:offset+4])[0]

def crc32(data):
    return zlib.crc32(data) & 0xFFFFFFFF

def read_iso_record(f):
    dirlen = struct.unpack("B", f.read(1))[0]

    if dirlen <= 1:
        return None

    dirbuf = struct.pack("B", dirlen) + f.read(dirlen - 1)

    lba = get_u32_le(dirbuf, 0x02)
    size = get_u32_le(dirbuf, 0x0A)
    flags = get_u8(dirbuf, 0x19)
    name = dirbuf[0x21 : 0x21 + get_u8(dirbuf, 0x20)].decode("ASCII")

    if name == "\x00":
        name = '.'
    elif name == "\x01":
        name = '..'
    else:
        name = name.rsplit(';', 1)[0]

    return {"lba":lba, "size":size, "flags":flags, "name":name}

def read_iso_tree(f, toc, dirname=''):
    subdirs = []

    while True:
        record = read_iso_record(f)

        if record is None:
            break
        elif record["flags"] & 0b10 != 0 and record["name"] != '.' and record["name"] != '..':
            subdirs.append(record)
        elif record["flags"] & 0b10 == 0:
            toc[os.path.join('', dirname, record["name"]).replace(os.sep, '/')] = record
            toc[os.path.join('/', dirname, record["name"]).replace(os.sep, '/')] = record
            toc[os.path.join('./', dirname, record["name"]).replace(os.sep, '/')] = record

    for record in subdirs:
        f.seek(2048 * record["lba"])
        read_iso_tree(f, toc, os.path.join(dirname, record["name"]))

def get_filename(buf, offset):
    filename = b''
    while buf[offset:offset+1] != b"\0":
        filename += buf[offset:offset+1]
        offset += 1
    return filename.decode("ASCII")

def extract(inf, dst, size):
    with open(dst, "wb") as outf:
        read_max = 2048
        left = size
        while left > 0:
            if read_max > left:
                read_max = left
            buf = inf.read(read_max)
            if buf == b"":
                break # EOF
            outf.write(buf)
            left -= read_max

exe_meta = [
    # SLPM-65051 (v1.50)
    # Executable timestamp: 2001-08-22 02:50:16 GMT+0900
    {
        "path"           : "SLPM_650.51",
        "crc"            : 0x2FB23919,
        "elf_header_size": 0x700,
        "imagebase"      : 0x100000,
        "toc_offset"     : 0x2BB900,
        "toc_count"      : 3443
    },

    # SLPM-65631 - Saigo no Uta - Konami Dendou Selection (v1.50)
    # Executable timestamp: 2002-02-26 06:11:56 GMT+0900
    {
        "path"           : "SLPM_650.98",
        "crc"            : 0x1388A129,
        "elf_header_size": 0x800,
        "imagebase"      : 0x100000,
        "toc_offset"     : 0x2CCB80,
        "toc_count"      : 3894
    },

    # SLUS-20228 (v1.20)
    # Executable timestamp: 2001-08-14 15:13:52 GMT+0900
    {
        "path"           : "SLUS_202.28",
        "crc"            : 0xAA6B485D,
        "elf_header_size": 0x700,
        "imagebase"      : 0x100000,
        "toc_offset"     : 0x2BB180,
        "toc_count"      : 3443
    },

    # SLUS-20228GH - Greatest Hits (v2.01)
    # Executable timestamp: 2002-07-11 05:18:18 GMT+0900
    {
        "path"           : "SLUS_202.28",
        "crc"            : 0xB6DA54E6,
        "elf_header_size": 0x800,
        "imagebase"      : 0x100000,
        "toc_offset"     : 0x2CCF00,
        "toc_count"      : 3894
    },

    # SLES-50382 - Special Edition / The Collection (v1.10)
    # Executable timestamp: 2001-10-01 08:46:52 GMT+0900
    {
        "path"           : "SLES_503.82",
        "crc"            : 0xD3402685,
        "elf_header_size": 0x800,
        "imagebase"      : 0x100000,
        "toc_offset"     : 0x2BD400,
        "toc_count"      : 3724
    }
]

def main(argc=len(sys.argv), argv=sys.argv):
    if argc != 2:
        print("Usage: %s <iso-file>" % argv[0])
        return 1

    isopath = os.path.realpath(argv[1])

    if not os.path.isfile(isopath):
        print("Invalid filepath")
        return 1

    with open(isopath, "rb") as iso:
        iso.seek(0x8000)
    
        if iso.read(8) != b"\x01CD001\x01\x00":
            print("ISO seems to be invalid")
            return 1
    
        iso.seek(0x809C)
    
        rootdir = read_iso_record(iso)
    
        iso.seek(2048 * rootdir["lba"])
    
        iso_toc = {}

        read_iso_tree(iso, iso_toc)

        version = None

        for v in exe_meta:
            if v["path"] in iso_toc:
                path = v["path"]
                crc = v["crc"]
                lba = iso_toc[path]["lba"]
                size = iso_toc[path]["size"]
                iso.seek(2048 * lba)
                exebuf = iso.read(size)
                if crc32(exebuf) == crc:
                    version = v
                    break

        if version is None:
            print("Unsupported version")
            return 1

        elf_header_size = version["elf_header_size"]
        imagebase = version["imagebase"]
        toc_offset = version["toc_offset"]
        toc_count = version["toc_count"]

        out_root = "%s - extracted" % os.path.splitext(isopath)[0]

        for i in range(toc_count):
            meta_offset = (get_u32_le(exebuf, toc_offset + (i * 8) + 0x00) - imagebase) + elf_header_size
            path_offset = (get_u32_le(exebuf, toc_offset + (i * 8) + 0x04) - imagebase) + elf_header_size

            type = get_u32_le(exebuf, meta_offset + 0x00)

            if type != 0x50:
                continue
            
            size = get_u32_le(exebuf, meta_offset + 0x0C)
            
            offset_in_file = 0
            
            while True:
                type = get_u32_le(exebuf, meta_offset + 0x00)

                if type != 0x50:
                    break

                offset_in_file += get_u32_le(exebuf, meta_offset + 0x08)
                meta_offset = (get_u32_le(exebuf, meta_offset + 0x04) - imagebase) + elf_header_size
            
            parent_path_offset = (get_u32_le(exebuf, meta_offset + 0x04) - imagebase) + elf_header_size
            parent_path = get_filename(exebuf, parent_path_offset).upper()

            if parent_path in iso_toc:
                sub_path = get_filename(exebuf, path_offset)
                sub_dirpath = os.path.dirname(sub_path)

                out_path = os.path.join(out_root, sub_path)
                out_dirpath = os.path.join(out_root, sub_dirpath)

                if not os.path.isdir(out_dirpath):
                    os.makedirs(out_dirpath)

                iso.seek(2048 * iso_toc[parent_path]["lba"] + offset_in_file)

                extract(iso, out_path, size)

                print("Extracted: %s" % sub_path)

        input("All done.")

    return 0

if __name__ == "__main__":
    main()
