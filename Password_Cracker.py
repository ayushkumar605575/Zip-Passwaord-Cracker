import sys
from concurrent.futures import ThreadPoolExecutor
from itertools import permutations
from os import remove
from time import time

from colorama import Fore, init
from pyzipper import AESZipFile
from tqdm import tqdm

c=0
try:
    from pyperclip import copy
except ImportError:
    c=1
init(True)
INFO = '''
*=======================================*
|...........ZIP PASS CRACKER............|
+---------------------------------------+
|-> Version: 3.5.6                      |
|-> Developer: Ayush Kumar              |
|-> Late_Updated: 08/03/2023            |
*=======================================*
'''


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def read_in_chunks(file_object, chunk_size=2048):
    while 1:
        if data := file_object.readlines(chunk_size):
            yield data
        else:
            break
def pass_gen_2(words):
    n_words = list(range(len(words),0,-1))
    print(n_words)
    for i in range(1,((len(n_words)-1)//2)+1,2):
        n_words[i],n_words[-i]=n_words[-i],n_words[i]
    print(n_words)
    with open("./Gen-Pass.txt","w",encoding='utf-8') as file:
        for i in tqdm(n_words,total=len(n_words),unit="words"):
            for word in permutations(words,i):
                file.write("".join(word)+'\n')
def Pass_Gen():
    words = []
    print(Fore.YELLOW+"[!] Input all the keywords you remember about your Passcode \n(Press Enter without entering anything when you are done.)\n")
    print(Fore.GREEN+'\n[!] Enter the terms you remember for your password (MAX -> 9 Keywords) ')
    while 1:
        hint = str(input(f"{Fore.LIGHTRED_EX}(Case sensitive): - "))
        if not hint:
            break
        elif hint not in words:
            words.append(hint)
    pass_gen_2(words)
# Pass_Gen()
# exit()
def Zip_Password_cracker(zip_file):
    print()
    #Getting file inside the zip file with smallest size for attack
    if 'Zip pass key.txt' in zip_file.namelist():
        file_name = 'Zip pass key.txt'
    else:
        min_size = min(i.file_size for i in (zip_file.filelist) if i.file_size != 0)
        file_name = [i.filename for i in (zip_file.filelist) if i.file_size == min_size][0]
            # print(file_name)
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

    print(Fore.LIGHTWHITE_EX+"[!] Cracking ZIP file Password\n")
    t=time()
    with open(wordlist,encoding='utf-8') as f:
        for words in tqdm(read_in_chunks(f),total=Total,unit="threads"):
            if pswd!=None:
                exc.shutdown()
                break
            with ThreadPoolExecutor() as exc:
                r=exc.submit(Worker,words,file_name)
        f.close()
    zip_file.close()

    print(Fore.LIGHTGREEN_EX+"\nTotal time taken "+Fore.LIGHTCYAN_EX+"--⇒>►▶ "+Fore.WHITE+str(round((time()-t),3)))

def Worker(words,file_name):
    global pswd
    for w in words:
        try:
            zip_file.open(file_name,'r',pwd=w.strip().encode()).read(1)
            if c==0:
                copy(w)
                print("\n\n\n"+Fore.LIGHTYELLOW_EX+"Password is"+Fore.LIGHTCYAN_EX+" --⇒> "+Fore.LIGHTGREEN_EX+w+Fore.LIGHTMAGENTA_EX+"\t(COPIED TO CLIPBOARD)"+"\n\n\n")
            else:
                print("\n\n\n"+Fore.LIGHTYELLOW_EX+"Password is"+Fore.LIGHTCYAN_EX+" --⇒> "+Fore.LIGHTGREEN_EX+w+Fore.LIGHTRED_EX+"\tCOPY THE PASSWORD"+"\n\n\n")
            pswd= w
            break
        except Exception:
            continue
if __name__ == '__main__':
    workers, pswd, wordlist = [],None,"./Gen-Pass.txt"
    print(INFO)
    print(Fore.LIGHTWHITE_EX+'''\n[!] Press '1' for Cracking Passcode.\n
[!] Press '2' for Cracking Passcode with your own password_list.\n
[!] Press '3' for Generating Passwords for 3rd-Party Software.\n
[!] Press '9' for exiting program.
''')
while 1:
    choice = int(input(Fore.LIGHTCYAN_EX+"\nEnter your Choice : - "))
    if choice == 9:
        print(f'{Fore.YELLOW}Exiting...')
        sys.exit()
    elif choice in {1, 2}:
        if choice==1:
            Pass_Gen()
        if choice == 2:
            wordlist = str(input(f"{Fore.YELLOW}Enter Location of Password List : - ")) or "./Gen-Pass.txt"
        while 1:
            zip_file_name = str(input(Fore.LIGHTCYAN_EX+'\nEnter Location of ZIP File : - ')).replace('"',"")
            try:
                zip_file = AESZipFile(zip_file_name)
                zip_file.open(name=zip_file.namelist()[0]).read(1)
                print(f"{Fore.LIGHTRED_EX}File is not password Protected")
            except FileNotFoundError as e:
                print("\n",e)
                continue
            except RuntimeError:
                break
        Zip_Password_cracker(zip_file)
        print(
            f"{Fore.LIGHTYELLOW_EX}Do you want to remove the temporary password Dictionary ?"
        )
        if int(input("Enter 1 or 0 : -> ")):
            remove(wordlist)
            print(f"{Fore.LIGHTRED_EX}File Removed")
        print(f'{Fore.YELLOW}Exiting...')
    elif choice ==3:
        Pass_Gen()
