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

    def run_nmap_and_fetch_port_list(self, target_ip):
        # initializing important decleration
        nm = nmap.PortScanner()
        list_ports = []

        # scans target's top 1000 ports
        nm.scan(target_ip, "1-1000", arguments="-T5 -sC -sV -oN pyre_output.txt")

        for host in nm.all_hosts():
            print(f"Target: {host}")
            print(f"State: {nm[host].state()}")
            print("---------------------------------")
            for protocol in nm[host].all_protocols():
                protocol_port_list = nm[host][protocol].keys()

                for port in sorted(protocol_port_list):
                    port_info = nm[host][protocol][port]
                    print(
                        f"{port}\t{port_info['state']}\t{port_info['name']}\t{port_info['product']}\t{port_info['version']}\n"
                    )
                    list_ports.append(str(port))

        return list_ports

    def run_directory_ffuf(self):
        subprocess.Popen(
            [
                "ffuf",
                "-t",
                str(self.data["ffuf_concurrency"]),
                "-ac",
                "-u",
                f"http://{self.data['webpage']}",
                "-H",
                f"Host:{self.data['webpage']}/FUZZ",
                "-w",
                self.data["directory_wordlist"],
            ],
        )

    def run_subdirectory_ffuf(self):
        subprocess.Popen(
            [
                "ffuf",
                "-t",
                str(self.data["ffuf_concurrency"]),
                "-ac",
                "-u",
                f"http://{self.data['webpage']}",
                "-H",
                f"Host:FUZZ.{self.data['webpage']}",
                "-w",
                self.data["subdirectory_wordlist"],
            ]
        )


def has_all_dependencies():
    # update this everytime a new tool is added
    LIST_REQUIRED_TOOLS = ["ffuf", "nmap"]
    is_tool_missing = False
    for tool in LIST_REQUIRED_TOOLS:
        if shutil.which(tool) == None:
            rprint(
                f"[bold red]\\[!] MISSING REQUIRED TOOL: {tool}[/bold red]",
            )
            is_tool_missing = True
    return is_tool_missing


def call_web_recon_tools():
    tools = Tools()
    # tools.run_whatweb()
    tools.run_directory_ffuf()
    tools.run_subdirectory_ffuf()


FETCH_TOOL_COMMAND = {"80": call_web_recon_tools}


def main():
    parser = argparse.ArgumentParser(
        prog="PYRE",
        description="PYRE's your recon engine, is an auotmated recon tool to facilitate the initial recone stage",
    )
    parser.add_argument("-s", "--scan", help="-s <ip address>", type=str)
    parser.add_argument("-w", "--web", help="only does web recon")
    args = parser.parse_args()

    if has_all_dependencies() == True:
        return

    tools = Tools()

    has_nmap_results = tools.run_nmap_and_fetch_port_list(args.scan)
    if has_nmap_results:
        for port in has_nmap_results:
            if str(port) in FETCH_TOOL_COMMAND:
                FETCH_TOOL_COMMAND[str(port)]()
    else:
        rprint("[bold red]\\[!] Ports scan is empty[bold red]")
        rprint("[bold blue]\\[+] Opening scan result for manual check")
        subprocess.Popen(["cat", "pyre_output.txt"])


main()
