import argparse
import os
import sys

from CalcDebtors import CalcDebtors
from CalcRating import CalcRating
from DataReader import DataReader
from TextDataReader import TextDataReader
from XMLDataReader import XMLDataReader

READERS: dict[str, type[DataReader]] = {
    ".txt": TextDataReader,
    ".xml": XMLDataReader,
}


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def get_reader(path: str) -> DataReader:
    extension = os.path.splitext(path)[1].lower()
    if extension not in READERS:
        raise ValueError(f"Unsupported data file format: '{extension}'")
    return READERS[extension]()


def main():
    path = get_path_from_arguments(sys.argv[1:])

    reader = get_reader(path)
    students = reader.read(path)
    print("Students: ", students)

    rating = CalcRating(students).calc()
    print("Rating: ", rating)

    debtors = CalcDebtors(students).calc()
    print("Students with debts in exactly two subjects: ", debtors)


if __name__ == "__main__":
    main()
