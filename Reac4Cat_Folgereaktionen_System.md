# Asserted Reactions 
|Reactions| Equation|
|:---|:---|
|Reaction 1|A + B -Cat(X)-> C|
|Reaction 2|C + D -Cat(X)-> E|

# User Defined Input
|Reactor|Input or Output|Composition|
|:---|:---|:---|
|Reactor1|Input|B, A, X |
|		 |Output|A,C|
|Reactor2|Input|A,B,D,X|
|	     |Output|C,D,E|

# Expected Reactions
|Reactor|Reaction|
|:---|:---|
|Reactor1| Reaction1|
|Reactor2| Reaction1, Reaction2|