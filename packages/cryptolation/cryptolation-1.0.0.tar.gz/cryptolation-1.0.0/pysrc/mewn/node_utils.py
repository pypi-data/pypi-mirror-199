from typing import Tuple
import astroid
from astroid import MANAGER as MGR
MGR.not_specific = set()
MGR.specific = set()
#region Src
try:
	from pysrc.utils.utils import custom_perm, safe_get, chain_get
	from pysrc.utils.utils import check, to_bool
except Exception as e:
	pass

try:
	from utils.utils import custom_perm, safe_get, chain_get
	from utils.utils import check, to_bool
except Exception as e:
	pass

#endregion

"""
# A check to see if the node is a call node and if it is, it will return the node's function
file:///Users/maister/Projects/CryptoGuard4Py/pysrc/mewn/node_utils.py:25
"""

@check()
def get_pretty_infer_names_base(node: astroid.Expr, filter_name: str = 'builtins'):

	return [
		x.pytype()
		for x in infers(node) #TODO :> Fix This #node.inferred()
		if not str(x.pytype()).startswith(filter_name) # and not is_uninferable(x)
	]

class cur_store:
	@check()
	def __init__(self):
		"""
		The __init__ function initializes the class. It creates a dictionary called
		variables and stores it in the instance of this class. The variables dictionary
		is used to store all variables that are defined within a program, as well as any
		values they may take on.

		:param self: Refer to the object itself
		:return: Nothing
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		self.variables = {}
		self.functions = {}

	@check()
	def _store(self, obj, func=False):
		"""
		The _store function is a helper function that stores the given object in
		either the functions or variables dictionary. It returns an integer value
		representing its location in either of those dictionaries.

		:param self: Access the class' attributes and methods
		:param obj: Store the object that is being stored
		:param func=False: Determine whether the object being stored is a function or variable
		:return: The index of the object that is being stored
		:doc-author: frantzme
	**Verified: FALSE**aw
		"""
		if func:
			self.functions[str(len(self.functions.keys()))] = obj
			return int(len(self.functions) - 1)
		else:
			self.variables[str(len(self.variables.keys()))] = obj
			return int(len(self.variables) - 1)

	@check()
	def __call__(self, searchBy: int = None, func=False):
		"""
		The __call__ function allows the class to be called as a function.
		This is useful for when you want to call an instance of the class and get either
		the functions or variables dictionary back, depending on whether you pass in True or False.


		:param self: Access variables that belongs to the class
		:param searchBy:int=None: Determine if the user is searching for a function or variable
		:param func=False: Determine whether the function should return a list of variables or functions
		:return: The value of the variable or function
		:doc-author: frantzme
		**Verified: FALSE**
		"""
		if searchBy is None:
			return self.functions if func else self.variables
		elif func and str(searchBy) in self.functions:
			return self.functions[str(searchBy)]
		elif not func and str(searchBy) in self.variables:
			return self.variables[str(searchBy)]
		return None

@check()
def full_context_from_method_chain(depth) -> Tuple[list, list]:
	"""
	The full_context_from_method_chain function is a function that takes in a list of dictionaries,
	and returns two lists. The first list contains the context for each layer of permutations, and the second
	list contains details about each layer. This function is used to generate all possible permutations from
	a method chain.

	:param depth: Determine how many layers deep the function chain is
	:return: A tuple of two lists
	:doc-author: frantzme
	**Verified: FALSE**s
	"""

	try:
		from pysrc.utils.Conversing import translator
	except Exception as e:
		pass
	try:
		from utils.Conversing import translator
	except Exception as e:
		pass

	from copy import deepcopy as dc

	store = cur_store()
	import collections
	full_args = collections.defaultdict(set)
	"""
	This next section is about computing the complicated different amount of permutations
	region perms: arg_permutations
	"""
	try:
		for function in depth:
			function['func'] = str(store._store(function['func'], func=True))
			if len(function['args']) > 0:
				for arg_key, arg_value in function['args'].items():
					full_args["{0}:{1}".format(function['func'], arg_key)] = []
					for x in arg_value:
						full_args["{0}:{1}".format(function['func'], arg_key)].append(str(store._store(x)))
			else:
				full_args["{0}:_None".format(function['func'])] = [None]

	except: pass

	perm_layers, context, details = custom_perm(full_args), [], []

	for perm_layer_itr,perm_layer in enumerate(perm_layers):
		layer_details, top_layer = [], None
		for function_idx, function in enumerate(store(func=True)):
			str_function_idx, layer_func = str(function_idx) + ":", {}
			perm_layer_variables = [
				x.replace(str_function_idx, '')
				for x in perm_layer.keys()
				if x.startswith(str_function_idx)
			]

			layer_func['func'] = store(function_idx, func=True)
			layer_func['args'] = {}

			for key in perm_layer_variables:
				if 'None' not in key:
					full_key = "{0}{1}".format(str_function_idx, key)
					temp_erooni = store(perm_layer[full_key])
					layer_func['args'][key] = store(perm_layer[full_key])

			if top_layer is None:
				top_layer = {'func': layer_func['func'], 'args': layer_func['args']}

			layer_details += [layer_func]
		details += [layer_details]

		context += [
			translator.setting_context_to_single_function(top_layer['func'],
											   top_layer['args'],
											   dc(layer_details)[1:])
		]

	return (context, details)

@check()
def inject_args(fn: astroid.nodes.FunctionDef, args_list: list):
	"""
	The inject_args function takes a function definition and a dictionary of arguments to be injected into the function.
	It then creates new variables for each argument, assigns them their values, and inserts them into the beginning of the body
	of the given function. This allows us to inject arguments without having to modify any other code in this file.

	:param fn:astroid.nodes.FunctionDef: Get the name of the function
	:param args_list:list: Pass a list of arguments to inject into the function
	:return: A function definition with the arguments of
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	try:
		from pysrc.utils.Conversing import translator
	except Exception as e:
		pass
	try:
		from utils.Conversing import translator
	except Exception as e:
		pass

	for name, arg in args_list.items():
		if name.startswith("idx_"):
			og_target = fn.args.args[int(name.replace("idx_", ''))]
		else:
			og_target = [x for x in fn.args.args if x.name == name][0]

		og_value = arg
		from copy import deepcopy as dc

		if isinstance(og_target, str):
			target = translator.new_assignname()
		else:
			target = dc(og_target)

		assignment = translator.new_assignment(target, dc(og_value))
		fn.body.insert(0, assignment)
		assignment.parent = fn
		fn.set_local(target.name, target)

	return

@check()
def retrieve_specific_body(node: astroid.Call, string_match):
	"""
	The retrieve_specific_body function is a helper function that retrieves the body of a specific node.
	It does this by traversing through the tree and finding all nodes with an as_string value that contains
	the string match. It then returns the first one it finds.
	
	:param node:astroid.Call: Retrieve the body of a function
	:param string_match: Determine which function to retrieve
	:return: The body of a function call
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	try:
		from pysrc.utils.Conversing import translator
	except Exception as e:
		pass
	try:
		from utils.Conversing import translator
	except Exception as e:
		pass

	if hasattr(node, 'value'):
		node = node.value
	elif isinstance(node, astroid.With):
		node = node.items[0][0]
	if string_match not in node.as_string():
		suffix = '.' + '.'.join(node.as_string().split('.')[1:])
		if not any([
				string_match in str(x + suffix)
				for x in get_pretty_infer_names_base(
					chain_get('func.expr'.split('.'), node, True)) or []
		]):
			return None

	if isinstance(safe_get('func', node), astroid.Name) \
		and isinstance(node, astroid.Call) \
		and len(safe_get('args', node, [])) == 1:

		return retrieve_specific_body(node.args[0], string_match)

	elif hasattr(node, 'func'):

		return translator.continuous_lookup(node.func, string_match)
	return None


@check()
def get_args(node) -> dict:
	"""
	The get_args function takes a node as input and returns a dictionary of the arguments passed to that function.
	The get_args function is used by the get_caller_info function to extract information about what functions are being called.

	:param node: Infer the value of a node
	:return: A dictionary of the arguments and their values
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	output = {}
	try:
		if hasattr(node, 'value'):
			node.args = node.value.args
			node.keywords = node.value.keywords

		if isinstance(node, (astroid.Attribute, astroid.Name)):
			node.args = node.parent.args
			node.keywords = node.parent.keywords

		elif isinstance(node, astroid.nodes.AssignName):
			node.args = []
			raw = type('', (), {})()
			raw.arg = node.name
			raw.value = node.parent.value
			node.keywords = [raw]

		if node.args:
			for itr, arg in enumerate(node.args):
				output["_raw_argument_{0}".format(itr)] = infer_value(arg)
		if node.keywords:
			for keyword in node.keywords:
				output[keyword.arg] = infer_value(keyword)

	except: pass
	return output


@check()
def infer_value(node) -> list:
	"""
	The infer_value function takes a node and returns a list of values that are inferred from the node.
	The infer_value function is called by the infer_node function, which passes in each AST node to be evaluated.
	If the value of an AST Node can not be inferred, it will return an Unknown object.

	:param node: Infer the value of a variable
	:return: A list of values that are inferred from the given node
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	try:
		from pysrc.utils.Conversing import translator
	except Exception as e:
		pass
	try:
		from utils.Conversing import translator
	except Exception as e:
		pass

	output = []
	if False and safe_get('qual_name', node):
		output += [
			safe_get('qual_name', node)
		]

	try:
		if not hasattr(node, 'value'):
			output += [
				node.as_string() if is_uninferable(x) else x
				for x in infers(node) #TODO :> Fix This #node.inferred()
			]
		if isinstance(node.value, astroid.Call):
			output += [translator.new_const(node)]
		elif isinstance(node.value, astroid.nodes.Const):
			output += [node.value]
		elif isinstance(node, astroid.nodes.Const):
			output += [node]
		elif isinstance(node.value, astroid.nodes.Dict):
			for temp_key, temp_value in node.value.items:
				for temp_value_infer in infers(temp_value): #TODO :> Fix This #temp_value.inferred():
					output += [{
						temp_key, temp_value_infer
					}]
		else:
			inferred_values = list(node.value.ilookup(node.value.name))
			raw_values = list(node.value.lookup(node.value.name)[1])
			output += [
				infer if not is_uninferable(infer) else translator.new_const(raw.parent)
				for infer, raw in zip(inferred_values, raw_values)
			]

	except astroid.exceptions.NameInferenceError as e:
		output += [astroid.Unknown]
	except astroid.exceptions.InferenceError as e:
		output += [node.as_string()]
	except AttributeError as e:
		try:
			output += infers(node.value) #TODO :> Fix This #list(node.value.inferred())
		except Exception as e:
			output += [node.arg]
	except Exception as e:
		pass

	return output

#@check()
def infers(arg, strings=False, option=1): #TODO :> Fix This #arg.inferred():
	if option == 1:
		try:
			return old_infers(arg, strings)
		except Exception as e:
			return []

	output = None
	try:
		base = old_infers(arg, strings)
	except Exception as e:
		pass

	try:
		new_one = new_infers(arg, strings)
	except Exception as e:
		pass

	try:
		new_two = new_two_infers(arg, strings)
	except Exception as e:
		pass

	if option is None or option == 1:
		output = base
	if option == 2:
		output = new_one
	if option == 3:
		output = new_two

	step = 'a'
	return output

#@check()
def new_infers(arg, strings=False):
	"""
	The infers function is a helper function that takes in an argument and returns the inferred value of that argument.
	It does this by iterating through all the possible values of an argument, and returning a list containing all those values.
	If it encounters any type other than astroid.nodes.Call or astroid.Instance, it will return a list containing only itself.

	Filter based on:
		* __Filter based on .pytype() != startswith builtins__
		* Filter based on parent is Module?

	:param arg: Get the name of the function
	:return: The inferred value of a node
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	#region SrcImport
	try:
		from pysrc.utils.Conversing import translator
	except Exception as e:
		pass
	try:
		from utils.Conversing import translator
	except Exception as e:
		pass
	#endregion

	output = set()

	if safe_get('qual_name', arg):
		output.add(translator.raw_const(safe_get('qual_name', arg))) #output.add(safe_get('qual_name', arg) if strings else translator.raw_const(safe_get('qual_name', arg)))

	if isinstance(arg, astroid.nodes.Call):
		output |= set(new_infers(arg.func, strings))
# value.parent.name.lower() not in ['', 'builtins', 'collections'] #TEMP
	if arg.__class__.__name__ != "Instance" and translator.get_parent(arg, custom_stop=astroid.Module).name.lower() not in ["builtins", "collections"]:
		try:
			for value in arg.inferred():
				if not is_uninferable(value) and translator.get_parent(value, custom_stop=astroid.Module).name.lower() in [ "builtins", "collections"]:
					MGR.not_specific.add("{0}.{1}".format(value.parent.name, value.name))
					hai = 0o1_1201
				if not is_uninferable(value): # and chain_get("parent.__class__.__name__".split('.'), value) != "Module":
					temp_ = chain_get("parent.__class__.__name__".split('.'), value) #TEMP
					temp__ = value.parent.name #TEMPwd
					qual_name = "{0}.{1}".format(value.parent.name, value.name) #TEMP
					MGR.specific.add(qual_name)
					output.add(
						translator.raw_const("{0}.{1}".format(value.parent.name, value.name)) #"{0}.{1}".format(value.parent.name, value.name) if strings else value
					)
		except Exception as e:
			for value in arg.inferred():
				print(value)
				a = '1'
			pass
	else:
		test = 1 #TODO Fix This

	return list(output)

#@check() #TODO :> NOTE:> This should be created and used in the future
def old_infers(arg, strings=False):
	"""
	The infers function is a helper function that takes in an argument and returns the inferred value of that argument.
	It does this by iterating through all the possible values of an argument, and returning a list containing all those values.
	If it encounters any type other than astroid.nodes.Call or astroid.Instance, it will return a list containing only itself.

	Filter based on:
		* __Filter based on .pytype() != startswith builtins__
		* Filter based on parent is Module?

	:param arg: Get the name of the function
	:return: The inferred value of a node
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	#region SrcImport
	try:
		from pysrc.utils.Conversing import translator
	except Exception as e:
		pass
	try:
		from utils.Conversing import translator
	except Exception as e:
		pass
	#endregion
	output = []
	if safe_get('qual_name', arg):
		output += [
			translator.raw_const(safe_get('qual_name', arg))
		]

	if isinstance(arg, astroid.nodes.Call):
		return old_infers(arg.func)

	if arg.__class__.__name__ != "Instance":
		for value in arg.inferred():
			if not is_uninferable(value):
				output += [value]
	else:
		test = 1 #TODO Fix This

	return output

#@check() #TODO :> NOTE:> This should be created and used in the future
def new_two_infers(arg, strings=False):
	"""
	The infers function is a helper function that takes in an argument and returns the inferred value of that argument.
	It does this by iterating through all the possible values of an argument, and returning a list containing all those values.
	If it encounters any type other than astroid.nodes.Call or astroid.Instance, it will return a list containing only itself.

	Filter based on:
		* __Filter based on .pytype() != startswith builtins__
		* Filter based on parent is Module?

	:param arg: Get the name of the function
	:return: The inferred value of a node
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	#region SrcImport
	try:
		from pysrc.utils.Conversing import translator
	except Exception as e:
		pass
	try:
		from utils.Conversing import translator
	except Exception as e:
		pass
	#endregion
	output = []
	if safe_get('qual_name', arg) and False:
		output += [
			translator.raw_const(safe_get('qual_name', arg))
		]

	if isinstance(arg, astroid.nodes.Call):
		return new_two_infers(arg.func)

	if arg.__class__.__name__ != "Instance":
		for value in arg.inferred():
			if not is_uninferable(value):
				output += [value]
	else:
		test = 1 #TODO Fix This

	return output


@check()
def is_uninferable(node) -> bool:
	"""
	The is_uninferable function checks whether or not the result from an Astroid's inferred value is uninferable.
	For example, if a variable has no assigned value, then it will be inferred as an Uninferable object.

	**Verified: TRUE**

	:param node: Check if the inferred value is a list or not
	:return: True if the inferred value is an instance of either unknown or uninferable
	:doc-author: Trelent

	A check whether or not the result from an Astroid's inferred value is uninferable

	:param node: an Astroid Node
	:return: bool
	"""
	return isinstance(node, (astroid.Unknown, astroid.Uninferable.__class__))
