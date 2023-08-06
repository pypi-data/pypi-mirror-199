#!/usr/bin/env python3.8

# region Imports
import pathlib, zipfile
from fileinput import FileInput as finput
import os
import sys
from setuptools import find_packages, setup
from pathlib import Path
import glob
try:
	from pylint.reporters.json_reporter import JSONReporter
except:
	pass
#endregion
#To Check Syntax := python -m py_compile <x>
#region pysrc
try:
	from pysrc import cryptoguard4py
except:
	pass
try:
	import cryptoguard4py
except:
	pass
try:
	from pysrc.information import VERSION, REQ
except:
	pass
try:
	from information import VERSION, REQ
except:
	pass
#endregion

"""TODO
Add Performance:
* https://www.realpythonproject.com/how-to-benchmark-functions-in-python/
* https://realpython.com/python-timer/
* https://stackoverflow.com/questions/5929107/decorators-with-parameters

Run Custom Commands via:
https://lug.dev/

https://jqplay.org/
https://stedolan.github.io/jq/tutorial/
using lug.dev and jq

> .[0] | {html_url}
apt-get -y install jq && curl 'URL' | jq '.[] | {html_url}'

apt-get install jq && curl 'https://api.github.com/repos/Trusted-AI/adversarial-robustness-toolbox/commits?since=2021-12-23T16:34:00' | jq '.[] | {html_url}'


full dock.sh cmd?
dock -x run -d pydev:lite -c "apt-get -qq -y install jq > /dev/null && curl '<URL>' | jq '.[] | {html_url}'"

https://github.com/Trusted-AI/adversarial-robustness-toolbox/tree/3e3a43816e471334da123197c72512f3877c253e

python3 <(curl -sL https://rebrand.ly/pydock) -x run -d pydev:lite -c "apt-get -qq -y install jq > /dev/null && curl 'https://api.github.com/repos/Trusted-AI/adversarial-robustness-toolbox/commits?since=2021-12-23T16:34:00' | jq '.[] | {html_url}'"
"""

# endregion
# region Basic Information
here = os.path.abspath(os.path.dirname(__file__))
py_version = sys.version_info[:2]
NAME = "cryptoguard4py"
AUTHOR = 'Miles Frantz'
EMAIL = 'frantzme@vt.edu'
DESCRIPTION = 'My short description for my project.'
GH_NAME = "franceme"
URL = f"https://github.com/{GH_NAME}/{NAME}"
long_description = pathlib.Path(f"{here}/README.md").read_text(encoding='utf-8')
REQUIRES_PYTHON = '>=3.8.0'
RELEASE = "?"
entry_point = f"pysrc.{NAME}"
revaluating="revaluating_15"

# endregion
# region CMD Line Usage
def selfArg(string):
	return __name__ == "__main__" and len(
		sys.argv) > 1 and sys.argv[0].endswith('/setup.py') and str(
			sys.argv[1]).upper() == str(string).upper()
def rrun(string):
	try:
		print(string)
		os.system(string)
	except:
		pass
def zip_program(outputName:str = "cryptolation.zip"):
	base_path = os.path.abspath(__file__).replace(os.path.basename(__file__),'')
	outputName = os.path.join(base_path, outputName)
	#http://blog.ablepear.com/2012/10/bundling-python-files-into-stand-alone.html
	if os.path.exists(outputName):
		os.system(f"rm {outputName}")

	#zipf = zipfile.ZipFile(outputName, 'w', zipfile.ZIP_DEFLATED)
	zipf = zipfile.PyZipFile(outputName, 'w')
	success = 0
	os.chdir(base_path)
	try:
		zipf.write("setup.py") #Current Issue
		zipf.write("README.md")
		zipf.write("__main__.py")
		zipf.writepy("__main__.py")
		zipf.writepy("pysrc")
		for root, dirs, files in os.walk('pysrc/'):
			for file in [x for x in files if not x.endswith('.pyc')]:
				ending_path = os.path.relpath(os.path.join(root, file), os.path.join('pysrc/', '..'))
				zipf.write(
					os.path.join(root, file),
					ending_path
				)
		print(f"Successful: {outputName}")
	except Exception as e:
		print(f"Failing the exception check: {e}")
		success = 1
	zipf.close()
	return outputName

if selfArg('help') or selfArg('list'):
	print()
	for key,value in {
		'upsmall':'Upgrade the minor version.',
		'upmedium':'Upgrade the middle version.',
		'uplarge':'Upgrade the major version.',
		'format':'Format the source code.',
		'package':'Create a self installer using pyinstaller.',
		'rrun':'Directly run the source code.',
		'install':'Install the dependencies.',
		'dockerfile':'Create a dockerfile.',
		'zip':'Zip the source code.',
	}.items():
		print(f"{key}: {value}")
	sys.exit(0)

if selfArg('upsmall'):
	update = (0, 0, 1)
elif selfArg('upmedium'):
	update = (0, 1, 0)
elif selfArg('uplarge'):
	update = (1, 0, 0)
else:
	update = None

if update:
	current_version = VERSION
	version_tuple = tuple(current_version.split('.'))
	updated_version_tuple = '.'.join(
		tuple(map(lambda i, j: str(int(i) + int(j)), update, version_tuple)))

	if selfArg('upmedium'):
		updated_version_tuple = '.'.join(updated_version_tuple.split('.')[:-1]) + '.0'
	if selfArg('uplarge'):
		updated_version_tuple = updated_version_tuple.split('.')[0]+'.0.0'

	print(f"Updating to version: {updated_version_tuple}")
	for foil_path in ["pysrc/information", "information"]:
		foil = f"{foil_path}/__init__.py"
		try:
			with finput(foil, inplace=True) as foil:
				for line in foil:
					if line.startswith("VERSION"):
						print(f"VERSION = \"{updated_version_tuple}\"")
					else:
						print(line, end='')
		except:
			pass

	with finput('README.md', inplace=True) as foil:
		for line in foil:
			if line.startswith('## Current Version: '):
				print(f"## Current Version: {updated_version_tuple}")
			else:
				print(line, end='')
	sys.exit(0)
elif selfArg('format'):
	#region Imports
	try:
		from yapf.yapflib.yapf_api import FormatFile
	except:
		rrun(f"{sys.executable} -m pip install yapf")
		from yapf.yapflib.yapf_api import FormatFile
	try:
		import reindent
	except:
		rrun(f"{sys.executable} -m pip install reindent")
		import reindent
	#endregion
	for folderpath in ["pysrc"]:
		#region Python Files
		python_files = [
			str(Path(filename).resolve())
			for filename in glob.iglob(os.path.join(folderpath, '**/*.py'), recursive=True)
		]
		print(f"Formatting the folder {folderpath}")
		for file in python_files:
			try:
				FormatFile(str(file), style_config="google", in_place=True)
			except Exception as e:
				print(f"Failure with the file {file}: {e}")
			print(".", end='')
		print('')
		rrun(f"reindent -n --newline LF {folderpath}/")
		print()
		for file in python_files:
			try:
				for line in finput(file, inplace=1):
					print(line.replace("    ",'\t').replace("	", "\t"), end='')
			except:
				pass
			print(".", end='')
		print('')
		#endregion
		#region Json Files
		import json

		for json_file in [
				str(Path(filename).resolve()) for filename in glob.iglob(
					os.path.join(folderpath, '**/*.json'), recursive=True)
		]:
			with open(json_file, "r") as reader:
				contents = json.load(reader)

			rrun(f"rm {json_file}")
			with open(json_file, "w+", encoding="utf-8") as writer:
				json.dump(contents, writer, indent=4)

			from fileinput import FileInput as finput
			print(f"Changing spaces to tabs in file: {json_file}")
			for line in finput(json_file, inplace=1):
				print(line.replace("	", "\t"), end='')
		print()
		#endregion
		for folderpath in ["./tests"]:
			for extension in ["csv", "sql"]:
				print(f"Formatting the file by extensions {extension} from folder {folderpath}")
				for source in [
					str(Path(filename).resolve())
					for filename in glob.glob( folderpath + f"/**/*.{extension}", recursive=True)
				]:
					rrun(f"rm {source}")
	sys.exit(0)
elif selfArg('package'):
	print("Creating the appimage")
	import platform, uuid
	current_os = platform.system()

	instructions = [
		"pyinstaller", f"-n {NAME}.sh", "--clean", "--onefile", "-y",
		f"--key={uuid.uuid4()}_{uuid.uuid4()}_{uuid.uuid4()}"
	]

	#if current_os != 'Linux':
	#   instructions += ["--console"]

	instructions += [f"{os.path.join(*entry_point.split('.'))}.py"]

	[rrun(x) for x in ["rm -r dist/"]]
	print("Installers done")
	rrun(' '.join(instructions))
	print("Creation Done")
	sys.exit(0)
elif selfArg('rrun'):
	sys.exit(cryptoguard4py.main(sys.argv[2:]))
elif selfArg('install'):
	sys.exit(rrun('python3 -m pip install -e .'))
elif selfArg('dockerfile'):
	rrun("rm Dockerfile")

	with open("Dockerfile", "w+") as writer:
		writer.write("""FROM python:3.8
COPY . /app
WORKDIR /app
rrun python3 setup.py install
CMD ["python3", "pysrc/cryptoguard4py.py"]
""")
	sys.exit(0)
elif selfArg('zip'):
	sys.exit(zip_program())
elif selfArg('hugger'):
	from glob import glob as re
	zip_foil = zip_program()
	imp = lambda x: os.system("{} -m pip install --upgrade {}".format(sys.executable, x))
	imp('hugg');import hugg;from glob import glob as re
	print("Starting")
	with hugg.face("frantzme/11_Revaluating_Source", "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") as repo:
		print("Into")
		try:
			del repo['cryptolation.zip']
		except:pass
		print("Deleted")
		repo.upload(path_in_repo='cryptolation.zip', path=zip_foil, auto_accept_all_pull_requests=True,use_pull_request=True)
		print("Uploaded")
		if False:
			try:
				os.remove('cryptolation.zip')
			except:
				pass
		if False:
			for foil in re("tests/*.py"):
				repo[foil.replace('tests/','')] = foil
		if False:
			for foil in re("rsc/{0}/*.py".format(revaluating)):
				repo.upload(path_in_repo=foil.replace("rsc/{0}/".format(revaluating), ''), path=foil, auto_accept_all_pull_requests=True,use_pull_request=True)
		print(repo.files())
	if False:
		with hugg.face("frantzme/11_Pulling", "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") as repo:
			for foil in [
				"Grabber.py","CommonUtils.py",
			]:
				repo.upload(path_in_repo=foil, path="rsc/{0}/".format(revaluating)+str(foil), auto_accept_all_pull_requests=True,use_pull_request=True)
	with hugg.face("frantzme/11_Pulling", "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") as repo:
		repo.logout()
	with hugg.face("franceme/11_Revaluating_Source", "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") as repo:
		repo.logout()

	sys.exit(0)
# endregion
# region Setup

setup(
	name="cryptolation",
	version=VERSION,
	description=DESCRIPTION,
	long_description=long_description,
	long_description_content_type='text/markdown',
	author=AUTHOR,
	author_email=EMAIL,
	#cmdclass={'build_sphinx':BuildDoc},
	command_options={
		'build_sphinx': {
			'project': ('setup.py', NAME),
			'version': ('setup.py', VERSION),
			'release': ('setup.py', RELEASE),
			'source_dir': ('setup.py', 'source')
		}
	},
	python_requires=REQUIRES_PYTHON,
	url=URL,
	packages=find_packages(
		exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
	entry_points={
		'console_scripts': ['mycli=pysrc.cryptoguard4py:main'],
	},
	install_requires=REQ,
	extras_require={
		'Deployment': ['pyinstaller==4.2'],
		'Documentation': [
			"alabaster==0.7.12",
			"Babel==2.9.0",
			"certifi==2020.12.5",
			"chardet==4.0.0",
			"colorama==0.4.4",
			"commonmark==0.9.1",
			"docutils==0.16",
			"idna==2.10",
			"imagesize==1.2.0",
			"Jinja2==2.11.2",
			"MarkupSafe==1.1.1",
			"mccabe==0.6.1",
			"packaging==20.8",
			"Pygments==2.7.4",
			"pyparsing==2.4.7",
			"pytz==2020.5",
			"recommonmark==0.7.1",
			"requests==2.25.1",
			"snowballstemmer==2.0.0",
			"timeout-decorator==0.5.0",
			"toml==0.10.2",
			"urllib3==1.26.2",
			"yapf==0.30.0",
		]
	},
	include_package_data=True,
	# license='MIT',
	classifiers=[
		# Trove classifiers
		# Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
		# 'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
	],
	test_suite='tests.test_suites',
	# $ setup.py publish support.
	#
	# cmdclass={
	#   'upload': UploadCommand,
	# },
)
# endregion
