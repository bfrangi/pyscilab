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


def latex_table(data:dict) -> str:
	table ='''
\\begin{table}[H]
	\\centering
	\\begin{tabular}{ alignment-tabs-placeholder } \\hline
		headers-placeholder \\\\ \\toprule
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
				x = re.sub(r'([^ \$]+) \\cdot 10\^\{([-0123456789]+)\} \\pm ([^ ]+) \\cdot 10\^\{([-0123456789]+)\}', lambda m: simplify(m.group(1),m.group(2), m.group(3), m.group(4)), x)
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
	table_list = table.split("\t\tdata-placeholder")
	table = table_list[0] + data_lines + table_list[1]

	return table