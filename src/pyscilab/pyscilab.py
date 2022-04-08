import re
from math import log10, floor
from typing import Tuple
import decimal

def round_sig(num:float, sig:int=1) -> Tuple[float, int]:
	'''
	Rounds num to sig significant digits
	
			Parameters:
					num (float): Number to round
					sig (int): Number of significant digits to round to

			Returns:
					rounded_num (float): Rounded number
					dec (int): Number of decimals of rounded number (if there are any) 
					or number of zeros after last significant digit (if no decimals).
					In this last case, dec is negative. Ex: round_sig(3234, 1) returns
					the tuple (3000, -3) and round_sig(0.3234, 1) returns the tuple
					(0.3, 1).
	'''
	if num==0:
		return num, 0 
	else:
		dec = sig - int(floor(log10(abs(num)))) - 1
		return round(num, dec), dec


def round_with_error(val:float, err:float) -> Tuple[str, str]:
	'''
	Returns val rounded to the number of decimals that are contained in err when we 
	round it to the first significant digit. Both numbers are returned as strings
	with the same number of decimals, even if it means useless zeros! Note that if
	the error is zero, the method does nothing except convert values to string.

	Ex: round_with_error(2.301245, 0.0212) returns ("2.30", "0.02")

			Parameters:
					val (float): Value to round
					err (float): Error value used to determine how to round val

			Returns:
					rounded_val (str): Rounded val
					rounded_err (str): Rounded err
	'''
	if float(err) == 0.:
		return str(val), str(err)
	
	err, dec = round_sig(err)
	val = round(val, dec)
	rounded_val, rounded_err = str(val), str(err)
	
	# Add zeros to the end of the number if necessary
	v = decimal.Decimal(rounded_val)
	current_decimals = abs(v.as_tuple().exponent)
	e = decimal.Decimal(rounded_err)
	correct_decimals = abs(e.as_tuple().exponent)
	if current_decimals < correct_decimals:
		if "e" in rounded_val:
			val_list = rounded_val.split("e")
			rounded_val = val_list[0]
			if "." in rounded_val:
				rounded_val += "0"* (correct_decimals-current_decimals)
			else:
				rounded_val += "." + "0"* (correct_decimals-current_decimals)
			rounded_val = rounded_val + "e" + val_list[1]
		else:
			if "." in rounded_val:
				rounded_val += "0"* (correct_decimals-current_decimals)
			else:
				rounded_val += "." + "0"* (correct_decimals-current_decimals)
	
	if float(err) % 1 == 0:
		rounded_val = str(int(float(rounded_val)))
		rounded_err = str(int(float(rounded_err)))

	return rounded_val, rounded_err


def exponential_to_latex(val:float) -> str:
	'''
	Converts python exponential notation to LaTeX exponential notation.

	Ex: exponential_to_latex(1056e-16) returns 1.056 \cdot 10^{-13}
	Ex: exponential_to_latex(1e-2) returns 0.01

			Parameters:
					val (float): Value to convert to LaTeX exponential notation
			
			Returns:
					latex_val (str): New val in LaTeX exponential notation
	'''
	latex_val = re.sub(r'([^e]+)e(-)?(0)?([^e0]+)', r'\g<1> \\cdot 10^{\g<2>\g<4>}' , str(val))
	return latex_val


def latex_exp_common_fact(val:str, val_exponent:str, err:str, err_exponent:str) -> str:# This does NOT work!!
	'''
	Simplifies expressions of value-error pairs so that they are both multiplied by
	just one exponential instead of each by their own exponential. Output is given as 
	LaTeX code.

	Ex: latex_exp_common_fact("0.2123", "2", "0.6", "1") returns "( 2.123 \pm 0.6) \cdot 10^{1}"

			Parameters:
					val (float): Value without the exponential part
					val_exponent (float): Exponent of the exponential part of val
					err (float): Error of val without the exponential part
					err_exponent (float): Exponent of the exponential part of err
			
			Returns:
					val_and_err_latex (str): Simplified value + error in LaTeX code
					with only one exponential for both the value and its error.

	'''
	val, val_exponent, err, err_exponent = float(val), int(val_exponent), float(err), int(err_exponent)
	common_exponent = max(val_exponent, err_exponent)

	val = val / 10**(common_exponent - val_exponent)
	err = err / 10**(common_exponent - err_exponent)

	while val//1 == 0:
		val = float(re.sub( r'([0123456789]+)\.([0123456789])', r'\g<1>\g<2>.', str(val)))
		err = float(re.sub( r'([0123456789]+)\.([0123456789])', r'\g<1>\g<2>.', str(err)))
		common_exponent -= 1

	return f"( {val}" + f" \\pm {err}) \\cdot 10^" + "{" + str(common_exponent) + "}"


def latex_table(data:dict) -> str:
	'''
	Returns a LaTeX table generated from the given data dictionary.

			Parameters:
					data (dict): Dictionary with the data to plot. It should have the
					following structure:

					data = {
						"caption":"Enter here the caption for the table",
						"label":"Enter here the label for the table",
						"float": "h",	# Enter float option here
						"data":{# Here, the data for the different columns should be given
								# You can add as many as you need.
							"Col 1": [List with the values for Col 1],
							"Col 1_error": [List with the values of the error for Col 1],
							"Col 1_header": "Column 1 Header",
							"Col 2": [List with the values for Col 2],
							"Col 2_error": [List with the values of the error for Col 2],
							"Col 2_header": "Column 2 Header",
							...
						}
					}

					All headers and captions may contain latex code. Specifying the 'float' 
					option is optional. Giving error data is also optional, and the name of 
					the columns can be any, as long as it is consistent for the column data, 
					error data and column header. For example, this is valid:

					data = {
						"caption":"Example table",
						"label":"tab-1",
						"float": "h",
						"data":{
							"My First Column": [10, 20, 30, 40, 50, 60, 70, 80],
							"My First Column_error": [1, 0.2, 3, 4, 2, 0.002, 3, 5],
							"My First Column_header": "Column 1 Header",
							"My Second Column": [1, 2, 3, 4, 5, 6, 7, 8],
							"My Second Column_header": "Column 2 Header",
						}
					}

					All columns must contain the same number of elements, as is also
					the case with the errors.
	'''
	table ='''
\\begin{table}float-placeholder
	\\centering
	\\begin{tabular}{ alignment-tabs-placeholder } \\hline
		headers-placeholder \\\\ \\hline
		data-placeholder \\hline
	\\end{tabular}
	\\caption{ caption-placeholder }
	\\label{tab:label-placeholder}
\\end{table}
	'''
	headers = []
	columns = {}
	errors = {}
	for item in data['data']:
		if "_header" in item:
			headers.append(data['data'][item])
		elif "_" not in item:
			columns[item] = data['data'][item]
			if item + "_error" in data['data']:
				errors[item] = data['data'][item + "_error"]
			else:
				errors[item] = None

	headers_line = ""
	for i in range(len(headers)):
		if i < len(headers) - 1:
			headers_line += headers[i] + "\t&\t"
		else:
			headers_line += headers[i]

	number_of_columns = len(headers)
	alignment_tabs = "c"*number_of_columns

	values_and_errors = {}

	for column_name in columns:
		column = columns[column_name]
		error = errors[column_name]
		if error:
			val_and_err = []
			for val, err in zip(column, error):
				val, err = round_with_error(val, err)
				val, err = exponential_to_latex(val), exponential_to_latex(err)
				x = "$" + val + " \\pm " + err + "$"
				x = re.sub(r'([^ \$]+) \\cdot 10\^\{([-0123456789]+)\} \\pm ([^ ]+) \\cdot 10\^\{([-0123456789]+)\}', lambda m: latex_exp_common_fact(m.group(1),m.group(2), m.group(3), m.group(4)), x)
				val_and_err.append(x)
		else:
			val_and_err = ["$" + str(val) + "$" for val in column]
		values_and_errors[column_name] = val_and_err
	
	data_lines = ""
	for i in range(len(values_and_errors[list(values_and_errors.keys())[0]])):
		line = ""
		for column in values_and_errors:
			item = values_and_errors[column][i]
			line += item + "\t&\t"
		data_lines += "\t\t" + line[:-3] + "\\\\ \n"
	data_lines = data_lines[:-1]


	table = re.sub('caption-placeholder', data['caption'], table)
	table = re.sub('label-placeholder', data['label'], table)
	table = re.sub('alignment-tabs-placeholder', alignment_tabs, table)
	table = re.sub('headers-placeholder', headers_line, table)
	if 'float' in data.keys():
		table = re.sub('float-placeholder', "[" + data['float'] + "]", table)
	else:
		table = re.sub('float-placeholder', '', table)
	table_list = table.split("\t\tdata-placeholder")
	table = table_list[0] + data_lines + table_list[1]

	return table