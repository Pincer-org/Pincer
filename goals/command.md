
# Command

When creating a command, the function will be able to have a `ctx` parameter.
This parameter will be optional, and if not set, will not cause any error.

The Context object will work similarly to the `discordpy` package.



## Simplest command

The command syntax will be very similar to the original discordpy one.
However, instead of `await ctx.send`, the command will return an object.
When the return type is a string, this will send a simple message.

```py
@command('my_command')
async def ping() -> str:
    return 'pong'
```

A `Message` object could also be returned for further customization:
```py
@command('my_command')
async def ping(ctx: Context) -> Message:
    return Message(
        'pong',
        replied_from=ctx.message
    )
```

## Watchers
Watcher objects can be returned to have an even trigger which allow to 
execute a watcher decorated function.

```py
def check(ctx: Context, m: Message):
    return m.author == ctx.author

@command('something')
async def something() -> Tuple[Embed, Watcher]:
    ...
    return an_embed, watcher(
        'button_click', check=check, something_else
    )

@watcher
async def something_else(ctx: Context) -> Embed:
    ...

```