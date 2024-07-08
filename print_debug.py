from datetime import  datetime

disable_print = True

print_string = ""
def millis():
    now = datetime.now()
    return now.microsecond // 1000


time_stamp = millis()

def print_time(msg):
    global disable_print
    if disable_print:
        return
    global time_stamp
    global print_string
    print_string = f'{print_string}{millis() - time_stamp}ms- {msg}\n'
    time_stamp = millis()


def commit_print():
    global disable_print
    if disable_print:
        return
    global print_string
    print("-------------------------")
    print(print_string)
    print_string = ""