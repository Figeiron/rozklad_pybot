import pandas as pd
import urllib.request
from selection_generate import generate_menu
from bs4 import BeautifulSoup
from urllib.request import urlopen


def download_file(url, local_filename):
	urllib.request.urlretrieve(url, local_filename)


def process_data(local_filename, group_name, sheet_name):
	df = pd.read_excel(local_filename, sheet_name=sheet_name)
	if group_name not in df.columns:
		data_name = f"Групу {group_name} не знайдено"
		return data_name
	next_column_index = df.columns.get_loc(group_name) + 1
	next_column_name = df.columns[next_column_index] if next_column_index < len(df.columns) else None
	selected_columns = [group_name]
	if next_column_name:
		selected_columns.append(next_column_name)
	df = df[selected_columns].dropna(how='all')
	df = df.drop(df.index[df.index % 2 != 0])
	df = df.apply(lambda x: x.str.ljust(30, "-") if x.name == group_name else x)
	result = df.to_string(index=False, header=False)
	result_with_dividers = insert_dividers(result, group_name)
	return result_with_dividers


def insert_dividers(data, group):
	divider = '**====================================**'
	lines = data.split('\n')
	result_with_dividers = ''
	for i, line in enumerate(lines):
		if i == 0:
			result_with_dividers += f'{group}\n{divider}\n'
		result_with_dividers += line + '\n'
		if (i + 1) % 4 == 0:
			result_with_dividers += divider + '\n'
	return result_with_dividers


async def send_data(event, file_name, button_id1, sheet_index):
	local_filename = file_name
	download_file(f"https://www.uatk.ck.ua/images/Rozklad/{local_filename}", local_filename)
	rozklad = process_data(local_filename, button_id1, sheet_index)
	await event.edit(rozklad, buttons=await generate_menu("back"))


async def process_data_prog(event, button_id1):
	await send_data(event, "prog.xls", button_id1, 0)


async def process_data_mex(event, button_id1):
	await send_data(event, "mex.xls", button_id1, 1)


async def process_data_econom(event, button_id1):
	await send_data(event, "ekonom.xls", button_id1, 0)


async def process_data_1k(event, button_id1):
	await send_data(event, "prog.xls", button_id1, 0)


async def schedule_changes(event):
	url = 'http://www.uatk.ck.ua/uk/zmini-u-rozkladi'
	response = urlopen(url)
	soup = BeautifulSoup(response, 'html.parser')
	table = soup.find('tbody')
	tds = table.find_all('td')
	results = []
	for td in tds:
		if td.find('strong') is not None:
			results.append(td.text.strip())
		elif 'style="text-align: left;"' in str(td):
			results.append(td.text.strip())
		elif ' style="text-align: center' in str(td):
			results.append(td.text.strip())

	await event.edit('\n'.join(results), buttons=await generate_menu("back"))





