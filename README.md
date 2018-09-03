# Certi-finder

## Buscador de certificados da UTFPr na linha de comando.

Eu queria pegar todos os meus certificados da utf para checar minha atividades complementares mas eu não sabia o que eu tinha participado então eu e um colega fizemos esse scraper que checa todos eventos de todos os anos (>2013).

Por padrão, o comando apenas mostra no terminal o nome do aluno, o papel que teve no evento e o link do documento. Logo abaixo tem um comando para baixar os documentos também.

## Como usar

    usage: certi-finder [-h] [-v] [-w] [-s SEPARADOR] *Seu nome*

    Baixa os certificados de participação da utfpr.

    positional arguments:
      nome                  Nome a ser pesquisado

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Ativa saída prolixa (fala muito)
      -w, --watch           Inicia o navegador ~Com cabeça~
      -s SEPARADOR, --separador SEPARADOR
                            Define o separador dos campos (default: ,)

Como baixar os certificados
------

```bash
$ python3 -u certi-finder.py "domingos" | grep -o '[^,]*$' | xargs wget -q
```

Se você tiver muitos certificados, baixe em paralelo:

```bash
$ python3 -u certi-finder.py "domingos" | grep -o '[^,]*$' | xargs -n 1 -P 20 wget -q
```

>  Nota que o terminal vai ficar limpo por causa da flag **-q**. 

ou com o *gnu parallel*:

```bash
$ python3 -u certi-finder.py "aline" | grep -o '[^,]*$' | parallel -j 500% wget -q
```

Se quiser acompanhar a o processo, pode também usar:

```bash
$ python3 -u certi-finder.py "joao" | grep -o '[^,]*$' | parallel -j 500% --bar wget -q
```

Dependencias
------------

1. É necessário ter o Firefox intalado (Testado na versão 61.0.1)
2. Selenium, para controlar o firefox 

```bash
$ sudo pip install -U selenium
```

3. Se quiser usar o **parallel**, precisa instalar também.

```bash
$ sudo pacman -S parallel #no arch linux
```

A fazer
-------

1. Parametrizar por qualquer utf, por enquanto só busca a de campo mourão
2. Colocar a possibilidade de usar o chrome

Os dados vem do site http://apl.utfpr.edu.br/extensao/certificados/listaPublica


Para você se divertir
-----

```bash
$ python3 -u certi-finder.py "" | grep -o '[^,]*$' | tee /dev/stderr | parallel -j 500% wget -q
```

> baixa todos os certificados de todo mundo, ótimo para encher o HD
