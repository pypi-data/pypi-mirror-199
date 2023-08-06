"""
░░░░░░░░░░░██╗░░░░░░░██╗██╗░░░██╗██████╗░██████╗░███████╗░░░░░░██████╗░░█████╗░██████╗░██████╗░░░░░░░░░░░░
░░░░░░░░░░░██║░░██╗░░██║██║░░░██║██╔══██╗██╔══██╗╚════██║░░░░░░██╔══██╗██╔══██╗██╔══██╗██╔══██╗░░░░░░░░░░░
░░░░░░░░░░░╚██╗████╗██╔╝██║░░░██║██║░░██║██║░░██║░░███╔═╝█████╗██║░░██║███████║██████╔╝██████╔╝░░░░░░░░░░░
░░░░░░░░░░░░████╔═████║░██║░░░██║██║░░██║██║░░██║██╔══╝░░╚════╝██║░░██║██╔══██║██╔═══╝░██╔═══╝░░░░░░░░░░░░
░░░░░░░░░░░░╚██╔╝░╚██╔╝░╚██████╔╝██████╔╝██████╔╝███████╗░░░░░░██████╔╝██║░░██║██║░░░░░██║░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░╚═╝░░░╚═╝░░░╚═════╝░╚═════╝░╚═════╝░╚══════╝░░░░░░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░░░░░░░░░░░░

 [*]Descr:     ERC20 DAPP, CREATE ACCOUNTS, GET ALL TOKEN BALANCES & USD VALUE FOR AN ACCOUNT/WALLET,     
               MAKE TRANSACTIONS, INTERACT SMART CONTRACTS, SWAP ERC20 TOKENS, GET CURRENT CRYPTO PRICES, 
               AUTHENTICATE TO EXCHANGE ACCOUNT VIA API, CONVERT CRYPTO TO CRYPTO VALUE AND BASE64 DECODER
 [*]Coder:     Wuddz_Devs                                                                                 
 [*]Email:     wuddz_devs@protonmail.com                                                                  
 [*]Github:    https://github.com/wuddz-devs                                                              
 [*]Reddit:    https://reddit.com/users/wuddz-devs                                                        
 [*]Twitter:   https://twitter.com/wuddz_devs                                                             
 [*]Telegram:  https://t.me/wuddz_devs                                                                    
 [*]Videos:    https://mega.nz/folder/IWVAXTqS#FoZAje2NukIcIrEXXKTo0w                                     
 [*]Youtube:   https://youtube.com/@wuddz-devs                                                            

 [*]Menu:                                                                                                 
    1    =>    Create Account                                                                             
    2    =>    Check Account Balance(s)                                                                   
    3    =>    Send/Deposit To An Account                                                                 
    4    =>    Get Account Address & Balance(s) From Private Key Or Mnemonic Seed                         
    5    =>    Get Transaction Hash Attributes                                                            
    6    =>    Compile, Deploy Smart Contract To Blockchain                                               
    7    =>    Interact, Read & Execute Smart Contract Functions                                          
    8    =>    Verify Deployed Smart Contract On Etherscan/Polygonscan                                    
    9    =>    Swap/Purchase ERC20 Tokens Using 0x Api                                                    
    x    =>    Interact With Exchange Account (Authentication ApiKey, ApiSecret, ApiPassword etc...)      
    d    =>    Decode Base64 String                                                                       
    p    =>    Crypto Price & Conversion                                                                  
    l    =>    Load Dapp_Config From File                                                                 
    s    =>    Save Dapp_Config To File                                                                   
    n    =>    Choose Blockchain Network                                                                  
    e    =>    Exit Program                                                                               
"""

import re, sys, json, base64, dapp_trade, dapp_config, requests, warnings, platform, secrets, string, importlib
from pycoingecko import CoinGeckoAPI
from time import sleep
from pathlib import Path
from web3 import Web3, EthereumTesterProvider
from subprocess import call
from getpass import getpass
from os import system
warnings.simplefilter(action='ignore', category=FutureWarning)
system('')


class Wuddz_Dapp:
    def __init__(self):
        self.da=''
        self.pk=''
        self.name=platform.system()
        pkg=str(Path.home().expanduser().joinpath('Desktop','DAPP'))
        if not Path(pkg).exists():Path(pkg).mkdir(parents=True, exist_ok=True)
        self.cf=Path(pkg).joinpath('contract_info.txt')
        self.kf=Path(pkg).joinpath('key_file.txt')
        self.kd=Path(pkg).joinpath('key_data.txt')
        self.tr=Path(pkg).joinpath('tx_receipts.txt')
        self.lf=Path(pkg).joinpath('dapp_trade-log.txt')
        self.dc=(Path(__file__).absolute().parent).joinpath('dapp_config.py')
    
    def clear_screen(self):
        if self.name=='Linux':system('clear')
        elif self.name=='Windows':system('cls')
        elif self.name=='Darwin':system("printf '\\33c\\e[3J'")
    
    def get_menu(self,pstr=None):
        if pstr:print(pstr)
        a=input('\n\033[1;32;40m...Hit Enter|Return Key To Continue....\033[0m\n') or ''
    
    def decode_bsf(self,bss):
        if bss:self.get_menu('\n\033[1;34;40m'+str(base64.b64decode(bss).decode('utf-8'))+'\033[0m')
    
    def account_auth(self):
        doc=""" [*]Account Authentication:                                                                                                     
                                                                                                                                
    Key-File = Text File Containing Encrypted Account Data When Account Is Created (Requires Base64 Password From Key-Data File)
                                                                                                                                
    Private Key         e.g  0x5cf948ea8ede930971f938023a08a8ac2fc984035ffac89a8e9c33c657b24e33                                 
    Key-File Full Path  e.g  /home/kali/Desktop/key-file.txt                                                                    
    """
        ad=' [*]Address  e.g  0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
        if not self.da and not self.pk:
            try:
                pp=getpass(f'\n\033[1;32;40m{doc}\n\033[0mInput Private Key Or File Path=> ')
                if Path(pp).is_file():
                    pwd=getpass('Input Base64 Encoded Password=> ')
                    psd=str(base64.b64decode(pwd).decode('utf-8'))
                    da=input(f'\n\033[1;32;40m{ad}\n\n\033[0mInput Address=> ')
                    with open(pp, 'r', encoding='utf-8') as fr:
                        for line in fr:
                            if str((da.split('0x')[1]).lower()) in str(line):
                                pk=self.web3.to_hex(self.web3.eth.account.decrypt(line, psd))
                elif len(pp)>=64:pk=pp
                self.da=self.account_key(pk,'d')
                self.pk=pk
                self.clear_screen()
            except:
                self.get_menu(f'\n\033[1;31;40mPrivate Key Not Valid!!\033[0m')
                return
        return self.da,self.pk
    
    def crypto_price(self,cc):
        try:
            tlst=[]
            cg=CoinGeckoAPI()
            if cc=='s':self.token_id(cg)
            elif cc:
                ccl=cc.split()
                cd=cg.get_coin_by_id(ccl[1])
                cpa=cg.get_price(cd['id'],'usd')[str(cd['id'])]['usd']
                crp="${:,.2f}".format(float(ccl[0])*float(cpa))
                syma=cd['symbol'].upper()
                if len(ccl)==2:self.get_menu(f"\n\033[1;34;40m{cc.replace(ccl[1],syma)} => {crp} USD\033[0m")
                elif len(cc.split())==3:
                    cb=cg.get_coin_by_id(ccl[2])
                    symb=cb['symbol'].upper()
                    cpb=cg.get_price(ccl[2],'usd')[str(ccl[2])]['usd']
                    cvv=float(ccl[0])*(float(cpa)/float(cpb))
                    self.get_menu(f"\n\033[1;34;40m{ccl[0]} {syma} => {cvv} {symb}\nTotal Value => {crp} USD\033[0m")
        except requests.exceptions.ConnectionError:
            self.get_menu(f'\n\033[1;31;40mNo Connection Error!!\033[0m')
        except:
            self.get_menu(f'\n\033[1;31;40m{cc} Not Valid!!\033[0m')
    
    def token_id(self,cg):
        doc=""" [*]Search For Token & Copy TokenId To Use For Price & Conversion:                                                            
                                                                                                                              
    String = Name Of Token (Outputs List Matching String => "Id: TokenId,  Name: TokenName, Symbol: TokenSymbol" On Each Line)
                                                                                                                              
    Input String  =>  [e.g bitcoin Outputs List Matching "bitcoin" => "Id: bitcoin  Name: bitcoin Symbol: BTC "]              
    Input b       =>  To Go Back
    """
        while True:
            self.clear_screen()
            st=input(f"\033[1;32;40m{doc}\n\033[0mInput String or b=> ")
            if st=='b':break
            elif st:
                sd=cg.search(st)['coins']
                for i in range(len(sd)):
                    print(f"Id: {sd[i]['id']},  Name: {sd[i]['name']},  Symbol: {sd[i]['symbol']}")
                self.get_menu()
    
    def token_swap(self):
        addr, private_key=self.account_auth()
        doc=""" [*]Specify Blockchain To Get Info For Token Swap/Purchase:                  
                                                                             
    1. Ethereum (Mainnet)                    6. Optimism (Optimism Mainnet)  
    2. Goerli (Ethereum Testnet)             7. Fantom (Fantom Mainnet)      
    3. Polygon (Polygon Mainnet)             8. Celo (Celo Mainnet)          
    4. Mumbai (Polygon Testnet)              9. Avalanche (Avalanche Mainnet)
    5. Binance Smart Chain (BNB Mainnet)    10. Arbitrum (Arbitrum Mainnet)  
                                                                             
    Input Number               =>    [e.g 5 = Binance Smart Chain]           
    Or Hit Enter|Return Key    =>    For Ethereum (Mainnet)                  
    """
        aoc=""" [*]Specify Token Swap/Purchase Arguments:                       
                                                                 
    Address  =>  [e.g 0xdac17f958d2ee523a2206206994597c13d831ec7]
    Amount   =>  [e.g 1000000000000000000]"""                    
        td={'1': '','2': 'goerli.',
            '3': 'polygon.','4': 'mumbai.',
            '5': 'bsc.','6': 'optimism.',
            '7': 'fantom.','8': 'celo.',
            '9': 'avalanche.','10': 'arbitrum.'
            }
        chain=input(f'\n\033[1;32;40m{doc}\033[0m\nInput Number=> ') or '1'
        self.clear_screen()
        ld={
            '1  ->  BuyToken                      (e.g DAI Or Token Smart Contract Address)':'',
            '2  ->  Slippage                      (e.g 0.01 = 1% slippage)':'0.01',
            '3  ->  SellToken                     (e.g ETH Or Token Smart Contract Address)':'',
            '4  ->  SellAmount Or Set BuyAmount   (e.g Sell Specified Amount Of Sell Token)':'',
            '5  ->  BuyAmount Or Set SellAmount   (e.g Buy Specified Amount Of Buy Token)':'',
            '6  ->  TakerAddress                  (e.g Address)':addr
            }
        kd={k.split()[0]:k for k in ld.keys()}
        hd=self.function_dict(ld,kd,aoc,swap='swap')
        bt=[x for x in (v for k,v in hd.items())]
        dt=[d for d in bt if d]
        bs='Buy'
        if bt[3]:bs='Sell'
        try:
            ff=dt[4]
            bts,btd=self.token_sinfo(dt[0])
            sts,std=self.token_sinfo(dt[2])
            url=requests.get(f'https://{td[str(chain)]}api.0x.org/swap/v1/quote?buyToken={dt[0]}&sellToken={dt[2]}&\
{bs.lower()}Amount={dt[3]}&slippagePercentage={dt[1]}&takerAddress={self.web3.to_checksum_address(ff)}')
            api=url.json()
            sa=int(api['sellAmount'])/10**int(std)
            ba=int(api['buyAmount'])/10**int(btd)
            tp="{:,.2f}".format(float(api["price"]))
            gp=format(self.web3.from_wei(int(api['gasPrice']),'ether'),'f')
            print(f'\n\033[1;34;40mPrice Of {bs} Token: ${tp}\nGas: {gp} ETH\nBuyAmount:\
{format(ba,"f")} {bts}\nSellAmount: {format(sa,"f")} {sts}\nSlippage: {api["expectedSlippage"]}\033[0m')
            apr=input('\n\033[1;32;40mDo You Approve This Transaction?\nInput y or n=> ') or 'n'
            if apr.lower()=='y':
                self.token_approve(api['sellTokenAddress'],str(td[chain])[:-1],addr,private_key,mamt=api['sellAmount'])
                nonce=self.web3.eth.get_transaction_count(addr)
                tx={
                    'nonce': nonce,
                    'from':addr,
                    'to': self.web3.to_checksum_address(api['to']),
                    'data': api['data'],
                    'value': int(api['value']),
                    'gas': int(api['gas']),
                    'gasPrice': int(api['gasPrice']),
                    'chainId': api['chainId']
                    }
                self.sign_transaction(tx,private_key)
        except requests.exceptions.ConnectionError:
            self.get_menu(f'\n\033[1;31;40mNo Connection Error!!\033[0m')
        except:self.get_menu(f'\n\033[1;31;40m{url.text}\033[0m')
    
    def token_sinfo(self,addr):
        ts=''
        td=''
        if len(addr)==42:c,b,ts,n,td=self.contract_info(self.web3.to_checksum_address(addr))
        else:
            ts=addr
            td=18
            if addr!='ETH':
                for k,v in dapp_config.tcd.items():
                    if k.split('_')[0]==addr:
                        c,b,ts,n,td=self.contract_info(self.web3.to_checksum_address(v))
                        break
        return ts,td
    
    def token_approve(self,sta,spa,wla,pk,mamt=None):
        da=dapp_config.exp['mainnet']
        if spa:da=dapp_config.exp[spa]
        nonce=self.web3.eth.get_transaction_count(wla)
        contract=self.web3.eth.contract(address=self.web3.to_checksum_address(sta),abi=dapp_config.abi)
        spender=self.web3.to_checksum_address(da)
        tx=contract.functions.approve(spender, int(mamt)).build_transaction({
            'from': wla,
            'nonce': nonce,
        })
        self.sign_transaction(tx,pk,hs='Transaction Approved')
    
    def sign_transaction(self,tx,private_key,hs=None,cd=None):
        signed_tx=self.web3.eth.account.sign_transaction(tx, private_key)
        tx_hash=self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt=self.web3.eth.wait_for_transaction_receipt(tx_hash)
        if cd:return tx_receipt,tx_hash
        elif hs:
            print(f'\n\033[1;34;40m{hs}\nTx_Hash: {self.web3.to_hex(tx_receipt.transaction_hash)}\033[0m')
        else:
            self.get_menu(f'\n\033[1;34;40mTransaction Completed Successfully\nTx_Hash: \
 {self.web3.to_hex(tx_receipt.transaction_hash)}\033[0m')
        self.trx_hash(self.web3.to_hex(tx_hash),'t')
    
    def contract_data(self,fnc,fn,abi):
        doc=f" [*]{fnc}() Function Arguments:"
        ld={}
        hd={}
        ex=''
        for i in range(len(abi)):
            if abi[i]['type']=='function' and abi[i]['name']==fnc:
                ex=abi[i]['stateMutability']
                lst=abi[i]['inputs']
                for n in range(len(abi[i]['inputs'])):
                    la=f'{int(n)+1} -> {abi[i]["inputs"][n]["type"]} ({abi[i]["inputs"][n]["name"]})'
                    ld[str(la)]=''
                    hd[str(int(n)+1)]=la
        ld=self.function_dict(ld,hd,doc)
        return ld,ex
    
    def function_dict(self,ld,hd,sdoc,swap=None):
        doc="""    Input Number  =>  To Set Argument Value                  
    Input d       =>  When Done Setting Values               
    Input c       =>  To Convert To/From Wei Or Decimal Value
"""
        if swap:doc=doc+"""    Input t       =>  Get Token Info                         
"""
        while True:
            try:
                self.clear_screen()
                lda=input(f'\n\033[1;32;40m{sdoc}\n\n{doc}\n \
[*]Current Arguments:\033[1;34;40m'+json.dumps(ld, indent=4)+'\n\033[0mInput Choice=> ')
                if lda=='d':break
                elif lda=='c':self.convert_value()
                elif lda=='t':self.token_addr('swap')
                kyv=hd[str(lda)]
                ldk=input(f'\nInput Argument "{lda}" Value=> ')
                ld[str(kyv)]=ldk
            except:pass
        return ld
    
    def token_addr(self,ft=None):
        doc=""" [*]Token Symbol Or Smart Contract Address:                                               
    
    Input Token Symbol                    [e.g tkx | TKX]                                 
    Input Token Smart Contract Address    [e.g 0xdac17f958d2ee523a2206206994597c13d831ec7]
    Or Hit Enter|Return Keyboard Key      {}                                              
"""
        self.clear_screen()
        tca=''
        ttt=''
        tkn='Token'
        ds='For All Token Balances In Account'
        if ft:ds='To Go Back'
        ts=input(f"\033[1;32;40m{doc.format(ds)}\033[0m\nInput Choice=> ") or 'b'
        if ts=='b':
            if ft:ttt=ts
            elif not ft and self.nw not in 'mainnet,polygon':ttt='ETH'
        elif ts:
            if len(ts)==42:
                tca=self.web3.to_checksum_address(ts)
                c,b,ttt,tkn,dec=self.contract_info(tca)
            elif ts.upper()=='ETH':
                ttt=ts.upper()
                tkn='Ethereum'
            else:
                ts=ts.upper()
                for k,v in dapp_config.tcd.items():
                    if k.split('_')[0]==ts:
                        tca=self.web3.to_checksum_address(v)
                        c,b,ttt,tkn,dec=self.contract_info(tca)
                        break
                if not ttt:
                    self.get_menu(f"\n\033[1;31;40m{ts} Not A Valid Token!!")
                    return
            if ttt and ft=='swap':
                self.get_menu(f'\n\033[1;34;40mAddress: {tca}\nName: {tkn}\nSymbol: {ttt}\nDecimals: {dec}\nNetwork: {self.nw}\033[0m')
                return
        return tca,ttt,tkn
    
    def account_balance_sub(self,bjs):
        tot=[]
        for i in range(len(bjs['tokens'])+1):
            usdc='0'
            try:
                nam=bjs['tokens'][i]['tokenInfo']['name']
                sym=bjs['tokens'][i]['tokenInfo']['symbol']
                dec=bjs['tokens'][i]['tokenInfo']['decimals']
                rbal=bjs['tokens'][i]['rawBalance']
                bal=rbal
                if str(dec)!='0':bal=int(rbal)/10**int(dec)
                if bjs['tokens'][i]['tokenInfo']['price']:
                    pri=bjs['tokens'][i]['tokenInfo']['price']['rate']
                    usd=eval(f'{pri}*{bal}')
                    tot.append(usd)
                    usdc="{:,.2f}".format(usd)
                print(f'\n\033[1;34;40m{nam}: {bal} \033[1;32;40m(${usdc} USD) \033[1;34;40m{sym}\033[0m')
            except:pass
        return tot
    
    def eth_value(self,addr):
        chk=self.web3.to_checksum_address(addr)
        ebal=self.web3.eth.get_balance(chk)
        return self.web3.from_wei(ebal, 'ether')
    
    def account_balance(self,addr):
        ethv=self.eth_value(addr)
        tca,ttt,tkn=self.token_addr()
        if self.nw in 'mainnet,polygon,bsc':
            tot=[]
            url=f'https://api.ethplorer.io/getAddressInfo/{addr}?apiKey=freekey'
            if tca:url=f'https://api.ethplorer.io/getAddressInfo/{addr}?token={tca}&showETHTotals=false&apiKey=freekey'
            ab=requests.get(url)
            bjs=ab.json()
            prc=bjs['ETH']['price']['rate']
            txc=bjs['countTxs']
            if bjs.get('tokens'):tot=self.account_balance_sub(bjs)
            eus=eval(f'{prc}*{ethv}')
            usdt="${:,.2f}".format(sum(tot)+eus)
            eusd="${:,.2f}".format(eus)
            print(f'\n\033[1;34;40mEthereum: {ethv} \033[1;32;40m({eusd} USD) \033[1;34;40mETH\n\n\033[1;34;40mAccount: {addr}\033[0m')
            enn=self.ens_addr(addr,'name')
            if enn:print(f'\033[1;34;40mEnsName: {enn}\033[0m')
            self.get_menu(f'\033[1;34;40mTotal Value: \033[1;32;40m{usdt} USD\n\033[1;34;40mTotal Transactions: {txc}\033[0m')
        else:
            if tca and ttt!='ETH':contract,ethv,ttt,tkn,dec=self.contract_info(str(tca),chk=chk)
            self.get_menu(f'\n\033[1;34;40mAccount: {addr}\nBalance: {ethv} {ttt}\033[0m')
    
    def contract_info(self,tca,chk=None):
        ethv=''
        contract=self.web3.eth.contract(abi=dapp_config.abi,address=tca)
        if chk:ethv=contract.functions.balanceOf(str(chk)).call()
        dec=contract.functions.decimals().call()
        sym=contract.functions.symbol().call()
        nam=contract.functions.name().call()
        if str(dec)!='0' and chk:ethv=ethv/10**dec
        return contract,ethv,sym,nam,dec
    
    def account_create(self):
        psd=''.join(secrets.choice((string.ascii_letters+string.digits).strip()) for i in range(32))
        self.web3.eth.account.enable_unaudited_hdwallet_features()
        acct, mnemonic=self.web3.eth.account.create_with_mnemonic()
        encrypted=self.web3.eth.account.encrypt(acct.key, psd)
        with open(self.kf, 'a', encoding='utf-8') as fw:
            fw.write(json.dumps(encrypted)+'\n')
        with open(self.kd, 'a', encoding='utf-8') as kw:
            pk=base64.urlsafe_b64encode(bytes(self.web3.to_hex(acct.key), 'utf-8'))
            pd=base64.urlsafe_b64encode(bytes(psd, 'utf-8'))
            mn=base64.urlsafe_b64encode(bytes(mnemonic, 'utf-8'))
            kw.write(f'Account: {acct.address}\nPrivate_Key: {pk}\nPrivate_Key_Password: {pd}\nMnemonic: {mn}\n\n')
        self.get_menu(f'\n\033[1;34;40mAccount_Created=> {acct.address}\033[0m')
    
    def account_deposit(self,addr):
        addr=self.web3.to_checksum_address(addr)
        account, private_key=self.account_auth()
        while account and private_key:
            try:
                dec=''
                nonce=self.web3.eth.get_transaction_count(account)
                tbal=self.eth_value(account)
                tca,ttt,tkn=self.token_addr('deposit')
                if ttt=='b':break
                elif tca and ttt!='ETH':contract,tbal,ttt,tkn,dec=self.contract_info(str(tca),account)
                amnt=input(f'\n\033[1;34;40mBalance: {tbal} {ttt}\033[0m\n\nInput Amount To Transfer=> ') or 'a'
                amt=self.web3.to_wei(amnt, 'ether')
                if dec:amt=float(amnt)*(10**dec)
                if ttt=='ETH':
                    gas=self.web3.eth.estimate_gas({'to': addr,'value': amt})
                    tx={
                        'nonce': nonce,
                        'to': addr,
                        'value': amt,
                        'gas': gas,
                        'gasPrice': self.web3.eth.gas_price
                        }
                else:
                    gas=contract.functions.transfer(str(addr),int(amt)).estimate_gas()
                    tx=contract.functions.transfer(str(addr),int(amt)).build_transaction({
                        'nonce': nonce,
                        'gas': gas,
                        'gasPrice': self.web3.eth.gas_price
                        })
                self.sign_transaction(tx,private_key)
            except:pass
    
    def account_key(self,addr,k=None):
        if ' ' in addr:
            self.web3.eth.account.enable_unaudited_hdwallet_features()
            acct=self.web3.eth.account.from_mnemonic(str(addr))
        else:acct=self.web3.eth.account.from_key(addr)
        if k is None:bal=self.account_balance(acct.address)
        else:return acct.address
    
    def contract_deploy(self,addr):
        fd=str(list(Path(dapp_config.scdir).rglob(f'{addr}.json'))[0])
        if not Path(fd).exists():call(['truffle', 'compile'], cwd=dapp_config.scdir)
        with open(fd, 'r', encoding='utf-8') as cf:
            ci=json.load(cf)
        abi=ci['abi']
        bc=ci['bytecode']
        account, private_key=self.account_auth()
        contract=self.web3.eth.contract(abi=abi, bytecode=bc)
        tx_id=contract.constructor().build_transaction({
            'nonce': self.web3.eth.get_transaction_count(account),
            'gasPrice': self.web3.eth.gas_price})
        tx_receipt,tx_hash=self.sign_transaction(tx_id,private_key,cd='cd')
        contract_addr=tx_receipt.contractAddress
        with open(self.cf, 'a', encoding='utf-8') as fw:
            fw.write(f'name: {addr}.json\nabi: {abi}\naddress: {contract_addr}\nnetwork: {self.node_url}\n\n')
        print(f'\n\033[1;34;40mSmart_Contract_Address: {contract_addr}\033[0m')
        cna=f'{addr}@{contract_addr}'
        if self.nw!='ganache':call(['truffle', 'run', 'verify', cna, '--network', self.nw], cwd=dapp_config.scdir)
        self.trx_hash(tx_hash,'t')
        self.get_menu()
    
    def block_network(self):
        doc="""
 [*]Choose Blockchain Network:                                                               
                                                                                             
     1    =>    Mainnet          [Ethereum Blockchain]                                       
     2    =>    Ropsten          [Ethereum Test Network]                                     
     3    =>    Kovan            [Ethereum Test Network]                                     
     4    =>    Rinkeby          [Ethereum Test Network]                                     
     5    =>    Goerli           [Ethereum Test Network]                                     
     6    =>    Ganache          [Truffle Local System Based Test Network e.g 127.0.0.1:7545]
     7    =>    Polygon          [Polygon Blockchain]                                        
     8    =>    Mumbai           [Polygon Test Network]                                      
     9    =>    Development      [Truffle Local System Based Test Network e.g 127.0.0.1:8545]
    10    =>    BSC              [Binance Smart Chain]                                       
    11    =>    BSCTestnet       [Binance Smart Chain Test Network]                          
     b    =>    Back To Menu                                                                 
    """
        self.clear_screen()
        d={'1':'mainnet','2':'ropsten','3':'kovan',
           '4':'rinkeby','5':'goerli','6':'ganache',
           '7':'polygon','8':'mumbai','9':'development',
           '10':'bsc','11':'bsctestnet'}
        nc=input(f"\033[1;32;40m{doc}\033[0m\nInput Network Choice=> ") or 'a'
        if nc=='b':return
        elif nc in str(list(range(1,12))):
            nw=str(d[nc])
            node_url=eval(f'dapp_config.{nw}')
            return nw,node_url
    
    def config_main(self,ct):
        doc=""" [*]Config File Location Examples:                       
                                                         
    /home/kali/Documents/dapp_config.py             
    C:\\Users\\wuddz_devs\\Documents\\dapp_config.py
    """
        self.clear_screen()
        fl=str(Path(input(f"\033[1;32;40m{doc}\033[0m\nInput Config File Location=> ")).absolute())
        if ct=='l':
            if Path(fl).is_file():
                cl="Config Loaded Successfully"
                self.save_config(fl,self.dc)
                importlib.reload(dapp_config)
        else:
            cl=f"Config Saved Successfully => {fl}"
            self.save_config(self.dc,fl)
        self.get_menu(f'\n\033[1;34;40m{cl}\033[0m')
    
    def save_config(self,rf,wf):
        with open(rf,'r',encoding='utf-8') as fr:
            with open(wf,'w',encoding='utf-8') as fw:
                fw.write(fr.read())
    
    def contract_call(self,contract,cf,dec=None):
        try: 
            fnc=eval(f'contract.functions.{cf}.call()')
            if dec and len(str(fnc))>int(dec):fnc=fnc/(10**int(dec))
            print(f'\033[1;34;40m{cf} = {fnc}\033[0m')
        except:pass
    
    def convert_value(self):
        doc=""" [*]Convert To/From Wei Or Specified Decimal Value:             
                                                                
    2000000000 f w     =>    Convert 2000000000 From Wei        
    2000000000 f 12    =>    Convert 2000000000 From 12 Decimals
    2 t w              =>    Convert 2 To Wei                   
    2 t 12             =>    Convert 2 To 12 Decimals           
    """
        while True:
            try:
                self.clear_screen()
                cv=input(f'\n\033[1;32;40m{doc}\n\033[0mInput Parameters Or b To Go Back=> ')
                if cv=='b':break
                cv=cv.split()
                if cv[2]=='w':
                    if cv[1]=='t':self.get_menu(f"\n\033[1;34;40mWei => {self.web3.to_wei(float(cv[0]), 'ether')}\033[0m")
                    elif cv[1]=='f':self.get_menu(f"\n\033[1;34;40mEth => {self.web3.from_wei(float(cv[0]), 'ether')}\033[0m")
                elif str(cv[2]).isdigit():
                    if cv[1]=='t':val=float(cv[0])*10**int(cv[2])
                    else:val=float(cv[0])/10**int(cv[2])
                    self.get_menu(f"\n\033[1;34;40mValue => {val}\033[0m")
            except:pass
    
    def contract_verify(self,adr,ctr):
        addr=input(f'\n\033[1;32;40m{adr}\033[0m\n\nInput Smart Contract Address=> ')
        cn=input(f'\n\033[1;32;40m{ctr}\033[0m\n\nInput ContractName=> ')
        if addr and cn:
            cna=f'cn@{addr}'
            call(['truffle', 'run', 'verify', cna, '--network', self.nw], cwd=dapp_config.scdir)
            self.get_menu()
    
    def trx_hash(self,addr,trh=None):
        tl=[]
        txr=dict(self.web3.eth.get_transaction(addr))
        txr['gas']=format(self.web3.from_wei(txr['gas'], 'ether'),'f')
        txr['gasPrice']=format(self.web3.from_wei(txr['gasPrice'], 'ether'),'f')
        txr['value']=self.web3.from_wei(txr['value'], 'ether')
        print()
        for t,v in txr.items():
            if not 'logs' in str(t):
                if 'hexbytes' in str(type(v)):v=v.hex()
                if trh:tl.append(f'{t} => {v}')
                else:print(f'\033[1;34;40m{t} => {v}\033[0m')
        if tl:
            with open(self.tr, 'a', encoding='utf-8') as fw:
                fw.write(f'{self.node_url}\n')
                for l in tl:
                    fw.write(f'{l}\n')
                fw.write(f'\n\n')
        else:self.get_menu()
    
    def remote_abi(self,addr):
        abi=''
        try:
            cn=''
            ed={'User-Agent': 'Mozilla/5.0', 'Host':'api.etherscan.io'}
            hd={'User-Agent': 'Mozilla/5.0', 'Host':f'api-{self.nw}.etherscan.io'}
            md={'User-Agent': 'Mozilla/5.0', 'Host':'api-testnet.polygonscan.com'}
            pd={'User-Agent': 'Mozilla/5.0', 'Host':'api.polygonscan.com'}
            if self.nw=='mainnet':
                cn=requests.get(f'https://api.etherscan.io/api?module=contract&action=getabi&address={addr}', headers=ed).text
            elif self.nw=='mumbai':
                cn=requests.get(f'https://api-testnet.polygonscan.com/api?module=contract&action=getabi&address={addr}', headers=md).text
            elif self.nw=='polygon':
                cn=requests.get(f'https://api.polygonscan.com/api?module=contract&action=getabi&address={addr}', headers=pd).text
            elif self.nw!='ganache':
                cn=requests.get(f'https://api-{self.nw}.etherscan.io/api?module=contract&action=getabi&address={addr}', headers=hd).text
            abi=json.loads(cn)['result']
        except requests.exceptions.ConnectionError:
            print(f'\033[1;31;40mNo Connection Error!!\033[0m')
        return abi
    
    def local_abi(self):
        abi=''
        cnt=input('\nInput Contract Name Or Pass=> ')
        if cnt:
            with open(Path(dapp_config.scdir).joinpath('build','contracts',f'{cnt}.json'), 'r', encoding='utf-8') as cf:
                ci=json.load(cf)
            abi=ci['abi']
        return abi
    
    def contract_rw(self,addr):
        doc="""    Input Contract Function    =>    [e.g balanceOf]                               
    Input b                    =>    Back To Menu                                  
    Input c                    =>    Convert To/From Wei Or Specified Decimal Value
    """
        abi=''
        if self.nw in 'mainnet,polygon':abi=self.remote_abi(addr)
        else:abi=self.local_abi()
        if abi:
            contract=self.web3.eth.contract(str(addr), abi=abi)
            cfs=[(str(c).split('>')[0]).split(' ')[1] for c in contract.all_functions()]
            if cfs:
                dec=''
                if 'decimals()' in str(cfs):dec=contract.functions.decimals().call()
                while True:
                    self.clear_screen()
                    print(f'\n\033[1;32;40m [*]All Contract Functions For => {addr}:\033[0m\n')
                    for c in cfs:
                        if '()' in c:self.contract_call(contract,c,dec=dec)
                        else:print(f'\033[1;34;40m{c}\033[0m')
                    fnc=input(f'\n\033[1;32;40m{doc}\033[0m\nInput Choice=> ')
                    if fnc=='b':break
                    elif fnc=='c':self.convert_value()
                    elif fnc:
                        self.contract_rw_sub(fnc,cfs,contract,dec)
                        self.get_menu()
            else:self.get_menu('\n\033[1;31;40m*Contract Not Valid*\033[0m')
        else:self.get_menu('\n\033[1;31;40m*Contract Abi Not Found*\033[0m')
    
    def contract_rw_sub(self,fnc,cfs,contract,dec):
        et=''
        print(f'\n\033[1;34;40mNetwork Connected: {self.web3.is_connected()}\033[0m')
        fn=re.search(f'{fnc}\((.*?)\)',str(cfs)).group(1)
        if fn:
            fd,et=self.contract_data(fnc,fn,contract.abi)
            fo=f'{fnc}('
            for k,v in fd.items():
                if v:
                    if 'uint' in str(k):fo+=f'int("{v}"),'
                    else:fo+=f'"{v}",'
            if fo[-1]!='(':
                fp=f'{fo[:-1]})'
                if str(et) not in 'pure,view':
                    account, private_key=self.account_auth()
                    nonce=self.web3.eth.get_transaction_count(account)
                    gas=eval(fp).estimate_gas()
                    tx=eval(fp).build_transaction({'nonce': nonce, 'gas': gas, 'gasPrice': self.web3.eth.gas_price})
                    self.sign_transaction(tx,private_key)
                else:self.contract_call(contract,fp,dec=dec)
        else:self.contract_call(contract,f'{fnc}()',dec=dec)
    
    def ens_addr(self,adr,fn):
        addr=''
        try:
            addr=eval(f'self.web3.ens.{fn}("{adr}")')
            addr=re.search('\S+.eth',addr).group()
        except:pass
        return addr
    
    def exec_arg(self,pre,var,nn=None):
        cmd=''
        if not nn:cmd=f'\n\033[1;34;40mNetwork {self.nw} Connected: {self.cnn}\033[0m\n\n'
        if 'Private Key' in var:
            addr=getpass(cmd+"\033[1;32;40m"+pre+"\033[0m\n\nInput "+var+"=> ") 
        else:addr=input(cmd+"\033[1;32;40m"+pre+"\033[0m\n\nInput "+var+"=> ") 
        if '.eth' in addr:addr=self.ens_addr(addr,'address')
        return str(addr)
    
    def sub_main(self,etht):
        sd={'2':'account_balance@Address','3':'account_deposit@Deposit Address',
            '4':'account_key@Private Key/Mnemonic Seed','5':'trx_hash@Transaction Hash',
            '6':'contract_deploy@Contract Name','7':'contract_rw@Smart Contract Address',
            'd':'decode_bsf@Base64 String','p':'crypto_price@Choice'}
        if etht in list(sd.keys()):
            nn=''
            func=sd[etht].split('@')
            while True:
                try:
                    self.clear_screen()
                    if func[0] in 'decode_bsf,crypto_price':nn='n'
                    addr=self.exec_arg(self.help_docs(func[0]),f'{func[1]} or b Back To Menu',nn)
                    if addr=='b':break
                    eval(f'self.{func[0]}(addr)')
                except Exception as e:self.get_menu(f"\n\033[1;31;40m{e}\033[0m")
        else:
            self.clear_screen()
            if etht=='8':self.contract_verify(self.help_docs('contract_verify'))
            else:self.token_swap()
    
    def help_docs(self,ds):
        decode_bsf=' [*]Decode Base64 String e.g ZmVOUW9Ia2h6N2VERshiMAFQRVRCNExZcGF1c01UZng='
        ctr=' [*]ContractName  e.g  FeeCollector'
        adr=' [*]Account/Smart Contract Address  e.g  vitalik.eth | 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
        account_key=' [*]Private Key    e.g  0x5cf948ea8ede930971f938023a08a8ac2fc984035ffac89a8e9c33c657b24e33\n\
 [*]Mnemonic Seed  e.g  problem aunt wealth guilt debris lonely annual favorite element run expect bicycle'
        trx_hash=' [*]Transaction Hash  e.g  0xcdb204672ef292393ca2922d4f44f2f081045e1f62f16a0a174d40adfdf2c80e'
        crypto_price=""" [*]Crypto Price & Conversion:                                   
                                                                 
    Amount    =  1.2 | 5 | 1004                                  
    TokenName =  Ethereum | bitcoin | binancecoin                
                                                                 
    Formats:                                                     
    Amount TokenName                                             
    Amount From(TokenName) To(TokenName)                         
                                                                 
    Examples:                                                    
    1.2 ethereum               =>    Price Of 1.2 Ethereum In USD
    100 binancecoin bitcoin    =>    Bitcoin Value Of 100 BNB    
                                                                 
    Input Format  =>  To Get Required Price/Value                
    Input s       =>  Search For Id Of Token                     """
        if ds.split('_')[1] in 'balance,deposit,rw':return adr
        elif ds=='contract_deploy':return ctr
        elif ds=='contract_verify':return adr,ctr
        return eval(ds)
    
    def slow_print(self,doc):
        for d in doc:
            sys.stdout.write(f"\033[1;32;40m{d}")
            sleep(0.0005)
    
    def main(self):
        self.node_url=''
        self.web3=Web3(EthereumTesterProvider)
        while True:
            try:
                self.clear_screen()
                self.slow_print(__doc__)
                etht=input("\033[0m\nInput Choice=> ") or 'z'
                if etht=='e':break
                elif etht in 'l,s':self.config_main(etht)
                elif etht in 'd,p':self.sub_main(etht)
                elif etht=='n':self.nw,self.node_url=self.block_network()
                elif etht=='x':dapp_trade.Exchange_Trade().sub_main()
                elif etht=='1':self.account_create()
                elif etht in '2,3,4,5,6,7,8,9':
                    if not self.node_url:self.nw,self.node_url=self.block_network()
                    self.web3=Web3(Web3.HTTPProvider(self.node_url))
                    self.cnn=self.web3.is_connected()
                    if self.cnn==True:self.sub_main(etht)
                    else:self.get_menu(f'\n\033[1;31;40mCan"t Connect To {self.node_url}!!\033[0m')
            except KeyboardInterrupt:break
            except:pass
        self.clear_screen()

def cli_main():
    Wuddz_Dapp().main()
