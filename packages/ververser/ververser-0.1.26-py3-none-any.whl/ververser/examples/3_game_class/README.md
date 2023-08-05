# Ververser Example 3: Game Class

Instead of letting ververser call free functions, one could also define a game class, and let ververser manage an instance of it. 
This is recommended, as state will often be shared between the typical game hooks, and by putting the function in a class, this state is easily shared. 
this example illustrates how such a class can be defined.