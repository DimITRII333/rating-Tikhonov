# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

import pytest
from src.Types import DataType
from src.XMLDataReader import XMLDataReader
# Модули src импортируют друг друга без префикса "src.",
# поэтому базовый класс берём из того же модуля, что и XMLDataReader
from DataReader import DataReader


class TestXMLDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> tuple[str, DataType]:
        text = '<?xml version="1.0" encoding="UTF-8" ?>\n' + \
            '<root>\n' + \
            '    <student name="Иванов Константин Дмитриевич">\n' + \
            '        <subject name="математика">91</subject>\n' + \
            '        <subject name="химия">100</subject>\n' + \
            '    </student>\n' + \
            '    <student name="Петров Петр Семенович">\n' + \
            '        <subject name="русский язык">87</subject>\n' + \
            '        <subject name="литература">78</subject>\n' + \
            '    </student>\n' + \
            '</root>\n'

        data = {
            "Иванов Константин Дмитриевич": [
                ("математика", 91), ("химия", 100)
            ],
            "Петров Петр Семенович": [
                ("русский язык", 87), ("литература", 78)
            ]
        }
        return text, data

    @staticmethod
    def write_file(tmpdir, text: str) -> str:
        p = tmpdir.mkdir("datadir").join("my_data.xml")
        p.write_text(text, encoding='utf-8')
        return str(p)

    @pytest.fixture()
    def filepath_and_data(self,
                          file_and_data_content: tuple[str, DataType],
                          tmpdir) -> tuple[str, DataType]:
        path = self.write_file(tmpdir, file_and_data_content[0])
        return path, file_and_data_content[1]

    def test_is_data_reader(self) -> None:
        assert isinstance(XMLDataReader(), DataReader)

    def test_read(self, filepath_and_data: tuple[str, DataType]) -> None:
        file_content = XMLDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]

    def test_read_twice_does_not_accumulate(
            self, filepath_and_data: tuple[str, DataType]) -> None:
        reader = XMLDataReader()
        reader.read(filepath_and_data[0])
        file_content = reader.read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]

    def test_read_strips_whitespace(self, tmpdir) -> None:
        text = '<root><student name="  Сидоров Иван  ">' + \
            '<subject name=" физика "> 64 </subject>' + \
            '</student></root>'
        path = self.write_file(tmpdir, text)
        assert XMLDataReader().read(path) == {
            "Сидоров Иван": [("физика", 64)]
        }

    def test_read_empty_root(self, tmpdir) -> None:
        path = self.write_file(tmpdir, "<root></root>")
        assert XMLDataReader().read(path) == {}

    def test_read_student_without_subjects(self, tmpdir) -> None:
        path = self.write_file(
            tmpdir, '<root><student name="Новиков Н.Н."/></root>')
        assert XMLDataReader().read(path) == {"Новиков Н.Н.": []}

    def test_student_without_name_raises(self, tmpdir) -> None:
        path = self.write_file(
            tmpdir,
            '<root><student><subject name="химия">70</subject>'
            '</student></root>')
        with pytest.raises(ValueError):
            XMLDataReader().read(path)

    def test_subject_without_name_raises(self, tmpdir) -> None:
        path = self.write_file(
            tmpdir,
            '<root><student name="Иванов И.И."><subject>70</subject>'
            '</student></root>')
        with pytest.raises(ValueError):
            XMLDataReader().read(path)

    @pytest.mark.parametrize("score", ["", "abc", "7.5"])
    def test_non_integer_score_raises(self, tmpdir, score: str) -> None:
        path = self.write_file(
            tmpdir,
            '<root><student name="Иванов И.И.">'
            f'<subject name="химия">{score}</subject>'
            '</student></root>')
        with pytest.raises(ValueError):
            XMLDataReader().read(path)

    def test_malformed_xml_raises(self, tmpdir) -> None:
        path = self.write_file(tmpdir, "<root><student name='x'></root>")
        with pytest.raises(ET.ParseError):
            XMLDataReader().read(path)

    def test_missing_file_raises(self, tmpdir) -> None:
        with pytest.raises(FileNotFoundError):
            XMLDataReader().read(str(tmpdir.join("nope.xml")))
