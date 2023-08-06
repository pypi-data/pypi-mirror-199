def _importFile(fileName):
	with open(fileName, "r") as f:
		lines = f.readlines()
	return lines

# Take the whole a2l file and extract the lines containing measurement or characteristic sections
def _linesToSections(lines):
	# Whether or not the current line is inside a section
	inSection = False
	output = []
	currentOutput = []
	for rawline in lines:
		# Remove leading and trailing whitespace
		line = rawline.lstrip()[:-1]

		if line == "/begin CHARACTERISTIC" or line == "/begin MEASUREMENT":
			inSection = True
		elif line == "/end CHARACTERISTIC" or line == "/end MEASUREMENT":
			inSection = False
			currentOutput.append(line)
			output.append(currentOutput)
			currentOutput = []
		
		if inSection:
			currentOutput.append(line)

	return output

def fileToSections(fileName):
	lines = _importFile(fileName)
	return _linesToSections(lines)
