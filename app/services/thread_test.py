
# import threading
# import time
# import random

# db = {}
# lock = threading.Lock()

# def delete_expired_keys():
#     global db
#     with lock:
#         for key in [key for key, (val, ex) in db.items() if time.time() >= ex]:
#             del db[key]
#             print(db)

# # checking expired keys function
# def check_expired_key():
#     while True:
#         delete_expired_keys()
#         time.sleep(1)


# if __name__ =="__main__":
#     checkThread = threading.Thread(target=check_expired_key)
#     checkThread.daemon = True
#     checkThread.start()

#     while True:
#         now = time.time()
#         print(f"Time is {time.time()}")
#         db[input("Enter a new key!: ")] = (random.randint(0,100), now + 10)


db = {
    "key": (10, {"ex": 10}),
    "key1": (10, {"ex": 10}),
    "key2": (10, {"ex": 10}),
    "key3": (10, {"ex": 10}),
}

for key, (value, options) in db.items():
    print(options)