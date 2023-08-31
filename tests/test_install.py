from hmbtg_utils.install import *

class TestCommand(Command):
    pass


def test_context():
    context = InstallContext()

    assert True
    
def test_add_to_context():
    context = InstallContext()
    context.add(TestCommand())
    assert len(context) == 1
    

def test_add_and_remove_context():
    context = InstallContext()
    cmd = TestCommand()
    context.add(cmd)
    context.remove(cmd)
    assert len(context) == 0