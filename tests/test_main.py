

def test_main():
    import runpy
    x=runpy.run_module('dbassembly')
    assert x['main']
    assert x['__package__'] == 'dbassembly'
    assert x['__name__'] == 'dbassembly.__main__'
