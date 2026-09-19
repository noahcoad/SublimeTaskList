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

Run **Task List: Toggle** from the command palette. Each press advances the line to the next icon, then
clears it:

⚛️ to do → 🅿️ in progress → ✴️ highlight → 🆘 error → ✅ done → *(none)*

Works on multiple lines and multiple selections at once, and keeps the icon after any leading
indentation. Markdown prefixes are preserved too — the icon lands after headers, bullets, ordered
list numbers, and blockquote markers:

```
## ✅ Header
- ⚛️ bullet
1. ⚛️ ordered item
> - ✅ nested quote + bullet
```

## Sorting

**Task List: Sort** puts a list in icon order — the same order the toggle cycles through, so open work
rises to the top and done work sinks to the bottom.

With a selection it sorts the selected lines. With just a cursor it finds the list on its own, growing
up and down over the run of task lines the cursor is in (or next to). Lines with no icon sort to the
end, same-icon lines keep their relative order, indented lines travel with the item above them, and
ordered-list numbers get rewritten so `1. 2. 3.` stays ascending.

```
1. ⚛️ update architecture diagram        1. 🅿️ get Figma ESC
2. ✅ order parts                   →    2. ⚛️ update architecture diagram
3. 🅿️ get Figma ESC                      3. ✅ order parts
```

## Legend

**Task List: Insert Legend** drops a one-line key at the cursor, so a shared file explains its own icons:

```
⚛️ to do → 🅿️ in progress → ✴️ highlight → 🆘 error → ✅ done
```

It's built from `icons` paired with `legend_labels`, joined by `legend_separator`, so it stays in sync
with whatever icons you've set.

## Key Bindings

None ship enabled, so nothing you already use gets clobbered. Open **Preferences > Package Settings >
Task List > Key Bindings** and copy the suggested bindings from the left pane to your own on the right:

```json
{ "keys": ["super+alt+t"], "command": "toggle_task_list" },
{ "keys": ["super+alt+s"], "command": "sort_task_list" }
```

## Settings

**Preferences > Package Settings > Task List > Settings** — the `icons` list is both the toggle cycle
and the sort order. The first entry is the "to do" icon you'll see most; 🟣, 🟪, and ✔️ all work well
there, as does any other emoji. `legend_labels` and `legend_separator` control the inserted legend.

Both Settings and Key Bindings are in the command palette too, as *Preferences: Task List …*.

## Also

Check out my other [Sublime Text packages](https://gist.github.com/noahcoad/712ba4e38467f5126eb8cedd9ecbc842).
