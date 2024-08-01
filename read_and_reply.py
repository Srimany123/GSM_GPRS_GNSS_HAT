import serial
import time
from collections import defaultdict

# Replace '/dev/ttyS0' with the correct serial port for your Raspberry Pi
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

def send_at_command(command, delay=2):
    ser.write((command + '\r').encode())  # Send the command
    time.sleep(delay)  # Wait for the module to process the command
    response = ser.read(ser.inWaiting()).decode()  # Read the response
    return response

def aggregate_messages_by_number():
    response = send_at_command('AT+CMGL="ALL"')
    messages_by_number = defaultdict(list)
    
    lines = response.split('\r\n')
    for i in range(len(lines)):
        if lines[i].startswith('+CMGL:'):
            header = lines[i].split(',')
            index = int(header[0].split(':')[1].strip())
            number = header[2].strip('"')
            message = lines[i+1]
            messages_by_number[number].append((index, message))
    
    return messages_by_number

def delete_message_by_index(index):
    send_at_command(f'AT+CMGD={index}')
    print(f"Message at index {index} deleted.")

def delete_messages_from_number(number):
    messages = aggregate_messages_by_number()
    if number in messages:
        for index, _ in messages[number]:
            delete_message_by_index(index)
        print(f"All messages from {number} deleted.")
    else:
        print(f"No messages found for {number}.")

def delete_all_logs_from_number(number):
    messages = aggregate_messages_by_number()
    if number in messages:
        for index, _ in messages[number]:
            delete_message_by_index(index)
        print(f"All logs from {number} deleted.")
    else:
        print(f"No logs found for {number}.")

def reply_to_number(number, message):
    send_at_command('AT+CMGF=1')
    send_at_command(f'AT+CMGS="{number}"')
    ser.write((message + '\x1A').encode())
    time.sleep(3)
    print("Reply sent.")

def main():
    while True:
        print("\nOptions:")
        print("1. Aggregate messages by number")
        print("2. Delete message by index")
        print("3. Delete all messages from a specific number")
        print("4. Reply to a specific number")
        print("5. Delete entire log from a specific number")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            messages = aggregate_messages_by_number()
            for number, msgs in messages.items():
                print(f"Messages from {number}:")
                for index, msg in msgs:
                    print(f"  - Index {index}: {msg}")
        elif choice == '2':
            index = int(input("Enter the index of the message to delete: "))
            delete_message_by_index(index)
        elif choice == '3':
            number = input("Enter the phone number to delete messages from: ")
            delete_messages_from_number(number)
        elif choice == '4':
            number = input("Enter the phone number to reply to: ")
            message = input("Enter the reply message: ")
            reply_to_number(number, message)
        elif choice == '5':
            number = input("Enter the phone number to delete entire log: ")
            delete_all_logs_from_number(number)
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")

    ser.close()

if __name__ == "__main__":
    main()
