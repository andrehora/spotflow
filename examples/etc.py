# x = ClassC.foo
# import dis
# # x = dis.dis(ClassC.__init__)
# # print(x)
# # LOAD_GLOBAL = dis.opmap['LOAD_GLOBAL']
# bytecode = dis.Bytecode(ClassC.__init__.__code__)
# print(bytecode.dis())
# for instr in bytecode:
#     print(instr)