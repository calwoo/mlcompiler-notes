%{
#define YYSTYPE double
#include "calc.tab.h"
#include <stdlib.h>
%}

white           [ \t]+
digit           [0-9]
integer         {digit}+
exponent        [eE][+-]?{integer}
real            {integer}("."{integer})?{exponent}?

%%

{white} { }
{real} {
    yylval = atof(yytext);
    return NUMBER;
}

"+" return PLUS;
"-" return MINUS;
"*" return TIMES;
"/" return DIVIDE;
"^" return POWER;
"(" return LPAREN;
")" return RPAREN;
"\n" return END;
