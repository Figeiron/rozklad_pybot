import json


# маніпуляції в admins.json
async def get_admin():
	with open("admins.json", "r") as f:
		data = json.load(f)
		result = []
		for item in data["admins"]:
			result.append(int(item))
		return result


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
			if item in data[key]:
				return f"Користувач {item} вже є адміністратором"
			else:
				data[key].append(item)
				f.seek(0)
				json.dump(data, f, indent=4)
				f.truncate()
				return f"Користувач {item} доданий до адміністраторів"
		else:
			data[key] = [item]
			f.seek(0)
			json.dump(data, f, indent=4)
			f.truncate()
			return f"Користувач {item} доданий до адміністраторів"


# маніпуляції в groups.json

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


# маніпуляції в message.json

async def write_to_json_file(key, item):
	try:
		with open("message.json", "r+") as file:
			data = json.load(file)
	except FileNotFoundError:
		data = {}

	data.setdefault(key, []).append(item)
	with open("message.json", "w") as file:
		json.dump(data, file, indent=4)


async def read_from_json_file():
	with open("message.json", 'r') as file:
		data = json.load(file)
		for username, messages in data.items():
			yield f"Користувач:\n [{username}](https://t.me/{username})"
			for message in messages:
				yield f"Повідомлення {message}"


# маніпуляції з user_data.json


async def write_data_to_json(data):
	with open("users_data.json", 'r') as json_file:
		json_data = json.load(json_file)
	user_id = data['id']
	if user_id in json_data:
		# Оновлення значень під існуючим ключем
		json_data[user_id].update({
			"id": data["id"],
			'username': data["username"],
			'first_name': data['first_name'],
			'last_name': data['last_name'],
			'phone': data['phone'],
			'admin': data['admin'],
			"bot_blocked": data["bot_blocked"]
		})
	else:
		# Додавання нового запису
		json_data[user_id] = {
			"id": data["id"],
			'username': data['username'],
			'first_name': data['first_name'],
			'last_name': data['last_name'],
			'phone': data['phone'],
			'admin': data['admin'],
			"bot_blocked": data["bot_blocked"]
		}

	with open("users_data.json", 'w') as json_file:
		json.dump(json_data, json_file, indent=4)


async def read_first_level_keys():
	with open("users_data.json", 'r') as json_file:
		json_data = json.load(json_file)
		keys = []
		for key in json_data:
			keys.append(key)
		return keys


async def get_data_by_id(user_id):
	with open("users_data.json", 'r') as json_file:
		json_data = json.load(json_file)
		user_data = json_data.get(str(user_id))
		return user_data


async def get_data():
	with open("users_data.json", 'r') as json_file:
		json_data = json.load(json_file)
		return json_data
