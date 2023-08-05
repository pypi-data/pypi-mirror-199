import os

def read(file_path):
	try:
		with open(file_path) as f:
			return f.read()
	except Exception as e:
		return e

def write(file_path, content):
	try:
		with open(file_path, "w") as f:
			return f.write(content)
	except Exception as e:
		return e

def create(file_path):
	try:
		with open(file_path, "x") as f:
			return True
	except Exception as e:
		return e

def exists(file_path):
	return os.path.exists(file_path)
