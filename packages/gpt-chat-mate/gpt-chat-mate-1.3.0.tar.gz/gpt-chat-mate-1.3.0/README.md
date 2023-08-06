# GPTChatMate v1.3.0
I python cli front-end for the chatGPT API.

## Installation
Note: This app requires `sqlite3` version `>3.35.0`.
```
pip install gpt-chat-mate
```

## Configuration
Running the app for the first time will produce a `.config.json` file locally with default config options.

`db_filename` - the filename to use for the sqlite database.

`gpt_model` - which GPT model to use for the chat.

`print_style` - the pygments style to use for the GPT output.

`token_limit` - the limit on the number of [tokens](https://platform.openai.com/docs/introduction/tokens)
that the app will send in a single API call.
Note: the user will still be shown the full conversation history even if the token limits the conversation sent
to the API.

## Usage
Install via pip, and run via the package name.
```
gpt-chat-mate
```

### Commands

`chat optional[<ID>]` - Start a new chat or continue an existing one by providing the ID.

`delete <ID>` - Delete an existing chat.

`list` - List existing chats stored in the database.

`help` - List available commands.

`exit` - Exit the program.
