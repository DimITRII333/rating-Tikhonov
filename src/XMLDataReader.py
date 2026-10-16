import xml.etree.ElementTree as ET

from Types import DataType
from DataReader import DataReader


class XMLDataReader(DataReader):
    """Чтение данных о студентах из XML-файла.

    Ожидаемый формат:
        <root>
            <student name="Иванов Иван Иванович">
                <subject name="математика">67</subject>
            </student>
        </root>
    """

    STUDENT_TAG = "student"
    SUBJECT_TAG = "subject"
    NAME_ATTR = "name"

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        self.students = {}
        root = ET.parse(path).getroot()
        for student in root.iter(self.STUDENT_TAG):
            key = self._get_name(student)
            self.students[key] = [
                (self._get_name(subject), self._get_score(subject))
                for subject in student.iter(self.SUBJECT_TAG)
            ]
        return self.students

    def _get_name(self, element: ET.Element) -> str:
        name = (element.get(self.NAME_ATTR) or "").strip()
        if not name:
            raise ValueError(
                f"Element <{element.tag}> has no '{self.NAME_ATTR}' attribute")
        return name

    @staticmethod
    def _get_score(subject: ET.Element) -> int:
        return int((subject.text or "").strip())
