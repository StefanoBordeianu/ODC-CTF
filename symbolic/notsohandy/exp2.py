import angr
import claripy

TARGET = 0x0101422
base = 0x0100000
angr_base = 0x400000
AVOID = [0x001013dc, 0x001012a5, 0x00101422]
angr.options.LAZY_SOLVES

chars = [claripy.BVS(f"c_{i}",size = 8) for i in range(49)]
flag = claripy.Concat(*chars)


proj =angr.project.Project('./notso_original')

argv = ['./notso_original']
argv.append(flag) # symbolic first argument
inital_state = proj.factory.entry_state(args=argv)

for i in range(49):
    inital_state.solver.add(chars[i] >= 0x20)
    inital_state.solver.add(chars[i] <= 0x7e)

inital_state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)
inital_state.options.add(angr.options.LAZY_SOLVES)


simgr = proj.factory.simulation_manager(inital_state)
print("start exploring")
simgr.explore(find=(TARGET-base+angr_base))
print("ended exploring")

if simgr.found:
 print("FOUND WOOOOOOOOOOOOOOOOOOSOOOOOOOOOOOOOOOOOOOOOOOOOOO")
 found = simgr.found[0]
 print(str(found.solver.eval(flag).to_bytes(49,byteorder='big')))