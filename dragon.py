import requests
import re
import os
import time
import socket
import sys
from urllib.parse import urljoin, urlparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import questionary

# الإعدادات الفنية والحقوق
console = Console()
AUTHOR = "Monkey D Dragon"
GITHUB_REPO = "https://github.com/toolss0824828402/scanner.git"

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
    [bold cyan]      Official Repo: {GITHUB_REPO}[/bold cyan]
    """
    console.print(Panel(banner, border_style="red", title="v6.0 Ultimate Deep Crawler"))

def deep_dragon_scan(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # استخراج النطاق الأساسي لضمان البحث في نفس المسار
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc
    
    # متغيرات البيانات (للبحث عن 99+ معلومة)
    results_data = {
        "Network": {},
        "Internal_Links": [],
        "External_Links": [],
        "Vulnerabilities": [],
        "Metadata": [],
        "Security_Headers": []
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        # 1. تحليل الشبكة والاستخبارات
        t1 = progress.add_task("[cyan]Targeting Network...", total=100)
        try:
            ip_address = socket.gethostbyname(base_domain)
            geo = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5).json()
            results_data["Network"] = {"IP": ip_address, "Geo": geo}
            progress.update(t1, completed=100)
        except: progress.update(t1, description="[red]Net Error", completed=100)

        # 2. الزحف الذكي (نفس المسار + 99 معلومة)
        t2 = progress.add_task("[magenta]Deep Crawling Path...", total=100)
        try:
            response = requests.get(url, timeout=12, headers={'User-Agent': 'Mozilla/5.0'})
            # استخراج كافة الروابط وتحويلها لروابط كاملة
            raw_links = re.findall(r'href=["\'](.[^"\']+)["\']', response.text)
            
            for link in raw_links:
                full_link = urljoin(url, link)
                if base_domain in full_link:
                    results_data["Internal_Links"].append(full_link)
                else:
                    results_data["External_Links"].append(full_link)
            
            # البحث عن Metadata (أكثر من 99 نوع فرعي يمكن استخراجه هنا)
            metas = re.findall(r'<meta (.[^>]+)>', response.text)
            results_data["Metadata"] = metas[:99] # تحديد البحث بـ 99 معلومة
            
            progress.update(t2, completed=100)
        except: progress.update(t2, description="[red]Crawl Failed", completed=100)

        # 3. فحص الثغرات والرؤوس الأمنية
        t3 = progress.add_task("[red]Vulnerability Shield Test...", total=100)
        headers_to_check = ["Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options"]
        for header in headers_to_check:
            if header in response.headers:
                results_data["Security_Headers"].append(f"[green]✔ {header}[/green]")
            else:
                results_data["Security_Headers"].append(f"[red]✘ {header} (Missing)[/red]")
        
        # بايلودات فحص متقدمة
        payloads = {"SQLi": "' OR 1=1", "XSS": "<svg/onload=alert(1)>", "LFI": "../../../etc/passwd"}
        for name, p in payloads.items():
            try:
                test_r = requests.get(url, params={"id": p, "search": p}, timeout=5)
                if p in test_r.text:
                    results_data["Vulnerabilities"].append(f"[bold red]Potential {name} Risk[/bold red]")
            except: pass
        progress.update(t3, completed=100)

    # --- عرض التقارير النهائية بفخامة ---
    print_banner()
    
    # تقرير الاستخبارات
    net = results_data["Network"]
    geo = net.get("Geo", {})
    intel_table = Table(title="[bold yellow]Intelligence Report[/bold yellow]", expand=True)
    intel_table.add_column("Property", style="cyan")
    intel_table.add_column("Data")
    intel_table.add_row("Resolved IP", net.get("IP", "N/A"))
    intel_table.add_row("Origin", f"{geo.get('country', 'N/A')} - {geo.get('city', 'N/A')}")
    intel_table.add_row("ISP / Org", geo.get("org", "N/A"))
    console.print(intel_table)

    # تقرير الروابط (نفس المسار)
    links_count = len(results_data["Internal_Links"])
    link_table = Table(title=f"[bold magenta]Internal Path Links ({links_count})[/bold magenta]", expand=True)
    link_table.add_column("URL (Same Path Only)")
    for l in list(set(results_data["Internal_Links"]))[:15]: 
        link_table.add_row(l)
    console.print(link_table)

    # تقرير البيانات المكتشفة (99+)
    meta_table = Table(title=f"[bold green]Detected Meta/Asset Tags ({len(results_data['Metadata'])})[/bold green]", expand=True)
    meta_table.add_column("Tag Content")
    for m in results_data["Metadata"][:10]:
        meta_table.add_row(f"[dim]{m}[/dim]")
    console.print(meta_table)

    # تقرير الأمن
    sec_report = "\n".join(results_data["Security_Headers"] + results_data["Vulnerabilities"])
    console.print(Panel(sec_report, title="[bold red]Security Defense Analysis[/bold red]", border_style="red"))
    
    log_event(f"Deep Scan: {url} | Internal Links: {links_count} | IP: {net.get('IP')}")

def main():
    while True:
        print_banner()
        menu = questionary.select(
            "Welcome, Commander Dragon. Choose Operation:",
            choices=["Launch Deep Scan", "View Logs", "Update Tool", "Exit"]
        ).ask()

        if menu == "Exit": sys.exit()
        elif menu == "Launch Deep Scan":
            target = console.input("\n[bold white]Enter Target URL: [/bold white]").strip()
            if target: deep_dragon_scan(target)
        elif menu == "View Logs":
            clear_screen()
            if os.path.exists("history.txt"):
                with open("history.txt", "r") as f: console.print(f.read())
            else: console.print("[yellow]History empty.[/yellow]")
        elif menu == "Update Tool":
            os.system("git pull")
            console.print("[green]Tool updated if updates available.[/green]")
        
        questionary.press_any_key_to_continue().ask()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit()
