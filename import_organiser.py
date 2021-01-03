"""
This is a simple tool that organises imports in Python.
Imports are alphabetically ordered.
The 'import' comes before 'from ... import ...' 

Usage:
In terminal> python import_organiser.py --file=FILE_NAME.py
This will create another py file that has 'organised_' as a prefix + FILE_NAME.py
Alternatively, you can change that behaviour in the code.
"""

import click
import re

@click.command()
@click.option('--file', help='Your Python file.')
def organise_my_imports(file):
	import_pattern = "^import.*[^\s]"
	from_pattern = "^from.*[^\s]"
	from_pattern_parent = ".*[^\s](?=\s+import)"
	from_pattern_chunks = "\w+(?=,)"
	import_list = []
	from_list = []
	rest = []
	from_pattern_chunks_list = []
	with open(file, 'r', encoding='utf-8') as f:
		for i in f:
			if re.search(import_pattern, i):
				i = i.replace("\n", ",")
				for j in re.findall(from_pattern_chunks, i):
					import_list.append(j)
			elif re.search(from_pattern, i):
				from_list.append(i.replace("\n", ","))
			else:
				rest.append(i)
		for i in range(len(rest)-1, -1, -1):
			if rest[i] != '\n':
				break
			else:
				del rest[i]


		for k, v in enumerate(from_list):
			from_pattern_chunks_list.append([re.findall(from_pattern_parent, v)[0]])
			for i in re.findall(from_pattern_chunks, v):
				from_pattern_chunks_list[k].append(i)

		with open(f'organised_{f.name}', 'w', encoding='utf-8') as file:
			for i in sorted(import_list):
				file.write(f'import {i}\n')
			for i in sorted(from_pattern_chunks_list):
				for j in i[1:]:
					file.write(f'{i[0]} import {j}\n')
			for i in rest:
				file.write(i)
				if rest.index(i) == len(rest) - 1 and not i.endswith('\n'):
					file.write('\n')

organise_my_imports()
