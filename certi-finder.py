#!/bin/python3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import getopt
import sys
import argparse

#Lida com argumentos
parser = argparse.ArgumentParser(
    description="Baixa os certificados de participação da utfpr.",
    epilog="""Scrape do site http://apl.utfpr.edu.br/extensao/certificados/listaPublica"""
)
parser.add_argument("nome", help="Nome a ser pesquisado")
parser.add_argument('-v', "--verbose",help="Ativa saída prolixa (fala muito)", action="store_true")
parser.add_argument('-w', "--watch", help="Inicia o navegador ~Com cabeça~", action="store_true")
parser.add_argument('-s', "--separador", help="Define o separador dos campos (default: ,)")
parser.set_defaults(separador=',')

results = parser.parse_args()
nome = results.nome
separador = results.separador
verbose = results.verbose
headless = not results.watch
# fim lida cm argumentos

def get_element_by_name(name):
    """Eu acho essa linha muito grande entao fiz uma funçao"""
    return wait.until(expected.visibility_of_element_located((By.NAME,name)))
    

def get_element_by_id(id):
    """mesma que get_element_by_name"""
    return wait.until(expected.visibility_of_element_located((By.ID,id)))

def print_verbose(*args,**kwargs):
    if verbose:
        print(*args,**kwargs)

#Inicio da busca
options = Options()
options.add_argument('-headless')
print_verbose("Iniciando Navegador")
driver = webdriver.Firefox(firefox_options=options) if headless else webdriver.Firefox()

print_verbose("Acessando a página")
driver.get("http://apl.utfpr.edu.br/extensao/certificados/listaPublica")
wait = WebDriverWait(driver, timeout=10)

print_verbose("Selecionando Campus")
comboCampus = webdriver.support.ui.Select( driver.find_element_by_name("txtCampus") )
comboCampus.select_by_value("3")

comboAno = webdriver.support.ui.Select( driver.find_element_by_name("txtAno") )
anos = [ ano.text for ano in comboAno.options if ano.text != "Todos" ]

for ano in anos:
    print_verbose(f"Buscando eventos de {ano}")
    elementoAno = get_element_by_name("txtAno")
    comboAno = webdriver.support.ui.Select( elementoAno )
    comboAno.select_by_visible_text(ano)

    elementoEvento = get_element_by_name("txtEvento")
    comboEvento = webdriver.support.ui.Select( elementoEvento )
    eventos = [ evento.text for evento in comboEvento.options if evento.text != "Selecione..."]

    for evento in eventos:
        print_verbose(f"Bucando participacoes no evento \"{evento}\"")
        elementoEvento = get_element_by_name("txtEvento")   #precisa de outro find porque
                                                            #o selenium perde a referencia quando
                                                            #a pagina muda
        comboEvento = webdriver.support.ui.Select( elementoEvento )
        comboEvento.select_by_visible_text(evento)

        #pesquisa nome
        campoPesquisa = get_element_by_id("txtPesquisa")
        campoPesquisa.clear()
        campoPesquisa.send_keys( nome )
        campoPesquisa.submit()

        #processa a tabela
        sleep(0.8)
        elementoTabela = get_element_by_id("data_table")
        for row in elementoTabela.find_elements_by_tag_name("tr")[1:]:
            cells = row.find_elements_by_tag_name("td")
            if len(cells) < 3:
                continue
            for cell in cells:
                try:
                    print(cell.find_element_by_tag_name("a").get_attribute("href").replace("certificados/validar","emitir"), end="")
                except:
                    print(cell.text, end=separador)
            print("")

        #volta a pagina inicial
        get_element_by_id("botao_cancelar").click()
print_verbose("Fim da busca")
driver.close()