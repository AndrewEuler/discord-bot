# Bot for the administration of the discord channel
It has the following set of functions:

1. `create-channel` - Creates a text channel with the specified name.
2. `my-role` - Gives you a role on the server if you have the necessary rights for it.
3. `roll` - Throws a 6-sided die n-times.
4. `help` - Shows a list of all commands

When adding a new user to the discord channel, the bot welcomes him and adds the role assigned to him by default.
The `on_command_error` command is called if the user does not have enough rights for the command he called.

Additional functions:

To simplify the readability of the `help` command, the **«pretty_help»** library was added.

For convenient interaction with the bot and its exceptions, logging was added using the **«logging»** library.
