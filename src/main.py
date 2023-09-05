ver='1.0'
from ply.lex import lex
from ply.yacc import yacc
from prompt_toolkit import prompt
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import faststate

Netknife_Cli = WordCompleter(['telnet', 'ssh', 'ping', 'tcping',
                              'exit'], ignore_case=True)
lexer=lex(module=faststate)
parser=yacc(module=faststate,debug=True)
while True:
    input = prompt('>>>', history=FileHistory('history.txt'), 
                   auto_suggest=AutoSuggestFromHistory(),completer=Netknife_Cli)
    if not input:continue
    if input=='exit':
        print(exit)
        break
    parser.parse(input)

