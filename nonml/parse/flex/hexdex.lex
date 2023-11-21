/*
 * hexdex pattern: 0[xX]([0-9a-fA-F]{1-8})
 */

digit       [0-9]
alpha       [a-fA-F]
hextail     ({digit}|{alpha}){1,8}
hex         0[xX]{hextail}

%%
{hex}   printf("found a hex number %s", yytext);
.       printf("");
%%

main()
{
    yylex();
}
