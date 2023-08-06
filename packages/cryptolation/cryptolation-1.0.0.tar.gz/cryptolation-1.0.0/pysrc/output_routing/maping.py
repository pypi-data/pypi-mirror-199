try:
	from pysrc.utils.utils import check
	from pysrc.output_routing import vuln
except Exception as e:
	from utils.utils import check
	from output_routing import vuln

@check()
def map_results_to_output(file_reader, file_fully_qualified_name, prep_string, results, file, found_node, msg, name,
						  context_lambda, rule_num, severity, message=None, line: int = None):

	if context_lambda is None:
		def context_lambda():
			return None

	file_reader += vuln.Klass(
		type=file_fully_qualified_name,
		message=message if message is not None else ''.join([line['Error String'] for line in results]) + "Using {0}".format(prep_string),
		file=file,
		line=line if line is not None else found_node.lineno,
		matched=msg,
		rule=name,
		rule_num=rule_num,
		severity=severity,
		context=context_lambda()
	)