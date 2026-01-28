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

# إعدادات الواجهة والحقوق
console = Console()
AUTHOR = "Monkey D Dragon"
GITHUB_LINK = "https://github.com/toolss0824828402"

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
    [bold cyan]    GitHub: {GITHUB_LINK}[/bold cyan]
    """
    console.print(Panel(banner, border_style="red", subtitle="v4.0 Final Edition"))

def advanced_scan(target_url):
    # تصحيح الرابط تلقائياً
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url

    # قيم افتراضية لمنع أخطاء UnboundLocalError
    ip_addr = "Unknown"
    geo_info = {}
    found_links = []
    vulns = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        # المرحلة 1: المعلومات الأساسية
        t1 = progress.add_task("[cyan]Scanning Network Info...", total=100)
        try:
            domain = target_url.replace('https://','').replace('http://','').split('/')[0]
            ip_addr = socket.gethostbyname(domain)
            response = requests.get(f"http://ip-api.com/json/{ip_addr}", timeout=5)
            if response.status_code == 200:
                geo_info = response.json()
            progress.update(t1, completed=100)
        except:
            progress.update(t1, description="[red]Network Scan Failed", completed=100)

        # المرحلة 2: استخراج الروابط
        t2 = progress.add_task("[magenta]Scraping Content...", total=100)
        try:
            res = requests.get(target_url, timeout=10)
            found_links = list(set(re.findall(r'https?://[^\s<>"]+', res.text)))
            progress.update(t2, completed=100)
        except:
            progress.update(t2, description="[red]Scraping Failed", completed=100)

        # المرحلة 3: فحص الثغرات التجريبي
        t3 = progress.add_task("[red]Security Testing...", total=100)
        payloads = {"SQLi": "' OR 1=1 --", "XSS": "<script>alert(1)</script>"}
        for p_name, p_val in payloads.items():
            try:
                test_res = requests.get(target_url, params={"test": p_val}, timeout=5)
                if p_val in test_res.text:
                    vulns.append(f"[bold red]Detected: {p_name}[/bold red]")
            except: pass
        progress.update(t3, completed=100)

    # عرض التقارير النهائية
    print_banner()
    
    # جدول معلومات الموقع (تم حل مشكلة geo_info هنا)
    info_table = Table(title="[bold cyan]Target Intelligence Report[/bold cyan]", expand=True)
    info_table.add_column("Information", style="yellow")
    info_table.add_column("Value", style="white")
    info_table.add_row("IP Address", ip_addr)
    info_table.add_row("Country", geo_info.get('country', 'N/A'))
    info_table.add_row("City", geo_info.get('city', 'N/A'))
    info_table.add_row("ISP", geo_info.get('isp', 'N/A'))
    console.print(info_table)

    # جدول الروابط
    link_table = Table(title=f"[bold magenta]Detected Links ({len(found_links)})[/bold magenta]", expand=True)
    link_table.add_column("Sample URL", overflow="fold")
    for l in found_links[:12]: # عرض أول 12 رابط فقط
        link_table.add_row(l)
    console.print(link_table)

    # تقرير الأمان
    v_report = "\n".join(vulns) if vulns else "[green]No common flaws detected in basic scan.[/green]"
    console.print(Panel(v_report, title="[bold red]Security Analysis[/bold red]", border_style="red"))
    
    log_result(f"Scan on {target_url} | IP: {ip_addr} | Links: {len(found_links)}")

def main():
    while True:
        print_banner()
        choice = questionary.select(
            "Welcome, Dragon. Execute your command:",
            choices=[
                "1. Full Deep Scan",
                "2. View Command History",
                "3. Credits & Social",
                "4. Exit"
            ]
        ).ask()

        if choice == "4. Exit":
            console.print("[bold red]Dragon Offline.[/bold red]")
            break
        
        if "1." in choice:
            target = console.input("\n[bold white]Enter Target URL: [/bold white]")
            advanced_scan(target)
        elif "2." in choice:
            clear_screen()
            if os.path.exists("history.txt"):
                with open("history.txt", "r") as f: console.print(f.read())
            else: console.print("[yellow]History is empty.[/yellow]")
        elif "3." in choice:
            console.print(Panel(f"Developer: {AUTHOR}\nGitHub: {GITHUB_LINK}", title="About"))
        
        questionary.press_any_key_to_continue().ask()

if __name__ == "__main__":
    main()
