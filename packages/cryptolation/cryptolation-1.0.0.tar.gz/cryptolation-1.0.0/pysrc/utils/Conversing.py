import os, threading

import astroid
from astroid import MANAGER as MGR


#region Src
try:
	from pysrc.utils.utils import safe_get, compare, of_list,check, get_qual_name
	from pysrc.mewn import node_utils
except Exception as e:
	pass
try:
	from utils.utils import safe_get, compare, of_list,check, get_qual_name
	from mewn import node_utils
	#print(e)
except Exception as e:
	pass

#endregion

#https://www.tutorialspoint.com/python3/python_multithreading.htm
#https://stackoverflow.com/questions/19369724/the-right-way-to-limit-maximum-number-of-threads-running-at-once#answer-23524451
class Thread_GetQualName(threading.Thread):
    def run(self, func_node):
        MGR.thread_limit.acquire()
        try:
            func_node.qual_name = get_qual_name(func_node)
        finally:
            MGR.thread_limit.release()

class Thread_GetInference(threading.Thread):
    def run(self, node):
        MGR.thread_limit.acquire()
        try:
            node.infer_values = node_utils.infers(node) #TODO :> Fix This #.inferred()
            #func_node.qual_name = get_qual_name(func_node)
        finally:
            MGR.thread_limit.release()

class translator():
	@check()
	def __str__(self):
		if hasattr(self, 'astroid') and getattr(self, 'astroid',None):
			return self.astroid.as_string()
		else:
			return ''

	#@check()
	def has_call(self, method_name):
		output = []
		for itr, (key, value) in enumerate(self.raw_call_chains.items()):
			if method_name in value:
				cur = self.direct_call_chains[key].parent
				output += [
					#key #:~> [(call, inferred_function)]
					(cur, cur.func.inferred()[0])
				]
		return output

	@check()
	def __init__(self,
				 raw_code_or_file,
				 raw_astroid: astroid.Expr = None,
				 imports=None,
				 globals=None):
		MGR.call_chains = []
		self.raw_call_chains = {}
		self.direct_call_chains = {}
		if raw_astroid:
			self.astroid = raw_astroid
			self.imports = imports
			self.globals = globals
			self.assigns = []
			self.calls = []
			self.expr = []
			self.global_vars = {}
		else:
			"""Loading the code from the var if it's a string or a file
			region Loading Code: raw_code, file_path, file_name"""
			# Maybe Mimic this?
			"""
			https://github.com/zopefoundation/importchecker/blob/master/src/importchecker/importchecker.py
			"""
			if os.path.isfile(raw_code_or_file):
				with open(raw_code_or_file) as foil:
					contents = foil.readlines()
				self.raw_code = ''.join(contents)
				self.currentName = raw_code_or_file
			else:
				self.raw_code = raw_code_or_file
				self.currentName = None

			self.imports = {}
			self.globals = []
			self.calls = []
			self.assigns = []
			self.expr = []
			self.global_vars = {}

			@check()
			def gather_nodes(node):
				"""
				The gather_nodes function is a recursive function that goes through the AST and
				finds all of the global variables, functions, classes, and calls. It also finds
				all imports. The gather_nodes function returns a list of nodes that are either
				global variables or functions.

				:param node: Get the name of the node
				:return: A list of nodes that are in the current file
				:doc-author: frantzme
				**Verified: FALSE**
				"""
				# Restricting the nodes found to only ones in the current file,
				# Astroid goes recursively throughout the imports
				if translator.get_parent(node).name != '':
					return node

				#THREADING
				#https://www.tutorialspoint.com/python/python_multithreading.htm
				#https://www.tutorialspoint.com/the-threading-module-in-python

				try:

					if isinstance(node, astroid.Global):
						self.globals += [node]
						node.targets = {}
						for name in node.names:
							if name in self.global_vars:
								node.targets[name] = self.global_vars[name]
								self.global_vars[name].infer_values = []
								Thread_GetInference().run(self.global_vars[name])

						# TODO: Consider getting a inference yield here
						# Need to track the global variables before the level or scope
						#ASYNC
						#https://www.geeksforgeeks.org/how-to-run-two-async-functions-forever-python/
					elif isinstance(node, astroid.Call):
						# TODO: Get the Qual Name of the Call
						#ASYNC utils.utils.get_qual_name
						#https://www.geeksforgeeks.org/how-to-run-two-async-functions-forever-python/
						node.func.qual_name = None
						Thread_GetQualName().run(node.func)
						node.name = safe_get('name', node, None)
						MGR.call_chains += [
							node
						]
						self.calls += [node]

						def get_call_chain(calld_func: astroid.FunctionDef):
							"""
							TODO:> Performance
							@param calld_func:
							@return:
							"""
							call_chain = [
								calld_func.name
							]
							for func in node_utils.infers(calld_func, option=3):

								for body_node in func.body:
									if isinstance(body_node, astroid.FunctionDef):
										call_chain += get_call_chain(body_node)

							return call_chain

						try:
							if node.func.qual_name.startswith('.') or '.' not in node.func.qual_name:
								node.call_chain = get_call_chain(node.func)
							else:
								node.call_chain = []
						except Exception as e:
							node.call_chain = []
							pass
						node.str_call_chain = ':'.join(node.call_chain)

						if node.str_call_chain != '':
							self.raw_call_chains[node.func.qual_name] = node.str_call_chain
							self.direct_call_chains[node.func.name] = node.func

					elif isinstance(node, astroid.Assign):
						self.assigns += [node]
						if isinstance(node.scope(), astroid.Module):
							for targe in node.targets:
								self.global_vars[targe.name] = targe
					elif isinstance(node, astroid.Expr):
						self.expr += [node]
					else:
						for name in node.names:
							baseName, asName = name[0], ""

							if name[1]:
								asName = name[1]
							else:
								asName = baseName.split('.')[-1]

							modName = safe_get('modname', node)
							if modName:
								baseName = "{0}.{1}".format(modName, baseName)

							self.imports[asName] = baseName

				except Exception as e:
					pass
					#print(e)
					#print(node)

				return node

			for nyode in [
					astroid.Import, astroid.ImportFrom, astroid.Global,
					astroid.Call, astroid.Assign, astroid.Expr
			]:
				MGR.register_transform(nyode, gather_nodes)

			self.astroid = astroid.parse(self.raw_code)
		test = "asdf"

	@check()
	def get_shared_imports(self, rules):
		"""
		The get_shared_imports function takes a dictionary of rules and returns the set of imports that are shared by all rules.
		The get_shared_imports function is used to determine which imports should be included in the generated documentation.

		:param self: Reference the class instance in which the function is being called
		:param rules: Determine which imports to add
		:return: The set of imports that are shared by all the rules
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		if 'smart_imports' in self.imports.keys():
			return rules
		#region Src
		try:
			from pysrc.utils.utils import flatten_list
		except Exception as e:
			pass
		try:
			from utils.utils import flatten_list
		except Exception as e:
			pass
		#endregion
		astroid_shared = set(
			flatten_list([
				list(filter(lambda x: y.startswith(x), rules.keys()))
				for y in self.imports.values()
			]))
		return astroid_shared

	@check()
	def __getitem__(self, itemNumber: int):
		"""
		The __getitem__ function allows the class to be indexed.
		This is useful for iterating over a list of astroid nodes.

		:param self: Access variables that belongs to the class
		:param itemNumber:int: Get the index of the item in the astroid
		:return: The item at the specified index
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		try:
			return self.astroid.body[itemNumber]
		except Exception as e:
			return None

	@check()
	def __call__(self, searchBy):
		"""
		The __call__ function is a special method that allows an object to be called
		as a function. For example, the __call__ method of the class Foo can be used as
		a parameter for the function call Foo(bar). In this case, it will execute the code in __call__

		:param self: Reference the class instance (i
		:param searchBy: Determine what to search for
		:return: The node that matches the searchby value
		:doc-author: frantzme
	**Verified: FALSE**
		"""

		@check()
		def getattr(node):
			"""
			The getattr function is a helper function that returns the line number of
			the node passed to it.  If the searchBy parameter is an integer, then getattr
			returns the line number of that node.  Otherwise, if searchBy is a string, then
			getattr returns what string getattr would return for that node.

			:param node: Get the line number of the node
			:return: The line number of the node
			:doc-author: frantzme
	**Verified: FALSE**
			"""
			if isinstance(searchBy, int):
				return node.lineno
			else:
				return translator.str_node(node)

		@check()
		def node_search(subSearchBy, node):
			"""
			The node_search function is a helper function that searches through the body of
			a node for a specific attribute. It does this by recursively searching through each
			node's body until it finds the desired attribute or reaches an end point. The
			recursive search is necessary because nodes can have multiple children and there
			is no way to know which child contains the desired attribute without checking all of them.

			:param subSearchBy: Search for a specific node in the
			:param node: Search the tree
			:return: The node that matches the searchby value
			:doc-author: frantzme
	**Verified: FALSE**
			"""
			#TODO - Performance HERE
			for nyode in node.body:
				currentAttr = getattr(nyode)
				if (isinstance(searchBy, int) and currentAttr == subSearchBy
					) or (isinstance(searchBy, str) and
						 (currentAttr == subSearchBy or
						  currentAttr.endswith(subSearchBy))):
					return nyode
				elif ((isinstance(searchBy, int) and currentAttr < subSearchBy)
					  or True) and hasattr(nyode, 'body'):
					return node_search(subSearchBy, nyode)
				return None

		return node_search(searchBy, self.astroid)

	@check()
	def search(self,
				search_string: str,
				endsWith: bool = False,
				searchForTarget: bool = False):
		"""
		The search function searches through the file for a specific string.
		It can search for either the name of a function or an expression, and it will return all calls to that function/expression.
		If you want to search for an expression, put '*' before the string (e.g., *print)

		:param self: Access variables that are defined in the class
		:param search_string:str: Search for a string in the function call
		:param endsWith:bool=False: Determine if the search string should be at the end of the call_string
		:param searchForTarget:bool=False: Search for the target of an assignment
		:return: The calls that match the search string
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		output = []
		# region Preparing the search_stringw
		if search_string.startswith("."):
			search_string = search_string.split(".")[-1]
		if search_string.startswith("*."):
			search_string = search_string.split("*.")[-1]
		# endregion

		if not searchForTarget:
			call: astroid.Call
			for call in self.calls:
				# region Creating the call_string
				if safe_get('qual_name', call.func) and safe_get('qual_name', call.func) != "":
					call_string = call.func.qual_name
				else:
					call_string = call.func.as_string().split('(')[0]
					base_name = '.'.join(call_string.split('.')[:-1])

					check_name = (base_name or call_string)
					if check_name in self.imports.keys():
						call_string = "{0}.{1}".format(self.imports[check_name], call_string.split('.')[-1])

				# endregion
				if compare(search_string,call_string,endsWith,open_front=True,open_back=True):
					output += [call]
			expr: astroid.Expr
			for expr in self.expr:
				# region Creating the call_string
				call_string = expr.as_string().split('(')[0]
				base_name = '.'.join(call_string.split('.')[:-1])

				check_name = (base_name or call_string)
				if check_name in self.imports.keys():
					call_string = "{0}.{1}".format(self.imports[check_name], call_string.split('.')[-1])

				# endregion
				if compare(search_string,call_string,endsWith,open_front=True,open_back=True):
					output += [expr]
		else:
			assign: astroid.Assign
			for assign in self.assigns:
				if compare(search_string,assign.value.as_string(),endsWith,open_front=True,open_back=True):
					output += [assign]
					break

				for target in assign.targets:
					call_string = safe_get('name', target) or safe_get(
						'attrname', target)
					if compare(search_string,call_string,endsWith,open_front=True,open_back=True):
						output += [assign]
						break

		return output

	@staticmethod
	@check()
	def get_line_number(node) -> int:
		"""
		The get_line_number function accepts a node as an argument and returns the line number of that node.


		:param node: Get the line number of a node
		:return: The line number of the node
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		return int(node.lineno)

	@staticmethod
	@check()
	def str_node(node):
		"""
		The str_node function is a helper function that returns the string representation of
		a node.  It is used to help with the __str__ method for nodes.

		:param node: Define the node that is being converted to a string
		:return: The string representation of the node
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		return node.as_string()

	@check() #ToRust
	def determine_hierarchy_lvl_to_node(self, node):
		"""
		The determine_hierarchy_lvl_to_node function takes a node as an argument and returns the level of that node in the
		hierarchy. For example, if you pass it a FunctionDef named &quot;foo&quot; which is inside another function called &quot;bar&quot;, it will
		return 2. If you pass it an Assign name=&quot;foo&quot; inside of module foo, it will return 0 because names do not have parents.

		:param self: Reference the class instance in which the function is defined
		:param node: Determine the level of hierarchy
		:return: The level of the node in the hierarchy
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		level, moving_node = 0, node
		while hasattr(moving_node, 'parent'):
			if isinstance(moving_node, astroid.FunctionDef):
				level += 1
			moving_node = moving_node.parent
		return level

	@staticmethod
	@check() #Weary
	def get_parent(compute,custom_stop=None,layersToGo: int = -1, before_module: bool = False) -> astroid.FunctionDef:
		"""
		The get_parent function is used to find the parent of a given node.
		It does this by recursively calling itself until it finds a node that has no parent, or reaches the top of the tree.
		The function takes in three parameters: compute, custom_stop and layersToGo.
		compute is what we are trying to find the parent of; custom_stop is an optional parameter which allows us to specify any class type that we do not want get_parent() to traverse past; and layersToGo specifies how many levels deep into the tree get_parent() should go before returning compute (by default, it goes

		:param compute: Find the parent of a node
		:param custom_stop=None: Stop the search when we reach a certain point
		:param layersToGo:int=-1: Specify how many layers of parents to go up
		:param before_module:bool=False: Stop the recursion when we reach the module that contains
		:return: The parent of the compute
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		if isinstance(compute, astroid.Module):
			return compute
		elif layersToGo == 0:
			return compute
		elif custom_stop and isinstance(compute, custom_stop):
			return compute
		elif safe_get('parent', compute):
			if before_module and isinstance(compute.parent, astroid.Module):
				return compute
			else:
				return translator.get_parent(compute.parent, custom_stop,
											 layersToGo - 1, before_module)
		else:
			return compute

	@check()
	def find_calls(self, method) -> list:
		"""
		The find_calls function takes a method as an input and returns all the calls to that method in the current file.
		The function does this by iterating through every call in self.calls, checking if it is a Call node, then checking if
		the name of the inferred function (i.e., what is returned from node_utils.infers(call)) matches with the name of our
		method parameter.

		:param self: Reference the class instance
		:param method: Check if the method is called on a class or an instance
		:return: A list of tuples, where the first element is the call object and the second element is its inferred function
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		output = []

		method_name = method.name
		check_name = None

		run_debug = False
		if run_debug:
			found = self.has_call(method_name)
			kai = 'd'
			if found:
				return found

		found = self.has_call(method_name)
		if found:
			return found

		call: astroid.Calls
		for call_itr,call in enumerate(self.calls):
			step = 1

			for inferred_function in node_utils.infers(call):
				check_name = safe_get('name', inferred_function) #inferred_function.value if isinstance(inferred_function, astroid.Const) else safe_get('name', inferred_function)
				try:
					method.name
				except Exception as e:
					print('a')
				if check_name == method.name:
					output += [(call, inferred_function)]

		return output

	@staticmethod
	@check()
	def query_back(section_searching, name_looking_for: str):
		"""
		The query_back function is a helper function that searches for the previous node in the AST.
		It takes two arguments, section_searching and name_looking_for. The section_searching argument is
		the current node that we are searching from, and the name_looking for argument is what we are looking
		for in our search.

		:param section_searching: Search for the section of code that
		:param name_looking_for:str: Pass the name of a variable
		:return: The assignment node that is assigned to the name that we are looking for
		:doc-author: frantzme
	**Verified: FALSE**
		"""

		back_node: astroid.Name
		for back_node in of_list(section_searching.previous_sibling()):
			if isinstance(back_node, astroid.Assign):
				if isinstance(name_looking_for, str):
					compare = name_looking_for
				else:
					compare = name_looking_for.value

				if back_node.targets[0].value == compare:
					return back_node
		return None

	@check()
	def expand_function_calls(self, method_string, method):
		"""
		The expand_function_calls function takes a method string and the method itself,
		and returns a list of dictionaries. Each dictionary represents one function call in the
		method, with keys 'func' and 'args'. The value for each key is either an astroid node or
		a list of astroid nodes. For example:

		:param self: Reference the class instance in which the function is being called
		:param method_string: Get the name of the function that is being called
		:param method: Get the function name of the method that is being expanded
		:return: A list of dictionaries
		:doc-author: frantzme
	**Verified: FALSE**

		Returns mapped args and values

		@startuml
		start
		repeat
			:Get current method;
			:Retrieved wrapped arguments;
			:Map the current method to the args;
		repeat while (next method) is (yes)
		->no;
		:Return mapped function to args;
		stop
		@enduml
		http://www.plantuml.com/plantuml/uml/NOwn3i8m34Htli9ZE_03824s9XR-86eE6gbn8iUXvUzfABIqNgoptlcEQ9gaHdJt5II8C8iiSxX0gSaYO2KFROCzhe4RL1oUiDIBYN7SHXxPZtpQa5SJILjitf66ptLq_HccAjIthWDLZE67r-GILI-aUcRt9mwBinJAmkIdClVCZRh09MOTaJJ4MPp1Dllk3G00
		"""
		depth, iterating_func = [], method_string
		for function_call in self.recursively_get_return_graph(method):
			sub_depth = {'func': function_call, 'args': {}}

			keyword: astroid.Keyword
			for keyword in safe_get('keywords', iterating_func, []):
				sub_depth['args'][keyword.arg] = node_utils.infers(keyword.value) #TODO :> Fix This #list(keyword.value.inferred())
			for idx, arg in enumerate(iterating_func.args):
				sub_depth['args']["idx_{0}".format(idx)] = node_utils.infers(arg, strings=True)

			iterating_func = iterating_func.func
			depth += [sub_depth]
		depth.reverse()
		return depth

	@check()
	def recursively_get_return_graph(self, function) -> list:
		"""
		The recursively_get_return_graph function takes a function as an input and returns the return graph of that function.
		The return graph is defined as all functions which are called within the given function, including itself.

		:param self: Reference the object instance of the class that is calling it
		:param function: Store the function that is being analyzed
		:return: A list of function nodes that are the return graph
		:doc-author: frantzme
	**Verified: FALSE**
		Returns the called functions along the chain

		@startuml
		start
		repeat
			:retrieve class name;
			:add class name onto list;
		repeat while (has another class in the chain) is (yes)
		->no more;
		:return class names;
		stop
		@enduml
		#http://www.plantuml.com/plantuml/uml/NOx12eD034Jl_Oevwg4_K47wAy4DxCAQI19R-lUjL7JRkJqcandWAm-okEm0uuNfn4qtux323yPKoHr2Cm-_5vHIOq8b5BLu37z_ySobChfC3XADpBRdYk13c38LwL4StOkzF-BNKHIpMbEypLfDcbu_JGzT3hYpf7MkRm00

		"""

		output = []
		try:
			output += [function]
			while hasattr(function, 'parent') and not isinstance(
					function.parent, astroid.Module):
				function = function.parent
				output += [function]

		except Exception as e:
			pass
		return output

	@staticmethod
	@check()
	def identify_method(tree, looking_for):
		"""
		The identify_method function takes a tree and a method call node as its arguments.
		It then iterates through the body of the tree until it finds the same line number as
		the method call node, and returns that node. If it does not find an identical line number,
		it recursively calls itself on any child nodes with bodies (i.e., functions) to see if they contain
		the desired method call.

		:param tree: Identify the method in which the
		:param looking_for: Find the method that is being called
		:return: The method that is being called
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		lyst = tree.body
		for itr in range(len(lyst)):
			tree_node = lyst[itr]
			if tree_node.lineno == looking_for.lineno:
				return tree_node
			elif tree_node.lineno > looking_for.lineno and hasattr(
					lyst[itr - 1], 'body'):
				return translator.identify_method(lyst[itr - 1], looking_for)
		return None

	@staticmethod
	@check()
	def retrieve_method_type(tree, looking_for=astroid.Call):
		"""
		The retrieve_method_type function is a helper function that takes in an AST node and returns the type of method
		that it is. This function will be used to determine what kind of method we are currently looking at, so that we can
		determine whether or not this method should be considered as a candidate for our test suite.

		:param tree: Retrieve the method type
		:param looking_for=astroid.Call: Specify what type of node we are looking for
		:return: The type of the method that is being called
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		if isinstance(safe_get('value', tree), looking_for):
			return safe_get('value', tree)

		lyst = safe_get('body', tree, [])
		for itr in range(len(lyst)):
			tree_node = lyst[itr]
			if isinstance(tree_node, looking_for):
				return tree_node
			elif hasattr(lyst[itr - 1], 'body'):
				return translator.identify_method(lyst[itr - 1], looking_for)
		return None

	@staticmethod
	@check()
	def new_const(node):
		"""
		The new_const function is a helper function that takes in an astroid node and returns
		a new astroid node with the same value as the input. This is necessary because we are
		modifying the AST to remove all docstrings, which would otherwise be interpreted as nodes.

		:param node: Specify the node that is being visited
		:return: A new node of type 'const' with the value
		:doc-author: frantzme
	**Verified: FALSE**
		"""

		out = astroid.nodes.const_factory(node.value.as_string())
		out.lineno = node.value.lineno
		return out

	@staticmethod
	@check()
	def raw_const(string, lineno=-1):
		"""
		The raw_const function is a helper function that creates an astroid.Const node
		with the given string as its value. The lineno attribute of the Const node is set to -2,
		which will cause it to be excluded from any code coverage reports generated by pytest-cov.

		:param string: Create a new node of the astroid
		:param lineno=-1: Indicate that the line number should be set to -
		:return: A constant node with the value of string
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		out = astroid.nodes.const_factory(string)
		out.lineno = lineno
		return out

	@staticmethod
	@check()
	def new_assignment(target, value):
		"""
		The new_assignment function takes two arguments: a target and a value.
		It returns an Assign node with the given target and value, but it also
		sets the parent of both nodes to be an empty Assign node. This is so that
		the nodes can be used in place of their original versions without having to worry about parents.

		:param target: Specify the variable name that is being assigned to
		:param value: Pass the value of the assignment
		:return: A new assignment node with the target and value nodes as children
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		assign = astroid.nodes.Assign()
		assign.lineno = 0
		name = astroid.nodes.AssignName()
		name.name = target.name
		assign.targets = [name]
		target.parent = assign
		value.parent = assign

		if hasattr(value, 'value'):
			raw_value = value.value
		else:
			raw_value = value

		assign.value = astroid.nodes.const_factory(raw_value)
		return assign

	@staticmethod
	@check()
	def new_assignname(target):
		"""
		The new_assignname function creates a new AssignName object, which is used to represent an assignment target.
		The new_assignname function takes one argument: the name of the variable being assigned to.
		It returns a new AssignName object with default values for all of its properties.

		:param target: Store the name of the variable that is being assigned to
		:return: A new assignname object
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		new_karg = astroid.nodes.AssignName()
		new_karg.lineno = 0
		new_karg.is_function = False
		new_karg.is_lambda = False
		new_karg.is_statement = False
		new_karg.name = target
		return new_karg

	@staticmethod
	@check()
	def setting_context_to_single_function(method, args, depths=[]):
		"""
		The setting_context_to_single_function function takes a function and its arguments,
		and injects the arguments into the function. It also handles nested functions by recursively calling itself.


		:param method: Set the context of the function
		:param args: Set the parameters of the function
		:param depths=[]: Keep track of the depth of recursion
		:return: The method that is
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		@check()
		def clean_body(fn):
			"""
			The clean_body function removes the line numbers from the docstring.
			This is necessary because they are not valid Python syntax, and thus cause
			problems when running doctests.

			:param fn: Pass the function object to be cleaned
			:return: The function body without the docstring
			:doc-author: frantzme
	**Verified: FALSE**
			"""
			idx_to_pop = []
			for itr, linee in enumerate(fn.body):
				lineno = linee.lineno
				if lineno:
					break
				else:
					idx_to_pop += [itr]

			idx_to_pop.reverse()
			for idx in idx_to_pop:
				fn.body.pop(idx)
			return

		clean_body(method)
		node_utils.inject_args(method, args)

		if len(depths) > 0:
			next_layer = depths.pop(0)
			found_function = [
				x for x in method.body if isinstance(x, astroid.FunctionDef) and
				                          x.name == next_layer['func'].name
			][0]

			if found_function and len(next_layer['args']):
				translator.setting_context_to_single_function(found_function,
				                                   next_layer['args'], depths)

		return method

	@staticmethod
	@check()
	def continouous_lookup(node:astroid, string_match):
		"""
		The continouous_lookup function is a helper function for the lookup_attribute function.
		It takes in an astroid node and a string match, and returns the first node that matches
		the string match. If it finds no nodes that match, then it recursively calls itself on
		the func attribute of the given node.

		:param node:astroid: Traverse the ast
		:param string_match: Match the name of the function
		:return: The node that contains the string_match
		:doc-author: frantzme
	**Verified: FALSE**
		"""
		if safe_get('attrname', node) == string_match \
			or safe_get('name', node) == string_match \
			or safe_get('attrname', node) in string_match:
			return node
		elif hasattr(node, 'expr') and hasattr(node.expr, 'func'):
			return translator.continouous_lookup(node.expr.func, string_match)
		else:
			return None
