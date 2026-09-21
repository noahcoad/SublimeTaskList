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

Each icon carries its own `label`, so the legend can't drift from the toggle cycle. `legend_separator`
sets what goes between the entries; an icon with no label is left out.

The labels are yours to reword — they're only what the legend prints, so rename them to whatever your
files call things: `underway`, `parked`, `waiting`, `blocked`, `completed`.

## Key Bindings

None ship enabled, so nothing you already use gets clobbered. Open **Preferences > Package Settings >
Task List > Key Bindings** and copy the suggested bindings from the left pane to your own on the right:

```json
{ "keys": ["super+alt+t"], "command": "toggle_task_list" },
{ "keys": ["super+alt+s"], "command": "sort_task_list" }
```

## Settings

**Preferences > Package Settings > Task List > Settings** — the `icons` list is both the toggle cycle
and the sort order, and each entry pairs an icon with the `label` the legend uses for it:

```json
"icons": [
	{ "icon": "⚛️", "label": "to do" },
	{ "icon": "✅", "label": "done" }
]
```

The first entry is the "to do" icon you'll see most; 🟣, 🟪, and ✔️ all work well there, as does any
other emoji. A bare string (`"icons": ["⚛️", "✅"]`) works too — it just won't appear in the legend.

Both Settings and Key Bindings are in the command palette too, as *Preferences: Task List …*.

## Also

Check out my other [Sublime Text packages](https://gist.github.com/noahcoad/712ba4e38467f5126eb8cedd9ecbc842).
