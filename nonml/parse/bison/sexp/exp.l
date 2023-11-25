whitespace   [ \t\n\r]+
digit        [0-9]
alphanum     [a-zA-Z0-9_]

%%

{whitespace}             ;

\/\/.*                   ;
\/\*.*?\*\/              ;

\"[^\"]*\"               { printf("STRING\n"); }
{digit}+                 { printf("NUMBER\n"); }
[a-zA-Z0-9_\-+*=!<>/]+   { printf("SYMBOL\n"); }
