# -*- coding: utf-8 -*-
from src.main import get_path_from_arguments, get_reader, main
from TextDataReader import TextDataReader
from XMLDataReader import XMLDataReader
import pytest


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(
        correct_arguments_string: tuple[list[str], str]) -> None:
    path = get_path_from_arguments(correct_arguments_string[0])
    assert path == correct_arguments_string[1]


def test_get_path_from_noncorrect_arguments(
        noncorrect_arguments_string: list[str]) -> None:
    with pytest.raises(SystemExit) as e:
        get_path_from_arguments(noncorrect_arguments_string[0])
    assert e.type == SystemExit


@pytest.mark.parametrize("path, reader_type", [
    ("data/data.txt", TextDataReader),
    ("data/data.xml", XMLDataReader),
    ("DATA.XML", XMLDataReader),
])
def test_get_reader_by_extension(path: str, reader_type: type) -> None:
    assert isinstance(get_reader(path), reader_type)


@pytest.mark.parametrize("path", ["data/data.json", "data/data"])
def test_get_reader_unsupported_extension(path: str) -> None:
    with pytest.raises(ValueError):
        get_reader(path)


def test_main_prints_debtors_count(tmpdir, monkeypatch, capsys) -> None:
    p = tmpdir.join("data.xml")
    p.write_text('<root>'
                 '<student name="Иванов И.И.">'
                 '<subject name="математика">40</subject>'
                 '<subject name="химия">50</subject>'
                 '</student>'
                 '<student name="Петров П.П.">'
                 '<subject name="математика">90</subject>'
                 '</student>'
                 '</root>', encoding='utf-8')
    monkeypatch.setattr("sys.argv", ["main.py", "-p", str(p)])
    main()
    output = capsys.readouterr().out
    assert "Rating: " in output
    assert "Students with debts in exactly two subjects:  1" in output
