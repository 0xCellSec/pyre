import argparse
import nmap
import shutil
import subprocess
import yaml
from rich import print as rprint


class Tools:
    def __init__(self):
        with open("config.yaml", "r", encoding="utf-8") as file:
            self.data = yaml.safe_load(file)

    def run_nmap(self, target_ip):
        # initializing important decleration
        nm = nmap.PortScanner()
        post_scan_list = []

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
                    post_scan_list.append(str(port))

        return port_list

    def run_whatweb(self):
        subprocess.Popen(["whatweb", self.data["webpage"]])

    def run_directory_ffuf(self):
        subprocess.Popen(
            [
                "ffuf",
                "-ac",
                "-u",
                f"http://{self.data['webpage']}",
                "-w",
                self.data["directory_wordlist"],
            ],
        )

    def run_subdirectory_ffuf(self):
        subprocess.Popen(
            [
                "ffuf",
                "-ac",
                "-u",
                f"http://{self.data['webpage']}",
                "-H",
                f"Host:FUZZ.{self.data['webpage']}",
                "-w",
                self.data["subdirectory_wordlist"],
            ]
        )


def check_dependencies():
    # update this everytime a new tool is added
    REQUIRED_TOOLS = ["ffuf", "whatweb", "nmap"]
    missing_tool = False
    for tool in REQUIRED_TOOLS:
        if shutil.which(tool) == None:
            rprint(
                f"[bold red]\\[!] MISSING REQUIRED TOOL: {tool}[/bold red]",
            )
            missing_tool = True
    return missing_tool


def handle_web_recon():
    tools = Tools()
    # tools.run_whatweb()
    tools.run_directory_ffuf()
    tools.run_subdirectory_ffuf()


DISPATCH = {"80": handle_web_recon}


def main():
    parser = argparse.ArgumentParser(
        prog="PYRE",
        description="PYRE's your recon engine, is an auotmated recon tool to facilitate the initial recone stage",
    )
    parser.add_argument("-s", "--scan", help="-s <ip address>", type=str)
    parser.add_argument("-w", "--web", help="only does web recon")
    args = parser.parse_args()

    if check_dependencies() == True:
        return

    tools = Tools()
    for port in tools.run_nmap(args.scan):
        if str(port) in DISPATCH:
            DISPATCH[str(port)]()


main()
