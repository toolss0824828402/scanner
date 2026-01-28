import requests
import re
import os
import time
import socket
import sys
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import questionary

console = Console()
AUTHOR = "Monkey D Dragon"
GITHUB_REPO = "https://github.com/toolss0824828402"

# قائمة موسعة جداً للمسارات والملفات الحساسة (تطوير 1000 ضعف)
SENSITIVE_DB = [
    '/admin', '/login', '/config.php', '/.env', '/backup.sql', '/.git', '/wp-json',
    '/phpmyadmin', '/api/v1', '/robots.txt', '/.htaccess', '/db_backup.zip',
    '/settings.py', '/docker-compose.yml', '/node_modules', '/v1/user/list',
    '/debug', '/cpanel', '/dashboard', '/test', '/tmp', '/private', '/ssh'
]

# قائمة النطاقات الفرعية الشائعة
SUBDOMAINS = ['admin', 'dev', 'test', 'api', 'mail', 'blog', 'staging', 'vpn', 'cloud']

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_event(data):
    try:
        with open("history.txt", "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {data}\n")
    except: pass

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
    [bold yellow]              COMMANDER: {AUTHOR}[/bold yellow]
    [bold cyan]      DRAGON'S FURY v8.0 | THE ULTIMATE INTEL ENGINE[/bold cyan]
    """
    console.print(Panel(banner, border_style="red"))

def scan_port(domain, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((domain, port)) == 0:
            return port
    except: pass
    finally: s.close()
    return None

def ultimate_dragon_engine(target):
    if not target.startswith(('http://', 'https://')): target = 'https://' + target
    parsed = urlparse(target)
    domain = parsed.netloc
    
    results = {"ports": [], "subdomains": [], "paths": [], "ip": "N/A", "geo": {}}

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TaskProgressColumn(), console=console) as progress:
        
        # 1. تحليل الـ IP والجغرافيا
        t1 = progress.add_task("[cyan]IP Intelligence...", total=100)
        try:
            results["ip"] = socket.gethostbyname(domain)
            results["geo"] = requests.get(f"http://ip-api.com/json/{results['ip']}", timeout=5).json()
            progress.update(t1, completed=100)
        except: progress.update(t1, description="[red]IP Error", completed=100)

        # 2. فحص النطاقات الفرعية (Subdomains)
        t2 = progress.add_task("[green]Hunting Subdomains...", total=len(SUBDOMAINS))
        base_domain = ".".join(domain.split(".")[-2:])
        for sub in SUBDOMAINS:
            try:
                sub_url = f"{sub}.{base_domain}"
                socket.gethostbyname(sub_url)
                results["subdomains"].append(sub_url)
            except: pass
            progress.advance(t2)

        # 3. فحص البورتات المتعدد (Multi-threaded Ports)
        t3 = progress.add_task("[yellow]Scanning Ports...", total=100)
        with ThreadPoolExecutor(max_workers=20) as executor:
            ports = [21, 22, 23, 25, 53, 80, 443, 3306, 8080, 27017]
            futures = [executor.submit(scan_port, domain, p) for p in ports]
            for f in futures:
                res = f.result()
                if res: results["ports"].append(res)
        progress.update(t3, completed=100)

        # 4. البحث العميق عن المسارات (Directory Brute)
        t4 = progress.add_task("[magenta]Deep Path Discovery...", total=len(SENSITIVE_DB))
        for path in SENSITIVE_DB:
            try:
                r = requests.head(urljoin(target, path), timeout=1, allow_redirects=False)
                if r.status_code in [200, 301, 403]:
                    results["paths"].append(f"{path} ({r.status_code})")
            except: pass
            progress.advance(t4)

    # --- العرض الأسطوري للنتائج ---
    print_banner()
    
    # خريطة البورتات والـ IP
    intel_t = Table(title="[bold red]Network Map[/bold red]", expand=True)
    intel_t.add_column("Type"); intel_t.add_column("Value", style="bold green")
    intel_t.add_row("IP", results["ip"])
    intel_t.add_row("ISP", results["geo"].get("isp", "N/A"))
    intel_t.add_row("Location", f"{results['geo'].get('country')} ({results['geo'].get('city')})")
    intel_t.add_row("Open Ports", ", ".join(map(str, results["ports"])))
    console.print(intel_t)

    # جدول النطاقات الفرعية
    sub_t = Table(title="[bold green]Subdomain Discovery[/bold green]", expand=True)
    sub_t.add_column("Host"); sub_t.add_column("Status")
    for s in results["subdomains"]: sub_t.add_row(s, "[green]ALIVE[/green]")
    console.print(sub_t)

    # جدول الملفات والمسارات
    path_t = Table(title="[bold magenta]Sensitive Files & Directories[/bold magenta]", expand=True)
    path_t.add_column("Path / File Found")
    for p in results["paths"]: path_t.add_row(f"[bold white]{p}[/bold white]")
    console.print(path_t)

    log_event(f"Ultimate Fury Scan: {target} | Subdomains: {len(results['subdomains'])} | Paths: {len(results['paths'])}")

def main():
    while True:
        print_banner()
        choice = questionary.select(
            "Welcome, Commander Dragon. Launch Operation:",
            choices=["Execute Full Fury Scan", "History Logs", "GitHub Repo", "Exit System"]
        ).ask()

        if choice == "Exit System": break
        if "Full" in choice:
            target = console.input("\n[bold white]Enter Target Domain: [/bold white]").strip()
            if target: ultimate_dragon_engine(target)
        elif "History" in choice:
            if os.path.exists("history.txt"):
                with open("history.txt", "r") as f: console.print(f.read())
        elif "GitHub" in choice:
            console.print(f"[bold cyan]Visit: {GITHUB_REPO}[/bold cyan]")
        
        questionary.press_any_key_to_continue().ask()

if __name__ == "__main__":
    main()
