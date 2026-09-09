#
# Marks a line as a task item, and cycles through task icons
# See readme.md for hotkey info and settings
#
# https://github.com/noahcoad/SublimeTaskList
#

import sublime, sublime_plugin

class ToggleTaskListCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# load the list of emoji icons to be used for lists
		icons = sublime.load_settings("TaskList.sublime-settings").get('icons')

		# go through each selection
		for s in self.view.sel():
			# go through each region backwards (so inserts don't change offset)
			for r in self.view.lines(s)[::-1]:
				# get the text for this line
				t = self.view.substr(r)

				# get the position of the first non-whitespace character
				pos = r.begin() + next((i for i, c in enumerate(t) if c != ' ' and c != '\t'), len(t))

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
