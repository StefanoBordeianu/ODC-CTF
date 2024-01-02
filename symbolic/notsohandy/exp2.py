import angr
import claripy

TARGET = 0x0101422
ENTRY = 0x001012d6
AVOID = [0x001013dc, 0x001012a5, 0x00101422]
angr.options.LAZY_SOLVES

chars = [claripy.BVS(f"c_{i}",size = 8) for i in range(49)]
flag = claripy.Concat(*chars)

counter = 0

class Fakelen(angr.SimProcedure): # create a custom SimProc
    def run(self):
        
        return self.state.solver.BVV(49, 64)



proj = angr.Project('./notsohandy', auto_load_libs=False)
proj.hook_symbol('strlen', Fakelen(), replace=True)

argv = ['./notsohandy']
argv.append(flag) # symbolic first argument
inital_state = proj.factory.blank_state(args=argv,addr = ENTRY)

for i in range(49):
    inital_state.solver.add(chars[i] >= 0x20)
    inital_state.solver.add(chars[i] <= 0x7e)

#inital_state.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)
inital_state.options.add(angr.options.LAZY_SOLVES)
# inital_state.solver.add(chars[30] == 0)
# inital_state.solver.add(chars[31] == 0)
# inital_state.solver.add(chars[29] == 0)


simgr = proj.factory.simulation_manager(inital_state)
print("start exploring")
simgr.explore(find=TARGET)
print("ended exploring")

if simgr.found:
 print("FOUND WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
 found = simgr.found[0]
 print(str(found.solver.eval(flag).to_bytes(49,byteorder='big')))


                                