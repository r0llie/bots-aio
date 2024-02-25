from web3.exceptions import ContractLogicError, TransactionNotFound
from colorama import init, Fore, Back, Style
from eth_account import Account
from web3 import Web3
import web3
import time, os, json
from utils.utils import claim_all_bots, show_profitability_table, send_all_bots_to_mission, get_user_missions  # Assuming you've moved logic to a function named process_bot
from keyauthmain import answer


def clear():
    os.system('cls')
    print("""
            ____________________________________________           
                                  __    __    _       
                  _____  ____    / /   / /   (_)  ___ 
                 / ___/ / __ \\  / /   / /   / /  / _ \\
                / /    / /_/ / / /   / /   / /  /  __/
               /_/     \\____/ /_/   /_/   /_/   \\___/ 
            ____________________________________________    
            """)

def menu():
    clear()
    os.system('')
    try:
        clear()
        print('\033[39m'+ """                                

        """+ Fore.RED + """[1]""" '\033[39m' + """ Bütün Botlarını Claimle
        """+ Fore.RED + """[2]""" '\033[39m' + """ Botlarını Göreve Yolla
        """+ Fore.RED + """[3]""" '\033[39m' + """ Görevdeki Botlarının Durumu
        """+ '\033[39m')
        ans = input("            Seçenek: ")
        if ans == "1":
            clear()
            claim_all_bots()
            menu()

        elif ans == "2":
            os.system('cls')
            show_profitability_table()
            missionId = input(Fore.GREEN + "         Mission ID : "+ '\033[39m')
            if int(missionId) not in range(1,28):
                print('\033[39m' +"[-] " + Fore.RED +f'Yanlış bir şey girdiniz. Menüye geri yönlendiriyorum.' + '\033[39m')
                time.sleep(5)
                menu()
            else:
                send_all_bots_to_mission(int(missionId))
                print('\033[39m' +"[+] " + Fore.GREEN +f' İşlem bitti.\n Menüye geri yönlendiriyorum.' + '\033[39m')
                time.sleep(5)
                menu()
        elif ans == "3":
            clear()
            get_user_missions()
            menu()
        else:
            print("\nYanlış seçenek.")
            time.sleep(1)
            clear()
            menu()
    except KeyboardInterrupt:
        os._exit(1)



if __name__ == "__main__":
    init()
    os.system('cls')
    answer()
    menu()
