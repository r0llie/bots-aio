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
        print('\033[39m' +'[-] ' + f"{filename} bulunamadı. İndiriliyor...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'w') as file:
                json.dump(response.json(), file)
            print('\033[39m'+ '[+] '  + Fore.GREEN + f"{filename} başarıyla indirildi." + '\033[39m')
        else:
            print('\033[39m'+ '[-] ' + Fore.RED + f"{filename} indirilemedi. HTTP Status Code: {response.status_code}\n Şimdi programdan çıkılacak." + '\033[39m')
            sleep(2)
            os._exit(1)
    else:
        print('\033[39m' + '[+] '+ Fore.GREEN + f"{filename} zaten mevcut.")

def check_and_create_config():
    config_file_path = 'config/config.json'
    config_template = {
        'polygon_rpc_endpoint': '',
        'private_key': '',
        'contract_address1': '',
        'contract_address2': '',
        'droidabi_url': 'https://raw.githubusercontent.com/r0llie/bots-aio/main/droidabi.json',
        'droidmissionabi_url': 'https://raw.githubusercontent.com/r0llie/bots-aio/main/droidmissionabi.json',
        'missiondata_url': 'https://raw.githubusercontent.com/r0llie/bots-aio/main/missionData.csv',
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
                    print(f'Bot listen bulunamadı veya boş. Botu durdurup düzeltmen önerilir...')
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
    print('\033[39m' + '[+] ' + f'Ayarlar yapıldı...')

    return w3, wallet_address, contract1, contract2, private_key, bot_ids , maxfeeaccepted

def load_profitability_table():
	config = check_and_create_config()
	downloadFromUrl(config['missiondata_url'], 'config/missionData.csv')

	df = pd.read_csv('config/missionData.csv')

	# Karlılık sütununu hesaplama
	df['Karlılık'] = (df['Puan'] / df['Süre']).astype(int)

	df = df.sort_values(by='Karlılık', ascending=False)

	
	# Tablo formatı için kullanılacak sütunları seçme
	table = df[['ID', 'Süre', 'Puan', 'Karlılık']]

	return table
