#!/usr/bin/env python3

#region Prep
import os,sys,json
from datetime import datetime
from copy import deepcopy as dc

imp = lambda x:os.system("{} -m pip install --upgrade {}".format(sys.executable, x))

try:
	os.system("yes|rm -r /usr/local/lib/python3.8/site-packages/pyarrow*")
except:
	pass

try:
	import funbelts as ut
	import hugg
	import pandas as pd
	import astroid
except:
	[imp(x) for x in ["funbelts", "hugg","astroid==2.11.2","setuptools==50.3.2","password_strength==0.0.3.post2","pandas"]]
	import funbelts as ut
	import hugg
	import pandas as pd
	import astroid

core_dirs = [
	"/workspace/CryptoGuard4Py/",
	"/opt/project/",
	"/sync/",
	"/tmp/"
]

core_dir = None
for temp_core_dir in core_dirs:
	if os.path.exists(temp_core_dir):
		core_dir = temp_core_dir
		break

join_path = f"{core_dir}"
if not os.path.exists(join_path):
	os.chdir('../')
else:
	os.chdir(join_path)
cur_path = os.path.abspath(os.curdir)
sys.path.append(cur_path)


crypto_path = ""
for core in core_dirs:
	if os.path.exists(os.path.join(core, 'cryptolation.zip')):
		crypto_path = os.path.join(core, 'cryptolation.zip')
		break

def cryptoscan(x, y="output.csv"):
	try:
		try:
			import cryptoguard4py as crypto
		except Exception as e:
			print(f"Failure to import cryptoguard4py: {e}")

		try:
			import pysrc.cryptoguard4py as crypto
		except Exception as e:
			print(f"Failure to import : {e}")

		crypto.main("-s {} -o {} {}".format(x, y, '-a' if all else '').split())
	except Exception as e:
		for cmd in [
			"{0} {1} -v".format(sys.executable,crypto_path),
			"{0} {1} -s {2} -o {3} -a".format(sys.executable,crypto_path, x, y)
		]:
			print(cmd);os.system(cmd)

	if os.path.exists(y):

		output = dc(
			pd.read_csv(y)
		)

		return output
	return pd.DataFrame()

def load_query_from_table(table_name, query, get_col=None):
	def load_table_from_global(table_name):
		output = pd.DataFrame()
		if os.path.exists('Data.sqlite'):
			with ut.SqliteConnect('Data.sqlite') as sqlite:
				output = dc(sqlite.read(table_name))
		else:
			repo = hugg.face("frantzme/11_", "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")

			try:
				with ut.ephfile(repo['Data.sqlite']) as eph:
					os.system("cp {0} {1}".format(eph(), './Data.sqlite'))
					with ut.SqliteConnect(eph()) as sqlite:
						output = dc(sqlite.read(table_name))
			except Exception as e:
				print(e)

		return output

	if get_col is not None:
		return load_table_from_global(table_name).query(query)[get_col].tolist()
	return load_table_from_global(table_name).query(query)

def get_files_from_table(table_name, query, get_col=None):
	for qual_name in load_query_from_table(table_name, query, get_col):
		with hugg.face("frantzme/11_", "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") as repo:
			with ut.ephfile(repo["Benchmark/Set_01_Dir/{}".format(qual_name)]) as foil:
				yield foil()

def clean_frame(og_frame):
	from copy import deepcopy as dc
	frame = dc(og_frame)

	print(1)
	for name in ["File_Name", "File"]:
		if name in frame.columns:
			try:
				frame = frame.query("{0} != '{1}'".format(name, name))
			except: pass

	print(2)
	for k in ["Number_of_Imports", "Line", "Rule_Number"]:
		try:
			frame[k] = frame[k].fillna(0).astype(int)
		except: pass

	print(3)
	for col in frame.columns.tolist():
		for not_have in ["Unnamed", "File_Name", "Time_Taken", "Context","File"]:
			try:
				if col.lower().startswith(not_have.lower()):
					frame.drop(col, axis=1, inplace=True)
			except: pass

	return frame

def compare_frames(frame_one_base, frame_one_base_name, frame_two_base,frame_two_base_name, to_html=None, to_csv=None):
	for temp_itr,temp in enumerate([frame_one_base, frame_two_base]):
		temp.to_csv("temp_{}.csv".format(temp_itr))

	try:
		compared = clean_frame(frame_one_base).reset_index(drop=True).sort_values(by=["Fully_Qualified_Name", "Type"]).reset_index(drop=True).compare(
			clean_frame(frame_two_base).reset_index(drop=True).sort_values(by=["Fully_Qualified_Name", "Type"]).reset_index(drop=True), result_names=(frame_one_base_name, frame_two_base_name))
	except Exception as e:
		print(e)
		compared = pd.DataFrame()

	try:
		if to_html is not None:
			compared.to_html(
				to_html
			)
	except Exception as e:
		print(e)
	try:
		if to_csv is not None:
			compared.to_csv(
				to_csv
			)
	except Exception as e:
		print(e)

	return compared

#endregion

def test_scan_all_random():
	base_take = """
,Fully_Qualified_Name,File_Name,Number_of_Imports,Time_Taken,IsVuln,Fully_Qualified_Loc,Type,Message,File,Line,Matched,Rule,Rule_Number,Severity,Context
0,Trap_Import_Field-Sensitive_random_rule_05_trapfile_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/Trap_Import_Field-Sensitive_random_rule_05_trapfile_0.py,2,0.4963269233703613,False,,,,,,,,,,
0,Trap_Import_Global_random_rule_05_trapfile_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/Trap_Import_Global_random_rule_05_trapfile_0.py,2,0.8721203804016113,False,,,,,,,,,,
0,Trap_Import_InterproceduralViaReturn_random_rule_05_trapfile_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/Trap_Import_InterproceduralViaReturn_random_rule_05_trapfile_0.py,2,1.3105647563934326,False,,,,,,,,,,
0,Trap_Import_Interprocedural_random_rule_05_trapfile_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/Trap_Import_Interprocedural_random_rule_05_trapfile_0.py,2,1.6377885341644287,False,,,,,,,,,,
0,Trap_Import_Path-Sensitive_random_rule_05_trapfile_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/Trap_Import_Path-Sensitive_random_rule_05_trapfile_0.py,2,2.4678337574005127,False,,,,,,,,,,
0,Trap_Import_random_rule_5_trapfile_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/Trap_Import_random_rule_5_trapfile_0.py,2,2.00606632232666,False,,,,,,,,,,
0,rule_00_Field-Sensitive_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Field-Sensitive_0.py,1,47.87181997299194,True,rule_00_Field-Sensitive_0:11,random.*,Using the library random.* @ line:11,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Field-Sensitive_0.py,11.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_Field-Sensitive_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Field-Sensitive_1.py,1,1.0867152214050293,True,rule_00_Field-Sensitive_1:8,random.*,Using the library random.* @ line:8,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Field-Sensitive_1.py,8.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_Global_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Global_0.py,1,0.9682915210723876,True,rule_00_Global_0:8,random.*,Using the library random.* @ line:8,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Global_0.py,8.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_Global_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Global_1.py,1,1.0934569835662842,True,rule_00_Global_1:8,random.*,Using the library random.* @ line:8,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Global_1.py,8.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_InterproceduralViaReturn_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_InterproceduralViaReturn_0.py,1,1.0759210586547852,True,rule_00_InterproceduralViaReturn_0:7,random.*,Using the library random.* @ line:7,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_InterproceduralViaReturn_0.py,7.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_InterproceduralViaReturn_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_InterproceduralViaReturn_1.py,1,1.2943317890167236,True,rule_00_InterproceduralViaReturn_1:7,random.*,Using the library random.* @ line:7,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_InterproceduralViaReturn_1.py,7.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_Interprocedural_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Interprocedural_0.py,1,1.453108549118042,False,,,,,,,,,,
0,rule_00_Interprocedural_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Interprocedural_1.py,1,1.4578874111175537,False,,,,,,,,,,
0,rule_00_Path-Sensitive_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Path-Sensitive_0.py,1,2.812844038009644,True,rule_00_Path-Sensitive_0:4,random.*,Using the library random.* @ line:4,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Path-Sensitive_0.py,4.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_Path-Sensitive_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Path-Sensitive_1.py,1,2.9448022842407227,True,rule_00_Path-Sensitive_1:4,random.*,Using the library random.* @ line:4,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_Path-Sensitive_1.py,4.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_insecure_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_insecure_0.py,1,1.0198512077331543,True,rule_00_insecure_0:3,random.*,Using the library random.* @ line:3,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_insecure_0.py,3.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_00_insecure_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_insecure_1.py,1,0.9280169010162354,True,rule_00_insecure_1:3,random.*,Using the library random.* @ line:3,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_00_insecure_1.py,3.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_Field-Sensitive_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Field-Sensitive_0.py,1,1.8186287879943848,True,rule_05_Field-Sensitive_0:11,random.*,Using the library random.* @ line:11,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Field-Sensitive_0.py,11.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_Field-Sensitive_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Field-Sensitive_1.py,1,1.9279687404632568,True,rule_05_Field-Sensitive_1:11,random.*,Using the library random.* @ line:11,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Field-Sensitive_1.py,11.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_Global_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Global_0.py,1,2.297300100326538,True,rule_05_Global_0:8,random.*,Using the library random.* @ line:8,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Global_0.py,8.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_Global_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Global_1.py,1,2.5587072372436523,True,rule_05_Global_1:8,random.*,Using the library random.* @ line:8,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Global_1.py,8.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_InterproceduralViaReturn_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_InterproceduralViaReturn_0.py,1,2.1698293685913086,True,rule_05_InterproceduralViaReturn_0:7,random.*,Using the library random.* @ line:7,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_InterproceduralViaReturn_0.py,7.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_InterproceduralViaReturn_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_InterproceduralViaReturn_1.py,1,2.8032450675964355,True,rule_05_InterproceduralViaReturn_1:7,random.*,Using the library random.* @ line:7,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_InterproceduralViaReturn_1.py,7.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_Interprocedural_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Interprocedural_0.py,1,2.694610595703125,False,,,,,,,,,,
0,rule_05_Interprocedural_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Interprocedural_1.py,1,2.9986279010772705,False,,,,,,,,,,
0,rule_05_Path-Sensitive_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Path-Sensitive_0.py,1,5.490279674530029,True,rule_05_Path-Sensitive_0:4,random.*,Using the library random.* @ line:4,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Path-Sensitive_0.py,4.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_Path-Sensitive_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Path-Sensitive_1.py,1,5.550339221954346,True,rule_05_Path-Sensitive_1:4,random.*,Using the library random.* @ line:4,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_Path-Sensitive_1.py,4.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_insecure_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_insecure_0.py,1,1.5999765396118164,True,rule_05_insecure_0:3,random.*,Using the library random.* @ line:3,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_insecure_0.py,3.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_05_insecure_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_insecure_1.py,1,1.6312971115112305,True,rule_05_insecure_1:3,random.*,Using the library random.* @ line:3,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_05_insecure_1.py,3.0,Cryptographically Insecure PRNGs,Using Insecure Random Number Generation,5.0,M,None
0,rule_08_Field-Sensitive_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Field-Sensitive_0.py,2,647.4029171466827,False,,,,,,,,,,
0,rule_08_Field-Sensitive_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Field-Sensitive_1.py,2,2.861158609390259,False,,,,,,,,,,
0,rule_08_Global_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Global_0.py,2,3.722302913665772,True,rule_08_Global_0:9,hashlib.pbkdf2_hmac,Value 100 is less than the required value of 1000 Using the library hashlib.pbkdf2_hmac @ line:9,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Global_0.py,9.0,Fewer Than 1000 Iterations,Using less than 1000 Iterations,8.0,L,{}
0,rule_08_Global_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Global_1.py,2,3.726950168609619,True,rule_08_Global_1:9,hashlib.pbkdf2_hmac,Value 100 is less than the required value of 1000 Using the library hashlib.pbkdf2_hmac @ line:9,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Global_1.py,9.0,Fewer Than 1000 Iterations,Using less than 1000 Iterations,8.0,L,{}
0,rule_08_InterproceduralViaReturn_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_InterproceduralViaReturn_0.py,2,4.441905498504639,True,rule_08_InterproceduralViaReturn_0:8,hashlib.pbkdf2_hmac,Value 100 is less than the required value of 1000 Using the library hashlib.pbkdf2_hmac @ line:8,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_InterproceduralViaReturn_0.py,8.0,Fewer Than 1000 Iterations,Using less than 1000 Iterations,8.0,L,{}
0,rule_08_InterproceduralViaReturn_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_InterproceduralViaReturn_1.py,2,4.256184339523315,True,rule_08_InterproceduralViaReturn_1:8,hashlib.pbkdf2_hmac,Value 100 is less than the required value of 1000 Using the library hashlib.pbkdf2_hmac @ line:8,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_InterproceduralViaReturn_1.py,8.0,Fewer Than 1000 Iterations,Using less than 1000 Iterations,8.0,L,{}
0,rule_08_Interprocedural_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Interprocedural_0.py,2,4.364913463592529,False,,,,,,,,,,
0,rule_08_Interprocedural_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Interprocedural_1.py,2,4.354063987731934,False,,,,,,,,,,
0,rule_08_Path-Sensitive_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Path-Sensitive_0.py,2,7.507742881774902,True,rule_08_Path-Sensitive_0:5,hashlib.pbkdf2_hmac,Value 100 is less than the required value of 1000 Using the library hashlib.pbkdf2_hmac @ line:5,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Path-Sensitive_0.py,5.0,Fewer Than 1000 Iterations,Using less than 1000 Iterations,8.0,L,[{'Error String': 'Value 100 is less than the required value of 1000'; 'Variable Name': '_raw_argument_3'; 'Inferred Variable Value': <Const.int l.6 at 0x7f60f2984850>}]
0,rule_08_Path-Sensitive_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Path-Sensitive_1.py,2,7.384958982467651,True,rule_08_Path-Sensitive_1:5,hashlib.pbkdf2_hmac,Value 100 is less than the required value of 1000 Using the library hashlib.pbkdf2_hmac @ line:5,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_Path-Sensitive_1.py,5.0,Fewer Than 1000 Iterations,Using less than 1000 Iterations,8.0,L,[{'Error String': 'Value 100 is less than the required value of 1000'; 'Variable Name': '_raw_argument_3'; 'Inferred Variable Value': <Const.int l.6 at 0x7f60f2afadf0>}]
0,rule_08_insecure_0, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_insecure_0.py,2,2.46366548538208,True,rule_08_insecure_0:4,hashlib.pbkdf2_hmac,Value 100 is less than the required value of 1000 Using the library hashlib.pbkdf2_hmac @ line:4,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_08_insecure_0.py,4.0,Fewer Than 1000 Iterations,Using less than 1000 Iterations,8.0,L,[{'Error String': 'Value 100 is less than the required value of 1000'; 'Variable Name': '_raw_argument_3'; 'Inferred Variable Value': <Const.int l.5 at 0x7f60f2ae53d0>}]
0,rule_09_insecure_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_09_insecure_1.py,3,3.3024706840515137,True,rule_09_insecure_1:5,Crypto.Cipher.DES*,Using the library Crypto.Cipher.DES* @ line:5,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_09_insecure_1.py,5.0,Using Insecure Block Ciphers,Using an Insecure Block Cipher,9.0,L,None
1,rule_09_insecure_1, /root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_09_insecure_1.py,3,3.3024706840515137,True,rule_09_insecure_1:5,Crypto.*,Using the library Crypto.* @ line:5,/root/.cache/huggingface/hub/datasets--frantzme--11_/snapshots/03304968889f6729d404fb9acbae33ea8c59afee/Benchmark/Set_01/rule_09_insecure_1.py,5.0,Insecure Cryptographic Hash,Using an insecure Hash,11.0,H,None
""".strip()

	output_file, total_content = f"{core_dir}/scan_all_random.csv", []

	with open("raw_results_log_random.csv","w+") as log:
		log.write("Date,File,FileNum,FileTot,Message\n")
		with hugg.face("frantzme/11_","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") as repo:
			with ut.ephfile(repo.find(lambda x:x.endswith('category.json'))) as categories:

				tyte = ut.arr_to_pd(json.loads(categories.contents)).query('Category == "HasRandom"')['FilePath'].tolist()
				tyte_len = len(tyte)

				for found_foil_itr, found_foil in enumerate(tyte):
					with ut.ephfile(repo[found_foil]) as foil:
						with ut.ephfile(output_file) as eph:
							log.write(f"{datetime.now()},{eph().split('/')[-1]},{found_foil_itr},{tyte_len},Started\n")
							try:
								total_content += [ cryptoscan(foil(),eph()) ]
								log.write(f"{datetime.now()},{eph().split('/')[-1]},{found_foil_itr},{tyte_len},Success\n")
							except Exception as e:
								print(e)
								log.write(f"{datetime.now()},{eph().split('/')[-1]},{found_foil_itr},{tyte_len},{e}\n")

	raw_results, base_results = pd.concat(total_content), None

	with ut.ephfile("_temp.csv") as eph:
		for line in base_take.split('\n'):
			eph += f"{line}\n"
		base_results = dc(pd.read_csv(eph()))

	compared = compare_frames(base_results, "base", raw_results,"raw","comparing_for_scan_all_random.html","comparing_for_scan_all_random.csv" )

	compared.to_csv("results.csv")

	assert compared.empty, "There should be no differences between the base and the raw results"

def main():
	test_scan_all_random()

if __name__ == '__main__':
	main()
