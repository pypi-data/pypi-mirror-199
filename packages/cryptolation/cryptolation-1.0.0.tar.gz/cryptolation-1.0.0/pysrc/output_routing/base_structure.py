from abc import ABC, abstractmethod
import datetime

def log(string):
	#print(string)
	t=2

klass_check = lambda type:False

#region Src
try:
	import pysrc.utils
	from pysrc.output_routing import vuln
	from pysrc.utils.utils import check
	from pysrc.output_routing.vuln import Klass
except Exception as e:
	pass
try:
	import utils
	from output_routing import vuln
	from utils.utils import check
	from output_routing.vuln import Klass
	klass_check = lambda type: isinstance(object, Klass)
except Exception as e:
	pass

#endregion

def klass_check(object):
	output = False
	try:
		output |= isinstance(object, pysrc.output_routing.vuln.Klass)
	except Exception as e: pass

	try:
		output |= isinstance(object, output_routing.vuln.Klass)
	except Exception as e: pass

	return output

@check()
def fancy_date(date: datetime.datetime):
	return date.strftime("%a %b %d %H:%M:%S %Z %Y")


class file_scan_struct(object):

	@check()
	def __init__(self, overlord, file: str, dedup: bool = True):
		#log("><Initiated")
		self.file = file
		self._imports = {}
		self._imports_num = 0
		self.vuln = []
		self.vuln_num = 0
		self.run_time = None
		self.overlord = overlord
		#log("PreQualify")
		self.qual_name = self.overlord.qualify(self.file)
		#log("PostQualify")
		self.dedup = dedup
		#log("Ended")

	@check()
	def __enter__(self):
		#log("Entered")
		import time
		self.start = True
		self.end = False
		self.start_date = datetime.datetime.now(datetime.timezone.utc)
		self.start_time = time.time()
		#log("Start time: {0}".format(self.start_time))
		return self

	@check()
	def __exit__(self, exc_type, exc_val, exc_tb):
		import time
		self.end_time = time.time()
		self.end_date = datetime.datetime.now(datetime.timezone.utc)
		self.run_time = self.end_time - self.start_time
		self.end = True
		self.overlord += self
		return self

	@check()
	def __iadd__(self, object):
		if klass_check(object):
			object.fully_qualified_loc = "{0}:{1}".format(self.qual_name, object.line)

			if not self.dedup:
				self.vuln += [object]
				self.vuln_num = self.vuln_num + 1
			elif (len(self.vuln) == 0 or
				  not any(x.is_(object) for x in self.vuln) and
				  not any(x.is_of(object) for x in self.vuln)):
				self.vuln += [object]
				self.vuln_num = self.vuln_num + 1
		elif isinstance(object, dict):
			self._imports = {**self.imports, **object}
		return self

	@check()
	def __len__(self):
		return len(self.vuln)

	@check()
	def __getitem__(self, sliced):
		if isinstance(sliced, int):
			return self.vuln[sliced]
		else:
			return self.toDict[sliced]

	@check()
	def add_vuln(self, vuln):
		if len(self.vuln) <= len(
				list(filter(lambda itym: itym is vuln, self.vuln))):
			self.vuln += [vuln]
			self.vuln_num = self.vuln_num + 1

	@check()
	def imports(self, object: dict = None):
		if object:
			self._imports = object
			self._imports_num = len(object.keys())
		return object

	@check()
	def imports_num(self) -> int:
		return self._imports_num

	@property
	@check()
	def toDict(self):
		return {
			'File Name': self.file,
			'Fully Qualified Path': self.qual_name,
			'Imports': self._imports,
			'Imports Lite': self._imports_num,
			'Vulnerabilities': self.vuln,
			'Vulnerabilities Lite': len(self.vuln),
			'Start Time': fancy_date(self.start_date),
			'Duration Time': self.run_time,
			'End Time': fancy_date(self.end_date),
		}

	@property
	@check()
	def toString(self):
		raw_output = self.toDict
		raw_output['Vulnerabilities'] = [
			vuln.base_str for vuln in raw_output['Vulnerabilities']
		]
		return str(raw_output)


class Structure(ABC):

	@check()
	def __enter__(self):
		self.output_writer = open(self.output_file, "w+")
		self.writeHeader()
		return self

	@check()
	def __exit__(self, exc_type, exc_val, exc_tb):
		import time
		self.end_date = datetime.datetime.now(datetime.timezone.utc)
		self.end_time = time.time()

		self.writeFooter()
		self.return_output = self.dict
		self.output_writer.close()
		self.return_output = self.dict
		return None

	@check()
	def __init__(self,
				 path,
				 output_type,
				 output_name: str = "TEMP",
				 open_writer: bool = True,
				 all_files: bool = False):
		super().__init__()
		import time,os

		self.start_date = datetime.datetime.now(datetime.timezone.utc)
		self.start_time = time.time()
		self.path = os.path.abspath(path)
		self.qualify = pysrc.utils.utils.get_fully_qualified_file_name(
			'' if os.path.isfile(self.path) else self.path)
		self.start = False
		self._end_time = None
		self._duration = None
		self._vuln_count = 0
		self._import_count = 0
		self.output_type = output_type
		self.output_file = output_name
		self.all_files = all_files

		if open_writer:
			self.output_writer = open(self.output_file, "w+")

	@check()
	def __iadd__(self, object: file_scan_struct):
		if object is not None and (len(object) > 0 or self.all_files):
			self.add_issue(object)
			self._vuln_count += len(object['Vulnerabilities'])
			self._import_count += len(object['Imports'])
		return self

	@check()
	def append(self, string_type):
		# region Local ofList imports
		try:
			from pysrc.utils.utils import of_list
		except Exception as e:
			pass
		try:
			from utils.utils import of_list
		except Exception as e:
			pass
		[
			self.output_writer.write("{0}\n".format(string))
			for string in of_list(string_type)
		]

	@property
	@check()
	def dict(self):
		import platform, multiprocessing
		platform_name = platform.uname()

		return {
			'Path': self.path,
			'Output File': self.output_file,
			'Output Type': self.output_type,
			'Start': self.start,
			'Start Time': fancy_date(self.start_date),
			'End Time': fancy_date(self.end_date),
			'Duration': self.duration,
			'System': platform_name.system,
			'Release': platform_name.release,
			'Version': platform_name.version,
			'Processor': platform_name.processor,
			'Cores': multiprocessing.cpu_count(),
			'Vulnerabilities': self.vulnerabilities
		}

	@property
	@check()
	def duration(self):
		if self._duration is None:
			self._duration = self.end_time - self.start_time
		return self._duration

	@property
	@check()
	def vulnerabilities(self):
		if self._vuln_count is None:
			self._vuln_count = sum(
				len(value['Vulnerabilities']) for value in self.files)
		return self._vuln_count

	@property
	@check()
	def imports(self):
		if self._import_count is None:
			self._import_count = sum(
				len(value['Imports'].keys()) for value in self.files)
		return self._import_count

	@abstractmethod
	@check()
	def writeHeader(self):
		pass

	@abstractmethod
	@check()
	def writeFooter(self):
		self.output_writer.close()

	@abstractmethod
	@check()
	def add_issue(self, object: file_scan_struct):
		pass

	@abstractmethod
	@check()
	def escape_string(self, string: object):
		pass
