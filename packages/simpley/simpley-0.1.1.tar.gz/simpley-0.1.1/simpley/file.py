def read(file_path):
	try:
		with open(file_path) as f:
			return f.read()
	except Exception as e:
		return e