import re
import random
import string

def replace_syntax(src, replacer=lambda s: s, str_replacer=lambda s: s):
	"""
	Given a Python code, strips all strings and comments, runs the given
	replacer function, and reinserts the strings and comments again.
	This is done by replacing each string/comment with a random uppercase
	identifier and undoing the process at the end.

	This is useful if you want to extend Python's syntax the easy way
	(string replacement) without touching stuff inside strings and comments.

	If you want to manipulate the strings themselves, `str_replacer` is
	invoked for each string/comment and its return used as replacement.
	"""
	replaced_strings = {}

	def replace_string(match):
		# The random ids looks like this: XVEJOHJJEGSRADYAXKUH
		id = ''.join(random.choice(string.ascii_uppercase) for i in range(20))
		replaced_strings[id] = str_replacer(match.group())
		return id

	string_pattern = r'r?u?("""|\'\'\'|\'|").*?(?<!\\)\2'
	comment_pattern = r'#[^\n]*'
	full_pattern = '({})|({})'.format(string_pattern, comment_pattern)
	
	# Use DOTALL for multi-line strings. Technically multi-line strings
	# require triple-quotes, but we assume the source code is syntactially
	# valid in this regard.
	stripped = re.sub(full_pattern, replace_string, src, flags=re.DOTALL)

	new = replacer(stripped)

	for id, replacement in replaced_strings.items():
		new = new.replace(id, replacement)

	return new

if __name__ == '__main__':
	print_and_return = lambda s: print(s) or s
	print(replace_syntax(open(__file__).read(), str.upper, print_and_return))