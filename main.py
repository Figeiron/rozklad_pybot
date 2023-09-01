import asyncio

from config import *
from selection_generate import *
from ProcessData import *
from json_management import *
from telethon import TelegramClient, events, errors


client = TelegramClient('rozklad_bot', api_id, api_hash).start(bot_token=bot_token)

selected_buttons = []


@client.on(events.NewMessage(pattern="/admin"))
async def admin_command(event):
	if event.sender_id in await get_admin():
		message, buttons = await generate_menu("admin_buttons")
		await event.respond(message, buttons=buttons)
	else:
		await event.respond("Ви повинні бути адміністратором.")


@client.on(events.CallbackQuery(data=b"adminback"))
async def admin_comands(event):
	message, buttons = await generate_menu("admin_buttons")
	await event.edit(message, buttons=buttons)


@client.on(events.CallbackQuery(data=b"removegroup"))
async def readg(event):
	await second_key_button_gen(event, "remove0")


@client.on(events.CallbackQuery(data=b"addgroup"))
async def readg(event):
	await second_key_button_gen(event, "add0")


@client.on(events.CallbackQuery(data=b"removeadmin"))
async def readg(event):
	await admin_gen(event, "removeadmin*")


@client.on(events.NewMessage(pattern='/start'))
async def changer(event):
	user = await event.get_chat()
	await collect_data(user.id)
	message, buttons = await generate_menu("menu")
	await event.respond(message, buttons=buttons)


@client.on(events.CallbackQuery(data=b"back"))
async def changer(event):
	message, buttons = await generate_menu("menu")
	await event.edit(message, buttons=buttons)


@client.on(events.CallbackQuery(data=b"user_gen"))
async def users(event):
	await users_gen(event)


@client.on(events.CallbackQuery(data=b"call_schedule"))
async def call_run(event):
	await call_schedule(event, call)


@client.on(events.CallbackQuery(data=b"schedule_changes"))
async def schedul(event):
	await schedule_changes(event)


@client.on(events.CallbackQuery(data=b"schedule_of_couples"))
async def facultet_k(event):
	message, buttons = await generate_menu("kurs")
	await event.edit(message, buttons=buttons)


@client.on(events.CallbackQuery(data=b"2k"))
async def facultet_2k(event):
	await facultet_k_selected(event, 2)


@client.on(events.CallbackQuery(data=b"3k"))
async def facultet_3k(event):
	await facultet_k_selected(event, 3)


@client.on(events.CallbackQuery(data=b"4k"))
async def facultet_4k(event):
	await facultet_k_selected(event, 4)


@client.on(events.CallbackQuery(data=b"1k"))
async def kurs1_group_selector(event):
	groups1k = await read_group("groups_1k", "groups1k")
	await kurs1_select_group(event, groups1k)


@client.on(events.CallbackQuery(data=b"2kProg"))
async def kurs2_prog_group_selector(event):
	groups2kprog = await read_group("groups_prog", "groups2kprog")
	await anykurs_select_group(event, "2", groups2kprog, "Prog")


@client.on(events.CallbackQuery(data=b"3kProg"))
async def kurs3_prog_group_selector(event):
	groups3kprog = await read_group("groups_prog", "groups3kprog")
	await anykurs_select_group(event, "3", groups3kprog, "Prog")


@client.on(events.CallbackQuery(data=b"4kProg"))
async def kurs4_prog_group_selector(event):
	groups4kprog = await read_group("groups_prog", "groups4kprog")
	await anykurs_select_group(event, "4", groups4kprog, "Prog")


@client.on(events.CallbackQuery(data=b"2kMex"))
async def kurs2_mex_group_selector(event):
	groups2kmex = await read_group("groups_mex", "groups2kmex")
	await anykurs_select_group(event, "2", groups2kmex, "Mex")


@client.on(events.CallbackQuery(data=b"3kMex"))
async def kurs3_mex_group_selector(event):
	groups3kmex = await read_group("groups_mex", "groups3kmex")
	await anykurs_select_group(event, "3", groups3kmex, "Mex")


@client.on(events.CallbackQuery(data=b"4kMex"))
async def kurs4_mex_group_selector(event):
	groups4kmex = await read_group("groups_mex", "groups4kmex")
	await anykurs_select_group(event, "4", groups4kmex, "Mex")


@client.on(events.CallbackQuery(data=b"2kEconom"))
async def kurs2_econom_group_selector(event):
	groups2keconom = await read_group("groups_econom", "groups2keconom")
	await anykurs_select_group(event, "2", groups2keconom, "Econom")


@client.on(events.CallbackQuery(data=b"3kEconom"))
async def kurs3_econom_group_selector(event):
	groups3keconom = await read_group("groups_econom", "groups3keconom")
	await anykurs_select_group(event, "3", groups3keconom, "Econom")


@client.on(events.CallbackQuery(data=b"4kEconom"))
async def kurs4_econom_group_selector(event):
	groups4keconom = await read_group("groups_econom", "groups4keconom")
	await anykurs_select_group(event, "4", groups4keconom, "Econom")


async def collect_data(user_id):
	user = await client.get_entity(user_id)
	if user.id in await get_admin():
		admin = True
	else:
		admin = False
	block = False
	try:
		message = await client.send_message(user_id, ".", silent=True)
		await  asyncio.sleep(0.5)
		await client.delete_messages(user_id, message)
	except errors.UserIsBlockedError:
		block = True
	data = {
		"id": str(user.id),
		'username': user.username,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'phone': user.phone,
		'admin': admin,
		"bot_blocked": block
	}
	await write_data_to_json(data)


@client.on(events.CallbackQuery())
async def autlog(event):
	button_id = event.data.decode("utf-8")
	user = event.sender
	print(f"{user.id}({user.username}) {button_id}")


@client.on(events.CallbackQuery())
async def button_click(event):
	button_id = event.data.decode("utf-8")
	try:
		button_id1 = button_id.split(".", 1)[1]
		if button_id1 in await read_type_group("groups_prog"):
			await process_data_prog(event, button_id1)
		elif button_id1 in await read_type_group("groups_mex"):
			await process_data_mex(event, button_id1)
		elif button_id1 in await read_type_group("groups_econom"):
			await process_data_econom(event, button_id1)
		elif button_id1 in await read_type_group("groups_1k"):
			await process_data_1k(event, int(button_id1))
		else:
			return None
	except:
		return None


@client.on(events.CallbackQuery())
async def button_click_group_hadler(event):
	button_id = event.data.decode("utf-8")
	if 'remove0' in button_id:
		button_id0, button_id1 = button_id.split("0", 1)
		await groups_gen(event, button_id1)
	if "removegroup0" in button_id:
		button_id0, button_id1, button_id2 = button_id.split("0", 2)
		respond = await remove_group_by_second_key(button_id1, button_id2)
		if respond == True:
			await event.respond(f"Групу {button_id2} видалено")
		else:
			await event.respond(f"Групу {button_id2} не видалено")
	if "add0" in button_id:
		button_id0, button_id1 = button_id.split("0", 1)
		await read_respond_for_group(event, button_id1)
	else:
		return None


@client.on(events.CallbackQuery())
async def button_click_admin_hadler(event):
	button_id = event.data.decode("utf-8")
	if "removeadmin*" in button_id:
		button_id0, button_id1 = button_id.split("*", 1)
		messege = await remove_admin_by_key("admins", int(button_id1))
		await event.respond(messege)
	if "addadmin" in button_id:
		await read_respond_for_admin(event)
	else:
		return None


async def read_respond_for_group(event, key):
	try:
		async with event.client.conversation(event.chat_id) as conv:
			await conv.send_message('Введіть групу')
			response = await conv.get_response()
			allow_response = response.message
			ret = await add_group_by_second_key(key, allow_response)
			if ret == True:
				await event.respond(f"Групу {allow_response} успішно додано")
			else:
				await event.respond(f"Групу {allow_response} не додано")
	except:
		await event.respond(f"Сталася помилка")


async def read_respond_for_admin(event):
	try:
		async with event.client.conversation(event.chat_id) as conv:
			await conv.send_message('Введіть адміна')
			response = await conv.get_response()
			allow_response = response.message
			user = await client.get_entity(allow_response)
			user_id = user.id
			ret = await add_admin_by_key("admins", user_id)
			await event.respond(ret)
	except:
		await event.respond(f"Сталася помилка")


@client.on(events.CallbackQuery(data=b"feedback"))
async def feedback(event):
	user = await event.get_chat()
	username = user.username
	try:
		async with client.conversation(event.chat_id) as conv:
			await conv.send_message("Надішліть повідомлення розробнику (тільки текст і емодзі)")
			response = await conv.get_response()
			allow_response = response.message

			buttons = [
				Button.inline("прочитати повідомлення", b"read_message")
			]

			await write_to_json_file(username, allow_response)
			await client.send_message(737208079, "У вас нове повідомлення", buttons=buttons)
			await event.respond("Повідомлення успішно надіслано")
	except TimeoutError:
		await event.respond("Сталася помилка:\n час очкування вичерпано")


@client.on(events.CallbackQuery(data=b"read_message"))
async def read_m(event):
	async for item in read_from_json_file():
		await event.respond(str(item), link_preview=False)


def auth_filter(event):
	return event.data.startswith(b"user.")


@client.on(events.CallbackQuery(func=auth_filter))
async def user_handler(event):
	button_id = event.data.decode("utf-8")
	user_id = button_id.split(".", 1)[1]
	await collect_data(int(user_id))

	data = await get_data_by_id(user_id)
	data.update({
		"username": f"[{data['username']}](https://t.me/{data['username']})"
	})
	allow_data = data.items()
	data_string = "\n".join([f"{key}: {value}" for key, value in data.items()])

	buttons = [
		[Button.inline("Повернутись", b"user_gen")]
	]

	if not data.get("bot_blocked", False):
		buttons.insert(0, [Button.inline("надіслати повідомлення", f"send|{data['id']}")])

	await event.edit(data_string, buttons=buttons, link_preview=False)


@client.on(events.CallbackQuery())
async def send_message(event):
	if "|" in event.data.decode("utf-8"):
		user_id = event.data.decode("utf-8").split("|", 1)[1]
		try:
			async with client.conversation(event.chat_id) as conv:
				await conv.send_message("напишіть повідомлення(текст і емодзі)")
				response = await conv.get_response()
				allow_response = response.message
				try:
					await client.send_message(int(user_id), allow_response)
				except:
					await event.respond("Неможливо надіслати повідомлення")
					raise events.StopPropagation
				await event.respond("Повідомлення успішно надіслано")
		except TimeoutError:
			await event.respond("Сталася помилка:\n час очкування вичерпано")


@client.on(events.CallbackQuery(data=b"cras"))
async def cras(event):
	with open('photo.jpg', 'rb') as photo_file:
		buttons = [[Button.url("Телеграм акули", "https://t.me/KasandrikOfficial")],
				   [Button.inline("Повернутись", b"delete")]
				   ]
		await event.respond("Акула технаря прямо зараз у вас на екрані", file=photo_file, buttons=buttons)


@client.on(events.CallbackQuery(data=b"delete"))
async def sdf(event):
	await event.delete()


@client.on(events.NewMessage(pattern="/getinfo"))
async def info(event):
	mass = event.message
	massage = mass.text
	username = massage.split(" ", 1)[1]
	await collect_data(username)


@client.on(events.CallbackQuery(data=b"advertisement"))
async def advertisement(event):
	data = await get_data()
	buttons = []

	for user_id, user_data in data.items():
		first_name = user_data.get('first_name')
		bot_blocked = user_data.get('bot_blocked', False)
		if bot_blocked:
			continue

		button_text = f"{user_id} ({first_name})"
		button_data = f"{user_id}"
		button = Button.inline(button_text, button_data.encode('utf-8'))

		if user_id in selected_buttons:
			checkmark_button = Button.inline("✅", f"uncheck.{user_id}".encode('utf-8'))
		else:
			checkmark_button = Button.inline("❌", f"check.{user_id}".encode('utf-8'))
		buttons.append([button, checkmark_button])

	buttons.append([Button.inline("Підтвердити", b"confirm")])
	buttons.append([Button.inline("Повернутись", b"adminback")])

	await event.edit("Оберіть користувачів для оголошення", buttons=buttons)


@client.on(events.CallbackQuery(pattern=r"(un)?check\.\d+"))
async def handle_check(event):
	button_data = event.data.decode('utf-8')
	action, user_id = button_data.split('.', 1)

	if action == 'check':
		selected_buttons.append(user_id)

	elif action == 'uncheck':
		selected_buttons.remove(user_id)

	await advertisement(event)


@client.on(events.CallbackQuery(data=b"confirm"))
async def confirm_selection(event):
	await event.delete()
	if not selected_buttons:
		await event.respond('Список вибраних користувачів порожній')
	else:
		await send_advertisement(event)
		selected_buttons.clear()


async def send_advertisement(event):
	try:
		async with client.conversation(event.chat_id) as conv:
			await conv.send_message("напишіть повідомлення(текст і емодзі)")
			response = await conv.get_response()
			allow_response = response.message
			for user in selected_buttons:
				try:
					await client.send_message(int(user), allow_response)
				except:
					await event.respond(f"неможливо відправити повідомлення користувачу{user}")
			await event.respond('Оголошення надіслано')
	except TimeoutError:
		await event.respond("час очікування вичерпано")
		raise events.StopPropagation


@client.on(events.NewMessage(pattern="/info"))
async def info(event):
	users = await read_first_level_keys()
	for user in users:
		try:
			await collect_data(int(user))
		except:
			await event.respond(f"Не вдалося отриамти данні користувача {user}")
	await event.respond("Всі данні отримано")


@client.on(events.NewMessage(pattern="/change_photo", from_users=[875709589, 737208079]))
async def photo_changer(event):
	try:
		async with client.conversation(event.chat_id) as conv:
			await conv.send_message("Надішліть фото(тільки одне)")

			while True:
				response = await conv.get_response()

				if response.photo:
					allow_response = response.photo
					try:
						await client.download_media(allow_response, file="photo.jpg")
					except:
						await event.respond("Неможливо зберегти фото")
						raise events.StopPropagation
					await event.respond("Фото успішно збережено")
					break

				await event.respond("Будь-ласка, надішліть тільки фото\n Спробуйте ще раз")
	except TimeoutError:
		await event.respond("Сталася помилка:\n Час очікування вичерпано")


client.run_until_disconnected()
