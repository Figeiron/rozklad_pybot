from json_management import get_admin



async def admin_handler(event):
	message = "Ви повинні бути адміністраторм для виконання цієї команди"
	user = await event.get_chat()
	username = user.username
	if username in await get_admin("admins"):
		return True
	else:
		return message
