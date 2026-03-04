# NanoBASIC

## Grammar definition

```BNF
<line> ::= <number> <statement> '\n' | 'REM' .\*'\n'

<statement> ::= 'PRINT' <expr-list> |
    'IF' <boolean-expr> 'THEN' <statement> |
    'GOTO' <expression> |
    'LET' <var> '=' <expression> |
    'GOSUB' <expression> |
    'RETURN'

<expr-list> ::= (<string> | <expression>) (',' (<string> | <expression>))\*

<expression> ::= <term> (('+'|'-') <term>)\*

<term> ::= <factor> (('_'|'/') <factor>)_

<factor> ::= ('-'|ε) <factor> | <var> | <number> | '('<expression>')'

<var> ::= ('_'|<letter>) ('_'|<letter>)\*

<number> ::= <digit> <digit>\*

<digit> ::= '0' | '1' | ... | '8' | '9'

<letter> ::= 'a'|'b'| ... |'y'|'z'|'A'|'B'| ... |'Y'|'Z'

<relop> ::= '<' ('>'|'='|ε) | '>' ('<'|'='|ε) | '='

<boolean-expr> ::= <expression> <relop> <expression>

<string> ::= '"' .\* '"'

```
