#!/usr/bin/python3
import os
import sys
import argparse
import threading

"""
./setup.py zip;ipython

import os,sys;sys.path.insert(0,'cryptolation.zip');import pysrc.cryptoguard4py as crypy;crypy.argz(version=True)()#crypy.main("--h")
"""

from astroid import MANAGER as MGR

#region Src

try:
	import pysrc.rules.rule_source as ru
	import pysrc.sanity as sanity
	from pysrc.utils import utils
	from pysrc.rules import rule_mgmt
	from pysrc.information import VERSION
	from pysrc.output_routing import management
	from pysrc.utils.utils import check,retrieve_files
except Exception as e:
	from utils import utils
	import sanity
	from rules import rule_mgmt
	import rules.rule_source as ru
	from information import VERSION
	from output_routing import management
	from utils.utils import check,retrieve_files

try:
	import crusty
except Exception as e:
	print("Failure to import cryptoguard4py: {0}".format(e))
	pass
try:
	sys.path.append("../crusty")
	import crusty
except Exception as e:
	print("Failure to import from non-src: {0}".format(e))
	pass
#endregion

base_name = os.path.basename(__file__)
cur_path = str(__file__).replace(f"/{base_name}", '')
NAME = base_name.replace(".py", "")

from dataclasses import dataclass
@dataclass
class argz:
	source: str = False
	version: bool = False
	rule: str = None
	output: str = "_temp_.csv"
	format: str = None
	exclude_paths: list = None
	all_files: bool = False
	get_structure: bool = False
	inference: int = None
	install: bool = False
	optimize_ast: bool = False
	modules: list = None

	def __str__(self):
		output_string = ""

		if self.version:
			output_string += " --version {0} ".format(self.version)
		if self.source:
			output_string += " --source {0} ".format(self.source)
		if self.rule:
			output_string += " --rule {0} ".format(self.rule)
		if self.output:
			output_string += " --output {0} ".format(self.output)
		if self.format:
			output_string += " --format {0} ".format(self.format)
		if self.exclude_paths:
			output_string += " --exclude_paths {0} ".format(self.exclude_paths)
		if self.all_files:
			output_string += " --all_files {0} ".format(self.all_files)
		if self.get_structure:
			output_string += " --get_structure {0} ".format(self.get_structure)
		if self.inference:
			output_string += " --inference {0} ".format(self.inference)
		if self.install:
			output_string += " --install {0} ".format(self.install)
		if self.optimize_ast:
			output_string += " --optimize_ast {0} ".format(self.optimize_ast)
		if self.modules:
			output_string += " --modules {0} ".format(self.modules)

		return output_string

	def __repr__(self):
		return "ARGS<{0}>".format(str(self))

	def __call__(self):
		print(self)
		return main(str(self).split(' '))

	def pull(self, remove=True):
		main(str(self).split(' '))
		import pandas as pd
		output = pd.read_csv(self.output)
		if remove:
			os.remove(self.output)
		return output

@check()
def arguments(string_set):
	parser = argparse.ArgumentParser(description="{0}:> {1}".format(NAME, VERSION))

	parser.add_argument("-v",
						"--version",
						action='store_true',
						help='Show the current version')
	parser.add_argument(
		"-s",
		"--source",
		dest="source",
		action='store',
		#type=lambda x: x if os.path.exists(x.strip()) else
		#parser.error("Path {0} does not Exist".format(x)),
		help='The current source versions')
	parser.add_argument(
		"-r",
		"--rule",
		dest="rule",
		action='store',
		type=lambda x: x
		if (os.path.isfile(x.strip()) and x.endswith('.json')
		   ) else parser.error("File {0} does not exist or isn't a json file".format(x)),
		help='The extra rule path')
	parser.add_argument("-o",
						"--output",
						dest="output",
						action='store',
						help="The output file to be written to.",
						default="raw_output.csv")
	parser.add_argument(
		"-f",
		"--format",
		dest="format",
		action='store',
		help=
		"A user defined output format extending the output structure (see the -g flag).",
		default="csv")
	parser.add_argument(
		"-x",
		"--exclude_paths",
		dest="exclude_paths",
		action='store',
		help=
		"Excluding the files by providing a specific regex (ex. __init__.py or \/venv\/ for the venv folder).",
		default=[],
		nargs='+')
	parser.add_argument("-a",
						"--all_files",
						action='store_true',
						help="Print out non vulnerability files",
						default=False)
	parser.add_argument(
		"-g",
		"--get_structure",
		action='store_true',
		help="Print the base structure of the outputting format.",
		default=False)
	parser.add_argument("-i",
						"--inference",
						action='store',
						help="How many inferences should be checked",
						type=lambda x: x if isinstance(x, int) and x >= 0 else
						parser.error("Please enter a non-negative integer"),
						default=100)
	parser.add_argument(
		"--install",
		action='store_true',
		help="Install the required dependencies needed for the project to run",
		default=False)
	parser.add_argument(
		"--optimize_ast",
		action='store_true',
		#help="Optimize the AST's that are loaded to reduce the memory required.",
		default=False)
	parser.add_argument(
		"--modules",
		dest="modules",
		action='store',
		help="Write out the modules that are being scanned for to an output file.",
		default=None,
		required=False)

	#parser = parser.parse_args(string_set)
	parser, unknown = parser.parse_known_args(string_set)
	if os.path.exists(parser.output):
		try:
			os.remove(parser.output)
		except:
			pass

	if parser.version:
		print("{0}".format(VERSION.strip()))
		return 0

	if parser.install:
		for package in [
	"astroid==2.11.2",
	"setuptools==50.3.2",
	#"password_strength==0.0.3.post2",
	#"stdlib_list==0.8.0",
	"pandas",
	"hugg",
	"funbelts",
]:
			try:
				os.system("{0} -m pip install {1}".format(sys.executable, package))
			except Exception as e:
				pass

	if parser.modules is not None:
		rules, secure_values = ru.load(parser.rule)
		file_output = utils.of_list(parser.modules)[0]

		mod_output = []
		mod_strip = lambda x: x.replace(".*", "").replace("*", "").split(" | ")[0].split(".^")[0].replace("^((?!safe_).)", "")
		for mod, specifics in rules.items():
			mod_output += [mod_strip(mod)]
			for specific in specifics:
				if 'criteria' in specific:
					mod_output += [mod_strip("".join([mod, specific['criteria']]))]

		with open(file_output, "w+") as f:
			for mod in list(set(mod_output)):
				f.write("{0}\n".format(mod))
		print(file_output)
		return 0

	if parser.get_structure:
		import inspect, astroid
		try:
			import pysrc.output_routing.base_structure as strc
		except:
			pass
		try:
			import output_routing.base_structure as strc
		except:
			pass

		structure_body = astroid.parse(inspect.getsource(strc.Structure))
		to_filter = [
			itr for itr, body_node in enumerate(structure_body.body[0].body)
			if not (isinstance(body_node, astroid.FunctionDef) and
					body_node.decorators is not None and "abstractmethod" in
					[x.name for x in body_node.decorators.nodes])
		]

		to_filter.reverse()

		for filtering in to_filter:
			structure_body.body[0].body.pop(filtering)

		body = f"""import os,sys
try:
		from pysrc.output_routing.base_structure import Structure
except:
		pass
try:
		from output_routing.base_structure import Structure
except:
		pass

#USE THIS TO INSTALL ANY PACKAGES
#os.system("{0} -m pip install ".format(sys.executable))

{structure_body.as_string().replace('class Structure(ABC)','class application(Structure)')}
"""

		#with open("./current_structure.py", "w+") as f:
		#	   f.write(structure_body.as_string())
		print(body)

	return parser

@check()
def main(string):
	if "--test" in string:
		print("Testing")
		sys.argv = ""
		sanity.main()
		return 0

	args_trimmed = arguments(string)
	#print(args_trimmed)
	if isinstance(args_trimmed, int):
		return args_trimmed

	MGR.max_inferable_values = args_trimmed.inference
	MGR.optimize_ast = args_trimmed.optimize_ast
	MGR.thread_limit = threading.BoundedSemaphore(10)

	with management.get_structure(args_trimmed.format)(args_trimmed.source.strip(),
											   args_trimmed.output.strip(),
											   all_files=args_trimmed.all_files) as handler:
		rules, secure_values = ru.load(args_trimmed.rule)
		print("[", end='', flush=True)
		#print(":>"+args_trimmed.source)
		#print(":>"+args_trimmed.source.strip())
		try:
			for foil in retrieve_files(args_trimmed.source.strip(), args_trimmed.exclude_paths):
				#print(foil,flush=True)
				cur_output = rule_mgmt.search(handler, foil, rules, secure_values)
				#print(cur_output,flush=True)
				#handler += rule_mgmt.search(handler, foil, rules, secure_values)
				handler += cur_output
				print(".", end='', flush=True)
		except Exception as e:
			print(e)
		print("]")

	return 0

@check()
def hollow_main():
	sys.exit(main(sys.argv))

if __name__ == '__main__':
	hollow_main()
