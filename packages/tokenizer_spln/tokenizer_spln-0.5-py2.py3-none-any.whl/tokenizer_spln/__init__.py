#!/usr/bin/env python3
"""Módulo para tokanizar livros"""
__version__ = "0.5"

import sys
import re
import argparse

def main():

    #Process Arguments

    parser = argparse.ArgumentParser(
        prog='tok',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'''
        ========================================================================
        |               **Tokenizer SPLN version {__version__}**                         |
        ========================================================================
                      Module to tokenize books made in SPLN                '''
    )
    parser.add_argument('input',metavar='filename',type=str,nargs='?',help='input file', default=None)
    parser.add_argument('-o','--output',type=str,nargs=1,help='output file', default=None)
    #parser.add_argument('-l','--language',help='define the language (english by default)',type=str,nargs=1,default='en')
    parser.add_argument('-p','--poem',help="saves peoms delimited inside <poem></poem> in text",action='store_true')
    parser.add_argument('--version','-v', action='version', version="%(prog)s "+__version__)
    parser.add_argument('-e','--encoding',help="encoding of files", type=str,nargs=1,default='utf8')
    args = parser.parse_args()

    text = ""  
    if(not args.input):
        for line in sys.stdin:
            text+=line
    else:   
        file = open(args.input,'r',encoding=args.encoding)
        text = file.read()
        file.close()



    # 0. Tratar poemas

    list_poemas = []

    def save_poems(poema):
        """Saves a poem in a data structure"""
        list_poemas.append(poema[1])
        return f">>{len(list_poemas)}<<"

    if args.poem:
        regex_poema = r'<poem>(.*?)</poem>'
        text = re.sub(regex_poema,save_poems,text,flags=re.S)

    # 1. Quebra de pagina

    regex_nl = r'([a-z0-9,;-])\n\n([a-z0-9,;-])'
    text = re.sub(regex_nl,r'\1\2',text)

    # 2. Marcar capitulos

    regex_cap = r'.*(CAPÍTULO +(\w+|\d+)).*'
    text = re.sub(regex_cap,r'\n# \1',text)

    # 3. Separar paragrafos de linhas pequenas

    regex_par = r'([.!?;])\n(([^.!?;]|[\u00C0-\u017F]))'
    text = re.sub(regex_par,r'\1\n/PAR/ \2',text)

    # 4. Juntar linhas da mesma frase

    regex_line = r'([^.!?])\n+([^.!?])'
    text = re.sub(regex_line,r'\1 \2',text)

    # 5. Separar pontuação das palavras.

    regex_pont = r'([.!,?;:' + r'\"\-\”\–\`()\[\]])?(\w+)([.!,?;:' + r'\"\-\”\–\`()\[\]])'
    text = re.sub(regex_pont,r'\1 \2 \3',text)

    # Save to arquive
    if(not args.output):
        print(text)
        if(args.poem):
            print('=====//POEMS//=====')
            for poema in list_poemas:
                print(poema)
                print('=====//=====')

    else:
        file = open(args.output,'w',encoding=args.encoding)
        file.write(text)
        file.close()
        if(args.poem):
            file.write('=====//POEMS//=====')
            for poema in list_poemas:
                file.write(poema)
                file.write('=====//=====')