import glob, os, re, functools, time, astroid
from datetime import datetime
from pathlib import Path

counter = 1

def check(base=None):
	"""
	The check function is a decorator that logs the time it takes for a function to execute.
	It also logs the name of the function, its module and class, and its start and end times.
	The check function writes this information to basic_logging.csv.

	:param base=None: Specify the base of the log file
	:return: A decorator
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	def decorator(function):
		"""
		The decorator function is used to log the time it takes for a function to run.
		It will also log the name of the function, its module and its qualified name.
		The decorator will write this information into a csv file called basic_logging.csv

		:param function: Specify the function that is being decorated
		:return: The wrapper function
		:doc-author: frantzme
		**Verified: TRUE**
		"""
		filename = "basic_logging.csv"
		if not os.path.exists(filename):
			with open(filename,"w+") as f:
				f.write("time,func_name, qual_name, start, end, duration\n")
		@functools.wraps(function)
		def wrapper(*args, **kwargs):
			"""
			The wrapper function is a decorator that will log the time it takes for a function to run.
			It will also write this data to a file called &quot;log_time.csv&quot; in the current working directory.

			:param *args: Pass a non-keyworded, variable-length argument list
			:param **kwargs: Catch all keyword arguments that are passed to the wrapper function
			:return: The result of the function it wraps
			:doc-author: frantzme
			**Verified: TRUE**
			"""
			tic = time.perf_counter()
			result = function(*args, **kwargs)
			toc = time.perf_counter()

			with open(filename,"a+") as f:
				f.write("{0},{1},{2}.{3},{4},{5},{6}\n".format(datetime.now(), function.__name__, function.__module__, function.__qualname__, tic, toc,toc - tic))

			return result
		return wrapper
	return decorator

@check()
def set_key_values_for_dict(dyct:astroid.Dict):
	"""
	The set_key_values_for_dict function takes a dictionary and sets the values of each key to its corresponding value.
	For example, if the input is:
	{'a': 1, 'b': 2}
	Then the output will be: {'a': 1, 'b': 2}.  This function is used in conjunction with set_key_values_for_dicts.

	:param dyct:astroid.Dict: Store the values of the keys and values in a dictionary
	:return: A dictionary of the keys and values from the astroid
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	dyct.values = {}
	for (key, value) in dyct.items:
		dyct.values[key.value] = value.value
	return dyct.values

def get_qual_name(func):
	"""
	The get_qual_name function is a helper function that returns the qualified name of a function.
	It does this by inspecting the locals of an inferred result from astroid inference, and returning
	the value associated with __qualname__ if it exists in those locals. If it doesn't exist, then
	it simply returns the qname (qualified name) of that inferred result.

	:param func: Get the name of the function
	:return: The qualified name of the function
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	try:
		from pysrc.mewn import node_utils
	except Exception as e:
		from mewn import node_utils
	inferred_results = node_utils.infers(func) #TODO :> Fix This #func.inferred()
	if len(inferred_results) != 1:
		return None

	try:
		inferred_locals = inferred_results[0].locals
		#if '__qualname__' in inferred_locals:
		cur = str(inferred_locals['__qualname__'][0].value)
	except Exception as e:
		cur = inferred_results[0].qname()
	return cur[1:] if cur.startswith('.') else cur

@check()
def to_bool(raw_value):
	"""
	The to_bool function converts a string to a boolean value.
	It accepts the following values:
		* TRUE, True, true, 1 -&gt; True
		* FALSE, False, false or 0 -&gt; False

	:param raw_value: Pass the value of the parameter from
	:return: A boolean value
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	value = str(raw_value).upper()
	if "TRUE" in value:
		return "true"
	elif "FALSE" in value:
		return "false"
	else:
		return raw_value

@check() #Shifted Over to Rust
def safety_list(lyst: list):
	"""
	The safety_list function is a helper function that takes in a list and returns it if it is not None or empty.
	Otherwise, the safety_list function will return an empty list.

	:param lyst:list: Check if the list is empty or not
	:return: A list or an empty list depending on the input
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	if lyst is not None and lyst:
		return lyst
	else:
		return []


@check() #Shifted Over to Rust
def chain_get(attribute: list, obj, pillowGet: bool = False):
	"""
	The chain_get function is a helper function that allows you to get the value of an attribute from an object,
	even if it's buried in a chain of other objects. For example, let's say we have this class:
	class Person(object):
	name = &quot;John&quot;

	:param attribute:list: Get the value of an attribute from a dictionary
	:param obj: Get the value of the attribute
	:param pillowGet:bool=False: Determine if we should return the pillow object or just the attribute
	:return: The value of the last attribute in the chain
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	output = None
	attribute.reverse()
	if pillowGet:
		output = obj

	while obj:
		obj = safe_get(attribute[-1], obj)
		attribute.pop()

		if pillowGet and obj:
			output = obj
		if not attribute:
			return output or obj

	return output


@check() #Shifted Over to Rust #> Need to update the Rust portion
def safe_get(attribute, obj, _default=None):
	"""
	The safe_get function is a helper function that allows us to access the value of an attribute
	of an object, or return a default value if the attribute does not exist. This is useful for when
	we want to make sure we don't crash our program because of some weirdness in how Python handles
	attributes and dictionaries.

	:param attribute: Specify the attribute of the object that is being retrieved
	:param obj: Get the attribute from the object
	:param _default=None: Specify a default value to return if the attribute is not found
	:return: The value of the attribute if it exists in the object
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	if isinstance(obj,dict):
		return obj.get(attribute, _default)
	if hasattr(obj, attribute) and getattr(obj, attribute) is not None:
		return getattr(obj, attribute)
	else:
		return _default


@check()
def new_match(name: str, dyct: dict) -> str:
	"""
	The new_match function takes a string and a dictionary as arguments.
	If the string is in any of the values of the dictionary, it returns that value.
	Otherwise, it returns None.

	:param name:str: Store the name of the player that is being compared to all other players in the dictionary
	:param dyct:dict: Access the dictionary
	:return: The name of the player if that player is in the dictionary
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	if any(lambda obj: compare(name, obj) for value in dyct.values()):
		return name
	else:
		return None


@check()
def match(lib: dict, dyct: dict) -> str:
	"""
	The match function takes a library and a dictionary of libraries.
	It returns the name of the library if it is found in the dictionary,
	or None otherwise.

	:param lib:dict: Get the fully qualified name of the library
	:param dyct:dict: Check if the library is already in the
	:return: The fully qualified name of the library if it is
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	name = get_fully_qualified_name(lib)
	if any(lambda obj: compare(name, obj) for value in dyct.values()):
		return name
	elif any(lambda obj: compare(get_fully_qualified_name(lib, True), obj)
			 for value in dyct.values()):
		return name
	else:
		return None


@check()
def get_fully_qualified_file_name(base_path: str):

	@check()
	def decipher_name(file: str) -> str:
		"""
		The decipher_name function takes a file path and returns the name of the module
		 that would be created by importing that file. This is done by replacing all
		 instances of os.sep with '.', removing '.py' from the end, and prepending any
		 parent directory names to it.

		:param file:str: Determine the file name of the module that is being imported
		:return: The name of the file without the
		:doc-author: frantzme
		**Verified: TRUE**
		"""
		import os
		if base_path is not None and base_path != '' and os.path.abspath(
				file).startswith(base_path):
			return "{0}.{1}".format(os.path.basename(os.path.normpath(base_path)),os.path.abspath(file).replace(base_path, '').replace(os.sep, '.').replace('.py', '')).replace(
				"..", ".")
		else:
			return os.path.basename(file).replace('.py', '')

	return decipher_name


@check()
def get_fully_qualified_name(lib: dict,
							 full: bool = False,
							 use_class_name: bool = False) -> str:
	"""
	The get_fully_qualified_name function takes a library dictionary and returns the fully qualified name of that library.
	The fully qualified name is either the class_name or imports attribute, depending on whether use_class_name is True or False.
	If full is True, then it will return the full path to that attribute (e.g., &quot;os.path&quot;).  Otherwise, it will just return the last element in that path (e.g., &quot;path&quot;).

	:param lib:dict: Pass the library information
	:param full:bool=False: Determine whether or not the fully qualified name should be returned
	:param use_class_name:bool=False: Determine whether or not the class name should be used in the fully qualified name
	:return: The fully qualified name of the library
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	return str(lib['imports'] if not use_class_name or not 'class_name' in lib else lib['class_name']) + full * ".{0}".format(lib['criteria'])


@check()
def get_fully_qualified_name_curry(imports: str):

	@check()
	def curry_prep(lib: dict, full: bool = False, use_class_name: bool = False):
		"""
		The curry_prep function is used to prepare the library for use in a curry function.
		It takes the library and returns either a string or list of strings that can be used as arguments
		for a curry function. If it finds criteria with an := operator, it will return just the value after
		the operator (i.e., :=). Otherwise, if there is no class_name key in lib, then it will return
		imports + . + lib['criteria']. If there is a class_name key in lib and use_class_name = True, then
		it will return imports + . + lib

		:param lib:dict: Pass the library to be used
		:param full:bool=False: Determine if the function should return a string with the full path to the criteria or just a string of it's name
		:param use_class_name:bool=False: Make the function work with both classes and functions
		:return: The value of the criteria key in the dictionary, unless it starts with &quot;:=&quot;, in which case it returns the value after that symbol
		:doc-author: frantzme
		**Verified: TRUE**
		"""

		try:
			if lib['criteria'].startswith(':='):
				return lib['criteria'][2:]
			else: #TODO: This is a hack, need to fix this
				return f"{imports if not use_class_name or not 'class_name' in lib else lib['class_name']}" + full * f".{lib['criteria']}"
		except Exception as e:
			# print(e)
			pass

	return curry_prep


@check()
def retrieve_files(path, exclude_expressions=[]):
	"""
	The retrieve_files function accepts a path and an optional list of expressions to exclude.
	If the path is a file, it returns that file. If the path is a directory, it returns all files in that directory (recursively).
	The optional list of expressions can be used to filter out unwanted files. For example:

	:param path=os.path.abspath(os.curdir): Set the path to the current directory
	:param exclude_expressions=[]: Exclude files that match the
	:return: A list of files that match the
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	#print("Looking into :> {0}".format(path))
	if len(of_list(exclude_expressions)) > 0:
		regex = re.compile(" | ".join(map(str.strip, exclude_expressions)), re.X | re.I)
		include = lambda file_path: not bool(regex.search(file_path))
	else:
		include = lambda _: True

	if os.path.isfile(path):
		return [path] if include(path) else []

	"""
	print(">>")
	print(len(of_list(exclude_expressions)))
	print(os.path.join(path, '**/*.py'))
	print(
		[
			str(Path(filename).resolve())
			for filename in glob.iglob(os.path.join(path, '**/*.py'),recursive=True)
		]
	)
	"""

	return [
		str(Path(filename).resolve())
		for filename in glob.iglob(os.path.join(path, '**/*.py'),recursive=True)
		if include(filename)
	]


@check()
def flatten_list(lyst: list) -> list:
	"""
	The flatten_list function takes a list of lists and returns a single list containing all the items in the original
	list, with sublists replaced by their contents. For example:

	:param lyst:list: Pass a list to the function
	:return: A list of all the items in a nested list
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	if not lyst:
		return []

	big_list = len(lyst) > 1
	if isinstance(lyst[0], list):
		return flatten_list(lyst[0]) + (big_list * flatten_list(lyst[1:]))
	else:
		return [lyst[0]] + (big_list * flatten_list(lyst[1:]))


@check() #Shifted Over to Rust
def compare(regex,
			string,
			starts_with: bool = False,
			strip_start: bool = False,
			open_front: bool = False,
			open_back: bool = False):
	"""
	The compare function takes in a regex and string.
	It returns True if the regex matches the string, or if it is contained within the string.
	The compare function also has optional parameters for whether to match at the beginning of a word, and whether to strip whitespace from both ends of strings before comparing them.

	:param regex: Match the string
	:param string: Compare with the regex parameter
	:param starts_with:bool=False: Determine if the string starts with the regex
	:param strip_start:bool=False: Strip the beginning of a string
	:param open_front:bool=False: Determine if the regex is a prefix to the string
	:param open_back:bool=False: Check if the string is a substring of the regex
	:return: True if the regex is found in the string, false otherwise
	:doc-author: frantzme

	**Verified: SURE**

	Added a ^ and $ to encapsulate the beginning and end of the string
	re.search(regex, str(string).replace('"', '').replace("'", "")) is not None
	"""
	#TODO: Fix the issue here
	try:
		if regex in ['*', string]:
			return True
		not_starts_with, not_ends_with = not str(regex).startswith(
			"*") and not open_front, not str(regex).endswith("*") and not open_back
		return re.search(
			f"{'^' * (not_starts_with and not strip_start)}{regex}{'$' * not_ends_with}",
			string) is not None or (starts_with * string.startswith(regex))
	except Exception as e:
		print(e)
		return False


@check()
def of_list(obj: object, functor=None, group_nodeList=True) -> list:
	"""
	The of_list function creates a list out of an object, and potentially applying a functor.

	:param obj:object: Specify the object to be iterated over
	:param functor=None: Pass a function to the of_list function
	:param group_nodeList=True: Group the nodes in a list
	:return: A list of the object passed in, if it is a list
	:doc-author: frantzme
	**Verified: TRUE**

	Creating a list out of an object, and potentially applying a functor

	@param obj: object (single or list)
	@param functor: function (lambda type)
	@return: list
	"""
	if not functor or functor is None:
		functor = lambda x: x

	if isinstance(obj, list):
		return [functor(x) for x in obj]
	else:
		return [functor(obj)]


@check()
def custom_perm(variants):
	"""
	The custom_perm function takes in a custom input style
	{
	  &quot;debug&quot; : [&quot;on&quot;, &quot;off&quot;],
	  &quot;locale&quot; : [&quot;de_DE&quot;, &quot;en_US&quot;, &quot;fr_FR&quot;]
	}

	:param variants: Specify the different options for each parameter
	:return: A list of dictionaries
	:doc-author: frantzme
	**Verified: TRUE**

	Takes in a custom input style
	https://stackoverflow.com/questions/3873654/combinations-from-dictionary-with-list-values-using-python

	{
	  "debug" : ["on", "off"],
	  "locale" : ["de_DE", "en_US", "fr_FR"]
	}
	==>
	[
		{'debug': 'on', 'locale': 'de_DE'},
		{'debug': 'on', 'locale': 'en_US'},
		{'debug': 'on', 'locale': 'fr_FR'},
		{'debug': 'off', 'locale': 'de_DE'},
		{'debug': 'off', 'locale': 'en_US'},
		{'debug': 'off', 'locale': 'fr_FR'}
	]
	"""
	import itertools as it

	varNames = sorted(variants)
	return [
		dict(zip(varNames, prod))
		for prod in it.product(*(variants[varName] for varName in varNames))
	]


@check()
def to_string(object,
			  prefix: str = None,
			  suffix: str = None,
			  lambd=None) -> str:
	"""
	The to_string function is a helper function that converts an object to a string.
	It takes three arguments: prefix, suffix, and lambd.
	prefix is the text that will be prepended to the output string.
	suffix is the text that will be appended to the output string.
	lambd is a lambda function which can be used for formatting or other purposes.

	:param object: Convert the object to a string
	:param prefix:str=None: Add a prefix to the string
	:param suffix:str=None: Specify a suffix to be added to the end of the string
	:param lambd=None: Pass in a lambda function that can be used for formatting or other purposes
	:return: A string representation of the object
	:doc-author: frantzme
	**Verified: TRUE**
	"""
	if not prefix:
		prefix = ""
	if not suffix:
		suffix = ""
	if not lambd:
		lambd = lambda x: x

	@check()
	def replace_last(string, old, new):
		return new.join(str(string).rsplit(old, 1))

	if isinstance(object, dict):
		output = "{"
		for key, value in object.items():
			output += """{0}\"{1}\"{2}: {3},\n""".format(prefix, lambd(key), suffix,to_string(value, prefix, suffix, lambd))
		output = replace_last(output, ",", "")
		output += "}"
	elif isinstance(object, list):
		output = "["
		for value in object:
			output += f"""{0},\n""".format(to_string(value, prefix, suffix, lambd))
		output = replace_last(output, ",", "")
		output += "]"
	elif hasattr(object, "toDict"):
		output = to_string(object.toDict(), prefix, suffix, lambd)
	elif hasattr(object, "toString"):
		output = object.toString(prefix, suffix, lambd)
	else:
		output = "\"{0}{1}{2}\"".format(prefix, lambd(object), suffix)

	return output