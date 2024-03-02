import json
import os
import requests  # requests kütüphanesini içe aktar
from eth_account import Account
from web3 import Web3
from colorama import init, Fore, Back, Style
import pandas as pd
init()

def downloadFromUrl(url, filename):
    if not os.path.exists(filename):
        print('\033[39m' +'[-] ' + f"{filename} not found. Downloading...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'w') as file:
                json.dump(response.json(), file)
            print('\033[39m'+ '[+] '  + Fore.GREEN + f"{filename} downloaded successfully." + '\033[39m')
        else:
            print('\033[39m'+ '[-] ' + Fore.RED + f"{filename} cant download. HTTP Status Code: {response.status_code}\n Will exit." + '\033[39m')
            sleep(2)
            os._exit(1)
    else:
        print('\033[39m' + '[+] '+ Fore.GREEN + f"{filename} OK.")

def check_and_create_config():
    config_file_path = 'config/config.json'
    config_template = {
        'polygon_rpc_endpoint': '',
        'private_key': '',
        'contract_address1': '0x16a4d696A9AA85704991ec9e674a0A44D62fD7C0',
        'contract_address2': '0x4D947Ffe459A0B0fa23402D40Ea368486f8A0e8f',
        'droidabi_url': 'https://raw.githubusercontent.com/r0llie/bots-aio/main/config/droidabi.json',
        'droidmissionabi_url': 'https://raw.githubusercontent.com/r0llie/bots-aio/main/config/droidmissionabi.json',
        'missiondata_url': 'https://raw.githubusercontent.com/r0llie/bots-aio/main/config/missionData.csv',
        'maxfeeaccepted': 0.1,
        'bot_ids': []  # Bot ID'leri için boş bir liste olarak başlat
    }

    # Config dosyasının varlığını ve içeriğini kontrol et
    if not os.path.exists(config_file_path) or os.stat(config_file_path).st_size == 0:
        print("Config dosyası bulunamadı veya boş. Yeni bir tane oluşturuluyor...")
        config = config_template
    else:
        with open(config_file_path, 'r') as file:
            config = json.load(file)

        # Eksik anahtarları veya boş değerleri kontrol et ve güncelle
        for key, default_value in config_template.items():
            if key not in config or not config[key]:
                if key == 'bot_ids':  # 'bot_ids' için özel durum, kullanıcıdan giriş almak yerine boş liste kullan
                    config[key] = default_value
                    print(f'You have no bots in config...')
                else:
                    config[key] = input(f'{key} için değer girin: ')

    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)

    return config

def load_config():
    config = check_and_create_config()
    
    bot_ids = config.get('bot_ids', [])

    # ABI dosyalarını indir
    downloadFromUrl(config['droidabi_url'], 'config/droidabi.json')
    downloadFromUrl(config['droidmissionabi_url'], 'config/droidmissionabi.json')
    
    w3 = Web3(Web3.HTTPProvider(config['polygon_rpc_endpoint']))
    wallet_address = Web3.to_checksum_address(Account.from_key(config['private_key']).address)
    private_key = config['private_key']
    maxfeeaccepted = config['maxfeeaccepted']

    # ABI'ları yükle
    with open('config/droidabi.json', 'r') as f:
        contract_abi1 = json.load(f)
    with open('config/droidmissionabi.json', 'r') as f:
        contract_abi2 = json.load(f)

    contract1 = w3.eth.contract(address=config['contract_address1'], abi=contract_abi1)
    contract2 = w3.eth.contract(address=config['contract_address2'], abi=contract_abi2)
    print('\033[39m' + '[+] ' + f'Configured...')

    return w3, wallet_address, contract1, contract2, private_key, bot_ids , maxfeeaccepted

def load_profitability_table():
	config = check_and_create_config()
	downloadFromUrl(config['missiondata_url'], 'config/missionData.csv')

	df = pd.read_csv('config/missionData.csv')

	# Karlılık sütununu hesaplama
	df['Profitability'] = (df['Score'] / df['Time']).astype(int)

	df = df.sort_values(by='Profitability', ascending=False)

	
	# Tablo formatı için kullanılacak sütunları seçme
	table = df[['ID', 'Time', 'Score', 'Karlılık']]

	return table
