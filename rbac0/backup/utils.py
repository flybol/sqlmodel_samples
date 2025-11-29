import time

def get_ms_timestamp():
    timestamp = time.time()
    ms_timestamp = int(timestamp * 1000)
    return ms_timestamp