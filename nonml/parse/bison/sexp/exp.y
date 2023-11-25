%{
#include "exp.h"
#include <vector>
%}

%token NUMBER
%token STRING
%token SYMBOL

%start Exp
%%

Exp:
    Atom
    | List
    ;

Atom:
    NUMBER { $$ = Exp(std::stoi($1)); }
    | STRING { $$ = Exp($1); }
    | SYMBOL { $$ = Exp($1); }
    ;

List:
    '(' ListEntries ')' { $$ = $2; }
    ;

ListEntries:
    %empty { $$ = Exp(std::vector<Exp>{}); }
    | ListEntries Exp { $1.list.push_back($2); $$ = $1; }
    ;
