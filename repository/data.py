from dataclasses import dataclass


@dataclass
class DataItem:
    content: str
    shortcut: str


@dataclass
class DataSet:
    data_items: list[DataItem]

    def add_data(self, data_item: DataItem) -> None:
        self.data_items.append(data_item)

    def new_pk(self) -> int:
        return len(self.data_items) + 1


INITIAL_DATA_SET = [
    DataItem(
        shortcut="1", content=("chess_id=FR001, last_name=Carlsen, first_name=Magnus")
    ),
]


class DataRepository:
    data: DataSet

    def __init__(self) -> None:
        self.data = DataSet(INITIAL_DATA_SET)

    def read_data(self) -> DataSet:
        return self.data

    def write_data(self, content: str):
        new_pk = self.data.new_pk()
        data_item: DataItem = DataItem(shortcut=str(new_pk), content=content)
        self.data.add_data(data_item)
