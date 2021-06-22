grammar reggie;

graph: '{' graphstatement (',' graphstatement)* '}';

graphstatement:
	basestatement
	| ('(' basestatement ')' statementmodifier);

statementmodifier: intmodifier | plusmodifier | starmodifier;

basestatement: subgraph | vertex2vertex | vertex;

subgraph: (ID ':') '{' vertex2vertex (',' vertex2vertex)* '}';

vertex:
	structuralid (':' labelfilter)? coloringfilter? structuralvertexpattern*;

coloringfilter: '{' STRING (',' STRING)* '}';

structuralvertexpattern: (
		intmodifier
		| starmodifier
		| plusmodifier
	);

intmodifier: '[' INT ']';

starmodifier: '*';

plusmodifier: '+';

structuralid: (ID | QUESTIONMARK_WILDCARD);

labelfilter: label ( '|' label)* | '(' label ( '|' label)* ')';

label: ID;

vertex2vertex: vertex (edge vertex)*;

edge: '->' | '<->';

ID: ('a' ..'z' | 'A' ..'Z' | '_') (
		'a' ..'z'
		| 'A' ..'Z'
		| '0' ..'9'
		| '_'
	)*;

//ARROW: '->'; STAR_WILDCARD: '*'; //Not used to describe any label but rather PLUS_WILDCARD: '+';
QUESTIONMARK_WILDCARD: '?';
WS: [ \t]+ -> skip;
NL: [\r\n]+ -> skip; // Define whitespace rule, toss it out
INT: [0-9]+;

STRING: '"' (ESC | SAFECODEPOINT)* '"';

fragment HEX: [0-9a-fA-F];

fragment UNICODE: 'u' HEX HEX HEX HEX;

fragment ESC: '\\' (["\\/bfnrt] | UNICODE);

fragment SAFECODEPOINT: ~ ["\\\u0000-\u001F];
