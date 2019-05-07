grammar lfrX;

skeleton: moduledefinition body 'endmodule';

moduledefinition: 'module' ID ('(' ioblock ')')? ';';

body
    :   (statements)+
    ;

ioblock
    :    ID (',' ID)*
    |    explicitIOBlock ( ',' explicitIOBlock)?
    ;

explicitIOBlock
    :   'finput' ID (',' ID)*
    |   'foutput' ID (',' ID)*
    |   'control' ID (',' ID)*
    ;

statements
    :   statement
//    |   (blocks)+ //Uncomment this once we are making the distribute and always blocks
    |   technologydirectives
    ;

statement
    :   ioassignstat  //This needs ot be replaced by any number different kinds of statements that will
    |   assignstat
    |   tempvariablesstat
    ;

tempvariablesstat
    :   fluidstat
    |   reactorstat
    |   nodestat
    ;

nodestat : 'node' ID ;

reactorstat : 'reactor' ID ;

fluidstat : 'fluid' ID ;

assignstat
    :   'assign' variables '=' number  ';'
    |   'assign' variables '=' variables ';'
    |   'assign' variables '=' expression ';'
    ;


//TODO: Look up how the grammar is given for Verilog. This will have be to correct for actually solving the logic things
expression
    :   variables (binary_operator (variables))+
    |   unary_operator (variables)
    ;

variables: ID; //TODO: Add the concatenated variables too

ioassignstat
    :   explicitIOBlock ';'
    ;

technologydirectives:   '#' directive  (('|' | '&') directive)*;

directive
    :   performancedirective
    |   technologymappingdirective
    ;

technologymappingdirective : 'MAP' ('\'' ID+ '\'' | '"' ID+ '\'') operator=binary_operator ;

performancedirective : ID   '='  number unit? ;

unit: ID;


ID
    :   ('a'..'z' | 'A'..'Z'|'_')('a'..'z' | 'A'..'Z'|'0'..'9'|'_')*
    ;

WS : [ \t\r\n]+ -> skip ;


One_line_comment
   : '//' .*? '\r'? '\n' -> channel (HIDDEN)
   ;


Block_comment
   : '/*' .*? '*/' -> channel (HIDDEN)
   ;



// Operators - Taken from Verilog2001
unary_operator
   : '+'
   | '-'
   | '!'
   | '~'
   | '&'
   | '~&'
   | '|'
   | '~|'
   | '^'
   | '~^'
   | '^~'
   ;

binary_operator
   : '+'
   | '-'
   | '*'
   | '/'
   | '%'
   | '=='
   | '!='
   | '==='
   | '!=='
   | '&&'
   | '||'
   | '**'
   | '<'
   | '<='
   | '>'
   | '>='
   | '&'
   | '|'
   | '^'
   | '^~'
   | '~^'
   | '>>'
   | '<<'
   | '>>>'
   | '<<<'
   ;

unary_module_path_operator
   : '!'
   | '~'
   | '&'
   | '~&'
   | '|'
   | '~|'
   | '^'
   | '~^'
   | '^~'
   ;

binary_module_path_operator
   : '=='
   | '!='
   | '&&'
   | '||'
   | '&'
   | '|'
   | '^'
   | '^~'
   | '~^'
   ;



//Numbers - Taken from the Verilog 2001
number
   : Decimal_number
   | Octal_number
   | Binary_number
   | Hex_number
   | Real_number
   ;


Real_number
   : Unsigned_number '.' Unsigned_number | Unsigned_number ('.' Unsigned_number)? [eE] ([+-])? Unsigned_number
   ;


Decimal_number
   : Unsigned_number | (Size)? Decimal_base Unsigned_number | (Size)? Decimal_base X_digit ('_')* | (Size)? Decimal_base Z_digit ('_')*
   ;


Binary_number
   : (Size)? Binary_base Binary_value
   ;


Octal_number
   : (Size)? Octal_base Octal_value
   ;


Hex_number
   : (Size)? Hex_base Hex_value
   ;


fragment Sign
   : [+-]
   ;


fragment Size
   : Non_zero_unsigned_number
   ;


fragment Non_zero_unsigned_number
   : Non_zero_decimal_digit ('_' | Decimal_digit)*
   ;


fragment Unsigned_number
   : Decimal_digit ('_' | Decimal_digit)*
   ;


fragment Binary_value
   : Binary_digit ('_' | Binary_digit)*
   ;


fragment Octal_value
   : Octal_digit ('_' | Octal_digit)*
   ;


fragment Hex_value
   : Hex_digit ('_' | Hex_digit)*
   ;


fragment Decimal_base
   : '\'' [sS]? [dD]
   ;


fragment Binary_base
   : '\'' [sS]? [bB]
   ;


fragment Octal_base
   : '\'' [sS]? [oO]
   ;


fragment Hex_base
   : '\'' [sS]? [hH]
   ;


fragment Non_zero_decimal_digit
   : [1-9]
   ;


fragment Decimal_digit
   : [0-9]
   ;


fragment Binary_digit
   : X_digit | Z_digit | [01]
   ;


fragment Octal_digit
   : X_digit | Z_digit | [0-7]
   ;


fragment Hex_digit
   : X_digit | Z_digit | [0-9a-fA-F]
   ;


fragment X_digit
   : [xX]
   ;


fragment Z_digit
   : [zZ?]
   ;
