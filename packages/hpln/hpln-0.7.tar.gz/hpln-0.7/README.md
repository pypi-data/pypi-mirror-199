# HPLN

Criação de uma **processador de linguagem natural** em Python.

[+] Versão **0.7**

<br>


![enter image description here](https://raw.githubusercontent.com/henriqueparola/spln-2223/main/TPC4/images/banner.png)

## Modo de uso

```
usage: hpln.py [-h] [--fl] [--pl] [--pag PAG] [--abr ABR] [--lang LANG] texto

Processador de linguagem natural

positional arguments:
  texto        Arquivo de texto de entrada

optional arguments:
  -h, --help   show this help message and exit
  --fl         Retorna uma frase por linha
  --pl         Retorna uma palavra por linha
  --pag PAG    Retorna o conteúdo da página fornecida
  --abr ABR    Ficheiro de abreviações do utilizador
  --lang LANG  Especificação da língua das abreviações
```

## Informações
  * O parâmetro **lang** especifica a linguagem na qual as abreviações estão escritas. As abreviações utilizadas neste cenário fazem parte das abreviações *defaults* utilizadas pelo sistema. Atualmente existem abrevisações para as seguintes línguas:
    * Inglês: *en*
    * Português: *pt* 
  * Com o fornecimento do ficheiro **abr**, as abreviações utilizadas serão as que o utilizador passar através do ficheiro de configuração. Este ficheiro deve possuir uma abreviação **por linha**.  

## Abreviações
  * Inglês:
    * dr
    * prof
    * dec
    * sr
    * srta
    * sra
  * Português:
    TODO


