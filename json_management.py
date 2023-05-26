import json


async def get_admin(key):
	with open("admins.json", "r") as f:
		data = json.load(f)

	if key in data:
		result = []
		for item in data[key]:
			result.append(item)
		return result
	else:
		return False


async def remove_admin_by_key(key, value):
	with open("admins.json", "r") as f:
		data = json.load(f)

	if key in data:
		if value in data[key]:
			data[key].remove(value)
			with open("admins.json", "w") as f:
				json.dump(data, f)

			return f"Адміністратора {value} успішно видалено"
	return f"Адміністратора {value} не видалено"


async def add_admin_by_key(key, item):
	with open("admins.json", "r+") as f:
		data = json.load(f)

		if key in data:
			data[key].append(item)
		else:
			data[key] = [item]
		f.seek(0)
		json.dump(data, f, indent=4)
		f.truncate()
		return True if item in data[key] else False


async def read_group(groups_type, groups):
	with open('groups.json', 'r') as f:
		group_list = json.load(f)[groups_type][groups]

	return group_list


async def read_second_key():
	with open('groups.json', 'r') as f:
		data = json.load(f)

		second_keys = []
		for key in data.keys():
			if isinstance(data[key], dict):
				second_keys.extend(list(data[key].keys()))

		return second_keys


async def get_groups_by_second_key(second_level_key):
	with open("groups.json") as f:
		data = json.load(f)

	for key in data.keys():
		if second_level_key in data[key]:
			groups = data[key][second_level_key]
			if groups:
				return groups


async def read_type_group(groups):
	with open('groups.json', 'r') as f:
		data = json.load(f)

		groups_prog = data[groups]
		groups_prog_list = []
		for sublist in groups_prog.values():
			groups_prog_list += sublist
		return groups_prog_list


async def remove_group_by_second_key(second_level_key, group_name):
	with open("groups.json") as f:
		data = json.load(f)

	for first_level_key, groups in data.items():
		if second_level_key in groups:
			if group_name in groups[second_level_key]:
				groups[second_level_key].remove(group_name)
				if not groups[second_level_key]:
					del groups[second_level_key]
				with open("groups.json", "w") as f:
					json.dump(data, f)
				return True
	return False


async def add_group_by_second_key(second_level_key, group_name):
	with open("groups.json") as f:
		data = json.load(f)

	for first_level_key, groups in data.items():
		if second_level_key in groups:
			groups[second_level_key].append(group_name)
			with open("groups.json", "w") as f:
				json.dump(data, f)
			return True
	return False
