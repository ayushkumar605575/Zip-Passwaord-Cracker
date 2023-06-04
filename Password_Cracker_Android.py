import sys
from itertools import permutations
from multiprocessing import Process, cpu_count
from os import path, remove
from threading import Thread
from time import sleep, time

from colorama import Fore, init
from pyzipper import AESZipFile
from tqdm import tqdm

init(True)

INFO = '''
      *=======================================*
      |...........ZIP PASS CRACKER............|
      +---------------------------------------+
      |-> Version: 4.5.6-A                    |
      |-> Developer: Ayush Kumar              |
      |-> Late_Updated: 11/03/2023            |
      *=======================================*
'''

def Worker(words,file_name):
    global pswd
    for w in words:
        try:
            zip_file.open(file_name,'r',pwd=(w.strip().encode())).read(1)
            pswd = w
            print(f"{Fore.LIGHTYELLOW_EX}Password is : - {Fore.GREEN}{w}")
            if pswd != None:
                return
        except Exception:
            continue

def Processes(worker):
    if pswd != None:
        return
    for i in tqdm(workers,total=len(worker),unit="threads"):
        if pswd != None:
            return
        i.start()
    for i in workers:
        if pswd != None:
            return
        i.join()

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def pass_gen_2(words):
    with open("./Gen-Pass.txt","w",encoding='utf-8') as file:
        for i in tqdm(range(len(words),0,-1),unit="words"):
            for word in permutations(words,i):
                file.write("".join(word)+'\n')

def Pass_Gen():
    words = []
    print(Fore.YELLOW+"[!] Input all the keywords you remember about your Passcode \n(Press Enter without entering anything when you are done.)\n")
    print(Fore.GREEN+'\n[!] Enter the terms you remember for your password ')
    while 1:
        hint = str(input(f"{Fore.LIGHTRED_EX}(Case sensitive): - "))
        if not hint:
            break
        elif hint not in words:
            words.append(hint)
    sleep(1)
    print(Fore.LIGHTYELLOW_EX+"\n[!] Generating Passwords\n")
    sleep(1)
    pass_gen_2(words)

    if choice == 3:
        print(Fore.LIGHTGREEN_EX+"\nLocation of Password File : - "+str(path.realpath('./Gen-Pass.txt')))


def Start_cracking(worker,_cpu):
    Processor = list(split(worker,_cpu))
    no_of_process = [Process(target=Processes,args=(i,)) for i in Processor if len(i)!=0]
    for i in no_of_process:
        i.start()
    for i in no_of_process:
        if pswd is None:
            i.join()
        else:
            return

#Useable
def read_in_chunks(file_object, chunk_size=2048):
    while 1:
        if data := file_object.readlines(chunk_size):
            yield data
        else:
            break

def details():
    Total, T_pass = 0 , 0
    with open(wordlist,encoding='utf-8') as f:
        for words in read_in_chunks(f):
            T_pass+=len(words)
            Total+=1

    print(
        f"{Fore.MAGENTA}[!] Total passwords to test:",
        T_pass,
        ' in ',
        Total,
        ' parts.\n',
    )


def Zip_Password_cracker():
    #Getting file inside the zip file with smallest size for attack
    if 'Zip pass key.txt' in zip_file.namelist():
        file_name = 'Zip pass key.txt'
    else:
        min_size = min(i.file_size for i in (zip_file.filelist) if i.file_size != 0)
        file_name = [i.filename for i in (zip_file.filelist) if i.file_size == min_size][0]

    details()
    print(Fore.LIGHTWHITE_EX+"[!] Cracking ZIP file Password\n")
    with open(wordlist,encoding='utf-8') as f:
        for words in read_in_chunks(f):
            workers.append(Thread(target=Worker,args=(words,file_name,)))

if __name__ == '__main__':
    workers,wordlist,pswd =[], "./Gen-Pass.txt",None
    print(INFO)
    print(Fore.LIGHTWHITE_EX+'''\n[!] Press '1' for Cracking Passcode.\n
[!] Press '2' for Cracking Passcode with your own password_list.\n
[!] Press '3' for Generating Passwords for 3rd-Party Software.\n
[!] Press '0' for Using your own hint file. (Admin Only)\n
[!] Press '9' for exiting program.
''')
while 1:
    choice = int(input(Fore.LIGHTCYAN_EX+"\nEnter your Choice : - "))
    if choice == 9:
        print(Fore.YELLOW+'Exiting...')
        sys.exit()
    elif choice ==1 or choice ==2:
        if choice==1:
            Pass_Gen()
        if choice == 2:
            wordlist = str(input(Fore.YELLOW+"Enter Location of Password List : - "))
            if len(wordlist) == 0:
                wordlist = "./Gen-Pass.txt"
        while 1:
            try:
                zip_file = AESZipFile(str(input(Fore.LIGHTCYAN_EX+'\nEnter Location of ZIP File : - ')).replace('"',""))
            except FileNotFoundError:
                print(Fore.LIGHTRED_EX+"File does not exists. \n")
            try:
                zip_file.testzip()         
                print(Fore.LIGHTYELLOW_EX+"File is not password protected.")
                continue
            except RuntimeError:
                break
        cpu = int(input(Fore.LIGHTMAGENTA_EX+"Number of CPU Cores to use : - "))
        if 0 < cpu <= cpu_count():
            print("Using "+str(cpu)+" CPU Cores")
        else:
            cpu = cpu_count()//2
            print(Fore.LIGHTRED_EX+"Due to certain system limitations, program is using "+str(cpu)+" CPU cores")
        t=time()
        Zip_Password_cracker()
        Start_cracking(workers,cpu)
        print(time()-t)
        zip_file.close()
        print(Fore.LIGHTYELLOW_EX+"Do you want to remove the temporary password Dictionary ?")
        if int(input("Enter 1 or 0 : -> ")):
            remove(wordlist)
            print(Fore.LIGHTRED_EX+"File Removed")
        print(Fore.YELLOW+'Exiting...')
    elif choice == 3:
        Pass_Gen()