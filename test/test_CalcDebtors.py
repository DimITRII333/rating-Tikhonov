# -*- coding: utf-8 -*-
import pytest
from src.Types import DataType
from src.CalcDebtors import CalcDebtors


class TestCalcDebtors:

    @pytest.fixture()
    def input_data(self) -> DataType:
        return {
            # нет задолженностей (61 — уже не долг)
            "Абрамов Петр Сергеевич": [
                ("математика", 61), ("русский язык", 76),
                ("программирование", 100)
            ],
            # ровно одна задолженность
            "Петров Игорь Владимирович": [
                ("математика", 60), ("русский язык", 80)
            ],
            # ровно две задолженности
            "Сидоров Сидор Сидорович": [
                ("математика", 45), ("физика", 58), ("история", 80)
            ],
            # ровно две задолженности, других предметов нет
            "Смирнов Олег Игоревич": [
                ("программирование", 0), ("английский язык", 55)
            ],
            # три задолженности
            "Кузнецова Анна Сергеевна": [
                ("математика", 50), ("химия", 40), ("биология", 30)
            ],
            # нет предметов
            "Новиков Николай Николаевич": []
        }

    def test_init(self, input_data: DataType) -> None:
        calc = CalcDebtors(input_data)
        assert calc.data == input_data
        assert calc.threshold == 61
        assert calc.debts_number == 2

    @pytest.mark.parametrize("student, debts", [
        ("Абрамов Петр Сергеевич", 0),
        ("Петров Игорь Владимирович", 1),
        ("Сидоров Сидор Сидорович", 2),
        ("Смирнов Олег Игоревич", 2),
        ("Кузнецова Анна Сергеевна", 3),
        ("Новиков Николай Николаевич", 0),
    ])
    def test_count_debts(self, input_data: DataType,
                         student: str, debts: int) -> None:
        assert CalcDebtors(input_data).count_debts(student) == debts

    def test_get_debtors(self, input_data: DataType) -> None:
        assert CalcDebtors(input_data).get_debtors() == [
            "Сидоров Сидор Сидорович", "Смирнов Олег Игоревич"
        ]

    def test_calc(self, input_data: DataType) -> None:
        assert CalcDebtors(input_data).calc() == 2

    def test_calc_empty_data(self) -> None:
        assert CalcDebtors({}).calc() == 0

    def test_calc_custom_parameters(self, input_data: DataType) -> None:
        assert CalcDebtors(input_data, debts_number=3).calc() == 1
        # при пороге 62 балл 61 у Абрамова становится долгом
        assert CalcDebtors(input_data, threshold=62,
                           debts_number=1).calc() == 2

    def test_unknown_student_raises(self, input_data: DataType) -> None:
        with pytest.raises(KeyError):
            CalcDebtors(input_data).count_debts("Неизвестный Студент")
