import angr
import claripy

TARGET = 0x001016a1
ENTRY = 0X001015c8


chars = [claripy.BVS(f"c_{i}",size = 8) for i in range(4)]
flag = claripy.Concat(*chars)

proj = angr.Project("./pnrg")

inital_state = proj.factory.blank_state(kwargs={'param addr':ENTRY})

# inital_state.solver.add(chars[30] == 0)
# inital_state.solver.add(chars[31] == 0)
# inital_state.solver.add(chars[29] == 0)
inital_state.regs.rdx = flag
inital_state.regs.eax = flag
inital_state.options.add(angr.options.LAZY_SOLVES)
simgr = proj.factory.simulation_manager(inital_state)
simgr.explore(find=TARGET)

if simgr.found:
 print("FOUND WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
 found = simgr.found[0]
 print(str(found.solver.eval(flag).to_bytes(4,byteorder='big')))
else:
 print("NOOOOOOOOOOOOOOOOOOOOOO :(")
