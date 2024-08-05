import csv
import sys
import os
from importlib import reload

current_dir = os.path.dirname(os.path.abspath(__file__))
ds_dir = "C://Users//17818//Documents//Data Source"
sys.path.append(current_dir)

import script


class VirtualFolder:
    def __init__(self, path, anchor):
        self.path = path
        self.anchor = anchor
        self.contents = None

    def convert_size(self, bytes):

        for i in ["Byte", "KB", "MB", "GB"]:
            if (bytes / 1024) < 1:
                return "%.2f%s" % (bytes, i)
            bytes = bytes / 1024
    
    def read_folder(self):
        self.contents = os.listdir(self.path)
        self.file_list = []

        for i in range(len(self.contents)):  # divide files into loaded and optional

            file_name = os.path.join(self.path, self.contents[i])
            file_size = os.path.getsize(file_name)

            if self.contents[i] in self.anchor.keys():
                self.file_list.append([i, self.contents[i], file_size, 1])
            else:
                self.file_list.append([i, self.contents[i], file_size, 0])

        
    def convert_file(self, file):
        return list(csv.reader(file))

    def load_file(self, filename):
        file_path = os.path.join(self.path, filename)
        print("loading {}...".format(file_path))
        with open(file_path, "r", newline="") as f:
            self.anchor[filename] = self.convert_file(f)
    
    def operate(self):
        while True:
            self.read_folder()

            os.system("cls")
            print("--------- Loaded Files List ---------\n")
            count, total_size = 0, 0
            for file in self.file_list:
                if file[3] == 1:
                    print("%-4d%-24s%-s" % (file[0], file[1], self.convert_size(file[2])))
                    count += 1
                    total_size += file[2]
            print("\nTotal:{}, {}\n\n\n".format(count, self.convert_size(total_size)))

            print("--------- Optional List -------------\n")  # print optional
            for file in self.file_list:
                if file[3] == 0:
                    print("%-4d%-24s%-s" % (file[0], file[1], self.convert_size(file[2])))
            print("\n")


            index = input(('Input index to load or "q" to cancel:'))
            if index == "q":
                os.system("cls")
                return True
            else:
                try:
                    file = self.file_list[int(index)]
                    if file[3] == 1:
                        del self.anchor[file[1]]
                    else:
                        self.load_file(self.contents[int(index)])
                except (ValueError, IndexError):
                    continue


class GateIDLE:
    def __init__(self):
        self.map = {
            "ld": "load_deals",
            "lk": "load_klines",
            "rs": "run_script",
            "cls": "cls",
        }
        self.db = {"klines": {}, "deals": {}}
        self.vf_klines = VirtualFolder(os.path.join(ds_dir, "candlesticks"),self.db["klines"])
        self.vf_deals = VirtualFolder(os.path.join(ds_dir, "deals"),self.db["deals"])

    def cls(self):
        os.system("cls")

    def load_deals(self):
        self.vf_deals.operate()
    
    def load_klines(self):
        self.vf_klines.operate()

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

