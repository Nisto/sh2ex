import os
import sys
import struct
import zlib

metalist = [
    # SLPM-12345 - E3 Demo (v0.30)
    # Executable timestamp: 2001-05-01 10:13:56 GMT+0900
    {
        "exepath"        : "SLPM_123.45",
        "execrc"         : 0x8556FA90,
        "toc_offset"     : 0x45C200,
        "toc_count"      : 539,

        "datpath"        : "SOUND.DAT",
        "irxpath"        : "IOP/SD0425/SOUNDCD.IRX",
        "irxcrc"         : 0x76CC7D44,
        "seq_start_sect" : 0,
        "seq_tbl_offset" : 0x13AC0,
        "seq_ent_count"  : 26,
        "stm_start_sect" : 2626,
        "stm_tbl_offset" : 0x13340,
        "stm_ent_count"  : 159,
    },

    # SLPM-61009 - Trial Version (v1.20)
    # Executable timestamp: 2001-08-11 11:18:02 GMT+0900
    {
        "exepath"        : "SLPM_610.09",
        "execrc"         : 0x37E6204D,
        "toc_offset"     : 0x2B3180,
        "toc_count"      : 3441,

        "datpath"        : "IOP/SOUND/SOUND.DAT",
        "irxpath"        : "IOP/SOUND/SOUNDCD.IRX",
        "irxcrc"         : 0xB05B19AA,
        "seq_start_sect" : 0,
        "seq_tbl_offset" : 0x13CE0,
        "seq_ent_count"  : 80,
        "stm_start_sect" : 13290,
        "stm_tbl_offset" : 0x137C0,
        "stm_ent_count"  : 109,
    },

    # SLPM-65051 (v1.50)
    # Executable timestamp: 2001-08-22 02:50:16 GMT+0900
    {
        "exepath"        : "SLPM_650.51",
        "execrc"         : 0x2FB23919,
        "toc_offset"     : 0x2BB900,
        "toc_count"      : 3443,

        "datpath"        : "IOP/SOUND/SOUND.DAT",
        "irxpath"        : "IOP/SOUND/SOUNDCD.IRX",
        "irxcrc"         : 0xB05B19AA,
        "seq_start_sect" : 0,
        "seq_tbl_offset" : 0x13CE0,
        "seq_ent_count"  : 80,
        "stm_start_sect" : 13290,
        "stm_tbl_offset" : 0x137C0,
        "stm_ent_count"  : 109,
    },

    # SLPM-65098 - Saigo no Uta (v1.50)
    # +
    # SLPM-65631 - Saigo no Uta - Konami Dendou Selection (v1.50)
    # Executable timestamp: 2002-02-26 06:11:56 GMT+0900
    {
        "exepath"        : "SLPM_650.98",
        "execrc"         : 0x1388A129,
        "toc_offset"     : 0x2CCB80,
        "toc_count"      : 3894,

        "datpath"        : "IOP/SOUND/SOUND.DAT",
        "irxpath"        : "IOP/SOUND/SOUNDCD.IRX",
        "irxcrc"         : 0xA2A69417,
        "seq_start_sect" : 0,
        "seq_tbl_offset" : 0x13D80,
        "seq_ent_count"  : 82,
        "stm_start_sect" : 13809,
        "stm_tbl_offset" : 0x137C0,
        "stm_ent_count"  : 122,
    },

    # SLUS-20228 (v1.20)
    # Executable timestamp: 2001-08-14 15:13:52 GMT+0900
    {
        "exepath"        : "SLUS_202.28",
        "execrc"         : 0xAA6B485D,
        "toc_offset"     : 0x2BB180,
        "toc_count"      : 3443,

        "datpath"        : "IOP/SOUND/SOUND.DAT",
        "irxpath"        : "IOP/SOUND/SOUNDCD.IRX",
        "irxcrc"         : 0xB05B19AA,
        "seq_start_sect" : 0,
        "seq_tbl_offset" : 0x13CE0,
        "seq_ent_count"  : 80,
        "stm_start_sect" : 13290,
        "stm_tbl_offset" : 0x137C0,
        "stm_ent_count"  : 109,
    },

    # SLUS-20228GH - Greatest Hits (v2.01)
    # Executable timestamp: 2002-07-11 05:18:18 GMT+0900
    {
        "exepath"        : "SLUS_202.28",
        "execrc"         : 0xB6DA54E6,
        "toc_offset"     : 0x2CCF00,
        "toc_count"      : 3894,

        "datpath"        : "IOP/SOUND/SOUND.DAT",
        "irxpath"        : "IOP/SOUND/SOUNDCD.IRX",
        "irxcrc"         : 0xA2A69417,
        "seq_start_sect" : 0,
        "seq_tbl_offset" : 0x13D80,
        "seq_ent_count"  : 82,
        "stm_start_sect" : 13809,
        "stm_tbl_offset" : 0x137C0,
        "stm_ent_count"  : 122,
    },

    # SLES-50382 - Special Edition / The Collection (v1.10)
    # Executable timestamp: 2001-10-01 08:46:52 GMT+0900
    {
        "exepath"        : "SLES_503.82",
        "execrc"         : 0xD3402685,
        "toc_offset"     : 0x2BD400,
        "toc_count"      : 3724,

        "datpath"        : "IOP/SOUND/SOUND.DAT",
        "irxpath"        : "IOP/SOUND/SOUNDCD.IRX",
        "irxcrc"         : 0x55D0DCE5,
        "seq_start_sect" : 0,
        "seq_tbl_offset" : 0x14120,
        "seq_ent_count"  : 80,
        "stm_start_sect" : 13290,
        "stm_tbl_offset" : 0x13B08,
        "stm_ent_count"  : 129,
    },

    # SLES-51156 - Director's Cut (v1.02)
    # Executable timestamp: 2002-11-07 10:15:08 GMT+0900
    {
        "exepath"        : "SLES_511.56",
        "execrc"         : 0xE6CFE16F,
        "toc_offset"     : 0x2CD980,
        "toc_count"      : 3894,

        "datpath"        : "IOP/SOUND/SOUND.DAT",
        "irxpath"        : "IOP/SOUND/SOUNDCD.IRX",
        "irxcrc"         : 0xA2A69417,
        "seq_start_sect" : 0,
        "seq_tbl_offset" : 0x13D80,
        "seq_ent_count"  : 82,
        "stm_start_sect" : 13809,
        "stm_tbl_offset" : 0x137C0,
        "stm_ent_count"  : 122,
    }
]

class ISOFS_IMAGE:
    #
    # DISCLAIMER:
    # Only supports reading the ISO filesystem / track (first track probably)
    # on NON-mixed-mode disk images.
    # -- Nisto
    #
    def __init__(self, path):
        self.path = path

        self.f = open(self.path, "rb")

        self.toc = {}

        self.f.seek(16 * 2352)
        pvd_raw = self.f.read(2352)

        self.f.seek(16 * 2048)
        pvd_user = self.f.read(2048)

        if self.is_raw_sector(pvd_raw) and self.is_pvd(pvd_raw[0x10:0x810]):
            #
            # Standard CD-ROM
            #
            pvd = pvd_raw[0x10:0x810]
            self.is_raw = 1
            self.is_xa = 0
            self.sector_size = 2352
            self.user_start = 0x10
            if pvd_raw[0x0F] == 1:
                self.user_size = 2048
                self.user_end = 0x810
            elif pvd_raw[0x0F] == 2:
                self.user_size = 2336
                self.user_end = 0x930
        elif self.is_raw_sector(pvd_raw) and self.is_pvd(pvd_raw[0x18:0x818]):
            #
            # CD-ROM XA
            #
            pvd = pvd_raw[0x18:0x818]
            self.is_raw = 1
            self.is_xa = 1
            self.sector_size = 2352
            self.user_start = 0x18
            # size of User Data is 2048 if Form 1, or 2324 if Form 2, and the
            # Form may vary across a track, so a global size / end offset of
            # the User Data doesn't really make sense for CD-ROM XA
            self.user_size = None
            self.user_end = None
        elif self.is_pvd(pvd_user):
            #
            # CD / DVD / ... (User Data only)
            #
            pvd = pvd_user
            self.is_raw = 0
            self.is_xa = 0
            self.sector_size = 2048
            self.user_start = 0x00
            self.user_size = 2048
            self.user_end = 2048
        else:
            print("Unrecognized disk image format")
            sys.exit(1)

        root_dr = self.drparse(pvd[0x9C:0xBE])

        self.seek_user(root_dr["lba"])

        root_dir = self.read_user(root_dr["size"])

        self.dirparse(root_dir)

    def is_raw_sector(self, buf):
        sync = buf[0x00:0x0C]
        if sync != b"\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00":
            return 0

        mm = buf[0x0C]
        if (mm>>4) & 0x0F > 9 or mm & 0x0F > 9:
            return 0

        ss = buf[0x0D]
        if (ss>>4) & 0x0F > 5 or ss & 0x0F > 9:
            return 0

        ff = buf[0x0E]
        if (ff>>4) & 0x0F > 7 or ff & 0x0F > 9 \
        or ((ff>>4) & 0x0F == 7 and ff & 0x0F > 4):
            return 0

        mode = buf[0x0F]
        if mode > 2:
            return 0

        return 1

    def is_pvd(self, buf):
        if len(buf) != 2048:
            return 0

        if buf[0x00:0x06] != b"\x01CD001":
            return 0

        return 1

    def set_xa(self, subcode):
        if subcode & 0b100000 == 0:
            self.user_size = 2048
            self.user_end = 0x818
        else:
            self.user_size = 2324
            self.user_end = 0x92C

    def read_user(self, size):
        usrbuf = b""
        if self.is_raw:
            offset_in_sector = self.f.tell() % self.sector_size
            if offset_in_sector != 0:
                if offset_in_sector < self.user_start:
                    self.f.seek(-offset_in_sector, os.SEEK_CUR)
                else:
                    if self.is_xa:
                        self.f.seek(-offset_in_sector, os.SEEK_CUR)
                        tmpbuf = self.f.read(offset_in_sector)
                        self.set_xa(tmpbuf[0x12])

                    if offset_in_sector < self.user_end:
                        user_remain = self.user_end - offset_in_sector

                        if size < user_remain:
                            return self.f.read(size)

                        usrbuf += self.f.read(user_remain)

                        size -= user_remain

                        self.f.seek(self.sector_size - (offset_in_sector + user_remain), os.SEEK_CUR)
                    else:
                        self.f.seek(self.sector_size - offset_in_sector, os.SEEK_CUR)

            if self.is_xa:
                while size > 0:
                    sectbuf = self.f.read(self.sector_size)
                    self.set_xa(sectbuf[0x12])
                    if size >= self.user_size:
                        usrbuf += sectbuf[self.user_start:self.user_end]
                        size -= self.user_size
                    else:
                        usrbuf += sectbuf[self.user_start:self.user_start+size]
                        self.f.seek(-self.sector_size + self.user_start + size, os.SEEK_CUR)
                        size = 0
            else:
                while size > 0:
                    if size >= self.user_size:
                        sectbuf = self.f.read(self.sector_size)
                        size -= self.user_size
                    else:
                        sectbuf = self.f.read(self.user_start + size)
                        size = 0
                    usrbuf += sectbuf[self.user_start:self.user_end]
        else:
            while size > 0:
                if size >= self.user_size:
                    usrbuf += self.f.read(self.user_size)
                    size -= self.user_size
                else:
                    usrbuf += self.f.read(size)
                    size = 0

        return usrbuf

    def seek_user(self, sectors, bytes=0):
        if self.is_xa:
            self.f.seek(sectors * self.sector_size)
            while bytes > 0:
                header = self.f.read(self.user_start)
                self.set_xa(header[0x12])
                if bytes >= self.user_size:
                    self.f.seek(self.sector_size - self.user_start, os.SEEK_CUR)
                    bytes -= self.user_size
                else:
                    self.f.seek(bytes, os.SEEK_CUR)
                    bytes = 0
        else:
            if self.is_raw and bytes > 0:
                sectors += bytes // self.user_size
                bytes = self.user_start + (bytes % self.user_size)
            self.f.seek(sectors * self.sector_size + bytes)

    def extract(self, outpath, size, raw=False):
        with open(outpath, "wb") as out:
            while size > 0:
                todo = 2048

                if todo > size:
                    todo = size

                if raw:
                    buf = self.f.read(todo)
                else:
                    buf = self.read_user(todo)

                out.write(buf)

                size -= todo

    def drparse(self, drbuf):
        dr_size = get_u8(drbuf, 0x00)
        lba = get_u32_le(drbuf, 0x02)
        size = get_u32_le(drbuf, 0x0A)
        flags = get_u8(drbuf, 0x19)
        name_len = get_u8(drbuf, 0x20)
        name = drbuf[0x21 : 0x21 + name_len].decode("ASCII")

        if name == "\x00":
            name = '.'
        elif name == "\x01":
            name = '..'
        else:
            name = name.rsplit(';', 1)[0]

        return {"lba":lba, "size":size, "flags":flags, "name":name}

    def dirparse(self, dirbuf, dirname=''):
        i = 0
        subdirs = []
        while i < len(dirbuf) and dirbuf[i] > 0:
            dr_len = dirbuf[i]

            record = self.drparse(dirbuf[i:i+dr_len])

            if record["flags"] & 0b10 != 0 and record["name"] != '.' and record["name"] != '..':
                subdirs.append(record)
            elif record["flags"] & 0b10 == 0:
                self.toc[os.path.join('', dirname, record["name"]).replace(os.sep, '/')] = record
                self.toc[os.path.join('/', dirname, record["name"]).replace(os.sep, '/')] = record
                self.toc[os.path.join('./', dirname, record["name"]).replace(os.sep, '/')] = record

            i += dr_len

        for record in subdirs:
            self.seek_user(record["lba"])
            dirbuf = self.read_user(record["size"])
            self.dirparse(dirbuf, os.path.join(dirname, record["name"]))

def crc32(data):
    return zlib.crc32(data) & 0xFFFFFFFF

def get_u8(buf, off=0):
    return struct.unpack("B", buf[off:off+1])[0]

def get_u32_le(buf, off=0):
    return struct.unpack("<I", buf[off:off+4])[0]

def get_c_string(buf, off):
    end = off

    while buf[end] != 0:
        end += 1

    return buf[off:end].decode("ASCII")

def vfs_ex(disk, meta, exebuf):

    e_phoff  = get_u32_le(exebuf, 0x1C)
    p_offset = get_u32_le(exebuf, e_phoff+0x04)
    p_vaddr  = get_u32_le(exebuf, e_phoff+0x08)

    toc_offset = meta["toc_offset"]
    toc_count = meta["toc_count"]

    out_root = "%s - vfs" % os.path.splitext(disk.path)[0]

    for i in range(toc_count):

        meta_address = get_u32_le(exebuf, toc_offset+0x00)
        meta_offset = p_offset + meta_address - p_vaddr

        type = get_u32_le(exebuf, meta_offset+0x00)

        if type == 0x50:

            vfs_offset    = 0
            vfs_size      = get_u32_le(exebuf, meta_offset+0x0C)
            vfs_path_addr = get_u32_le(exebuf, toc_offset+0x04)
            vfs_path_off  = p_offset + vfs_path_addr - p_vaddr

            while type == 0x50:

                vfs_offset += get_u32_le(exebuf, meta_offset+0x08)

                meta_address = get_u32_le(exebuf, meta_offset+0x04)
                meta_offset = p_offset + meta_address - p_vaddr

                type = get_u32_le(exebuf, meta_offset+0x00)

            disc_path_addr = get_u32_le(exebuf, meta_offset+0x04)
            disc_path_off  = p_offset + disc_path_addr - p_vaddr
            disc_path      = get_c_string(exebuf, disc_path_off).upper()

            if disc_path in disk.toc:

                vfs_path = get_c_string(exebuf, vfs_path_off)
                vfs_dirpath = os.path.dirname(vfs_path)

                out_path = os.path.join(out_root, vfs_path)
                out_dirpath = os.path.dirname(out_path)

                if not os.path.isdir(out_dirpath):
                    os.makedirs(out_dirpath)

                disk.seek_user(disk.toc[disc_path]["lba"], vfs_offset)

                print("Extracting: %s ..." % vfs_path)

                disk.extract(out_path, vfs_size)

        toc_offset += 8

def sound_ex(disk, meta, irxbuf):

    datpath        = meta["datpath"]
    seq_start_sect = meta["seq_start_sect"]
    seq_tbl_offset = meta["seq_tbl_offset"]
    seq_ent_count  = meta["seq_ent_count"]
    stm_start_sect = meta["stm_start_sect"]
    stm_tbl_offset = meta["stm_tbl_offset"]
    stm_ent_count  = meta["stm_ent_count"]

    dat_sect = disk.toc[datpath]["lba"]

    out_root = "%s - sound" % os.path.splitext(disk.path)[0]

    # ------------------------------------------------------

    out_dir = os.path.join(out_root, "TriggerData")

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    table_offset = seq_tbl_offset

    dat_offset = seq_start_sect * 2048

    core_sfx_cnt = 0
    misc_sfx_cnt = 0

    for i in range(seq_ent_count):
        id         = get_u32_le(irxbuf, table_offset+0x00)
        #bank_sect = get_u32_le(irxbuf, table_offset+0x04)
        bank_size  = get_u32_le(irxbuf, table_offset+0x08)
        #td_sect   = get_u32_le(irxbuf, table_offset+0x0C)
        td_size    = get_u32_le(irxbuf, table_offset+0x10)

        if id >= 50000 and id < 60000:
            basename = "TD %02d - BGM %d" % (i, id)
        elif id == 0:
            basename = "TD %02d - Core SFX %02d" % (i, core_sfx_cnt)
            core_sfx_cnt += 1
        elif id == 1:
            basename = "TD %02d - Misc SFX %02d" % (i, misc_sfx_cnt)
            misc_sfx_cnt += 1

        hd_name = "%s.HD" % basename
        bd_name = "%s.BD" % basename
        td_name = "%s.TD" % basename

        hd_path = os.path.join(out_dir, hd_name)
        bd_path = os.path.join(out_dir, bd_name)
        td_path = os.path.join(out_dir, td_name)

        disk.seek_user(dat_sect, dat_offset)
        header = disk.read_user(0x24)
        hd_size = get_u32_le(header, 0x1C)
        bd_size = get_u32_le(header, 0x20)

        # ----------------------------------

        disk.seek_user(dat_sect, dat_offset)

        print("Extracting: %s ..." % hd_name)
        disk.extract(hd_path, hd_size)

        print("Extracting: %s ..." % bd_name)
        disk.extract(bd_path, bd_size)

        dat_offset += ((bank_size - 1) & ~2047) + 2048

        # ----------------------------------

        disk.seek_user(dat_sect, dat_offset)

        print("Extracting: %s ..." % td_name)
        disk.extract(td_path, td_size)

        dat_offset += ((td_size - 1) & ~2047) + 2048

        table_offset += 20

    # ------------------------------------------------------

    out_dir = os.path.join(out_root, "Streams")

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    table_offset = stm_tbl_offset

    dat_offset = stm_start_sect * 2048

    for i in range(stm_ent_count):
        #stm_sect = get_u32_le(irxbuf, table_offset+0x00)
        stm_size  = get_u32_le(irxbuf, table_offset+0x04)
        #stm_vol  = get_u32_le(irxbuf, table_offset+0x08)

        stm_name = "Stream %03d.svag" % i
        stm_path = os.path.join(out_dir, stm_name)

        disk.seek_user(dat_sect, dat_offset)

        print("Extracting: %s ..." % stm_name)
        disk.extract(stm_path, stm_size)

        dat_offset += ((stm_size - 1) & ~2047) + 2048

        table_offset += 12

def main(argc=len(sys.argv), argv=sys.argv):

    if argc != 2:
        print("Usage: %s <disk>" % argv[0])
        return 1

    path_in = os.path.realpath(argv[1])

    disk = ISOFS_IMAGE(path_in)

    for meta in metalist:

        exepath = meta["exepath"]
        if exepath in disk.toc:

            irxpath = meta["irxpath"]
            if irxpath in disk.toc:

                disk.seek_user(disk.toc[exepath]["lba"])
                exebuf = disk.read_user(disk.toc[exepath]["size"])
                if crc32(exebuf) == meta["execrc"]:

                    disk.seek_user(disk.toc[irxpath]["lba"])
                    irxbuf = disk.read_user(disk.toc[irxpath]["size"])
                    if crc32(irxbuf) == meta["irxcrc"]:

                        vfs_ex(disk, meta, exebuf)

                        sound_ex(disk, meta, irxbuf)

                        input("All done.")

                        return 0

    input("Unsupported version.")

    return 1

if __name__ == "__main__":
    main()
