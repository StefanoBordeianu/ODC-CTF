import z3

MAG_0 = 0x0000000000000000
MAG_1 = 0xdfb0089900000000

def m_seedRand(state, seed):
    state[0] = seed & 0xffffffff
    index = 1
    while (index < 0x270):
      state[index] = state[index - 1] * 0x17b5
      index = index + 1
    return index



def genRandLong(index, state):
  
  if ((0x26f < index or index < 0)):
    if ((0x270 < index or index < 0)):
        m_seedRand(state,0x1105)
    for index in range(0xe3):
      uVar2 = state[index + 1]
      state[index] = state[index + 0x18d] ^ z3.LShR(((uVar2 & 0x7fffffff) | (state[index] & 0x80000000)), 1) ^ func(uVar2 & 1)
    for index in range(0xe3, 0x26f):
      uVar2 = state[index + 1]
      state[index] = state[index - 0xe3] ^ z3.LShR((uVar2 & 0x7fffffff | state[index] & 0x80000000), 1) ^ func(uVar2 & 1)
        
    uVar2 = state[0]
    state[0x26f] = state[0x18c] ^ z3.LShR((uVar2 & 0x7fffffff | state[0x26f] & 0x80000000), 1) ^ func(uVar2 & 1)
    index = 0
  
  iVar2 = index
  index = iVar2 + 1
  uVar1 = state[iVar2] ^ z3.LShR((state[iVar2]), 0xb)
  uVar1 = uVar1 ^ (uVar1 << 7) & 0x9d2c5680
  uVar1 = uVar1 ^ (uVar1 << 0xf) & 0xefc60000
  out = uVar1 ^ z3.LShR(uVar1, 0x12)
  return out, index

def func(value):
  if(value == 1):
      return MAG_1
  return MAG_0



def execution(seed):
  state = [0]*0x270
  index = m_seedRand(state, seed)
  for i in range(1000):
    x, index = genRandLong(index, state)
  x, index = genRandLong(index, state)
  print("Execution Finished")
  return x
      
solver = z3.Solver()

seed = z3.BitVec("seed", 32)

val = execution(seed)

solver.add(val == 0xf4df3126)
print(solver.assertions())

check = solver.check()
m = solver.model()
print(m)