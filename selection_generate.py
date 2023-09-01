from telethon import Button
from json_management import *


# генерація вибору напрямку
async def facultet_k_selected(event, course_number):
    button_fk = [
        [Button.inline("Програмування", f"{course_number}kProg")],
        [Button.inline("Економіка", f"{course_number}kEconom")],
        [Button.inline("Механіка", f"{course_number}kMex")],
        [Button.inline("Повернутись", b"back")]
    ]
    message_fk = f"Напрямки {course_number} курсу"
    await event.edit(message_fk, buttons=button_fk)


# генерація кнопк для всіх груп окрім першого курсу
async def anykurs_select_group(event, course_number, groups, course_type):
    buttons = [[Button.inline(f"Група {group}", f"{course_number}k{course_type}." + group)] for group in groups] + [
        [Button.inline("Повернутись", f"{course_number}k")]
    ]

    message = "Оберіть групу:"
    await event.edit(message, buttons=buttons)


# генерація кнопок груп першого курсу
async def kurs1_select_group(event, groups):
    buttons = [[Button.inline(f"Група {group}", b"1k." + group.encode('utf-8'))] for group in groups] + [
        [Button.inline("Повернутись", b"schedule_of_couples")]
    ]

    message = "Оберіть групу:"
    await event.edit(message, buttons=buttons)


# генерація кнопок підгруп для видалення
async def second_key_button_gen(event, process_type):
    keys = await read_second_key()
    buttons = [[Button.inline(f"{key}", f"{process_type}{key}")] for key in keys] + [
        [Button.inline("Повернутись", b"adminback")]
    ]

    message = "Оберіть підгрупу:"
    await event.edit(message, buttons=buttons)


async def groups_gen(event, group_key):
    keys = await get_groups_by_second_key(group_key)
    buttons = [[Button.inline(f"{key}", f"removegroup0{group_key}0{key}")] for key in keys] + [
        [Button.inline("Повернутись", b"adminback")]
    ]

    message = "Оберіть групу для видалення:"
    await event.edit(message, buttons=buttons)


# генерація кнопок адмінів
async def admin_gen(event, process_type):
    keys = await get_admin()
    buttons = [[Button.inline(f"{key}", f"{process_type}{key}")] for key in keys if key != 737208079] + [
        [Button.inline("Повернутись", b"adminback")]
    ]

    message = "Оберіть адміністратора для видалення"
    await event.edit(message, buttons=buttons)


# генерація кнопок користувачів
async def users_gen(event):
    data = await get_data()
    buttons = []

    for user_id, user_data in data.items():
        first_name = user_data.get('first_name')
        button_text = f"{user_id} ({first_name})"
        button_data = f"user.{user_id}"
        button = Button.inline(button_text, button_data.encode('utf-8'))
        buttons.append([button])

    buttons.append([Button.inline("Повернутись", b"adminback")])

    message = "Оберіть користувача:"
    await event.edit(message, buttons=buttons)


# генерація розкладу дзвінків
async def call_schedule(event, call):
    message = call
    buttons = [
        [Button.inline("Повернутись", b"back")]
    ]
    await event.edit(message, buttons=buttons)


# генерація кнопок меню
async def generate_menu(menu):
    if menu == "menu":
        buttons = [
            [Button.inline("Розклад дзвінків", b"call_schedule")],
            [Button.inline("Розклад пар", b"schedule_of_couples")],
            [Button.inline("Зміни у розкладі", b"schedule_changes")],
            [Button.inline("Акула технаря", b"cras")],
            [Button.inline("Звортній звязок з розробником", b"feedback")]
        ]
        message = "Чим можу допомогти?"
        return message, buttons
    elif menu == "back":
        buttons = [
            [Button.inline("Повернутись", data=b"back")]
        ]
        return buttons
    elif menu == "kurs":
        buttons = [
            [Button.inline("1", b"1k")],
            [Button.inline("2", b"2k")],
            [Button.inline("3", b"3k")],
            [Button.inline("4", b"4k")],
            [Button.inline("Повернутись", b"back")]
        ]
        message = "Оберіть курс"
        return message, buttons
    elif menu == "admin_buttons":
        buttons = [
            [Button.inline("Додати адміністратора", b"addadmin")],
            [Button.inline("Виділити адміністратора", b"removeadmin")],
            [Button.inline("Додати групу", b"addgroup")],
            [Button.inline("Видалити групу", b"removegroup")],
            [Button.inline("Користувачі", b"user_gen")],
            [Button.inline("Зробити оголошення", b"advertisement")]
        ]
        message = "Оберіть опцію"
        return message, buttons
    else:
        return None
