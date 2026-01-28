import requests
import re
import os
import time
import socket
import ssl
import json
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
import questionary
from OpenSSL import crypto

# الإعدادات الفنية والحقوق
console = Console()
AUTHOR = "Monkey D Dragon"
USER_GITHUB = "https://github.com/toolss0824828402"

class DragonIntelligence:
    def __init__(self, url):
        self.url = url if url.startswith('http') else 'https://' + url
        self.domain = urlparse(self.url).netloc
        self.results = {
            "api_keys": [], "tech_stack": [], "vulnerabilities": [],
            "ssl_info": {}, "discovered_files": [], "threats": []
        }

    # 1. صائد الـ API واستخراج الروابط من JS
    def api_js_hunter(self, html_content):
        # البحث عن أنماط مفاتيح API شائعة
        patterns = {
            "Google API": r"AIza[0-9A-Za-z-_]{35}",
            "Firebase": r"https://.*\.firebaseio\.com",
            "Generic Key": r"(?i)(key|api|token|secret|auth|password)[\s]*[:=][\s]*[\"']([a-zA-Z0-9_\-]{16,})[\"']"
        }
        for name, pattern in patterns.items():
            found = re.findall(pattern, html_content)
            if found: self.results["api_keys"].append(f"{name}: Found")

    # 2. فحص تقنيات الموقع (Wappalyzer Clone)
    def detect_tech(self, response):
        headers = response.headers
        tech = []
        if 'X-Powered-By' in headers: tech.append(headers['X-Powered-By'])
        if 'Server' in headers: tech.append(headers['Server'])
        if 'wp-content' in response.text: tech.append("WordPress CMS")
        if 'react' in response.text.lower(): tech.append("React.js")
        self.results["tech_stack"] = list(set(tech))

    # 4. فحص SSL/TLS المتقدم
    def analyze_ssl(self):
        try:
            cert = ssl.get_server_certificate((self.domain, 443))
            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            self.results["ssl_info"] = {
                "Issuer": x509.get_issuer().CN,
                "Expiry": x509.get_notAfter().decode('utf-8'),
                "Version": x509.get_version()
            }
        except: self.results["ssl_info"] = {"Status": "SSL Scan Failed"}

    # 10. صائد المستودعات (Repo Hunter)
    def repo_hunter(self):
        repos = ['/.git/config', '/.svn/entries', '/.env', '/composer.json', '/package.json']
        for repo in repos:
            try:
                r = requests.head(urljoin(self.url, repo), timeout=3)
                if r.status_code == 200: self.results["discovered_files"].append(repo)
            except: pass

def print_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    banner = f"""
    [bold red]
     ██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗
     ██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║
     ██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║
     ██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║
     ██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║
     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
    [/bold red]
    [bold yellow]              DEVELOPER: {AUTHOR}[/bold yellow]
    [bold cyan]      GITHUB: {USER_GITHUB}[/bold cyan]
    """
    console.print(Panel(banner, border_style="red", title="v9.0 KRAKEN EDITION"))

def run_kraken_engine(target):
    dragon = DragonIntelligence(target)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TaskProgressColumn(), console=console) as progress:
        
        t1 = progress.add_task("[cyan]Hunting APIs & Repos...", total=100)
        dragon.repo_hunter()
        progress.update(t1, completed=50)
        
        try:
            res = requests.get(dragon.url, timeout=10)
            dragon.api_js_hunter(res.text)
            dragon.detect_tech(res)
        except: pass
        progress.update(t1, completed=100)

        t2 = progress.add_task("[yellow]SSL Security Analysis...", total=100)
        dragon.analyze_ssl()
        progress.update(t2, completed=100)

    # --- عرض التقارير النهائية ---
    print_banner()
    
    # جدول الاستخبارات
    t_intel = Table(title="Intelligence Gathering", expand=True)
    t_intel.add_column("System"); t_intel.add_column("Findings", style="bold green")
    t_intel.add_row("Tech Stack", ", ".join(dragon.results["tech_stack"]))
    t_intel.add_row("Exposed Repos", ", ".join(dragon.results["discovered_files"]))
    t_intel.add_row("SSL Issuer", str(dragon.results["ssl_info"].get("Issuer")))
    console.print(t_intel)

    # لوحة الـ APIs
    api_report = "\n".join(dragon.results["api_keys"]) if dragon.results["api_keys"] else "No API Leaks Found"
    console.print(Panel(api_report, title="[bold red]API Hunter Results[/bold red]", border_style="red"))

    # نظام التقارير الاحترافية (حفظ تلقائي)
    report_name = f"report_{dragon.domain}.json"
    with open(report_name, "w") as f:
        json.dump(dragon.results, f, indent=4)
    console.print(f"\n[bold green][+] Professional Report Saved: {report_name}[/bold green]")

def main():
    while True:
        print_banner()
        cmd = questionary.select(
            "Kraken System Command:",
            choices=["Full Intelligence Scan", "View My GitHub", "Exit"]
        ).ask()

        if cmd == "Exit": break
        if cmd == "View My GitHub":
            console.print(f"[bold cyan]Visit Developer: {USER_GITHUB}[/bold cyan]")
            questionary.press_any_key_to_continue().ask()
        else:
            target = console.input("\n[bold white]Target URL: [/bold white]").strip()
            if target: run_kraken_engine(target)
            questionary.press_any_key_to_continue().ask()

if __name__ == "__main__":
    main()
