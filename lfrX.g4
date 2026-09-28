grammar lfrX;

skeleton: module+;

module: moduledefinition body 'endmodule';

moduledefinition: 'module' ID ('(' ioblock ')')? ';';

body: ( statements | distributionBlock)+;

ioblock:
	vectorvar (',' vectorvar)*
	| explicitIOBlock ( ',' explicitIOBlock)*;

vectorvar: ID vector?;

explicitIOBlock:
	'finput' declvar (',' declvar)*
	| 'foutput' declvar (',' declvar)*
	| 'control' declvar (',' declvar)*;

declvar: vector? ID;

distributionBlock:
	'distribute@' '(' sensitivitylist ')' 'begin' distributionBody 'end';

distributionBody: distributeBodyStat+;

distributeBodyStat:
	distributionassignstat
	| caseBlock
	| ifElseBlock;

ifElseBlock: ifBlock elseIfBlock* elseBlock?;

ifBlock: 'if' '(' distributeCondition ')' statementBlock;

elseBlock: 'else' statementBlock;

elseIfBlock:
	'else' 'if' '(' distributeCondition ')' statementBlock;

distributeCondition: distributeOrExpr;

distributeOrExpr: distributeAndExpr ('||' distributeAndExpr)*;

distributeAndExpr: distributeBitOrExpr ('&&' distributeBitOrExpr)*;

distributeBitOrExpr: distributeBitXorExpr ('|' distributeBitXorExpr)*;

distributeBitXorExpr:
	distributeBitAndExpr (('^' | '^~' | '~^') distributeBitAndExpr)*;

distributeBitAndExpr: distributeEqualityExpr ('&' distributeEqualityExpr)*;

distributeEqualityExpr:
	distributePrimary (('==' | '!=') distributePrimary)*;

distributePrimary: '(' distributeCondition ')' | number | variables;

statementBlock:
	'begin' distributionassignstat+ 'end'
	| distributionassignstat;

caseBlock: caseBlockHeader casestat+ defaultCaseStat? 'endcase';

caseBlockHeader: 'case' '(' lhs ')';

casestat: distvalue ':' statementBlock;

defaultCaseStat: 'default' ':' statementBlock;

distvalue: number;

distributionassignstat:
	lhs '<=' (number | variables | expression) ';'; //TODO: Have a switch->case block

sensitivitylist: signal (',' signal)*;

signal: ID vector?;

statements:
	statement ';'
	//    |   (blocks)+ //Uncomment this once we are making the distribute and always blocks
	| technologydirectives;

statement:
	ioassignstat //This needs ot be replaced by any number different kinds of statements that will
	| assignstat
	| tempvariablesstat
	| literalassignstat
	| moduleinstantiationstat;

// Verilog-style optional parameters before the instance name:
//   DIYcomponent #(length=10000, width=8000, height=2000) box(
//       .up(a), .right(None), .down(b), .left(None));
// Also accepts .length(10000) form. None = unconnected side (DIYcomponent).
moduleinstantiationstat:
	moduletype ('#' '(' moduleparamlist ')')? instancename '(' instanceioblock ')';

moduleparamlist: moduleparam (',' moduleparam)*;

moduleparam: ID '=' number | '.' ID '(' number ')';

instanceioblock: orderedioblock | unorderedioblock;

orderedioblock: vectorvar (',' vectorvar)*;

unorderedioblock:
	explicitinstanceiomapping (',' explicitinstanceiomapping)*;

explicitinstanceiomapping: '.' ID '(' (variables | 'None') ')';

instancename: ID;

moduletype: ID;

tempvariablesstat:
	fluiddeclstat
	| storagestat
	| numvarstat
	| signalvarstat
	| pumpvarstat;

signalvarstat: 'signal' declvar (',' declvar)*;

fluiddeclstat: 'flow' declvar (',' declvar)*;

storagestat: 'storage' declvar (',' declvar)*;

pumpvarstat: 'pump' declvar (',' declvar)*;

numvarstat: 'number' literalassignstat (',' literalassignstat)*;

assignstat: 'assign' lhs '=' ( bracketexpression | expression);

literalassignstat: ID '=' (bracketexpression | expression);

//TODO: Look up how the grammar is given for Verilog. This will have be to correct for actually solving the logic things
bracketexpression: unary_operator? '(' expression ')';

expression: (bracketexpression | expressionterm) (
		binary_operator (bracketexpression | expressionterm)
	)*;

expressionterm: unary_operator? variables | number;

logiccondition_operand: (bracketexpression | expressionterm) (
		binary_operator (bracketexpression | expressionterm)
	)*;

logiccondition:
	logiccondition_operand binary_module_path_operator logic_value;

logic_value: number;

vector:
	'[' start = Decimal_number (':' end = Decimal_number)? ']';

variables: vectorvar | concatenation;

concatenation: '{' vectorvar (',' vectorvar)* '}' vector?;

lhs: variables;

ioassignstat: explicitIOBlock;

technologydirectives:
	performancedirective
	| technologymappingdirective
	| materialmappingdirective
	| terminaldirective;

technologymappingdirective:
	'#MAP' '"' ID+ '"' '"' (
		mappingoperator
		| assignmode = ('assign' | 'storage' | 'pump')
	) '"';

materialmappingdirective: '#MATERIAL' ID materialtype = ID;

mappingoperator: binary_operator | unary_operator;

// Quoted target is an expression operator ("+", "~", …), CHANNEL, CTRLCHANNEL,
// or a #MAP mode keyword (assign / storage / pump). CHANNEL stamps FLOW
// connections of the next assign; CTRLCHANNEL stamps CONTROL.
constrainttarget: mappingoperator | ID | 'assign' | 'storage' | 'pump';

performancedirective:
	'#CONSTRAIN' '"' constrainttarget '"' constraint (
		('AND' | 'OR') constraint
	)*;

// Bind fluid nets to primitive terminals on the next mapped operator.
// Separate from #CONSTRAIN (geometry/performance). Same flush scope as #MAP:
// attaches to the following assign's operator node, then clears.
//
// Role form (NOZZLE DROPLET GENERATOR): oil_left / oil_right / aqueous / droplets
// Role form (DIYCOMPONENT): up / right / down / left
// Numeric form: #TERMINAL "~" 3 = oil_1
//
// Example (MAP-only droplet generator, no module instantiate):
//   #MAP "NOZZLE DROPLET GENERATOR" "~"
//   #TERMINAL "~" oil_left = oil_1 AND oil_right = oil_r
//   #TERMINAL "~" aqueous = aq AND droplets = drops
//   assign drops = ~aq;
terminaldirective:
	'#TERMINAL' '"' constrainttarget '"' terminalbinding (
		('AND' | 'OR') terminalbinding
	)*;

terminalbinding: role = ID '=' net = ID | term = number '=' net = ID;

constraint:
	ID operator = '=' number unit?
	| ID operator = '>' number unit?
	| ID operator = '<' number unit?
	| ID operator = '>=' number unit?
	| ID operator = '<=' number unit?;

unit: ID;

ID: ('a' ..'z' | 'A' ..'Z' | '_') (
		'a' ..'z'
		| 'A' ..'Z'
		| '0' ..'9'
		| '_'
	)*;

WS: [ \t\r\n]+ -> skip;

// Verilog-style comments (LFR surface syntax is Verilog-like)
One_line_comment: '//' .*? '\r'? '\n' -> channel (HIDDEN);

Block_comment: '/*' .*? '*/' -> channel (HIDDEN);

Import_line: '`' .*? '\r'? '\n' -> channel (HIDDEN);

// Operators - Taken from Verilog2001
unary_operator:
	'+'
	| '-'
	| '!'
	| '~'
	| '&'
	| '~&'
	| '|'
	| '~|'
	| '^'
	| '~^'
	| '^~';

binary_operator:
	'+'
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
	| '<<<';

unary_module_path_operator:
	'!'
	| '~'
	| '&'
	| '~&'
	| '|'
	| '~|'
	| '^'
	| '~^'
	| '^~';

binary_module_path_operator:
	'=='
	| '!='
	| '&&'
	| '||'
	| '&'
	| '|'
	| '^'
	| '^~'
	| '~^';

//Numbers - Taken from the Verilog 2001
number:
	Decimal_number
	| Octal_number
	| Binary_number
	| Hex_number
	| Real_number;

Real_number:
	Unsigned_number '.' Unsigned_number
	| Unsigned_number ('.' Unsigned_number)? [eE] ([+-])? Unsigned_number;

Decimal_number:
	Unsigned_number
	| (Size)? Decimal_base Unsigned_number
	| (Size)? Decimal_base X_digit ('_')*
	| (Size)? Decimal_base Z_digit ('_')*;

Binary_number: (Size)? Binary_base Binary_value;

Octal_number: (Size)? Octal_base Octal_value;

Hex_number: (Size)? Hex_base Hex_value;

fragment Sign: [+-];

fragment Size: Non_zero_unsigned_number;

fragment Non_zero_unsigned_number:
	Non_zero_decimal_digit ('_' | Decimal_digit)*;

fragment Unsigned_number: Decimal_digit ('_' | Decimal_digit)*;

fragment Binary_value: Binary_digit ('_' | Binary_digit)*;

fragment Octal_value: Octal_digit ('_' | Octal_digit)*;

fragment Hex_value: Hex_digit ('_' | Hex_digit)*;

fragment Decimal_base: '\'' [sS]? [dD];

fragment Binary_base: '\'' [sS]? [bB];

fragment Octal_base: '\'' [sS]? [oO];

fragment Hex_base: '\'' [sS]? [hH];

fragment Non_zero_decimal_digit: [1-9];

fragment Decimal_digit: [0-9];

fragment Binary_digit: X_digit | Z_digit | [01];

fragment Octal_digit: X_digit | Z_digit | [0-7];

fragment Hex_digit: X_digit | Z_digit | [0-9a-fA-F];

fragment X_digit: [xX];

fragment Z_digit: [zZ?];
