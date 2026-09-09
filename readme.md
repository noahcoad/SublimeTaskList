# Task List

Toggle an emoji icon onto a line in [Sublime Text](https://www.sublimetext.com/) — like *Toggle
Comment*, but it cycles through a set of task icons.

```
:: today
✅ order parts for automated sprayer
⚛️ update architecture diagram
⚛️ create POC proposal

:: archive
✅ change flight to Japan
⚛️ mail package to brother
```

## Usage

Run **Toggle Task List** from the command palette. Each press advances the line to the next icon, then
clears it:

⚛️ to do → ✅ done → 🅿️ in progress → ✴️ highlight → 🆘 error → *(none)*

Works on multiple lines and multiple selections at once, and keeps the icon after any leading
indentation.

## Key Bindings

None ships enabled, so nothing you already use gets clobbered. Open **Preferences > Package Settings >
Task List > Key Bindings** and copy the suggested binding from the left pane to your own on the right:

```json
{ "keys": ["super+alt+t"], "command": "toggle_task_list" }
```

## Settings

**Preferences > Package Settings > Task List > Settings** — the `icons` list is the cycle, in order.
The first entry is the "to do" icon you'll see most; 🟣, 🟪, and ✔️ all work well there, as does any
other emoji.

Both Settings and Key Bindings are in the command palette too, as *Preferences: Task List …*.

## Also

Check out my other [Sublime Text packages](https://gist.github.com/noahcoad/712ba4e38467f5126eb8cedd9ecbc842).
