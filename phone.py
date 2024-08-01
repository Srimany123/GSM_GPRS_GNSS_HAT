import serial
import time

# Replace '/dev/ttyS0' with the correct serial port for your Raspberry Pi to hat communication.
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

def send_at_command(command, sleep=1):
    ser.write((command + '\r').encode())
    time.sleep(sleep)
    response = ser.read(ser.inWaiting()).decode()
    return response

def send_sms(phone_number, message):
    send_at_command('AT+CMGF=1')  # Set SMS mode to text
    send_at_command(f'AT+CMGS="{phone_number}"')
    ser.write((message + '\x1A').encode())  # '\x1A' is the end-of-message char
    time.sleep(3)
    print("Message sent")

def make_call(phone_number):
    send_at_command(f'ATD{phone_number};')
    print("Call initiated. Type 'hangup' to end the call.")
    while True:
        command = input()
        if command.lower() == 'hangup':
            send_at_command('ATH')  # Hang up
            print("Call ended")
            break

def show_default_commands():
    print("\nDefault AT Commands and their Uses:")
    commands = [
        ("AT", "Test if the serial connection is working"),
        ("AT+CMGF=1", "Set SMS mode to text"),
        ("AT+CMGS=<number>", "Send SMS to <number>"),
        ("ATD<number>;", "Dial <number> and make a call"),
        ("ATH", "Hang up the call"),
        ("ATI", "Display product information"),
        ("AT+CSQ", "Signal quality test"),
        ("AT+CPIN?", "Check SIM card status"),
        ("AT+CREG?", "Network registration status"),
        ("AT+COPS?", "List available operators"),
        ("AT+CLIP=1", "Enable calling line identification"),
        ("AT+CLIR=1", "Restrict your number from being sent"),
        ("AT+CMGR=1", "Read SMS from storage location 1"),
        ("AT+CMGD=1", "Delete SMS at storage location 1"),
    ]
    for index, (command, description) in enumerate(commands, start=1):
        print(f"{index}. {command}: {description}")
    return commands

def execute_default_command(commands):
    index = int(input("Enter the command number: ")) - 1
    if 0 <= index < len(commands):
        command, _ = commands[index]
        if command == "AT+CMGS=<number>":
            phone_number = input("Enter phone number: ")
            message = input("Enter message: ")
            command = f'AT+CMGS="{phone_number}"'
            send_at_command(command)
            ser.write((message + '\x1A').encode())
            time.sleep(3)
        else:
            response = send_at_command(command)
            print(f"Response: {response}")
    else:
        print("Invalid command number.")

def custom_command():
    command = input("Enter the AT command to send: ")
    response = send_at_command(command)
    print(f"Response: {response}")

if __name__ == "__main__":
    while True:
        print("\nOptions:")
        print("1. Send SMS")
        print("2. Make Call")
        print("3. Show Default AT Commands")
        print("4. Execute Default AT Command by Number")
        print("5. Send Custom AT Command")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            phone_number = input("Enter phone number: ")
            message = input("Enter message: ")
            send_sms(phone_number, message)
        elif choice == '2':
            phone_number = input("Enter phone number: ")
            make_call(phone_number)
        elif choice == '3':
            show_default_commands()
        elif choice == '4':
            commands = show_default_commands()
            execute_default_command(commands)
        elif choice == '5':
            custom_command()
        elif choice == '6':
            break
        else:
            print("Invalid choice, please try again.")

    ser.close()
