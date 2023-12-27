protected  = 0x555555555000

#flag{y0ur_n3xt_s0lv3_1s...y7m3v}

elf_position = 0x1011b9
elf_start = 0x100000


def patch(unpacked):
    with open("./chall", "r+b") as f:
        original = f.read()
    patch_len = len(unpacked)
    offset = elf_position - elf_start
    print("offset:", hex(offset))
    print("offset + patch_len:", hex(offset+patch_len))
    patched = original[0:offset]+unpacked+original[offset+patch_len:]
    with open("./patched_2", "wb") as patched_file:
        patched_file.write(patched)


with open("./patch_2", "rb") as f_unpacked:
    unpacked = f_unpacked.read()
    patch(unpacked)
