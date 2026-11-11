#
# Marks a line as a task item, cycles through task icons, and sorts task lists by icon
# See readme.md for hotkey info and settings
#
# https://github.com/noahcoad/SublimeTaskList
#

import re, sublime, sublime_plugin

# markdown line prefixes the icon should go after: headers, bullets, ordered lists, blockquotes
PREFIX = re.compile(r'(?:#{1,6}|[-*+>]|\d+[.)])[ \t]+')

# ordered list number, so sorting can keep 1. 2. 3. ascending
ORDERED = re.compile(r'^([ \t]*)(\d+)([.)])')

def load_icons():
	"""-> [(icon, label)] ; entries are {"icon": .., "label": ..}, or a bare icon string"""
	pairs = []
	for e in sublime.load_settings("TaskList.sublime-settings").get('icons') or []:
		if isinstance(e, str): pairs.append((e, ""))
		elif isinstance(e, dict) and e.get('icon'): pairs.append((e['icon'], e.get('label') or ""))
	return pairs

def get_icons():
	return [icon for icon, label in load_icons()]

def get_alt_icons():
	"""the "alt_sort" order, then any toggle icons it leaves out, so every task line still sorts as a task"""
	alt = [i for i in sublime.load_settings("TaskList.sublime-settings").get('alt_sort') or [] if isinstance(i, str) and i]
	return alt and alt + [i for i in get_icons() if i not in alt]

def split_line(text, icons):
	"""-> (indent, icon_index) ; icon_index is -1 when the line has no task icon"""
	indent = text[:len(text) - len(text.lstrip(' \t'))]
	body = text[len(indent):]

	# skip past any markdown prefixes (nested bullets/quotes) so the icon lands after them
	while True:
		m = PREFIX.match(body)
		if not m: break
		body = body[m.end():]

	return indent, next((i for i, icon in enumerate(icons) if body.startswith(icon)), -1)

class ToggleTaskListCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# load the list of emoji icons to be used for lists
		icons = get_icons()

		# go through each selection
		for s in self.view.sel():
			# go through each region backwards (so inserts don't change offset)
			for r in self.view.lines(s)[::-1]:
				# get the text for this line
				t = self.view.substr(r)

				# get the position of the first non-whitespace character
				pos = r.begin() + next((i for i, c in enumerate(t) if c != ' ' and c != '\t'), len(t))

				# skip past any markdown prefixes (nested bullets/quotes) so the icon lands after them
				while True:
					m = PREFIX.match(self.view.substr(sublime.Region(pos, r.end())))
					if not m: break
					pos += m.end()

				# text from first non-white to end
				line = self.view.substr(sublime.Region(pos, r.end()))

				# check to see if these first characters match one of the task icons
				icon_index = next((index for index, icon in enumerate(icons) if len(line) >= len(icon) and line[0:len(icon)] == icon), -1)

				# if the first characters match one of the icons, cycle to the next
				if icon_index > -1:
					# how many characters should be removed?
					# also include space if there's one after the icon
					char_count_to_erase = len(icons[icon_index]) + (1 if len(line) > len(icons[icon_index]) and line[len(icons[icon_index]):len(icons[icon_index]) + 1] == " " else 0)

					# remove previous icon
					self.view.erase(edit, sublime.Region(pos, pos + char_count_to_erase))

					# if this isn't the last icon in the set, add the next one
					if icon_index < len(icons) - 1:
						self.view.insert(edit, pos, icons[icon_index + 1] + " ")

				# insert the first icon
				else:
					self.view.insert(edit, pos, icons[0] + " ")

class InsertTaskListLegendCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sep = sublime.load_settings("TaskList.sublime-settings").get('legend_separator') or " "

		# each icon carries its own label, so the legend can't drift from the toggle cycle
		legend = sep.join(icon + " " + label for icon, label in load_icons() if label)
		if not legend: return

		# back to front, so earlier inserts don't shift later regions
		for r in sorted(self.view.sel(), key=lambda r: -r.begin()):
			# a selection is replaced; a bare cursor gets the legend on a line of its own
			if not r.empty(): self.view.replace(edit, r, legend); continue
			line = self.view.line(r)
			if line.empty(): self.view.insert(edit, r.a, legend)
			elif r.a == line.a: self.view.insert(edit, line.a, legend + "\n")
			else: self.view.insert(edit, line.b, "\n" + legend)

class SortTaskListCommand(sublime_plugin.TextCommand):
	done_msg, setting = "sorted", "icons"

	def order(self):
		return get_icons()

	def run(self, edit):
		icons = self.order()
		if not icons: return sublime.status_message('Task List: no "%s" order in settings' % self.setting)

		# one block per selection, deduped (several cursors can land in the same list)
		blocks = []
		for s in self.view.sel():
			r = self.block(s, icons)
			if r is not None and not any(b.begin() == r.begin() for b in blocks): blocks.append(r)
		if not blocks: return sublime.status_message("Task List: no task list here")

		# sort back to front so earlier edits don't shift later regions
		results = [self.sort_region(edit, r, icons) for r in sorted(blocks, key=lambda r: -r.begin())]
		if 'reversed' in results: sublime.status_message("Task List: already %s, so reversed the order" % self.done_msg)
		elif 'sorted' in results: sublime.status_message("Task List: " + self.done_msg)
		else: sublime.status_message("Task List: nothing to reorder")

	def line_text(self, row):
		"""line at row, or None when row is off the ends of the buffer"""
		if row < 0: return None
		pt = self.view.text_point(row, 0)
		if self.view.rowcol(pt)[0] != row: return None
		return self.view.substr(self.view.line(pt))

	def is_blank(self, row):
		t = self.line_text(row)
		return t is not None and not t.strip()

	def has_icon(self, row, icons):
		t = self.line_text(row)
		return t is not None and split_line(t, icons)[1] > -1

	def indent_of(self, row, icons):
		t = self.line_text(row)
		return None if t is None else split_line(t, icons)[0]

	def in_run(self, row, base, icons):
		"""does this row continue the list? a task line at the base indent, or a child of one"""
		t = self.line_text(row)
		if t is None or not t.strip(): return False
		indent, icon_index = split_line(t, icons)
		if len(indent) < len(base): return False
		return icon_index > -1 or len(indent) > len(base)

	def step(self, row, d, base, icons):
		"""next row of the list in direction d, hopping over blank lines between items; None at the list's end"""
		p = row + d
		while self.is_blank(p): p += d
		return p if self.in_run(p, base, icons) else None

	def parent(self, row, icons):
		"""nearest line above with a shallower indent, so a cursor deep in a child note finds its task"""
		t = self.line_text(row)
		if t is None or not t.strip(): return None
		depth = len(split_line(t, icons)[0])
		for p in range(row - 1, -1, -1):
			t = self.line_text(p)
			if t.strip() and len(split_line(t, icons)[0]) < depth: return p
		return None

	def block(self, sel, icons):
		"""the region to sort: the selected lines, else the task list around the cursor"""
		lines = self.view.lines(sel)
		if not lines: return None

		# an actual multi-line selection sorts exactly what's selected
		if not sel.empty() and len(lines) > 1:
			return sublime.Region(lines[0].begin(), lines[-1].end())

		# a bare cursor grows over the task list it sits in, next to, or just under
		row = self.view.rowcol(sel.begin())[0]
		if not self.has_icon(row, icons):
			row = next((p for p in (self.parent(row, icons), row + 1, row - 1) if p is not None and self.has_icon(p, icons)), None)

		# a blank line inside a list (between two of its items) still belongs to it
		cur = self.view.rowcol(sel.begin())[0]
		if row is None and self.is_blank(cur):
			up, dn = cur, cur
			while self.is_blank(up): up -= 1
			while self.is_blank(dn): dn += 1
			if self.has_icon(dn, icons) and self.in_run(up, self.indent_of(dn, icons), icons): row = dn
		if row is None: return None

		# the cursor's own indent sets the level being sorted; deeper lines ride along as children
		base, top, bot = self.indent_of(row, icons), row, row
		while self.step(top, -1, base, icons) is not None: top = self.step(top, -1, base, icons)
		while self.step(bot, 1, base, icons) is not None: bot = self.step(bot, 1, base, icons)

		# don't start the block on a child line that has no parent inside it
		while top < row and (self.is_blank(top) or len(self.indent_of(top, icons)) > len(base)): top += 1

		return sublime.Region(self.view.text_point(top, 0), self.view.line(self.view.text_point(bot, 0)).end())

	def sort_region(self, edit, region, icons):
		"""sort one block in icon order, or reverse it when it's already in order -> 'sorted' | 'reversed' | 'unchanged'"""
		# group lines into items: a line at the base indent, plus any deeper/blank lines under it
		items, base = [], None
		for t in [self.view.substr(r) for r in self.view.lines(region)]:
			indent, icon_index = split_line(t, icons)
			if base is None: base = indent
			if items and (len(indent) > len(base) or not t.strip()):
				items[-1][1].append(t)
			else:
				# iconless lines sort to the end
				items.append([icon_index if icon_index > -1 else len(icons), [t]])

		# blank lines trailing an item are the gap between items; they stay put by position, like the numbers
		gaps = []
		for item in items:
			n = 0
			while len(item[1]) > 1 and not item[1][-1].strip(): item[1].pop(); n += 1
			gaps.append([""] * n)

		# remember the ordered-list numbers by position, to reapply after the sort
		nums = [ORDERED.match(item[1][0]) for item in items]

		# already in icon order -> reverse it (iconless lines stay at the end); stable either way
		keys = [item[0] for item in items]
		result = 'sorted'
		if keys == sorted(keys):
			items.sort(key=lambda item: (item[0] == len(icons), -item[0]))
			result = 'reversed'
		else: items.sort(key=lambda item: item[0])
		if [item[0] for item in items] == keys: return 'unchanged'

		out = []
		for i, item in enumerate(items):
			head, m, orig = item[1][0], ORDERED.match(item[1][0]), nums[i]
			if m and orig: head = orig.group(1) + orig.group(2) + orig.group(3) + head[m.end():]
			out.append(head)
			out.extend(item[1][1:])
			out.extend(gaps[i])

		self.view.replace(edit, region, "\n".join(out))
		return result

class AltSortTaskListCommand(SortTaskListCommand):
	"""Sort, but in the "alt_sort" order from settings instead of the toggle cycle"""
	done_msg, setting = "sorted (alternative)", "alt_sort"

	def order(self):
		return get_alt_icons()
