modules = ['BeautifulSoup','urllib','subprocess','webbrowser','requests','platform','zipfile','time','json','re','os']
from selenium.webdriver.support import expected_conditions as EC                                    # Módulo utilizado em conjunto com o WebDriverWait para aplicar condições nele
from urllib.request import urlopen, Request, urlretrieve                                            # Módulo utilizado para entrar nas páginas https da web usando um navegador headless para isso
from selenium.webdriver.support.ui import WebDriverWait                                             # Módulo utilizado para aplicar pausas no chrome driver
from selenium.webdriver.common.by import By                                                         # Módulo utilizado para definir formas de encontrar tags html no selenium por meio de métodos
from selenium import webdriver                                                                      # Módulo utilizado de forma similar ao urllib.request para abrir e navegar por páginas da web e lidar com páginas que precisam carregar códigos JS para funcionar
from bs4 import BeautifulSoup                                                                       # Módulo utilizado para fazer o scrapping documentos .html
import subprocess                                                                                   # Módulo utilizado para lançar comandos no terminal (Similar ao módulo OS porém com possibilidade de suprimir o print)
import webbrowser                                                                                   # Módulo utilizado para abrir uma página da internet normalmente
import requests                                                                                     # Módulo utilizado de forma similar ao urllib.request para evitar alguns erros
import platform
import zipfile
import time                                                                                         # Módulo utilizado para mexer com funções relacionadas a tempo
import json                                                                                         # Módulo utilizado para save as informações que coletamos em um arquivo no formato tipo .JSON 
import re                                                                                           # Módulo utilizado para refinar informações (útil para evitar e corrigir erros com o BeautifulSoup)
import os                                                                                           # Módulo utilizado para interagir com o sistema operacional


targetUrl = "https://www.google.com/"                                                               # Link utilizado para o scrapping
headers = {"User-Agent": "Mozilla/5.0"}                                                             # User-Agent é um header no navegador contém uma string de identificação com informações do navegador que está sendo utilizado


class Scrapy:
    # Função criada para substituir o time.sleep
    def delay(interval: int = 1) -> int:
        time.sleep(interval)
        return interval


    # Função criada para configurar um webdriver selenium
    def setup_driver(options: list[str] = ["--start-maximized","--detach"]) -> webdriver:
        driver_options = webdriver.ChromeOptions()                                                  # Chamado da função para adicionar opções ao webdriver
        [driver_options.add_argument(i) for i in options]                                           # Loop para adicionar as opções no webdriver
        driver = webdriver.Chrome(options=driver_options)                                           # Gera o webdriver já configurado
        return driver                                                                               # Retorna o webdriver para que possa ser utilizado

    
    # Função criada para fechar um webdriver verdadeiramente
    def close_driver(driver: webdriver, process: str = "chromedriver.exe", delay: int = 0) -> None:
        time.sleep(delay)                                                                           # Delay para fechar o chromedriver
        driver.close()                                                                              # Fecha o driver
        subprocess.check_output(f"taskkill /F /IM {process}", shell=True)                           # Finaliza o processo especificado
        return None                                                                                 # Retorno da função


    # Função criada para clicar em elementos html dentro de uma página aberta em um webdriver por meio do xpath
    def selenium_click_xpath(driver: webdriver, tag: str, attr: str, selector: str, interval: int = 0) -> None:
        target_element = driver.find_element(By.XPATH,f'//{tag}[{attr}="{selector}"]')              # Busca pelo elemento com as especificações
        driver.execute_script("arguments[0].click();", target_element)                              # Comando para clicar no elemento (Evita erros de sobreposição de tags)
        Scrapy.delay(interval)                                                                      # Intervalo de tempo
        return target_element                                                                       # Retorna o elemento


    # Função criada para clicar em elementos html dentro de uma página aberta em um webdriver por meio do xpath
    def selenium_click_class(driver: webdriver, tag: str, selector: str, interval: int = 0) -> None:
        target_element = driver.find_element(By.CLASS_NAME,f'{tag}.{selector}')                     # Busca pelo elemento com as especificações
        target_element.click()                                                                      # Comando para clicar no elemento (Evita erros de sobreposição de tags)
        Scrapy.delay(interval)                                                                      # Intervalo de tempo
        return target_element   


    # Função criada para coletar o código html de uma página em um webdriver
    def selenium_collect_html(driver: webdriver, url: str = targetUrl,interval: int = 0) -> BeautifulSoup:
        driver.get(url)                                                                             # Abre o link no webdriver
        Scrapy.delay(interval=interval)
        html = BeautifulSoup(driver.page_source,"html.parser")                                      # Converte a leitura do link em um BeautifulSoup
        return html                                                                                 # Retorna o código html gerado
    

    # Função criada para o selenium esperar por um elemento ficar disponível na página
    def selenium_wait_element(driver: webdriver, timer: int, method: By, selector: str, condition: EC) -> None:
        waiter = WebDriverWait(driver, timer)                                                       # Função para ativar o evento de espera
        element = waiter.until(condition((method, selector)))                                       # Execução do evento de espera até que as condições sejam cumpridas
        return element                                                                              # Retorno do elemento na função


    # Função para colectar o código html da página em forma de objeto BeautifulSoup (Função geral)
    def collect_html(url: str = targetUrl, headers: dict = headers, isFile: bool = True) -> BeautifulSoup:
        if (".html" in url and isFile):                                                             # Condicional para verificar se a url termina com .html (é um arquivo)
            response = open(url,errors="ignore").read()                                             # Abre o arquivo .html
        else:                                                                                       # Condicional contrária
            response = urlopen(Request(url = url,headers = headers))                                # Abre um link por meio de request
        html = BeautifulSoup(response,"html.parser")                                                # Mostra o código HTML na página traduzido para um objeto que pode ser quebrado em várias partes
        return html                                                                                 # Retorna o código html da função


    # Função criada para checar as permissões do usuário ou bot na página por meio do arquivo robots.txt
    def view_rules(url: str = targetUrl, headers: dict = headers) -> BeautifulSoup:
        html = Scrapy.collect_html(url + "robots.txt", headers)                                     # Chama nossa função geral criada para coletar o html da página
        return html                                                                                 # Retorna o código html


    # Função criada para converter string em BeautifulSoup
    def str_to_html(str_html: str) -> BeautifulSoup:
        html = BeautifulSoup(str_html,"html.parser")                                                  # Converte a string em questão em um BeautifulSoup
        return html                                                                                   # Retorna o BeautifulSoup gerado pela função


    # Função criada para corrigir erros de codificação (Bom para substituir items em unicode, ascii ou caracteres especiais no geral)
    def html_to_str(bs: BeautifulSoup, encoding: str = "utf-8", replacers: dict = {'\u2620':"?"}) -> str:
        bs = str(bs).encode(encoding)                                                               # Converte o BeautifulSoup em uma string codificada na codificação (enconding) especificada
        str_html = rf"{bs}"[2:-1]                                                                   # Filtro que retira o b''
        [str_html.replace(i,replacers[i]) for i in replacers]
        return str_html                                                                             # Retorna o html ainda codificado


    # Função criada para pular erros de codificação 
    def fixed_html(bs: BeautifulSoup) -> BeautifulSoup:
        html = Scrapy.html_to_str(bs)
        html = Scrapy.str_to_html(html)
        return html

    
    # Função criada para coletar todos os HREFs da página especificada
    def collect_hrefs(url: str = targetUrl, headers: dict = headers) -> list:
        html = Scrapy.collect_html(url, headers)                                                    # Função geral de conexão para coletar o código HTML
        hrefs = [i.attrs["href"] for i in html.find_all("a")]                                       # procura todos as tags a do código html e salva o HREF dela na lista
        return hrefs                                                                                # Retorna a lista de hrefs coletados


    # baixa uma imagem
    def download_img(nome,url,path: str = os.getcwd()) -> str:
        with open(f'{path}\\{nome}','wb') as f:                                                     # Cria o arquivo da img com o name da img e o tipo de arquivo
            img = requests.get(url)                                                                 # Faz um request para abrir a página contendo a img (src)
            f.write(img.content)                                                                    # Faz o download da img
        return path + nome                                                                          # Retorna a lista de imgs

        
    # Função criada para coletar imgs da página especificada (Utilizando módulo requests para evitar alguns erros)
    def collect_imgs(url: str = targetUrl, headers: dict = headers, save: bool = True, path: str = os.getcwd(), tipo: str = ".jpg") -> list:
        html = Scrapy.collect_html(url,headers)                                                     # Chama nossa função geral criada para coletar o html da página
        imgs = {}                                                                                   # Dicionário criado para armazenar as informações das imgs (src e alt)
        [imgs.update({i.attrs["alt"]:i.attrs["src"]}) for i in html.find_all("img")]                # Busca por todas as tags 'img' no código html e coleta sua fonte(src) e seu name(alt)
        if(save):                                                                                   # If para escolher save as imgs
            for i in imgs:                                                                          # Loop para caminhar por todas as imgs no dicionário imgs
                Scrapy.download_img(f'{i}{tipo}',imgs[i],path)                                      # Baixa a imagem
        return imgs                                                                                 # Retorna a lista de imgs


    # Função criada para save data em arquivos .json
    def save_json(data: dict, name: str, save: bool = True) -> dict:
        name += ".json" if(".json" not in name) else name                                           # Condicional criada para adicionar o .json automaticamente no paramêtro name caso ele não esteja presente
        if(save):                                                                                   # Condicional para save o arquivo
            with open(name, 'w') as json_file:                                                      # Abre o arquivo como um arquivo com terminação .JSON
                json.dump(data, json_file)                                                          # Salva o dicionario em formato de json no arquivo
                return json.load(name)                                                              # Retorna a leitura do arquivo .json em forma de dicionário
        else:                                                                                       # Condicional contrária
            return json.dump(data)                                                                  # Retorna apenas o objeto em formato JSON


    # Funcção criada para coletar todas tags dentro de um código html (Usado para coletar texto também)
    def collect_tags(bs: BeautifulSoup, tag: str, css_attr: str, css_class: str,  text: bool = False) -> list:
        tags = bs.find_all(tag,{css_attr:css_class})                                                # Procura todas as tags html presentes no código
        tags = [{"tag":i,"text":i.text} if(text) else {"tag":i} for i in tags]                      # Lista contendo pequenos dicionários que dividem tag e texto ou só a tag caso text for falso
        return tags                                                                                 # Retorna a lista criada na função


    # Função criada para coletar as tags e sua contagem em um tag html
    def view_subtags(bs: BeautifulSoup, tag_pattern: str = "<.*? ") -> list:
        match_dict = {}                                                                             # Dict criado para armazenar as tags e suas contagens
        matchs = [i[1:-1] for i in re.findall(tag_pattern,str(bs),re.IGNORECASE)]                   # Processo de refinamento de texto para identificar qualquer texto que começe com < e termine em um espaço vazio
        [match_dict.update({i:matchs.count(i)}) for i in matchs]                                    # Adição das tags + as vezes que aparecem no dict match_dict
        return match_dict                                                                           # Retorno da lista da função


    # Função criada para extrair todo o texto do código html em questão
    def get_text(bs: BeautifulSoup, pattern: str = "<.*?>.*?<.*?>", replacer: str = "", identify: str = "<.*?>", base: str = "") -> str:
        matches = re.findall(pattern,str(bs),re.IGNORECASE)                                         # Listas de matches encontradas na string
        text = base.join([re.sub(identify,replacer,i) for i in matches])                            # Procura pelo padrão na tag html e substui os seus <> deixando apenas o texto
        return text                                                                                 # Retorna o texto da função

    
    # Função criada para buscar por padrões em elementos html
    def get_element_re(bs: BeautifulSoup, pattern: str = "<.*?>.*?<.*?>") -> list[str]:
        matchs = re.findall(pattern,str(bs),re.IGNORECASE)                                          # Coleta a lista de matches na string em questão
        return matchs                                                                               # Retorno da lista gerada pela função

    
    # Função criada para abrir o navegador
    def normal_open_url(url: str) -> str:
        webbrowser.open(url)                                                                        # Abre o navegador
        return url                                                                                  # Retorno da função


    # Função criada para fazer o download de uma página web
    def selenium_download(driver: webdriver, name: str, path: str = os.getcwd()) -> str:
        with open(path + f"\\{name}","w") as f:                                                     # Cria um arquivo 
            f.write(driver.page_source)                                                             # Escreve o page_source da página no documento
        return path + f"\\{name}"                                                                   # Retorna o path do arquivo


    # Função criada para realizar o download automático do chromedriver
    def download_chromedriver(destiny: str, disk: str = "C:\\") -> str:
        # Tenta decodificar a string "destiny" com "UTF-8" caso tenha caracteres especiais ou esteja codificada
        try:
            destiny = destiny.decode("utf-8")
        except:
            pass

        # Identifica sistema operacional
        os_name = platform.system()
        if(os_name == "Windows"):
            chromeFile = "chromedriver_win32.zip"
            bar = "\\"
            # Coleta do path do chrome.exe
            for root, dirs, files in os.walk(disk):                                                                     # Olha os arquivos e pastas que estão no disco "disk"
                if 'chrome.exe' in files:                                                                               # Verifica se o chrome.exe está entre eles
                    chromePath = os.path.join(root, 'chrome.exe').replace(bar,bar*2)                                    # Converte as barras individuais em barras duplas para o python poder ler                      
                    break                                                                                               # Encerra a procura
            
            # Coleta de versão
            chromeVersion = os.popen(f"wmic datafile where name='{chromePath}' get Version /value")                     # Busca pela versão atual do chrome.exe no terminal por meio do path dele no windows
            chromeVersion = chromeVersion.read().replace("Version=","").replace("\n","").replace(" ","")                # Lê o resultado do comando anterior e retira os espaços vazios e outras informações desnecessárias
        
        elif(os_name == "Linux"):
            chromeFile = "chromedriver_linux64.zip"
            bar = "/"
            chromeVersion = os.popen('google-chrome --version')                                                         # Retorna a versão do Google Chrome
            chromeVersion = chromeVersion.read().replace("Google Chrome ","").replace("\n","").replace(" ","")          # Formata o texto retornado

        # Etapa de download
        downloadLink = f"https://chromedriver.storage.googleapis.com/{chromeVersion}/{chromeFile}"                      # Abre o link de download do chromedriver
        downloadLink = requests.get(downloadLink)                                                                       # Abre o link de download do chromedriver

        # Etapa de download e extração
        open(f"{destiny}{bar}chromedriver.zip",'wb').write(downloadLink.content)                                        # Baixa o conteúdo da página de download no local "destiny"
        with zipfile.ZipFile(f"{destiny}{bar}chromedriver.zip", 'r') as zip_ref:                                        # Abre o arquivo com terminação .zip em modo de leitura
            zip_ref.extractall(destiny)                                                                                 # Extrai o conteúdo do arquivo para o local "destiny"
        
        # Retorno do local do chromedriver.exe
        return f"{destiny}{bar}chromedriver.exe"

if(__name__ == "__main__"):
    Scrapy.download_chromedriver(os.getcwd())
