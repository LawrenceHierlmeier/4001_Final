import time
import os
from tabulate import tabulate

def main():
    while True:
        subfolders = [f.name for f in os.scandir('Sessions') if f.is_dir()]
        implants = []
        for i in range(len(subfolders)):
            status = open(f'Sessions/{subfolders[i]}/next', "r").read()
            implants.append([i, subfolders[i], status])
        print(tabulate(implants, headers=['Num', 'SessionID', 'Status']))

        num = int(input("Select Num: "))
        if num in range(len(subfolders)):
            implants[num][2] = open(f'Sessions/{subfolders[num]}/next', "r").read()
            print(tabulate([implants[num]], headers=['Num', 'SessionID', 'Status']))
            nextInstr = input("Enter Next Instruction: ")
            while(nextInstr != '-1'):
                open(f'Sessions/{subfolders[num]}/next', "w").write(nextInstr)
                implants[num][2] = open(f'Sessions/{subfolders[num]}/next', "r").read()
                print(tabulate([implants[num]], headers=['Num', 'SessionID', 'Status']))
                nextInstr = input("Enter Next Instruction: ")

main()
