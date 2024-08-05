import csv
import sys
import os
from importlib import reload

current_dir = os.path.dirname(os.path.abspath(__file__))
ds_dir = "C://Users//17818//Documents//Data Source"
sys.path.append(current_dir)

import script


def convert_size(bytes):

    for i in ["Byte", "KB", "MB", "GB"]:
        if (bytes / 1024) < 1:
            return "%.2f%s" % (bytes, i)
        bytes = bytes / 1024


class GateIDLE:
    def __init__(self):
        self.map = {
            "ld": "load_deals",
            "lk": "load_klines",
            "rs": "run_script",
            "cls": "cls",
        }
        self.db = {"klines": {}, "deals": {}}
        self.category_map = {
            "klines": os.path.join(ds_dir, "candlesticks"),
            "deals": os.path.join(ds_dir, "Data Source", "deals"),
        }

    def cls(self):
        os.system("cls")

    def load_files(self, category, file_name):
        file_path = os.path.join(self.category_map[category], file_name)

        print("loading {}...".format(file_path))
        with open(file_path, "r", newline="") as f:
            self.db[category][file_name] = list(csv.reader(f))

    def load_deals(self):
        while True:
            contents = os.listdir(self.category_map["deals"])
            file_list = []

            for i in range(len(contents)):  # divide files into loaded and optional
                file_name = os.path.join(self.category_map["deals"], contents[i])
                file_size = os.path.getsize(file_name)
                if contents[i] in self.db["deals"].keys():
                    file_list.append([i, contents[i], file_size, 1])
                else:
                    file_list.append([i, contents[i], file_size, 0])

            self.cls()  # print loaded
            print("--------- Loaded Files List ---------\n")
            count, total_size = 0, 0
            for file in file_list:
                if file[3] == 1:
                    print("%-4d%-24s%-s" % (file[0], file[1], convert_size(file[2])))
                    count += 1
                    total_size += file[2]
            print("\nTotal:{}, {}\n\n\n".format(count, convert_size(total_size)))

            print("--------- Optional List -------------\n")  # print optional
            for file in file_list:
                if file[3] == 0:
                    print("%-4d%-24s%-s" % (file[0], file[1], convert_size(file[2])))
            print("\n")


            index = input(('Input index to load or "q" to cancel:'))
            if index == "q":
                self.cls()
                return True
            else:
                try:
                    file = file_list[int(index)]
                    if file[3] == 1:
                        del self.db["deals"][file[1]]
                    else:
                        self.load_files("deals", contents[int(index)])
                except (ValueError, IndexError):
                    continue

    def run_script(self):
        reload(script)
        script.main(self)

    def decode(self, message):
        message = message.split()
        if message[0] in self.map.keys():
            func = self.map[message[0]]
        else:
            print("unidentifiable.")
            return False

        try:
            if len(message) == 1:
                eval("self.{}()".format(func))
            else:
                params = tuple(message[1:])
                eval("self.{}{}".format(func, params))
        except Exception as e:
            print(e)

    def response(self, message):
        if message.isspace() or len(message) == 0:
            pass
        else:
            self.decode(message)

    def ui(self):
        self.cls()
        while True:
            self.response(input(">>>"))


if __name__ == "__main__":
    gi = GateIDLE()
    gi.ui()


