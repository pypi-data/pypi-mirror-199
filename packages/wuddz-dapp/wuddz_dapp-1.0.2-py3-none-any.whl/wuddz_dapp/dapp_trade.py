""" [*]Execute Below Tasks On Exchange:
    
    ab    =>    Account Balances
    lb    =>    Limit Buy Order
    ls    =>    Limit Sell Order
    mb    =>    Market Buy Order
    ms    =>    Market Sell Order
    cb    =>    Close Buy Order
    cs    =>    Close Sell Order
    sl    =>    Stop_Loss
    oc    =>    Cancel All Orders
    oi    =>    View & Cancel Order_ID
    va    =>    View All Orders
    vo    =>    View Open Orders
    vp    =>    View Positions
    vw    =>    View Withdrawals
    vt    =>    View Symbol Market/Trade Info
    wt    =>    Withdraw Tokens From Exchange
    e     =>    Exit Program
"""

import ccxt, logging, json, re, dapp
from getpass import getpass
from logging.handlers import RotatingFileHandler
from os import system
from pprint import pprint
system('')


class Exchange_Trade:
    def __init__(self):
        self.wd=dapp.Wuddz_Dapp()
        fh=RotatingFileHandler(
            filename=self.wd.lf,
            mode='a',
            maxBytes=5*1024*1024,
            backupCount=2,
            encoding='utf-8',
            delay=False
            )
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-15s %(levelname)-8s %(message)s",
            datefmt="%y-%m-%d %H:%M:%S",
            handlers=[fh]
            )
    
    def main(self,exchange):
        exchange.load_markets()
        self.flst=exchange.has
        self.slst=exchange.symbols
        self.wlst=list(exchange.currencies.keys())
        self.exchange=exchange
        while True:
            try:
                self.wd.clear_screen()
                fc=input(f'\033[1;32;40m{__doc__}\033[0m\nInput Choice=> ').lower()
                self.wd.clear_screen()
                if fc=='ab':self.balance()
                elif fc[:1] in 'l,m,c':self.order_open(fc)
                elif fc in 'oc,oi':self.order_cancel(fc)
                elif fc in 'va,vo':self.orders_all(fc)
                elif fc=='sl':self.order_stop_full(fc)
                elif fc=='vp':self.order_position()
                elif fc=='vw':self.token_withdrawals()
                elif fc=='vt':self.token_info()
                elif fc=='wt':self.token_withdraw()
                elif fc=='e':break
                elif fc:print(f'\n\033[1;31;40m{fc} Not In List!!\033[0m')
                else:continue
                self.wd.get_menu()
            except Exception as e:
                self.wd.get_menu(f'\n\033[1;31;40m{e}!!\033[0m')
    
    def get_symbol(self,w=None):
        doc=""" [*]Specify Token Symbol (If Symbol Isn't Found, Returns List Of Available Symbols Matching String)
    
    Input Symbol    =>    [e.g BTC/USDT | eth/UsDt | eth]
        """
        while True:
            self.wd.clear_screen()
            symbol=''
            slst=self.slst
            sbc=input(f'\n\033[1;32;40m{doc}\n\033[0mInput Symbol=> ').upper()
            if sbc:
                if w:slst=self.wlst
                fms=[x for x in slst if x==sbc]
                if fms:
                    symbol=fms[0]
                    break
                [print(x) for x in slst if sbc in x]
                self.wd.get_menu()
        return symbol
    
    def order_vars(self,w=None):
        os="""3.Price     =>    [e.g 55000 | 61905.5]
        """
        ns="""4.StopPrice =>    [e.g 33304 | 44500]
    5.Side      =>    [e.g sell | buy]
        """
        ws="""3.Address   =>    [e.g 0xdac17f958d2ee523a2206206994597c13d831ec7]
    4.Tag       =>    [Optional e.g USDT]
    5.Chain     =>    [Optional e.g ERC20 | BEP20]
    6.Memo      =>    [Optional e.g v9d3r02m7qwqywtj5kpf83sf]
        """
        doc=""" [*]Specify Order Parameters:
    
    1.Symbol    =>    [e.g BTC/USDT]
    2.Amount    =>    [e.g 1 | 10 | 0.5]
    {}
    Input d     =>    When Done Setting Parameters
    Input n     =>    n=number Of Parameter To Set [e.g 1 => Input Symbol]
    Input p     =>    Fetch Current Trading/Market Info Of Symbol
    """
        od={'1.Symbol':'','2.Amount':'','3.Price':''}
        if w=='w':
            od={'1.Symbol':'','2.Amount':'','3.Address':'','4.Tag':None,'5.Chain':'','6.Memo':''}
            os=ws
        elif w=='s':
            od={'1.Symbol':'','2.Amount':'','3.Price':'','4.StopPrice':'','5.Side':''}
            os=ns
        elif w=='m':
            del od['3.Price']
            os=''
            w=''
        while True:
            self.wd.clear_screen()
            ov=input(f'\033[1;32;40m{doc.format(os)}\n    Current Parameters:\
\033[1;34;40m{json.dumps(od,indent=4)}\n\033[0mInput d or number=> ') or 'a'
            if ov=='d':break
            elif ov=='p':self.token_info()
            elif ov in str(list(range(1,len(od)+1))):
                v=re.search(f"'({ov}.\w+)'",str(od)).group(1)
                if ov=='1':
                    od[v]=self.get_symbol(w)
                    if w:
                        self.wd.get_menu('\033[1;34;40m'+json.dumps(self.exchange.currencies[str(od[v])],indent=4)+'\033[0m')
                else:od[v]=input(f'Input {v}=> ')
        return {k.split('.')[1]:v for k,v in od.items()}
    
    def token_info(self):
        pprint(self.exchange.fetch_ticker(self.get_symbol()))
    
    def balance(self):
        pprint(self.exchange.fetch_balance())
    
    def order_open(self,fc):
        if fc in 'mb,ms':
            od=self.order_vars('m')
            if fc=='mb':self.market_buy(od)
            elif fc=='ms':self.market_sell(od)
        else:
            od=self.order_vars()
            params={'time_in_force': 'GoodTillCancel'}
            if fc=='lb':self.limit_buy(od,params)
            elif fc=='ls':self.limit_sell(od,params)
            elif fc[:1]=='c':
                params['reduce_only']=True
                if fc=='cs':self.limit_buy(od,params)
                elif fc=='cb':self.limit_sell(od,params)
    
    def limit_buy(self,od,params):
        pprint(self.exchange.create_limit_buy_order(od['Symbol'],od['Amount'],od['Price'],params))
    
    def limit_sell(self,od,params):
        pprint(self.exchange.create_limit_sell_order(od['Symbol'],od['Amount'],od['Price'],params))
    
    def market_buy(self,od):
        pprint(self.exchange.create_market_buy_order(od['Symbol'],od['Amount']))
    
    def market_sell(self,od):
        pprint(self.exchange.create_market_sell_order(od['Symbol'],od['Amount']))
    
    def order_stop_full(self,fc):
        od=self.order_vars('s')
        pprint(self.exchange.create_stop_limit_order(
side=od['Side'],symbol=od['Symbol'],amount=od['Amount'],stopPrice=od['StopPrice'],price=od['Price']))
    
    def order_cancel(self,fc):
        if fc=='oc':pprint(self.exchange.cancel_all_orders())
        elif fc=='oi':
            symbol=self.get_symbol()
            olst=self.get_orders('vo',symbol)
            if olst:
                [print(o) for o in olst]
                self.wd.get_menu()
            oid=input("\nInput Order_ID To Cancel=> ")
            pprint(self.exchange.cancel_order(oid,symbol))
    
    def get_orders(self,oc,symbol):
        olst=[]
        od={'vo':'fetch_open_orders','va':'fetch_orders'}
        dd={'vo':'fetchOpenOrders','va':'fetchOrders'}
        if dd[oc] in self.flst:
            since=self.exchange.milliseconds()-86400000
            while since < self.exchange.milliseconds():
                limit=10
                orders=eval(f'self.exchange.{od[oc]}')(symbol,since,limit)
                if len(orders):
                    since=orders[len(orders)-1]['timestamp']+1
                    olst+=orders
                else:break
        return olst
    
    def orders_all(self,ot):
        symbol=self.get_symbol()
        pprint(self.get_orders(ot,symbol))
    
    def order_position(self):
        if 'fetchPositions' in self.flst:
            pprint(self.exchange.fetch_positions(self.get_symbol()))
    
    def token_withdraw(self):
        wd={}
        if self.flst.get('withdraw'):
            od=self.order_vars('w')
            for key in 'Chain,Memo':
                if od.get(key):wd[key.lower()]=od[key]
            pprint(self.exchange.withdraw(od['Symbol'],od['Amount'],od['Address'],od['Tag'],wd))
    
    def token_withdrawals(self):
        pprint(self.exchange.fetch_withdrawals())
    
    def auth_dict(self,ad,exc,exd):
        doc=""" [*]{} Exchange Required Authentication:
    
    Examples:                                                         
    Input apiKey      =>    [e.g 6dek4of7vge2z8uvxwt0qkty]            
    Input secret      =>    [e.g itigz23v-aezj-kua4-iasq-mxhe5o6cvdpt]
    Input password    =>    [e.g VTigz23vaezJKuA4IAsQmxHe5O6CvdPT]    
    """
        self.wd.clear_screen()
        print(f'\033[1;32;40m{doc.format(exc.upper())}\033[0m')
        lst=[x for x in ad.keys() if ad.get(x)]
        if exc=='kucoin':lst.append('password')
        for l in lst:
            exd[l]=getpass(f'Input {l}=> ')
        return exd
    
    def sub_main(self):
        doc=""" [*]Specify Exchange To Authenticate To:                                                
    
    Input Exchange    =>    [e.g  bybit | Binance (If Test Account Add 't' e.g bybit t)]
    Input b           =>    To Go Back                                                  
    """
        exd={
            'enableRateLimit': True,
            'options': {'adjustForTimeDifference': True}
            }
        while True:
            try:
                ta=''
                self.wd.clear_screen()
                exc=input(f'\033[1;32;40m{doc}\033[0m\nInput Choice=> ').lower()
                if exc=='b':break
                elif ' t' in exc:
                    ta='test'
                    exc=exc.split()[0]
                exch=getattr(ccxt,exc)
                exd=self.auth_dict(exch.requiredCredentials,exc,exd)
                exchange=eval(f'ccxt.{exc}(exd)')
                if ta:exchange.set_sandbox_mode(True)
                if exchange.check_required_credentials():
                    self.main(exchange)
                    break
            except Exception as e:
                self.wd.get_menu(f'\n\033[1;31;40m{e}!!\033[0m')
