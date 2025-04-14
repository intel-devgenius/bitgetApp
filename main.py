import tkinter as tk
import threading
import time
import bitget.v2.mix.account_api as AccountApi
import bitget.v2.mix.market_api as MarketApi
import bitget.v2.mix.order_api as OrderApi


from bitget.exceptions import BitgetAPIException
from tkinter import ttk, messagebox



# === Create App Window ===
def create_main_window():
    global root, data_thread, connect_status, stop_event
    connect_status = False
    stop_event = threading.Event()
    root = tk.Tk()
    root.title("Programa de Negociação Bitget")
    root.geometry("990x180")
    build_gui()
    # ======= Init GUI =========f
    dropdown.current(0)
    auto_checkButton.config(state="disabled")
    data_thread = threading.Thread(target=update_value, daemon=True)
    root.mainloop()
    

# === Button ===
def connect():
    global connect_status, account_API, market_API, order_API, connect_button
    global data_thread, stop_event  
    try:
        if not connect_status:
            api_key = api_entry.get()
            api_secret = secret_entry.get()
            passphrase = phrase_entry.get()
            account_API = AccountApi.AccountApi(api_key, api_secret, passphrase)
            market_API = MarketApi.MarketApi(api_key, api_secret, passphrase)
            order_API = OrderApi.OrderApi(api_key, api_secret, passphrase)
            
            stop_event.clear()  # Allow the thread to run
            if not data_thread or not data_thread.is_alive():  # Start the thread if not already running
                data_thread = threading.Thread(target=update_value, daemon=True)
                data_thread.start()
                auto_checkButton.config(state="normal")
                connect_button.config(text="Desconectar")
                secret_entry.config(state="readonly")
                api_entry.config(state="readonly")
                phrase_entry.config(state="readonly")         
                amount_entry.config(state="readonly")
                dropdown.state(["disabled"])
                time_entry.config(state = "disabled")
        else:
            if data_thread.is_alive():
                stop_event.set()
                exchange_rate_label.config(text=f"Taxa de câmbio: -------------")
                wallet_available_label.config(text=f"Carteira disponível: -------------")
                cur_pos_entry.config(text=f"-------------")
                available_pos_entry.config(text=f"-------------")
                auto_checkButton.config(state="disabled")
                connect_button.config(text="Conectar")
                secret_entry.config(state="normal")
                api_entry.config(state="normal")
                phrase_entry.config(state="normal")
                amount_entry.config(state="normal")
                dropdown.state(["!disabled"])
                time_entry.config(state = "normal")
        connect_status = not connect_status 
    except BitgetAPIException as e:
        messagebox.Error(e)
    
def exit_app():
    root.quit()

# === Build GUI Layout ===
def build_gui():
    create_top_section()
    create_checkboxes()
    create_auth_section()
    create_footer()
    create_last()
    
def dropdown_change(event):
    global symbol
    symbol = dropdown.get()
# === GUI Sections ===
def create_top_section():
    global dropdown, amount_entry, api_entry, connect_button
    global symbol
    dropdown = ttk.Combobox(root, values=["SOLUSDT", "BTCUSDT", "ETHUSDT"], width=20, state="readonly")
    dropdown.current(0)
    dropdown.bind("<<ComboboxSelected>>", dropdown_change)
    dropdown.grid(row=0, column=0, padx=10)
    symbol = dropdown.get()

    tk.Label(root, text="Valor da negociação").grid(row=0, column=1)
    amount_entry = tk.Entry(root, width=10)
    amount_entry.insert(0, "1")
    amount_entry.grid(row=0, column=2)

    tk.Label(root, text="API key").grid(row=0, column=4)
    api_entry = tk.Entry(root, width=45)
    api_entry.insert(0, "")
    api_entry.grid(row=0, column=5)
    connect_button = tk.Button(root, text="Conectar", width=10, command=connect)
    connect_button.grid(row=0, column=6)

def create_checkboxes():
    global auto_var, auto_checkButton, buy_checkButton
    global cur_pos_entry, available_pos_entry, time_entry

    auto_var = tk.BooleanVar(value=False)
    auto_checkButton = tk.Checkbutton(root, text="Automático/Manual", variable=auto_var)
    auto_checkButton.grid(row=1, column=0, sticky='w', padx=10)
    tk.Label(root, text="Máximo disponível: ").grid(row=1, column=1)
    cur_pos_entry = tk.Label(root, text = "-------------", width=20)
    cur_pos_entry.grid(row=1, column=2)
    tk.Label(root, text="Posição disponível:").grid(row=2, column=1)
    available_pos_entry = tk.Label(root, text = "-------------")
    available_pos_entry.grid(row=2, column=2)
    time_entry = tk.Entry(root, width=10)
    time_entry.insert(0, "60")
    time_entry.grid(row=2, column=0)

def create_auth_section():
    global secret_entry, phrase_entry

    tk.Label(root, text="Secret Key").grid(row=1, column=4)
    secret_entry = tk.Entry(root, width=45)
    secret_entry.insert(0, "")
    secret_entry.grid(row=1, column=5)

    tk.Label(root, text="PassPhrase").grid(row=2, column=4)
    phrase_entry = tk.Entry(root, width=45)
    phrase_entry.insert(0, "")
    phrase_entry.grid(row=2, column=5)
    

def create_footer():
    global exchange_rate_label, wallet_available_label, user_id_label, trading_status_label, current_sma_label, before_sma_label

    exchange_rate_label = tk.Label(root, text="Taxa de câmbio: -------------", width=30)
    exchange_rate_label.grid(row=4, column=0, pady=5)

    wallet_available_label = tk.Label(root, text="Carteira disponível: -------------")
    wallet_available_label.grid(row=4, column=1, padx=3, pady=5)
    trading_status_label = tk.Label(root, text="Status: ------")
    trading_status_label.grid(row=4, column=2, padx=3, pady=5)
    user_id_label = tk.Label(root, text = "Tempo: -------------")
    user_id_label.grid(row=4, column=5, padx=3, pady=5)
    current_sma_label = tk.Label(root, text = "Current SMA: -------------")
    current_sma_label.grid(row=3, column=1, padx=3, pady=5)
    before_sma_label = tk.Label(root, text = "Prev SMA: -------------")
    before_sma_label.grid(row=3, column=0, padx=3, pady=5)
    tk.Button(root, text="Sair", width=10, command=exit_app).grid(row=2, column=6)
def create_last():
    buy_open_button = tk.Button(root, text="Compre aberto", width=12, command = buyopen)
    buy_open_button.grid(row=6, column=0)
    sell_open_button = tk.Button(root, text="Vender aberto", width=12, command = sell_open)
    sell_open_button.config(state="disabled")
    sell_open_button.grid(row=6, column=1)
    buy_close_button = tk.Button(root, text="Compre Fechar", width=12, command = buy_close)
    buy_close_button.grid(row=6, column=2)
    sell_close_button = tk.Button(root, text="Vender Fechar", width=12, command = sell_close)
    sell_close_button.config(state="disabled")
    sell_close_button.grid(row=6, column=5)

def update_value():
    
    global current_price
    interval = float(time_entry.get())
    start_time = time.time()
    start_candle_time = start_time
    price_list =  []
    prev_price = 0
    now_price = 0
    while not stop_event.is_set():
        current_time = time.time()
        if not auto_var.get():
            start_time = current_time
        current_candle_time = current_time
        user_id_label.config(text = f"Tempo: {int(current_time - start_time)}")
        try:
            exch_data = market_API.ticker({"productType": "USDT-FUTURES", "symbol": symbol})
            wall_data = account_API.account({"productType": "USDT-FUTURES", "marginCoin": "USDT", "symbol": symbol})
            pos_data = account_API.singlePosition({"productType": "USDT-FUTURES", "symbol":symbol, "marginCoin":"USDT"})
            
            if exch_data['code'] == '00000' and wall_data['code'] == '00000' and pos_data['code'] == '00000':
                #manual method
                current_price = float(exch_data['data'][0]['lastPr'])
                price_list.append(current_price)
                crossedMarginLeverage = float(wall_data['data']['crossedMarginLeverage'])
                wallet_available = float(wall_data['data']['available'])
                exchange_rate_label.config(text=f"Taxa de câmbio: {current_price:.2f} USDT")
                wallet_available_label.config(text=f"Carteira disponível: {wallet_available:.2f} USDT")
                maximum_available = crossedMarginLeverage * wallet_available / current_price
                cur_pos_entry.config(text = f"{maximum_available:.2f}{symbol[:3]}")
                position_data = pos_data['data']
                available_position = 0
                if not position_data:
                    available_pos_entry.config(text = "0")
                    available_position = 0
                else:
                    available_position = position_data[0]['available']
                    available_pos_entry.config(text = f"{float(available_position): .2f}")
                
                if auto_var.get():#auto logic
                    print(f"current_time: {current_time}, start_time: {start_time}")
                    if current_candle_time - start_candle_time > interval:
                        print("candle change")
                        prev_price = now_price
                        # start_sma = current_sma
                        now_price = sum(price_list) / len(price_list)
                        price_list = []
                        # current_candles = market_API.candles({"symbol": symbol, "granularity": "1m", "productType": "USDT-FUTURES"})
                        # current_sma = sma(current_candles['data'])
                        start_candle_time = current_candle_time
                        current_sma_label.config(text = f"Current SMA: {now_price:.2f}")
                        before_sma_label.config(text = f"Prev SMA: {prev_price:.2f}")
                    if(current_time - start_time > interval):
                        print("trading time")
                        if prev_price != 0:
                            if now_price < prev_price:
                                print("1", maximum_available, amount_entry.get())
                                if float(maximum_available) >1.001*float(amount_entry.get()):
                                    buy_trading("buy","open")
                                    trading_status_label.config(text=f"Status: Abrir") 
                                else:
                                    trading_status_label.config(text=f"Status:Não Abrir")
                            else:
                                print("2",available_position, current_price)
                                if float(available_position) >=float(amount_entry.get()):
                                    buy_trading("buy", "close")
                                    trading_status_label.config(text=f"Status: Fechar")  
                                else:
                                    trading_status_label.config(text=f"Status: DesFechar")      
                        start_time = current_time   
                    
            else:
                exchange_rate_label.config(text=f"Taxa de câmbio: -------------")
                wallet_available_label.config(text=f"Carteira disponível: -------------")
                trading_status_label.config(text=f"Status: ------")
        except BitgetAPIException as e:
            print(f"Error in update_value: {e}")
            start_time = current_time
            start_candle_time = current_candle_time

def buyopen():
    buy_trading("buy", "open")
    
def buy_close():
    buy_trading("buy", "close")
    
def sell_open():
    buy_trading("sell", "open")
    
def sell_close():
    buy_trading("sell", "close")

def buy_trading(tt,stat):
    global current_price
    try:
        params = {
            "symbol": symbol,
            "productType": "USDT-FUTURES",
            "marginMode": "isolated",
            "marginCoin": "USDT",
            "size": amount_entry.get(),
            "price" : str(current_price),
            "side" : tt,
            "tradeSide" : stat,
            "orderType" : "limit",
        }
        response = order_API.placeOrder(params)
        print(f"{tt} {stat}", response)
    except NameError:
        print("current_price is not initialized yet.")
        return

def sma(data) :
    sum = 0
    for i in data:
        sum += float(i[1])
    return sum / len(data)

# === Launch App ===
if __name__ == "__main__":
    create_main_window()
    
