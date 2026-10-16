from Types import DataType


class CalcDebtors:
    """Подсчёт студентов, имеющих академические задолженности
    (балл ниже порога) ровно по заданному числу предметов."""

    DEBT_THRESHOLD: int = 61
    DEBTS_NUMBER: int = 2

    def __init__(self, data: DataType,
                 threshold: int = DEBT_THRESHOLD,
                 debts_number: int = DEBTS_NUMBER) -> None:
        self.data: DataType = data
        self.threshold: int = threshold
        self.debts_number: int = debts_number

    def count_debts(self, student: str) -> int:
        return sum(1 for _, score in self.data[student]
                   if score < self.threshold)

    def get_debtors(self) -> list[str]:
        return [student for student in self.data
                if self.count_debts(student) == self.debts_number]

    def calc(self) -> int:
        return len(self.get_debtors())
