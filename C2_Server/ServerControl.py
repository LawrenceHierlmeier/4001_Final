import time
import os
from tabulate import tabulate

def progressBar(current, total, barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

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
            open(f'Sessions/{subfolders[num]}/next', "w").write(nextInstr)

main()
