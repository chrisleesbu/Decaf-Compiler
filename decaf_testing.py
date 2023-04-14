import os
from decaf_checker import *
def template(monkeypatch, capsys, file, expected_out):
    monkeypatch.setattr("sys.argv", ['decaf_checker.py', os.path.join("hw2_testing", file)])
    just_scan()
    main()
    captured = capsys.readouterr()
    assert captured.out == expected_out
    
def test_empty_decaf(monkeypatch, capsys):
    template(monkeypatch, capsys, "empty.decaf", "\n")

def test_1_decaf(monkeypatch, capsys):
    expected_output = """--------------------------------------------------------------------------
Class Name: a
Superclass Name:
Fields:
FIELD 1, x, a, private, instance, int
Constructors:
Methods:
--------------------------------------------------------------------------
Class Name: b
Superclass Name: a
Fields:
FIELD 2, y, b, private, instance, int
Constructors:
Methods:
--------------------------------------------------------------------------
"""
    template(monkeypatch, capsys, "1.decaf", expected_output)

def test_2_decaf(monkeypatch, capsys):
    expected_output = """--------------------------------------------------------------------------
Class Name: a
Superclass Name:
Fields:
FIELD 1, a, a, private, instance, int
Constructors:
Methods:
--------------------------------------------------------------------------
"""
    template(monkeypatch, capsys, "2.decaf", expected_output)