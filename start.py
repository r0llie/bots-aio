from web3.exceptions import ContractLogicError, TransactionNotFound
from colorama import init, Fore, Back, Style
from eth_account import Account
from web3 import Web3
import web3
import time, os, json
from utils.utils import claim_all_bots, show_profitability_table, send_all_bots_to_mission, get_user_missions, clear  # Assuming you've moved logic to a function named process_bot


def menu():
    clear()
    os.system('')
    try:
        clear()
        print('\033[39m'+ """                                

        """+ Fore.RED + """[1]""" '\033[39m' + """ Claim all bots
        """+ Fore.RED + """[2]""" '\033[39m' + """ Send all bots to mission
        """+ Fore.RED + """[3]""" '\033[39m' + """ Check bots
        """+ '\033[39m')
        ans = input("            Choice: ")
        if ans == "1":
            clear()
            claim_all_bots()
            menu()

        elif ans == "2":
            os.system('cls')
            show_profitability_table()
            missionId = input(Fore.GREEN + "         Mission ID : "+ '\033[39m')
            if int(missionId) not in range(1,28):
                print('\033[39m' +"[-] " + Fore.RED +f'Wrong missonid input.' + '\033[39m')
                time.sleep(5)
                menu()
            else:
                send_all_bots_to_mission(int(missionId))
                print('\033[39m' +"[+] " + Fore.GREEN +f' Finished.\n Redirecting back to menu.' + '\033[39m')
                time.sleep(5)
                menu()
        elif ans == "3":
            clear()
            get_user_missions()
            menu()
        else:
            print("\nWrong choice.")
            time.sleep(1)
            clear()
            menu()
    except KeyboardInterrupt:
        os._exit(1)



if __name__ == "__main__":
    init()
    os.system('cls')
    menu()
