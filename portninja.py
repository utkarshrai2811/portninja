#!/usr/bin/python3

import socket
import os
import threading
import sys
from queue import Queue
from datetime import datetime

def main():
    socket.setdefaulttimeout(0.30)
    print_lock = threading.Lock()
    open_ports = []

    target = input("Enter the target IP address or URL: ")
    try:
        target_ip = socket.gethostbyname(target)
    except (UnboundLocalError, socket.gaierror):
        print("\n[-] Invalid format. Please provide a correct IP or web address. [-]\n")
        sys.exit()

    print("=" * 60)
    print("Scanning target "+ target_ip)
    print("Time started: "+ str(datetime.now()))
    print("=" * 60)
    start_time = datetime.now()

    def scan_port(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            port_connection = s.connect((target_ip, port))
            with print_lock:
                print("Port {} is open".format(port))
                open_ports.append(str(port))
            port_connection.close() # type: ignore

        except (ConnectionRefusedError, AttributeError, OSError):
            pass

    def worker():
        while True:
            port = port_queue.get()
            scan_port(port)
            port_queue.task_done()

    port_queue = Queue()
    for _ in range(200):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    for port in range(1, 65536):
        port_queue.put(port)

    port_queue.join()

    end_time = datetime.now()
    total_time = end_time - start_time
    print("Port scan completed in " + str(total_time))
    print("=" * 60)
    print("PortNinja recommends the following Nmap scan:")
    print("*" * 60)
    print("nmap -p {ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(open_ports), ip=target))
    print("*" * 60)
    nmap_command = "nmap -p {ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(open_ports), ip=target)
    end_time = datetime.now()
    total_time = end_time - start_time

    def automate():
        while True:
            print("Would you like to run the suggested Nmap scan?")
            print("-" * 60)
            print("1 = Run suggested Nmap scan")
            print("2 = Quit to terminal")
            print("-" * 60)
            choice = input("Option Selection: ")
            if choice == "1":
                try:
                    print(nmap_command)
                    os.makedirs(target, exist_ok=True)
                    os.chdir(target)
                    os.system(nmap_command)
                    end_time = datetime.now()
                    total_time = end_time - start_time
                    print("-" * 60)
                    print("Combined scan completed in " + str(total_time))
                    input("Press enter to quit...")
                    sys.exit()
                except FileExistsError as e:
                    print(e)
                    sys.exit()
            elif choice == "2":
                print("\nSayōnara")
                sys.exit()
            else:
                print("Please make a valid selection")

    automate()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nSayōnara")
        sys.exit()
