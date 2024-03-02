from .configure import load_config, load_profitability_table  # Yapılandırma bilgilerini yükleyin
from web3.exceptions import ContractLogicError, TransactionNotFound
from web3 import Web3
import json
import os
from time import sleep
from colorama import init, Fore, Back, Style
from tabulate import tabulate
from datetime import datetime, timedelta

init()

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


def claim_all_bots():

    w3, wallet_address, contract1, contract2, private_key, bot_ids , maxfeeaccepted = load_config()  # Yapılandırma bilgilerini yükleyin
    sleep(1)
    clear()
    nonce = w3.eth.get_transaction_count(wallet_address)
    gas_price = w3.eth.gas_price
    max_fee = w3.to_wei(maxfeeaccepted, 'ether')

    if len(bot_ids) <= 0:
        clear()
        print('\033[39m' + "Check bot ids in config.")
        print('\n *program will close after 3 secs*')
        sleep(3)
        os._exit(1)
    else:

        for bot_id in bot_ids:
            print('\033[39m' + f"Claiming BotID : {bot_id}")
            try:
                # Prepare the transaction without specifying 'gas' initially
                tx = contract2.functions.claimPoints(int(bot_id)).build_transaction({
                    'nonce': nonce,
                    'from': wallet_address,
                    'gasPrice': gas_price,
                })
        
                # Explicitly estimate gas with a safety margin
                estimated_gas = w3.eth.estimate_gas(tx) * 1.2  # Adding a 20% buffer
                tx['gas'] = int(estimated_gas)  # Update the transaction with estimated gas
        
                transaction_fee = gas_price * estimated_gas
                if transaction_fee > max_fee:
                    print('\033[39m' + "[-] "+ Fore.RED + f'{bot_id}, transaction fee: {transaction_fee}')
                    print('\033[39m'+"[-] " + Fore.RED + "Estimated fee is over your max fee.")
                    continue
        
                sign_tx = w3.eth.account.sign_transaction(tx, private_key)
                tran_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
                txn = w3.to_hex(tran_hash)
                nonce = nonce+1
                print('\033[39m'+"[+] " + Fore.GREEN + f'{bot_id} bot numarası için Transaction Fee: {transaction_fee}')
                print('\033[39m'+"[+] " + Fore.GREEN + f'Success. TX hash:{txn}')
        
            except ContractLogicError as e:
                print('\033[39m' + "[-] " + Fore.RED + "Contract Logic Error:", e)
            except TransactionNotFound as e:
                print('\033[39m' + "[-] " + Fore.RED + "No transaction :", e)
            except Exception as e:
                print('\033[39m' + "[-] " + Fore.RED + f"{bot_id} botID error :", e)
    input('\033[39m')

def send_all_bots_to_mission(missionId):
    w3, wallet_address, contract1, contract2, private_key, bot_ids , maxfeeaccepted = load_config()  # Yapılandırma bilgilerini yükleyin
    sleep(1)
    clear()
    nonce = w3.eth.get_transaction_count(wallet_address)
    gas_price = w3.eth.gas_price
    max_fee = w3.to_wei(maxfeeaccepted, 'ether')
    if len(bot_ids) <= 0:
        clear()
        print('\033[39m' + "Check bot ids in config.")
        print('\n *program will close after 3 secs*')
        sleep(3)
        os._exit(1)
    else:
        for bot_id in bot_ids:
            print('\033[39m' + f"BotID startMission : {bot_id}")
            try:
                droid_token_ids = [int(bot_id)]
                tx = contract2.functions.startMission(droid_token_ids, int(missionId)).build_transaction({
                    'nonce': nonce,
                    'from': wallet_address,
                    'gasPrice': gas_price,
                })

                estimated_gas = w3.eth.estimate_gas(tx) * 1.25  # Adding a 20% buffer
                tx['gas'] = int(estimated_gas)  # Update the transaction with estimated gas

                transaction_fee = gas_price * estimated_gas
                if transaction_fee > max_fee:
                    print('\033[39m' + "[-] "+ Fore.RED + f'{bot_id}, transaction fee: {transaction_fee}')
                    print('\033[39m'+"[-] " + Fore.RED + "Estimated fee is over your max fee.")
                    continue

                sign_tx = w3.eth.account.sign_transaction(tx, private_key)
                tran_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
                txn = w3.to_hex(tran_hash)
                nonce = nonce+1

                print('\033[39m'+"[+] " + Fore.GREEN + f'{bot_id}, transaction Fee: {transaction_fee}')
                print('\033[39m'+"[+] " + Fore.GREEN + f'Success. TX hash:{txn}')

            except ContractLogicError as e:
                print('\033[39m' + "[-] " + Fore.RED + "Contract Logic Error:", e)
            except TransactionNotFound as e:
                print('\033[39m' + "[-] " + Fore.RED + "No transaction :", e)
            except Exception as e:
                print('\033[39m' + "[-] " + Fore.RED + f"{bot_id} botID error :", e)
        input('\033[39m')

def show_profitability_table():
    table = load_profitability_table()
    os.system('cls')
    print('\033[39m')
    print(tabulate(table, headers='keys', tablefmt='pretty', showindex=False))


def get_user_missions():
    w3, wallet_address, contract1, contract2, private_key, bot_ids , maxfeeaccepted = load_config()
    sleep(1)
    clear()
    mission_info = contract2.functions.userMissions(wallet_address).call()
    ahmet = 0
    print('\033[39m' + "-----------------------------------------------------------------------------------")
    for mission in mission_info:
        ahmet = ahmet + 1
        mission_hash = mission[0]
        mission_type_id = mission[1]
        difficulty_level = mission[2]
        start_bot_id = mission[3]
        end_bot_id = mission[4]
        number_of_bots = mission[5]
        mission_start_timestamp = mission[6]
        mission_end_timestamp = mission[7]
        mission_giver_address = mission[8]
        bot_rarity_id = contract1.functions.droidRarities(start_bot_id).call()
        if bot_rarity_id == 1:
            bot_rarity = 'C'
        elif bot_rarity_id == 2:
            bot_rarity = 'R'
        elif bot_rarity_id == 3:
            bot_rarity = 'E'
        elif bot_rarity_id == 4:
            bot_rarity = 'L'
        else:
            print('wtf')

        bot_droid_id = contract1.functions.droidIds(start_bot_id).call()

        mission_end_time = datetime.fromtimestamp(mission_end_timestamp)
        remaining_time = mission_end_time - datetime.now()


        print('\033[39m' +f"[{ahmet} / {len(mission_info)}] " + Fore.GREEN + f"BotID : #{start_bot_id} , DroidId :#{bot_droid_id}{bot_rarity} , Mission End : {mission_end_time.strftime('%Y-%m-%d %H:%M:%S')}, Timeleft : {remaining_time}")
        print('\033[39m' + "-----------------------------------------------------------------------------------")

    print('\033[39m'+ f'[{ahmet} / {len(mission_info)}]' + Fore.GREEN +" Done.\n" + '\033[39m' + "Press a key to continue.\n")
    input()