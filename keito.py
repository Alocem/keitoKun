import websocket
import json
import time
import threading

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error occurred: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    uid = ws.uid  # Access UID from the WebSocketApp instance
    # Prepare the message
    message = {
        "id": 13,
        "cmd": 1001,
        "uid": uid,
        "data": {
            "amount": 500,
            "collectNum": 500,
            "timestamp": int(time.time() * 1000)
        }
    }
    
    # Send the message
    for _ in range(1000):
        ws.send(json.dumps(message))
        time.sleep(0.5)  # Add a small delay to avoid overwhelming the server
    print(f"Sent message for UID {uid}: {message}")


def run_websocket(uid):
    # Headers for the connection
    headers = {
        'Origin': 'https://game.keitokun.com',
        'Cache-Control': 'no-cache',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Cookie': '_ga=GA1.1.664420135.1739199804; _ga_LD12CVNEZ7=GS1.1.1739199803.1.1.1739199864.0.0.0'
    }

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"wss://game.keitokun.com/api/v1/ws?uid={uid}",
                                  header=headers,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
    ws.uid = uid  # Store UID in the WebSocketApp instance
    ws.run_forever()

def main():
    try:
        with open("account.txt", "r") as f:
            uids = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("Error: account.txt not found.  Please create it and put one UID per line.")
        return

    threads = []
    for uid in uids:
        thread = threading.Thread(target=run_websocket, args=(uid,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
