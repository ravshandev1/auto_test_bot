import requests
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from states import Register, Feedback, Subscribe
from config import get_user_lang, append_user, API, set_users, bot
from keyboards import main_btn, lang_btn, phone_btn, back_btn, pay_btn

router = Router()


@router.message(F.text == '/start')
async def start(mes: types.Message, state: FSMContext):
    res = requests.get(url=f"{API}/user/{mes.from_user.id}/")
    if res.status_code == 200:
        r = requests.get(url=f"{API}/information/")
        r = r.json()
        if get_user_lang(mes.from_user.id) == 'uz':
            await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_uz'],
                                   reply_markup=main_btn('uz', mes.from_user.id))
        else:
            await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_ru'],
                                   reply_markup=main_btn('ru', mes.from_user.id))
    elif res.status_code == 404:
        await mes.answer(
            f"Ассалому алайкум, {mes.from_user.full_name}!\nАвтошкола тестга хуш келибсиз\nВыберите язык / Тилни танланг",
            reply_markup=lang_btn)
        await state.set_state(Register.lang)
    else:
        await mes.answer("Server ishlamayabdi\nСервер не работает")


@router.callback_query(Register.lang)
async def lang(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    append_user({'telegram_id': call.from_user.id, 'lang': call.data})
    if call.data == 'uz':
        await call.message.answer("Исм фамилиянгизни киритинг.")
    elif call.data == 'ru':
        await call.message.answer("Введите свое имя и фамилию.")
    await state.update_data({'lang': call.data, 'telegram_id': call.from_user.id})
    await state.set_state(Register.name)
    await call.answer(cache_time=1)


@router.message(Register.name)
async def name(mes: types.Message, state: FSMContext):
    await state.update_data({'name': mes.text})
    if get_user_lang(mes.from_user.id) == 'uz':
        await mes.answer("Телефон рақамингизни юборинг.", reply_markup=phone_btn('uz'))
    else:
        await mes.answer("Пришлите свой номер телефона.", reply_markup=phone_btn('ru'))
    await state.set_state(Register.phone_number)


@router.message(Register.phone_number)
async def phone(mes: types.Message, state: FSMContext):
    r = requests.get(url=f"{API}/information/")
    r = r.json()
    data = await state.get_data()
    if mes.contact:
        data['phone_number'] = mes.contact.phone_number
    else:
        data['phone_number'] = mes.text
    res = requests.post(url=f"{API}/", data=data)
    if res.status_code == 200:
        if get_user_lang(mes.from_user.id) == 'uz':
            await mes.answer("Assalomu alaykum", reply_markup=main_btn('uz', mes.from_user.id))
            await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_uz'],
                                   reply_markup=main_btn('uz', mes.from_user.id))
        else:
            await mes.answer("Здравствуйте", reply_markup=main_btn('ru', mes.from_user.id))
            await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_ru'],
                                   reply_markup=main_btn('ru', mes.from_user.id))
    else:
        await mes.answer("Xato\nОшибка")
    await state.clear()


@router.callback_query(F.data.in_(['uz', 'ru']))
async def set_lang(call: types.CallbackQuery):
    r = requests.patch(url=f"{API}/", data={'telegram_id': call.from_user.id, 'lang': call.data})
    if r.status_code == 200:
        set_users(r.json())
    r = requests.get(url=f"{API}/information/")
    r = r.json()
    if call.data == 'uz':
        await call.message.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_uz'],
                                        reply_markup=main_btn('uz', call.from_user.id))
    else:
        await call.message.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_ru'],
                                        reply_markup=main_btn('ru', call.from_user.id))
    await call.answer(cache_time=1)


@router.message(F.text.in_(["🔄 Изменение языка", "🔄 Тилни алмаштириш"]))
async def change_lang(mes: types.Message):
    await mes.answer("Выберите язык / Тилни танланг", reply_markup=lang_btn)


@router.message(F.text.in_(["✍️ Мурожат қилинг!", "✍️ Обращайтесь!"]))
async def feedback(mes: types.Message, state: FSMContext):
    if mes.text == "✍️ Мурожат қилинг!":
        await mes.answer(
            "Ушбу бўлимда Сиз Тест саволлари бўйича мурожат қилишингиз мумкин!\nЎрганишингизга қийин бўлган Тест саволи бўйича бизга мурожат қилишингиз мумкин!\nХабар ёзганингизда Сизга мурожат қила олишимиз учун ўз телефон рақамингизни ҳам ёзиб қолдиринг!",
            reply_markup=back_btn('uz'))
    else:
        await mes.answer(
            "В этом разделе Вы сможете обратиться по вопросам тестов!\nВы можете обратиться по тестовым вопросам который Вам непонятно!\nЧтобы мы смогли Вам обратиться не забудьте написать свои контакты!",
            reply_markup=back_btn('ru'))
    await state.set_state(Feedback.text)


@router.message(Feedback.text)
async def feedback_text(mes: types.Message, state: FSMContext):
    r = requests.get(url=f"{API}/information/")
    r = r.json()
    if (mes.text != "🔙 Ортга") and (mes.text != "🔙 Назад"):
        requests.post(url=f"{API}/feedback/{mes.from_user.id}/", data={'message': mes.text})
        if get_user_lang(mes.from_user.id) == 'uz':
            await mes.answer("✅ Хабар юборилди, этиборингиз учун рахмат.")
        else:
            await mes.answer("✅ Сообщение отправлено, спасибо за внимание.")
    if get_user_lang(mes.from_user.id) == 'uz':
        await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_uz'],
                               reply_markup=main_btn('uz', mes.from_user.id))
    else:
        await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_ru'],
                               reply_markup=main_btn('ru', mes.from_user.id))
    await state.clear()


@router.message(F.text.in_(["🗓 Обунани активлаштиринг", "🗓 Активируйте подписку"]))
async def edit_profile(mes: types.Message, state: FSMContext):
    r = requests.get(url=f"{API}/check/{mes.from_user.id}/")
    rates = requests.get(url=f"{API}/rates/")
    markup = ReplyKeyboardBuilder()
    if get_user_lang(mes.from_user.id) == 'uz':
        for i in rates.json():
            markup.button(text=i['name_uz'])

        markup.button(text="🔙 Ортга")
        markup.adjust(1, 1, 1, 1)
        if r.status_code == 400:
            await mes.answer(
                "Хозирча обунангиз актив холатда эмас.\nОбунангизни активлаштириш учун қуйидаги тарифлардан бирини танланг:",
                reply_markup=markup.as_markup(resize_keyboard=True))
        elif r.status_code == 200:
            await mes.answer(
                f"Сизнинг обунангиз: {r.json()['end_at']} гача амал қилади:\nУзайтирмоқчи бўлсангиз қуйидаги тарифлардан бирини танланг:",
                reply_markup=markup.as_markup(resize_keyboard=True))
        else:
            await mes.answer("Xato")
    else:
        for i in rates.json():
            markup.button(text=i['name_ru'])
        markup.button(text="🔙 Назад")
        markup.adjust(1, 1, 1, 1)
        if r.status_code == 400:
            await mes.answer(
                "Ваша подписка в настоящее время неактивна.\nЧтобы активировать подписку, выберите один из следующих тарифов:",
                reply_markup=markup.as_markup(resize_keyboard=True))
        elif r.status_code == 200:
            await mes.answer(
                f"Ваша подписка годен до: {r.json()['end_at']}\nЕсли вы хотите продлить, выберите один из следующих тарифов:",
                reply_markup=markup.as_markup(resize_keyboard=True))
        else:
            await mes.answer("Ошибка")
    await state.set_state(Subscribe.rate)


@router.message(Subscribe.rate)
async def buy_rate(mes: types.Message, state: FSMContext):
    r = requests.get(url=f"{API}/information/")
    r = r.json()
    if mes.text == "🔙 Ортга":
        await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_uz'],
                               reply_markup=main_btn('uz', mes.from_user.id))
        await state.clear()
    elif mes.text == "🔙 Назад":
        await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_ru'],
                               reply_markup=main_btn('ru', mes.from_user.id))
        await state.clear()
    else:
        rates = requests.get(url=f"{API}/rates/")
        for i in rates.json():
            if i['name_uz'] == mes.text or i['name_ru'] == mes.text:
                await state.update_data({'name': mes.text, 'price': i['price'], 'id': i['id']})
        payment_types = requests.get(url=f"{API}/payment-types/")
        markup = ReplyKeyboardBuilder()
        for i in payment_types.json():
            markup.button(text=i['name'])
        markup.adjust(2)
        if get_user_lang(mes.from_user.id) == 'uz':
            markup.button(text="🔙 Ортга")
            await mes.answer("Тўлов усулини танланг:",
                             reply_markup=markup.as_markup(resize_keyboard=True))
        else:
            markup.button(text="🔙 Назад")
            await mes.answer("Выберите способ оплаты:",
                             reply_markup=markup.as_markup(resize_keyboard=True))
        await state.set_state(Subscribe.payment_type)


@router.message(Subscribe.payment_type)
async def payment_type(mes: types.Message, state: FSMContext):
    if mes.text == "🔙 Ортга":
        r = requests.get(url=f"{API}/check/{mes.from_user.id}/")
        rates = requests.get(url=f"{API}/rates/")
        markup = ReplyKeyboardBuilder()
        for i in rates.json():
            markup.button(text=i['name_uz'])
        markup.button(text="🔙 Ортга")
        if r.status_code == 400:
            await mes.answer(
                "Хозирча обунангиз актив холатда эмас.\nОбунангизни активлаштириш учун қуйидаги тарифлардан бирини танланг:",
                reply_markup=markup.as_markup(resize_keyboard=True))
        elif r.status_code == 200:
            await mes.answer(
                f"Сизнинг обунангиз: {r.json()['end_at']} гача амал қилади:\nУзайтирмоқчи бўлсангиз қуйидаги тарифлардан бирини танланг:",
                reply_markup=markup.as_markup(resize_keyboard=True))
        else:
            await mes.answer("Xato")
        await state.set_state(Subscribe.rate)
    elif mes.text == "🔙 Назад":
        r = requests.get(url=f"{API}/check/{mes.from_user.id}/")
        rates = requests.get(url=f"{API}/rates/")
        markup = ReplyKeyboardBuilder()
        for i in rates.json():
            markup.button(text=i['name_ru'])
        markup.button(text="🔙 Назад")
        if r.status_code == 400:
            await mes.answer(
                "Ваша подписка в настоящее время неактивна.\nЧтобы активировать подписку, выберите один из следующих тарифов:",
                reply_markup=markup.as_markup(resize_keyboard=True))
        elif r.status_code == 200:
            await mes.answer(
                f"Ваша подписка годен до: {r.json()['end_at']}\nЕсли вы хотите продлить, выберите один из следующих тарифов:",
                reply_markup=markup.as_markup(resize_keyboard=True))
        else:
            await mes.answer("Ошибка")
        await state.set_state(Subscribe.rate)
    else:
        payment_types = requests.get(url=f"{API}/payment-types/")
        data = await state.get_data()
        for i in payment_types.json():
            if i['name'] == mes.text:
                data['token'] = i['token']
                data['p_name'] = i['name']
                await state.update_data({'provider_id': i['id']})
        if get_user_lang(mes.from_user.id) == 'uz':
            title = f"{data['name']} учун тўлов"
            description = f"{data['name']} учун {data['price']} сўм тўловни {data['p_name']} орқали тўлаш учун ҳисоб"

        else:
            title = f"{data['name']} оплата за"
            description = f"{data['name']} за {data['price']} оплата сум {data['p_name']} счет для оплаты"
        await mes.answer(title, reply_markup=types.ReplyKeyboardRemove())
        summa = types.LabeledPrice(label=title, amount=int(data['price']) * 100)
        await bot.send_invoice(
            mes.chat.id,
            title=title,
            description=description,
            payload='INVOICE',
            provider_token=data['token'],
            currency='UZS',
            prices=[summa],
            reply_markup=pay_btn(get_user_lang(mes.from_user.id)),
        )
        await state.set_state(Subscribe.checkout)


@router.pre_checkout_query(Subscribe.checkout, lambda query: True)
async def pre_checkout_query(query: types.PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(query.id, ok=True)
    await state.set_state(Subscribe.success)


@router.message(Subscribe.success)
async def successful_payment(mes: types.Message, state: FSMContext):
    await mes.delete()
    data = await state.get_data()
    pay = requests.post(url=f"{API}/buy/{mes.from_user.id}/",
                        data={"id": data['id'], 'provider_id': data['provider_id']})
    r = requests.get(url=f"{API}/information/")
    r = r.json()
    if get_user_lang(mes.from_user.id) == 'uz':
        await mes.answer(f"✅Табриклаймиз! Сизнинг обунангиз {pay.json()['end_at']} гача актив")
        await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_uz'],
                               reply_markup=main_btn('uz', mes.from_user.id))
    else:
        await mes.answer(f"✅Поздравляю! Ваша подписка активна до {pay.json()['end_at']}")
        await mes.answer_photo(photo=types.FSInputFile(r['image']), caption=r['text_ru'],
                               reply_markup=main_btn('ru', mes.from_user.id))
    await state.clear()


@router.callback_query(F.data == '❌')
async def back(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    payment_types = requests.get(url=f"{API}/payment-types/")
    markup = ReplyKeyboardBuilder()
    for i in payment_types.json():
        markup.button(text=i['name'])
    markup.adjust(2)
    if get_user_lang(call.from_user.id) == "uz":
        markup.button(text="🔙 Ортга")
        await call.message.answer("Тўлов усулини танланг:", reply_markup=markup.as_markup(resize_keyboard=True))
    else:
        markup.button(text="🔙 Назад")
        await call.message.answer("Выберите способ оплаты:", reply_markup=markup.as_markup(resize_keyboard=True))
    await state.set_state(Subscribe.payment_type)
    await call.answer(cache_time=1)
