from rich.console import Console
import argparse
import nmap
import subprocess


def main():
    parser = argparse.ArgumentParser(
        prog="PYRE",
        description="PYRE's your recon engine, is an auotmated recon tool to facilitate the initial recone stage",
    )
    parser.add_argument("-s", "--scan", help="-s <ip address>", type=str)
    parser.add_argument("-d", "-dns", help="-d <website domain (google.com, etc)>")
    parser.add_argument("-H", "--host")

    args = parser.parse_args()
    # initializing important decleration
    nm = nmap.PortScanner()
    target_ip = args.scan

    # scans target's top 1000 ports
    nm.scan(target_ip, "1-1000", arguments="-T5 -sC -sV")

    for host in nm.all_hosts():
        print(f"Target: {host}")
        print(f"State: {nm[host].state()}")
        print("---------------------------------")
        for protocol in nm[host].all_protocols():
            port_list = nm[host][protocol].keys()

            for port in sorted(port_list):
                port_info = nm[host][protocol][port]
                print(
                    f"{port}\t{port_info['state']}\t{port_info['name']}\t{port_info['product']}\t{port_info['version']}\n"
                )


main()
