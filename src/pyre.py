import argparse
import nmap
import shutil
import subprocess
import os
from rich import print as rprint


def check_dependencies():
    REQUIRED_TOOLS = ["ffuf", "whatweb", "nikto", "nmap"]
    for tool in REQUIRED_TOOLS:
        if shutil.which(tool) == None:
            rprint(
                f"[bold red]\\[!] MISSING REQUIRED TOOL: {tool}[/bold red]",
            )


def run_nmap(target_ip):
    # initializing important decleration
    nm = nmap.PortScanner()

    # scans target's top 1000 ports
    nm.scan(target_ip, "1-1000", arguments="-T5 -sC -sV -oN pyre_output.txt")

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


def run_ffuf(target_ip):

    subprocess.Popen(
        [
            "ffuf",
            "-u",
            f"http://{target_ip}",
            "-w",
            "/usr/share/wordlists/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt",
        ]
    )


def main():
    parser = argparse.ArgumentParser(
        prog="PYRE",
        description="PYRE's your recon engine, is an auotmated recon tool to facilitate the initial recone stage",
    )
    parser.add_argument("-s", "--scan", help="-s <ip address>", type=str)
    parser.add_argument("-w", "--wordlist", help="-w path/to/wordlist.txt")
    parser.add_argument("-H", "--host")
    args = parser.parse_args()

    check_dependencies()
    run_nmap(args.scan)
    run_ffuf(args.scan)


main()
