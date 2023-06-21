# /usr/bin/env python

import serial
import datetime
import time
import os


def main():
    with serial.Serial('/dev/ttyACM0', 115200) as connection:
        time.sleep(3)
        while True:
            connection.write(b"connection request\n")
            if connection.readline() == b"connection confirmation\r\n":
                connection.write(b"connection acknowledgement\n")
                break
        print("Established connection (3-way handshake).")
        if not (data_directory := "Data") in os.listdir():
            os.mkdir(data_directory)
            print("Created 'Data' directory.")
        else:
            print("Checked if 'Data' directory is available.")
        # TODO: Add a separate json file which holds all additional data for the session.
        # TODO: Create directory for each Session.
        # TODO: Add the possibility to stop an ongoing session and continue it afterwards.
        new_filename = f"Data/Distances_{datetime.datetime.now().strftime('%D_%H_%M_%S').replace('/', '_')}.csv"
        connection.write(f"{170.}\n".encode())  # x distance
        connection.write(f"{70.}\n".encode())  # y distance
        connection.write(f"{1.}\n".encode())  # x distance step
        connection.write(f"{1.}\n".encode())  # y distance step
        with open(new_filename, 'a') as csv_file:
            csv_file.write("x [mm],y [mm],z [mm]\n")
        time.sleep(1)
        connection.write(b"__start__\n")
        print("Sent start message.")
        time0 = datetime.datetime.now()
        while (message := connection.readline().decode().replace("\r", "")) != "__close__\n":
            time1 = datetime.datetime.now()
            print(message.replace("\n", "") + f"\t{time1-time0}")
            time0 = time1
            with open(new_filename, 'a') as csv_file:
                csv_file.write(message)


if __name__ == '__main__':
    main()
