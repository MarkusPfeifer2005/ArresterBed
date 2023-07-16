# /usr/bin/env python
import logging
import serial
import datetime
import time
import os
import json


def main():
    logging.basicConfig(filename="communication.log", level=logging.INFO, format='%(asctime)s %(message)s')

    with serial.Serial('/dev/ttyACM0', 115200) as connection:
        time.sleep(3)
        while True:
            connection.write(b"connection request\n")
            if connection.readline() == b"connection confirmation\r\n":
                connection.write(b"connection acknowledgement\n")
                break
        logging.info("Established connection (3-way handshake).")
        if not (data_directory := "Data") in os.listdir():
            os.mkdir(data_directory)
            logging.info("Created 'Data' directory.")
        else:
            logging.info("Checked if 'Data' directory is available.")
        # TODO: Add the possibility to stop an ongoing session and continue it afterwards.
        new_filename = f"Data/Distances_{datetime.datetime.now().strftime('%D_%H%M%S').replace('/', '')}.csv"
        configuration = {
            "x distance [mm]": float(input("Enter the x distance [mm]: ")),
            "y distance [mm]": float(input("Enter the y distance [mm]: ")),
            "x distance_step [mm]": float(input("Enter the x distance step [mm]: ")),
            "y distance_step [mm]": float(input("Enter the y distance step [mm]: ")),
        }
        for setting, value in configuration.items():
            connection.write(f"{value}\n".encode())
            logging.info(f"Sent '{setting}': {value}.")
        configuration["sphere diameter [mm]"] = float(input("Enter the diameter of the sphere [mm]: "))
        configuration["top tripod [mm]"] = float(input("Enter the height of the top tripod [mm]: "))
        configuration["top sand [mm]"] = float(input("Enter the height of the top sand [mm]: "))
        with open(new_filename.replace(".csv", ".json"), 'w') as json_file:
            json.dump(configuration, json_file)

        with open(new_filename, 'a') as csv_file:
            csv_file.write("x [mm],y [mm],z [mm]\n")
        time.sleep(1)
        connection.write(b"__start__\n")
        logging.debug("Sent start message.")
        time0 = datetime.datetime.now()
        while (message := connection.readline().decode().replace("\r", "")) != "__close__\n":
            time1 = datetime.datetime.now()
            logging.debug(message.replace("\n", "") + f"\t{time1-time0}")
            time0 = time1
            with open(new_filename, 'a') as csv_file:
                csv_file.write(message)


if __name__ == '__main__':
    main()
