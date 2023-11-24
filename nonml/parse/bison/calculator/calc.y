%{
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define YYSTYPE double
%}

// tokens
%token NUMBER
%token PLUS MINUS TIMES DIVIDE POWER
%token LPAREN RPAREN
%token END

%left PLUS MINUS
%left TIMES DIVIDE
%left NEG
%right POWER

%start Input
%%
// rules

Input:
    | Input Line
    ;

Line:
    END
    | Expression END { printf("result: %f\n", $1); }
    ;

Expression:
    NUMBER { $$=$1; }
    | Expression PLUS Expression { $$=$1+$3; }
    | Expression MINUS Expression { $$=$1-$3; }
    | Expression TIMES Expression { $$=$1*$3; }
    | Expression DIVIDE Expression { $$=$1/$3; }
    | MINUS Expression %prec NEG { $$=-$2; }
    | Expression POWER Expression { $$=pow($1,$3); }
    | LPAREN Expression RPAREN { $$=$2; }
    ;

%%

// user-defined functions
int yyerror(char *s) {
    printf("%s\n", s);
}

int main() {
    if (yyparse())
        printf("success\n");
    else
        printf("error found\n");
}
