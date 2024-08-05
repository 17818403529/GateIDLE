import csv
import os

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

ar = {}
vf = VirtualFolder(r"C:\Users\17818\Documents\Data Source\deals",ar)
while True:
    vf.operate()