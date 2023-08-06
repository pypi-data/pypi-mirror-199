# region Src
import os.path, sys, imp

try:
	from pysrc.output_routing.base_structure import Structure, file_scan_struct, fancy_date
	from pysrc.output_routing import vuln
	from pysrc.utils import utils
except:
	pass
try:
	from output_routing.base_structure import Structure, file_scan_struct, fancy_date
	from output_routing import vuln
	from utils import utils
except Exception as e:
	#print(e)
	pass
try:
	from pysrc.utils.utils import check
except Exception as e:
	print("Failure to import cryptoguard4py: {0}".format(e))
	pass
try:
	from utils.utils import check
except Exception as e:
	print("Failure to import from non-src: {0}".format(e))
	pass

# endregion


@check()
def get_structure(type: str = "csv"):
	if os.path.isfile(type):
		mymodule = imp.new_module('userprovided')
		with open(type, 'r') as f:
			exec('\n'.join(f.readlines()), mymodule.__dict__)
		sys.modules['userprovided'] = mymodule
		return mymodule.application
	return csv


class csv(Structure):

	@check()
	def __init__(self,
				 path,
				 outputName: str = "TEMP_FILE",
				 all_files: bool = False):
		super().__init__(path=path,
						 output_type="csv",
						 output_name=outputName,
						 all_files=all_files)

	@check()
	def escape_string(self, string):
		return str(string).replace(',', ';').replace('"', "'")

	@check()
	def writeHeader(self):
		self.append(','.join(self.output_structure()))

	@check()
	def writeFooter(self):
		self.output_writer.close()

	# region CreateRow Method
	@staticmethod
	@check()
	def create_row(Fully_Qualified_Name="",
				   File_Name="",
				   Number_of_Imports="",
				   Time_Taken="",
				   MCC="",
				   IsVuln="",
				   Fully_Qualified_Loc="",
				   Type="",
				   Message="",
				   File="",
				   Line="",
				   Matched="",
				   Rule="",
				   Rule_Number="",
				   Severity="",
				   Context=""):
		sub = [
			Fully_Qualified_Name, File_Name, Number_of_Imports, Time_Taken, MCC,
			IsVuln, Fully_Qualified_Loc, Type, Message, File, Line, Matched,
			Rule, Rule_Number, Severity, Context
		]
		return ','.join(str(x) for x in sub)

	# endregion

	@staticmethod
	@check()
	def output_structure() -> list:
		return [
			"Fully_Qualified_Name", "File_Name", "Number_of_Imports",
			"Time_Taken", "IsVuln", "Fully_Qualified_Loc", "Type", "Message",
			"File", "Line", "Matched", "Rule", "Rule_Number", "Severity",
			"Context"
		]

	@check()
	def add_issue(self, struct: file_scan_struct):
		output = []
		base = ', '.join([
			self.escape_string(struct.qual_name),
			self.escape_string(struct.file),
			self.escape_string(struct._imports_num),
			self.escape_string(struct.run_time)
		])

		if hasattr(struct, 'vuln') and len(struct.vuln) > 0:
			for vuln in struct.vuln:
				output += ["{0},true,{1}".format(base, self.transform_file_vuln(vuln))]
		else:
			output += ["{0},false,,,,,,,,,,".format(base)]
		if output:
			self.append(output)

	@check()
	def transform_file_vuln(self, self_vuln: vuln):
		return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}".format(
		self.escape_string(self_vuln.fully_qualified_loc),self.escape_string(self_vuln.type),
				self.escape_string(self_vuln.message),self.escape_string(self_vuln.file),
				self.escape_string(self_vuln.line),self.escape_string(self_vuln.matched),
				self.escape_string(self_vuln.rule),self.escape_string(self_vuln.rule_num),
				self.escape_string(self_vuln.severity),self.escape_string(self_vuln.context))
