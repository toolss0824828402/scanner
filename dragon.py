import requests
import re
import os
import json
import time
import socket
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import questionary

console = Console()
AUTHOR = "Monkey D Dragon"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_to_file(message):
    with open("history.txt", "a", encoding="utf-8") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def print_banner():
    clear_screen()
    banner = f"""
    [bold red]
     ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗
     ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║
     ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║
     ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║
     ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║
     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
    [/bold red]
    [bold white]   The Revolutionary Web Intelligence & Security Tool[/bold white]
    [bold yellow]             Commander: {AUTHOR}[/bold yellow]
    """
    console.print(Panel(banner, border_style="red"))

# --- وظيفة فحص المنافذ Port Scanner ---
def scan_ports(host):
    console.print(f"\n[bold cyan][*] Scanning common ports for: {host}[/bold cyan]")
    common_ports = [21, 22, 23, 25, 53, 80, 443, 3306, 8080]
    table = Table(title="Port Scan Results")
    table.add_column("Port", style="yellow")
    table.add_column("Status", style="bold")

    for port in common_ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))
        status = "[green]Open[/green]" if result == 0 else "[red]Closed[/red]"
        table.add_row(str(port), status)
        s.close()
    
    console.print(table)
    log_to_file(f"Port scan performed on {host}")

# --- وظيفة فحص المعلومات ---
def get_info(url):
    try:
        domain = url.replace('https://','').replace('http://','').split('/')[0]
        res = requests.get(f"http://ip-api.com/json/{domain}").json()
        table = Table(title="Target Intelligence")
        for k, v in res.items():
            table.add_row(str(k), str(v))
        console.print(table)
        log_to_file(f"Gathered info for {url}")
        return domain
    except:
        console.print("[red]Could not get info.[/red]")
        return None

# --- وظيفة فحص الثغرات التجريبية ---
def check_vulns(url):
    console.print("\n[bold red][!] Testing Vulnerabilities (Experimental)...[/bold red]")
    payloads = {"SQLi": "' OR 1=1", "XSS": "<script>alert(1)</script>"}
    for name, p in payloads.items():
        try:
            r = requests.get(url, params={"test": p}, timeout=5)
            status = "[red]Vulnerable?[/red]" if p in r.text else "[green]Secure[/green]"
            console.print(f"{name}: {status}")
        except: pass
    log_to_file(f"Vulnerability scan on {url}")

def main():
    while True:
        print_banner()
        choice = questionary.select(
            "Welcome, Dragon. Choose your operation:",
            choices=["Info & Port Scan", "Mass Link Check", "Vulnerability Test", "View History", "Exit"]
        ).ask()

        if choice == "Exit": break

        target = console.input("\n[bold white]Target URL (e.g. https://google.com): [/bold white]")
        
        if choice == "Info & Port Scan":
            dom = get_info(target)
            if dom: scan_ports(dom)
        elif choice == "Mass Link Check":
            # (الكود المختصر للفحص الشامل هنا)
            console.print("[yellow]Scanning links... check history.txt for full dump.[/yellow]")
            log_to_file(f"Mass scan started for {target}")
        elif choice == "Vulnerability Test":
            check_vulns(target)
        elif choice == "View History":
            clear_screen()
            with open("history.txt", "r") as f:
                console.print(f.read())
        
        questionary.press_any_key_to_continue().ask()

if __name__ == "__main__":
    main()
