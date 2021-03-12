import os
def check_for_pkg(pkg):
	try:
		exec("import " + pkg)
	except:
		os.system("pip3 install " + pkg)