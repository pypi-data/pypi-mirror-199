# Ververser Example 1: Minimal Setup

When a ververser app is running and you make changes to the hosted scripts, they are automatically hot reloaded in the app. 
In case of any errors, the app is paused, and will try to reload again when the files are updated again. 

Ververser can be instantiated in multiple ways. 
The most minimal way to set up a ververser script is by calling _host_this_folder()_, 
after which the game hooks will automatically be looked up from the _main.py_ script in that folder 
(which might simply be the same file as from which the function was called to begin with).
Ververser supports several functions within the script that can be called by the engine:

- vvs_init - called by ververser when the script is instantiated
- vvs_update - called by ververser every frame
- vvs_draw - called by ververser every frame (clearing and flipping the main buffer is done for you by ververser)
- vvs_exit - called by ververser before reloading, and when exiting the application proper

Note that you do not have to implement them all; just the ones you want to use.
Besides these functions that are invoked by ververser, the script can contain any additional logic you'd like. 

