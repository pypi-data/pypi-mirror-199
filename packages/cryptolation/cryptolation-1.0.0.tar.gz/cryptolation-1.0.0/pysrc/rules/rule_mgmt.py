import sys, astroid, hugg
import funbelts as ut #ephfile
from astroid import MANAGER as MGR

try:
	import pysrc.rules.rule_source as ru
	from pysrc.utils.utils import check,retrieve_files
	from pysrc.mewn.node_utils import get_args, full_context_from_method_chain, is_uninferable, retrieve_specific_body
	from pysrc.mewn import node_utils
	from pysrc.output_routing import vuln, management
	from pysrc.output_routing.maping import map_results_to_output
	from pysrc.output_routing.base_structure import file_scan_struct, Structure
	from pysrc.utils import Conversing
	from pysrc.utils.Conversing import translator
	from pysrc.utils.utils import retrieve_files, of_list, safe_get, get_fully_qualified_name_curry, new_match, flatten_list, \
	compare, set_key_values_for_dict
except Exception as e:
	import rules.rule_source as ru
	from mewn.node_utils import get_args, full_context_from_method_chain, is_uninferable, retrieve_specific_body
	from mewn import node_utils
	from output_routing import vuln
	from output_routing.maping import map_results_to_output
	from output_routing.base_structure import file_scan_struct, Structure
	from output_routing.structures import management
	from utils import Conversing
	from utils.Conversing import translator
	from utils.utils import check,retrieve_files
	from utils.utils import retrieve_files, of_list, safe_get, get_fully_qualified_name_curry, new_match, flatten_list, \
	 compare, set_key_values_for_dict

def log(string):
	#print(string)
	t = 1

@check()
def search(overlord, file, rules=None, secure_values=None) -> None:
	"""
	The search function is responsible for searching the AST of a file for
	specific imports and then evaluating those imports to see if they are secure.


	:param overlord: Access the global variables
	:param file: Get the file name of the current file being
	:param rules=None: Pass in the rules
	:param secure_values=None: Pass the secure values to the
	:return: A list of results
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	MGR.stage = 'START'
	#log("Starting search")
	#with ut.ephfile(hugg.face("frantzme/prypi","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")['armageddon.zip']) as eph:
	with file_scan_struct(overlord, file) as file_reader:
		#log("Starting file reader")
		try:
			#log("Starting file reader try")
			tree = Conversing.translator(file)

			#sys.path.insert(0,eph())
			#from armageddon.src.independence import tree as tree_two

			#try:
			#	new_tree = tree_two(file)
			#except Exception as e:
			#	pass

			#log("Starting file reader try 2")
			shared = set(tree.get_shared_imports(rules))
			#log("Shared imports: {0}".format(shared))
			for import_name in set(tree.get_shared_imports(rules)):
				#log("Starting import name: {0}".format(import_name))
				imports = file_reader.imports(tree.imports)
				#log("Imports: {0}".format(imports))
				_get_qual = get_fully_qualified_name_curry(import_name)
				#log("Get qual: {0}".format(_get_qual))

				for lib in rules[import_name]:
					#log("Starting lib: {0}".format(lib))
					MGR.stage = 'TRACKING'
					file_fully_qualified_name = new_match(_get_qual(lib, True, False), imports)
					#log("File fully qualified name: {0}".format(file_fully_qualified_name))
					if file_fully_qualified_name:

						found_nodes = []
						try:
							#log("Starting file fully qualified name try")
							found_nodes = tree.search(
								lib['target'] if 'target' in lib else _get_qual(
									lib, True, 'target' not in lib),
								endsWith='builder' in lib,
								searchForTarget='target' in lib)
						except Exception as e:
							pass

						for found_node in found_nodes:
							#log("Starting found node: {0}".format(found_node))
							prep_string = f"the library {_get_qual(lib, True)} @ line:{found_node.lineno}"
							#log("Prep string: {0}".format(prep_string))
							lib['imports'] = import_name
							rule_num = lib['group']
							msg, name, severity = ru.unwravel(rule_num)

							#log("Starting found node try")
							map_results = lambda results=None,context_lambda=None: map_results_to_output(
									file_reader=file_reader,
									file_fully_qualified_name=
									file_fully_qualified_name,
									prep_string=prep_string,
									message="Using {0}".format(prep_string),
									file=file,
									msg=msg,
									name=name,
									context_lambda=context_lambda,
									rule_num=rule_num,
									severity=severity,
									line=found_node.lineno,
									found_node=found_node,
									results=results)

							if 'arguments' in lib and 'target' not in lib:
								#log("Starting found node try 2")
								handle_arguments(tree, found_node, lib,
												 secure_values, prep_string,
												 file_reader,
												 file_fully_qualified_name,
												 file, name, msg, rule_num,
												 severity)
							elif 'target' in lib and lib['criteria'] == '*':
								#log("Starting found node try 3")
								map_results()
							elif 'target' in lib:
								#log("Starting found node try 4")
								try:
									for target in of_list(found_node.targets):
										#log("Starting target: {0}".format(target))
										if hasattr(target, 'expr'):
											create = lambda pytype: "{0}.{1}".format(pytype, target.attrname)
											if any([
													compare(
														lib['criteria'],
														qual_name)
													for qual_name in of_list([
														str(x.pytype()) for x in
														node_utils.infers(target.expr) #TODO :> Fix This #target.expr.inferred()
													], create)
											]):
												#log("Starting target try")
												map_results()

										elif isinstance(target.parent,
														astroid.nodes.Assign):
											results = evaluate_conditions(
												tree, target, lib,
												secure_values)
											if results:

												@check()
												def context_lambda():
													return results

												#log("Starting target try 2")
												map_results(
													results=results,
													context_lambda=context_lambda
												)

								except Exception as e:
									print(e)
									pass
							else:
								#log("Starting found node try 5")
								map_results()
		except Exception as e:
			print(e)
			pass
	return


@check()
def handle_arguments(tree, found_node, lib, secure_values, prep_string,
					 file_reader, file_fully_qualified_name, file, name, msg, rule_num, severity):
	"""
	The handle_arguments function is responsible for evaluating the conditions of a given
	node. It does this by first determining if the node has any children, and then iterating
	through each child to determine if it is a callable method. If it is, we evaluate the
	conditions of that method using our evaluate_conditions function. We then pass those results
	to map_results_to_output which will handle writing them out to file.

	:param tree: Search for the found_node within the tree
	:param found_node: Determine the hierarchy level of the node
	:param lib: Check if the found value is a secure value
	:param secure_values: Determine the values that are considered secure
	:param prep_string: Determine the type of string that is being evaluated
	:param file_reader: Read the file and get the contents
	:param file_fully_qualified_name: Determine if the file is a library or not
	:param file: Determine the file name for the output
	:param name: Identify the rule that was triggered
	:param msg: Pass in the message to be displayed
	:param rule_num: Identify which rule is currently being evaluated
	:param severity: Determine the severity of a violation
	:return: The results of the evaluation of conditions
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	if tree.determine_hierarchy_lvl_to_node(found_node) == 0:
		results = evaluate_conditions(tree, found_node, lib, secure_values)
		if results:

			@check()
			def context_lambda():
				return results

			map_results_to_output(file_reader, file_fully_qualified_name, prep_string, results, file, found_node, msg,
				name, context_lambda, rule_num, severity)
	else:
		#print(tree.currentName)
		#with open("lookingfor.txt", "a+") as f:
		#	f.write("{0}\n".format(tree.currentName))s
		#TODO :> Problematic Here
		parent_def = tree.get_parent(found_node, astroid.FunctionDef)
		"""TODO - Performance multi-thread this?"""
		for (discovered, discovered_method) in tree.find_calls(parent_def):

			expanded_calls = tree.expand_function_calls(discovered, discovered_method)
			(context_runs, context_details) = full_context_from_method_chain(expanded_calls)

			for context, details in zip(context_runs, context_details):
				"""
				#TODO: Fix This
				Put in line search for found value in context
				identify found_node from within context, pass it to evaluate conditions
				"""
				identified_node = tree.identify_method(context, found_node)
				get_callable_method = tree.retrieve_method_type(identified_node)
				results = evaluate_conditions(context, get_callable_method, lib, secure_values)
				#TODO :> Problematic Here

				@check()
				def context_lambda():
					context_detail = {}
					for method_context in details: #TODO: Issue with pulling the func information
						try:
							method_context_func_name = method_context['func'].split(':')[1]
						except:
							method_context_func_name = str(method_context['func'])
						for method_context_value in method_context['args'].values():
							(name, _raw_value_) = method_context_value
							if method_context_func_name not in context_detail:
								context_detail[method_context_func_name] = {name.name: _raw_value_.value}
							else:
								context_detail[method_context_func_name][name.name] = _raw_value_.value
					return context_detail

				map_results_to_output(
					file_reader,
					file_fully_qualified_name,
					prep_string,
					results,
					file,
					found_node,
					msg,
					name,
					context_lambda,
					rule_num,
					severity
				)

@check()
def loop_thru_args(lib, argz, arg_name, secure_values, value_comprehension,pretty_comprehension, is_target_check,inner_value_loop) -> dict:
	"""
	The loop_thru_args function is the main function of this script. It loops through all arguments in a library and checks if they are valid according to the rules specified in the 'arguments' section of each library. If an argument is invalid, it returns a dictionary with two keys:
	&quot;error&quot;: The error message that will be displayed to users when this argument fails validation
	&quot;arg_name&quot;: The name of the argument that failed validation

	:param lib: Store the results of the loop_thru_args function
	:param argz: Get the argument values from the argz function
	:param arg_name: Determine which argument to verify
	:param secure_values: Determine if the value is secure or not
	:param value_comprehension: Define the way in which a value is to be verified
	:param pretty_comprehension: Make the output of this function more readable
	:param is_target_check: Determine if the value is being checked against a target
	:param inner_value_loop: Loop through the values of a list or dictionary
	:return: A dictionary containing the following:
	:doc-author: frantzme
	**Verified: FALSE**
	"""

	for verify in lib['arguments']:#May be able to make this query? instead of just looping????
		verify['pretty_comp'] = pretty_comprehension
		verify['value_comp'] = value_comprehension
		verify['target_check'] = is_target_check
		verify['inner_loop'] = inner_value_loop
		verify['to_verify'] = lambda working_value: ru.rule_check(verify, value_comprehension(working_value),secure_values)

		includes, verify['live_type'] = True, verify['type']
		if verify['live_type'].startswith('include'):
			includes = False
			verify['live_type'] = verify['live_type'].split('_')[-1]

		for idx, (arg_key, arg_values) in enumerate(argz().items()): #NOTE: From here this solely starts to iterate: BREAKONE
			temp_out = verify_arg_new(idx,arg_key,arg_values,includes,verify)
			if temp_out:
				return temp_out

	return {}

def verify_arg_new(arg_index:int, arg_name:str, arg_values:list,includes:bool,verify:dict,fromdict:bool=False):
	"""
	The verify_arg_new function is a helper function that verifies the value of an argument.
	It takes in a list of arguments, and then checks to see if the argument name matches any of the names in verify_arg_new's dictionary.
	If it does match, then it will check to see if there are any dictionaries within arg_values (the values passed into verify_arg).
	If there are dictionaries, then we iterate through them and check each key/value pair for correctness. If they aren't correct,
	then we return an error string with information about what went wrong.

	:param arg_index:int: Check if the variable is in the list of arguments
	:param arg_name:str: Check if the argument is included in the verify_arg function
	:param arg_values:list: Pass the values of the argument
	:param includes:bool: Check if the variable is included in the verify dict
	:param verify:dict: Verify the type of a variable
	:param fromdict:bool=False: Check if the dict is being used as a dictionary or not
	:return: A dictionary with the following keys:
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	if not includes and (arg_name == verify.get('name', None)) or (arg_index == verify.get('index', None)):
		includes = True
	if verify['target_check'](arg_name, verify,fromdict):
		for arg_value in of_list(arg_values):
			if isinstance(arg_value, astroid.Dict):
				for dict_key,dict_value in set_key_values_for_dict(arg_value).items():
					temp_value = verify_arg_new(arg_index, dict_key, dict_value, includes, verify,True)
					if temp_value:
						return temp_value
			else: #Not Dict
				for val in verify['inner_loop'](arg_value):
					working_value = arg_name if arg_value is None else val
					if not is_uninferable(working_value):
						error_string = verify['to_verify'](working_value)
						if error_string:
							return {
								'Error String':error_string,
								'Variable Name':verify['pretty_comp'](arg_name),
								'Inferred Variable Value':arg_value or verify['value_comp'](working_value)
							}
					if not includes:
						return {
							'Error String': "Variable is not included and the Inferred value is not set",
							'Variable Name': verify['pretty_comp'](safe_get('name', verify)),
							'Inferred Variable Value': "Variable should be set to {0}".format(verify['type'])
						}

	return None

@check()
def evaluate_conditions(tree, found_node, lib: dict,
						secure_values) -> list:
	"""
	The evaluate_conditions function is a function that takes in a node and returns
	a list of dictionaries. Each dictionary contains the following keys:

	:param tree: Get the node that is being evaluated
	:param found_node: Check if the node is a target
	:param lib:dict: Pass in the dictionary of values that
	:param secure_values: Prevent the loop_thru_args function
	:return: What?
	:doc-author: frantzme
	**Verified: FALSE**
	"""
	if found_node is None:
		return []

	import astroid
	output = []

	if isinstance(safe_get('value', found_node), astroid.node_classes.Name):

		temp_output = loop_thru_args( lib=lib,
			argz=lambda: {value: None for value in node_utils.infers(found_node.value)}, #TODO :> Fix This #found_node.value.inferred()},
			arg_name=lambda arg_name_value: found_node.value,
			secure_values=secure_values, value_comprehension=lambda raw_value: raw_value.qname(),
			pretty_comprehension=lambda founded_node: found_node.value.as_string(),
			is_target_check=lambda x, y: True, inner_value_loop=lambda value: [value])
		if temp_output:
			output += [temp_output]

	else:

		if lib['criteria'] == '*':
			arguments = get_args(found_node)
		else:
			if safe_get('args', found_node):
				arguments = get_args(found_node)
			else:
				arguments = get_args(retrieve_specific_body(found_node, lib['criteria']))

		@check()
		def is_target(arg_name, verify, fromdict=False) -> bool:
			"""
			Returns interesting logic if the argument is being targeted.

			* First Case
			is_index : if the argument didn't have a name

			and

			('index' not in verify): the rule doesn't specify a specific variable

			or

			('index' in verify and verify['index'] == int(name):
			the rule specifies this specific variable (i.e. the 3rd variable)

			* Second Case

			('name' in verify and verify['name'] == name): The name (id) of the
			variable matches the argument name specified by the rule

			@return: bool
			"""

			name = arg_name.replace('_raw_argument_', '')
			if not fromdict and safe_get('dict', verify) is not None:
				return (arg_name.startswith('_raw_argument') and
				 (('dict_index' in verify and verify['dict_index'] == int(name)))) or (
						'dict_name' in verify and verify['dict_name'] == name)
			else:
				return (arg_name.startswith('_raw_argument') and
					(('index' in verify and verify['index'] == int(name)))) or (
						'name' in verify and verify['name'] == name)

		@check()
		def inner_loop(arg_value):

			if isinstance(arg_value, astroid.ClassDef):
				output = arg_value.name
				rent = safe_get('parent', arg_value)
				if rent:
					output = rent.name + "." + output
				return output
			if hasattr(arg_value, 'value'):
				return str(arg_value.value).split("(")[0]
			elif hasattr(arg_value, 'pytype'):
				return arg_value.pytype()
			else:
				return arg_value

		temp_output = loop_thru_args(lib=lib,argz=lambda: arguments,arg_name=lambda arg_key: arg_key,
			secure_values=secure_values,value_comprehension=lambda working_value: working_value,
			pretty_comprehension=lambda arg_key: arg_key,is_target_check=is_target,
			inner_value_loop=lambda arg_value_value:[inner_loop(x) for x in of_list(arg_value_value) if x is not None])
		if temp_output:
			output += [temp_output]

	return output
