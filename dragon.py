import requests
import re
import os
import time
import socket
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import questionary

console = Console()
AUTHOR = "Monkey D Dragon"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_result(data):
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {data}\n")

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
    [bold yellow]             COMMANDER: {AUTHOR}[/bold yellow]
    [bold white]   REAL-TIME WEB INTELLIGENCE & SECURITY SUITE v3.0[/bold white]
    """
    console.print(Panel(banner, border_style="red"))

def advanced_scan(target_url):
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        # المرحلة 1: جمع معلومات الشبكة
        task1 = progress.add_task("[cyan]Gathering Network Info...", total=100)
        try:
            domain = target_url.replace('https://','').replace('http://','').split('/')[0]
            ip_addr = socket.gethostbyname(domain)
            geo_info = requests.get(f"http://ip-api.com/json/{ip_addr}", timeout=5).json()
            progress.update(task1, completed=100)
        except:
            progress.update(task1, description="[red]Network Info Failed", completed=100)

        # المرحلة 2: فحص الروابط (Mass Scan)
        task2 = progress.add_task("[magenta]Scraping & Checking Links...", total=100)
        try:
            res = requests.get(target_url, timeout=10)
            found_links = list(set(re.findall(r'https?://[^\s<>"]+', res.text)))
            progress.update(task2, completed=100)
        except:
            found_links = []
            progress.update(task2, description="[red]Scraping Failed", completed=100)

        # المرحلة 3: فحص الثغرات التجريبي
        task3 = progress.add_task("[red]Testing Vulnerabilities...", total=100)
        vulns = []
        payloads = {"SQLi": "' OR 1=1", "XSS": "<script>alert(1)</script>"}
        for p_name, p_val in payloads.items():
            try:
                r = requests.get(target_url, params={"test": p_val}, timeout=5)
                if p_val in r.text: vulns.append(f"[red]Confirmed {p_name}[/red]")
            except: pass
        progress.update(task3, completed=100)

    # عرض النتائج في جداول احترافية
    print_banner()
    
    # جدول 1: معلومات الموقع
    info_table = Table(title="[bold cyan]Target Origin Report[/bold cyan]", expand=True)
    info_table.add_column("Property", style="yellow")
    info_table.add_column("Value", style="white")
    info_table.add_row("IP Address", ip_addr)
    info_table.add_row("Country", geo_info.get('country', 'Unknown'))
    info_table.add_row("ISP", geo_info.get('isp', 'Unknown'))
    console.print(info_table)

    # جدول 2: فحص الروابط
    link_table = Table(title=f"[bold magenta]Extracted Links ({len(found_links)})[/bold magenta]", expand=True)
    link_table.add_column("Link Sample", overflow="fold")
    for l in found_links[:10]: link_table.add_row(l)
    console.print(link_table)

    # جدول 3: الثغرات
    v_status = "[green]No common vulnerabilities found (Basic Test)[/green]" if not vulns else ", ".join(vulns)
    console.print(Panel(f"Vulnerability Status: {v_status}", title="[bold red]Security Report[/bold red]", border_style="red"))
    
    log_result(f"Full Scan on {target_url} - IP: {ip_addr} - Links: {len(found_links)}")

def main():
    while True:
        print_banner()
        choice = questionary.select(
            "Welcome, Commander Dragon. Select your operation:",
            choices=["Start Deep Scan", "View Saved History", "Tool Update", "Exit"]
        ).ask()

        if choice == "Exit":
            break
        elif choice == "View Saved History":
            clear_screen()
            if os.path.exists("history.txt"):
                with open("history.txt", "r") as f: console.print(f.read())
            else: console.print("[yellow]No history yet.[/yellow]")
        elif choice == "Start Deep Scan":
            target = console.input("\n[bold white]Enter URL to Scan: [/bold white]")
            advanced_scan(target)
        
        questionary.press_any_key_to_continue().ask()

if __name__ == "__main__":
    main()
