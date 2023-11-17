        int nlines = 0, nchars = 0;

%%
\n      ++nlines; ++nchars;
.       ++nchars;
%%

main()
{
    yylex();
    printf("lines: %d, chars %d\n", nlines, nchars);
}
