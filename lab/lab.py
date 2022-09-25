import unittest
import dis


def run_unittest(test_case):
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
    runner.run(suite)


def is_super_call(frame):
    instructions = dis.Bytecode(frame.f_code)
    for instr in instructions:
        if instr.offset == frame.f_lasti and instr.opname == 'LOAD_GLOBAL' and instr.argval == 'super':
            return True
    return False


def handle_bytecode():

    class Foo:
        def bar(self):
            if 2 != 2:
                print()
            return 'a,b,c'.split()

    print(dis.dis(Foo.bar))
    RETURN_VALUE = dis.opmap['RETURN_VALUE']
    print('RETURN_VALUE', RETURN_VALUE)

    bytecode = dis.Bytecode(Foo.bar)
    print(bytecode.dis())
    for instr in bytecode:
        print(instr)


def runpy():
    import runpy
    msg = {'msg': [1,2,3]}
    runpy.run_path("comparator.py", init_globals=msg)


# handle_bytecode()