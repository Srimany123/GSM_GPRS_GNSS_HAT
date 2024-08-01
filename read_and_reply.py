import serial
import time
from collections import defaultdict

# Replace '/dev/ttyS0' with the correct serial port for your Raspberry Pi to hat communication
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

def send_at_command(command, delay=2):
    ser.write((command + '\r').encode())
    time.sleep(delay)
    response = ser.read(ser.inWaiting()).decode()
    return response

def aggregate_messages():
    response = send_at_command('AT+CMGL="ALL"')
    messages_by_number = defaultdict(list)
    lines = response.split('\r\n')
    for i in range(len(lines)):
        if lines[i].startswith('+CMGL:'):
            header = lines[i].split(',')
            index = int(header[0].split(':')[1].strip())
            status = header[1].strip('"')
            number = header[2].strip('"')
            timestamp = header[4].strip('"')
            message = lines[i + 1]
            messages_by_number[number].append((index, status, timestamp, message))
    
    return messages_by_number

def delete_message_by_index(index):
    send_at_command(f'AT+CMGD={index}')
    print(f"Message at index {index} deleted.")

def delete_messages_from_number(number):
    messages = aggregate_messages()
    if number in messages:
        for index, _, _, _ in messages[number]:
            delete_message_by_index(index)
        print(f"All messages from {number} deleted.")
    else:
        print(f"No messages found for {number}.")

def delete_all_logs_from_number(number):
    delete_messages_from_number(number)
    print(f"All logs from {number} deleted.")

def reply_to_number(number, message):
    send_at_command('AT+CMGF=1')
    send_at_command(f'AT+CMGS="{number}"')
    ser.write((message + '\x1A').encode())
    time.sleep(3)
    print("Reply sent.")
    # Log the reply message with a timestamp
    timestamp = time.strftime("%Y/%m/%d, %H:%M:%S", time.gmtime())
    with open("replies_log.txt", "a") as log_file:
        log_file.write(f"Reply to {number} at {timestamp}: {message}\n")

def show_numbers():
    messages = aggregate_messages()
    print("Numbers with messages:")
    for i, number in enumerate(messages.keys(), start=1):
        print(f"{i}. {number}")
    return list(messages.keys())

def show_messages_by_number(number):
    messages = aggregate_messages()
    if number in messages:
        print(f"Messages from {number}:")
        for index, status, timestamp, msg in messages[number]:
            print(f"  - Index {index}: [{status}] {timestamp} - {msg}")
        print("Replies sent to this number:")
        show_replies(number)
    else:
        print(f"No messages found for {number}.")

def show_replies(number):
    try:
        with open("replies_log.txt", "r") as log_file:
            lines = log_file.readlines()
            for line in lines:
                if number in line:
                    print(f"  {line.strip()}")
    except FileNotFoundError:
        print("No replies logged yet.")

def main():
    while True:
        print("\nOptions:")
        print("1. Show numbers with messages")
        print("2. Show messages by number")
        print("3. Delete message by index")
        print("4. Delete all messages from a specific number")
        print("5. Reply to a specific number")
        print("6. Delete entire log from a specific number")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            numbers = show_numbers()
        elif choice == '2':
            number = input("Enter the number to show messages for: ")
            show_messages_by_number(number)
        elif choice == '3':
            index = int(input("Enter the index of the message to delete: "))
            delete_message_by_index(index)
        elif choice == '4':
            number = input("Enter the phone number to delete messages from: ")
            delete_messages_from_number(number)
        elif choice == '5':
            number = input("Enter the phone number to reply to: ")
            message = input("Enter the reply message: ")
            reply_to_number(number, message)
        elif choice == '6':
            number = input("Enter the phone number to delete entire log: ")
            delete_all_logs_from_number(number)
        elif choice == '7':
            break
        else:
            print("Invalid choice, please try again.")

    ser.close()

if __name__ == "__main__":
    main()
