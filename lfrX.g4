grammar lfrX;

skeleton: module+ ;

module: moduledefinition body 'endmodule';

moduledefinition: 'module' ID ('(' ioblock ')')? ';';

body
   :   ( statements | distributionBlock ) +
   ;

ioblock
   :    vectorvar (',' vectorvar)*
   |    explicitIOBlock ( ',' explicitIOBlock)*
   ;

vectorvar : ID vector? ;

explicitIOBlock
   :   'finput' declvar (','declvar)*
   |   'foutput' declvar (',' declvar)*
   |   'control' declvar (','declvar)*
   ;

declvar : vector? ID ;

distributionBlock
   :  'distribute@' '(' sensitivitylist ')' 'begin' distributionBody 'end'
   ;

distributionBody
//TODO: modify the distribute block to be more precise
   :  (distributionassignstat)*
   |  caseBlock
   |  ifElseBlock
   ;

ifElseBlock: 'if' '(' sensitivitylist ')' statementBlock elseIfBlock* elseBlock?;

elseBlock: 'else' statementBlock;

elseIfBlock: 'else' 'if' '(' sensitivitylist ')' statementBlock;

statementBlock
   :   'begin' distributionassignstat+ 'end'
   |   distributionassignstat
   ;

caseBlock
   :  'case' '(' lhs ')' casestat+ 'endcase'
   ;

casestat
   :  distCondition ':' statementBlock
   ;

distCondition: number;

distributionassignstat
   :  lhs '<=' (number | variables | expression) ';'
   //TODO: Have a switch->case block
   ;

sensitivitylist : signal (',' signal)* ;

signal : ID vector? ;

statements
   :   statement ';'
//    |   (blocks)+ //Uncomment this once we are making the distribute and always blocks
   |   technologydirectives
   ;

statement
   :   ioassignstat  //This needs ot be replaced by any number different kinds of statements that will
   |   assignstat
   |   tempvariablesstat
   |   literalassignstat
   |   moduleinstantiationstat
   ;

moduleinstantiationstat: moduletype instancenames '(' instanceioblock ')';

instanceioblock
   :   orderedioblock
   |   unorderedioblock
   ;

orderedioblock:   vectorvar (',' vectorvar)* ;

unorderedioblock: explicitinstanceiomapping ( ',' explicitinstanceiomapping)*;

explicitinstanceiomapping : '.'vectorvar '('variables')' ;

instancenames: ID;

moduletype: ID;

tempvariablesstat
   :   fluiddeclstat
   |   storagestat
   |   numvarstat
   |   signalvarstat
   ;

signalvarstat: 'signal' declvar (',' declvar)* ;

fluiddeclstat : 'flow' declvar (',' declvar)* ;

storagestat : 'storage' declvar (',' declvar)* ;

numvarstat : 'number'  literalassignstat (',' literalassignstat)*  ;

assignstat
   :   'assign' lhs '='  ( bracketexpression | expression )
   ;

literalassignstat
    :   ID '=' (bracketexpression | expression)
    ;

//TODO: Look up how the grammar is given for Verilog. This will have be to correct for actually solving the logic things
bracketexpression
    :   unary_operator? '(' expression ')'
    ;

expression
   :   (bracketexpression | expressionterm ) (binary_operator (bracketexpression | expressionterm ))*
   ;

expressionterm
   :    unary_operator? variables
   |    number
   ;

logiccondition
    :   (bracketexpression | expressionterm ) (binary_operator (bracketexpression | expressionterm ))*
    ;

vector
   :   '[' start=Decimal_number (':' end=Decimal_number)?  ']'
   ;

variables
   : vectorvar
   | concatenation
   ;

concatenation : '{' vectorvar (',' vectorvar)* '}' vector? ;

lhs : variables;

ioassignstat
   :   explicitIOBlock
   ;

technologydirectives
   :    directive  (('|' | '&') directive)*
   ;

directive
   :    performancedirective
   |    technologymappingdirective
   |    materialmappingdirective
   ;

technologymappingdirective
    :   '#MAP'  '\''ID+ '\'' '\''(mappingoperator | assignmode=('assign' | 'storage')) '\''
    ;

materialmappingdirective
    :   '#MATERIAL' ID  materialtype=ID
    ;

mappingoperator
    :   binary_operator
    |   unary_operator
    ;

performancedirective 
   :  '#CONSTRAIN' constraint
   ;

constraint
   : '\'' (binary_operator|unary_operator) '\'' ID operator='=' number unit?
   | '\'' (binary_operator|unary_operator) '\'' ID operator='>' number unit?
   | '\'' (binary_operator|unary_operator) '\'' ID operator='<' number unit?
   | '\'' (binary_operator|unary_operator) '\'' ID operator='>=' number unit?
   | '\'' (binary_operator|unary_operator) '\'' ID operator='<=' number unit?
   ;

unit: ID;

ID  :   ('a'..'z' | 'A'..'Z'|'_')('a'..'z' | 'A'..'Z'|'0'..'9'|'_')* ;

WS : [ \t\r\n]+ -> skip ;


One_line_comment
   : '//' .*? '\r'? '\n' -> channel (HIDDEN)
   ;


Block_comment
   : '/*' .*? '*/' -> channel (HIDDEN)
   ;

Import_line
   : '`' .*? '\r'? '\n' -> channel (HIDDEN)
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
