# Streamlabs-Rcon-Integration


A Python exe for integrating Streamlabs and any game supporting Rcon. Its currently being used with Factorio, but should be compatible with any other Rcon interfaced game.
At present only really tested with Twitch, but should work with mixer and youtube based on API spec.


Installation & Usage
==========
Get the [latest version zip](https://github.com/muppet9010/Streamlabs-Rcon-Integration).
Unzip the files in to the desired folder.
Run the: > Streamlabs Rcon Integration.exe
Click on Settings button and enter your details.
Configure a profile or be happy with the sample one.
Select the desired profile and click Start.
The integration is now running between the Streamlabs account and the game using the selected profile.


Usage Concepts
========

The app takes in Streamlabs events and processes them through configurable reactions to trigger a desired action via Rcon in  game. These reactions are grouped togeather as savable profiles.

The complete list of Streamlabs events and their contained data attributes can be found in the [eventDefinitions.json file](https://github.com/muppet9010/Streamlabs-Rcon-Integration/eventDefinitions.json). The top section under `[ALL]` are generated and normalised by the program to provide some standard entries across all event types. The list of platform and event specific attributes are what streamlabs is currently sending. These often vary from their documentation and change periodically.

The app runs a single grouping of reactions at a time, being loaded and saved as a profile. During the process if no suitable option is found it will be shown within the app and that events processing stops. Its assumed you want to handle any event you get. Special options at each level exist for more simple uses cases.

When an Streamlabs event is received it is processed to have the standard `[ALL]` additional data attributes calculated for them. The reactions are reviewed to find the most approperiate one. First the reactions are checked for the first matching platform and type to the event. If no match is found the ValueType of the event is checked for in the reactions for a match.

Assuming a reaction for the event is found the reaction's filters are checked for the first that is met. Filters allow simple math script conditions to be used to select the approperiate action to do for the event. All of the events data items from Streamlabs and this app (generated up to this point) can be used witihn the filter in the format `[DATA_ITEM_NAME]`. i.e. `[VALUE] >= 5 and [VALUE] < 10`. There is a special `ALL` filter option that it configured will be triggered after all other filters have been checked. The filters within a reaction are not order specific and so should not overlap each others conditions.

The first complying reaction filter will then run an optional manipulator script if configured. This creates a new data item for the event `[MODVALUE]` with the scripts simple math script output value. This is used when you want to pass a modified value in to the game.

The action tied to the filter is an Rcon command that's run in the game. It can be multiple Rcon commands and utilise any of the events data items in the standard format `[DATA_ITEM_NAME]`. i.e. `/c game.print("[name] supported with $[VALUE] worth $[MODVALUE]")`. There is a special `NOTHING` action that is intended for intentionally ignoring the event.

All data items used in scripts are replaced with their event data values at execution time. The replaced text may require wrapping in quotes if it needs to be treated as a string.

Filter and manipulator scripts can include the logical statements `and`, `or` as well as brackets `()`. These scripts are run as Python code.

Actions can be a locally defined Lua string or use a shared named Lua string within the profile. This is to allow re-use when its convienent.

When the application starts up all profiles in the profile folder are checked for their compliance with the event handler types and their attributes. Any issues causes the program to stop loading and the issue is recorded to the log file. This is to avoid failure from mis-configuration at run time.

After configuring the application it is advised to run it and use the Streamlabs Test Widget option to send test events and confirm it behaves as you expect.




Development Building
=============
Uses the python modules and their dependcies:

- Python 3.7 and default install modules
- python-socketio[client]  =  https://python-socketio.readthedocs.io/en/latest/
- PyInstaller  =  https://www.pyinstaller.org/

Build the scripts into an exe using PyInstaller via Build.bat. It will place the exe in the "build\dist" folder.
