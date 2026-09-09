# Task List

A [Sublime Text](https://www.sublimetext.com/) Package

## Description

Toggles a Task List emoji in front of a line. \
Similar to "Toggle Comment", but cycles through emoji "icons".

Command is called "Toggle Task List", available from the command palette.

## Key Bindings

No key binding is set by default, so nothing you already use gets clobbered. \
Open **Preferences > Package Settings > Task List > Key Bindings** (or *Preferences: Task List Key Bindings* in the command palette) and copy the suggested binding from the left (default) side to the right (user) side:

```json
{ "keys": ["super+alt+t"], "command": "toggle_task_list" }
```

## Settings

Default icons: \
⚛️ to do \
✅ done \
✴️ highlight / warning \
🅿️ informational / in progress \
🆘 not done / error

Open **Preferences > Package Settings > Task List > Settings** (or *Preferences: Task List Settings* in the command palette) to change the `icons` list. The first entry is the "to do" icon you'll see most, so pick one you like:

| Icon | Name | Codepoint |
|---|---|---|
| ⚛️ | atom (default) | `U+269B U+FE0F` |
| 🟣 | purple dot | `U+1F7E3` |
| 🟪 | purple square | `U+1F7EA` |
| ✔️ | grey checkmark | `U+2714 U+FE0F` |

Any emoji works — see the [full emoji list](https://unicode.org/emoji/charts/full-emoji-list.html). Icons without a `U+FE0F` variation selector (like 🟣 and 🟪) render as color emoji most consistently across macOS, Windows, and Linux.

## For Example: `todo.txt`

```
:: today
✅ order parts for automated sprayer
⚛️ update architecture diagram
⚛️ create POC proposal

:: archive
✅ change flight to Japan
⚛️ mail package to brother
```

## Also
Check out my other [Sublime Text packages](https://gist.github.com/noahcoad/712ba4e38467f5126eb8cedd9ecbc842)
