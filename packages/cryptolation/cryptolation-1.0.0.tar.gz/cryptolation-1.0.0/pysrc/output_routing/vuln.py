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


class Klass:

	@check()
	def __init__(self,
				 type: str = None,
				 message: str = None,
				 file: str = None,
				 line: int = None,
				 matched: str = None,
				 rule: str = None,
				 rule_num: int = None,
				 severity: str = None,
				 context: list = None,
				 kol: int = None):
		self.type = type
		self.message = message
		self.file = file
		self.line = int(line)
		self.matched = matched
		self.rule = rule
		self.rule_num = int(rule_num)
		self.severity = severity
		self.context = context
		self.fully_qualified_loc = None
		self.kol = int(kol) if kol is not None else None

	@check()
	def __baseDict(self):
		return {
			'Qualified Loc': self.fully_qualified_loc,
			'File': self.file,
			'Line': self.line,
			'Kol': self.kol,
			'Rule Number': self.rule_num,
			'Severity': self.severity,
			'Context': self.context
		}

	@check()
	def toDict(self):
		return {
			'Qualified Loc': self.fully_qualified_loc,
			'Type': self.type,
			'Message': self.message,
			'File': self.file,
			'Line': self.line,
			'Kol': self.kol,
			'Matched': self.matched,
			'Rule': self.rule,
			'Rule Number': self.rule_num,
			'Severity': self.severity,
			'Context': self.context
		}

	@check()
	def is_(self, item):
		return isinstance(item, Klass) and all(
			self[attribute] == item[attribute]
			for attribute in list(self.toDict().keys()))

	@check()
	def is_of(self, item):
		baseCheck = isinstance(item, Klass) and all(
			self[attribute] == item[attribute]
			for attribute in list(self.__baseDict().keys()))

		if not baseCheck:
			return False
		import re
		return re.match(self.type, item.type) or re.match(item.type, self.type)

	@check()
	def __getitem__(self, item):
		return self.toDict()[item]

	@check()
	def __str__(self):
		return str(self.toDict())

	@check()
	def __repr__(self):
		return str(self.toDict())

	@property
	@check()
	def base_str(self):
		output = self.toDict()
		output['Context'] = None
		return output
