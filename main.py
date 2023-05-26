from config import *
from selection_generate import *
from ProcessData import *
from json_management import *
from telethon import TelegramClient, events
from functions import *
from telethon.tl.custom.conversation import Conversation

client = TelegramClient('rozklad_bot', api_id, api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage(pattern="/admin"))
async def admin_comands(event):
	resp = await admin_handler(event)
	if resp == True:
		message, buttons = await generate_menu("admin_buttons")
		await event.respond(message, buttons=buttons)
	else:
		await event.respond(resp)


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
	await admin_gen(event, "removeadmin0")


@client.on(events.NewMessage(pattern='/start'))
async def changer(event):
	message, buttons = await generate_menu("menu")
	await user_handler(event)
	await event.respond(message, buttons=buttons)


@client.on(events.CallbackQuery(data=b"back"))
async def changer(event):
	message, buttons = await generate_menu("menu")
	await event.edit(message, buttons=buttons)


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


@client.on(events.CallbackQuery())
async def button_click(event):
	button_id = event.data.decode("utf-8")
	if '.' in button_id:
		button_id0, button_id1 = button_id.split(".", 1)
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
		return None


@client.on(events.CallbackQuery())
async def button_click_group_hadler(event):
	button_id = event.data.decode("utf-8")
	user = await event.get_chat()
	username = user.username
	print(username, button_id)
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
	if "removeadmin0" in button_id:
		button_id0, button_id1 = button_id.split("0", 1)
		messege = await remove_admin_by_key("admins", button_id1)
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
	except Exception as error:
		await event.respond(f"Сталася помилка")


async def read_respond_for_admin(event):
	try:
		async with event.client.conversation(event.chat_id) as conv:
			await conv.send_message('Введіть адміна')
			response = await conv.get_response()
			allow_response = response.message
			ret = await add_admin_by_key("admins", allow_response)
			if ret == True:
				await event.respond(f"Адміністратора {allow_response} успішно додано")
			else:
				await event.respond(f"Адміністратора {allow_response} не додано")
	except Exception as error:
		await event.respond(f"Сталася помилка")


@client.on(events.CallbackQuery(data=b"feedback"))
async def feedback(event):
	user = await event.get_chat()
	username = user.username
	async with event.client.conversation(event.chat_id) as conv:
		await conv.send_message("Надішліть повідомлення розробнику(тіко текст!!!!!!!!!!!!)")
		response = await conv.get_response()
		allow_response = response.message
		await  client.send_message("DeD_Innnsultickkkkk", f"Користувач:\n {username}\n повідомлення:\n {allow_response}")
		await event.respond("Повідомлення успішшно надіслано")


client.run_until_disconnected()
