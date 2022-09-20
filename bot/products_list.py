from aiogram.utils.markdown import hide_link

available_products = {
    "sleds": {
        "name": "Сани",
        "description": f"<b>Сани</b>\n"
                       "Санки (или сани) – это древнейшее транспортное средство, представляющее собой повозку с полозьями. "
                       "Полозья крепились с одной стороны к саням, с другой – к лошадям, быкам или собакам."
                       f"{hide_link('https://static.3dbaza.com/models/117899/215256776d9c4d998ecffa7c.jpg')}\n\n"
                       "Цена: <b>40</b>",
        "price": 40,
        "logo": "https://static.3dbaza.com/models/117899/215256776d9c4d998ecffa7c.jpg"
    },
    "skis": {
        "name": "Лыжи",
        "description": f"<b>Лыжи</b>\n"
                       "Лыжи для человека представляют собой две длинные (150 — 220 сантиметров) деревянные или пластиковые планки с заострёнными и загнутыми носками."
                       "Лыжи крепятся к обуви с помощью креплений, в настоящее время для большинства креплений необходимы специальные лыжные ботинки. "
                       "Перемещение на лыжах использует их способность скользить по снегу. Лыжи также применяются на аэро и мотосанях, самолётах."
                       f"{hide_link('https://www.i-igrushki.ru/upload/iblock/ae3/ae33911e7a4f5aa2ea81acbb22bc818d.jpg')}\n\n"
                       "Цена: <b>50</b>",
        "price": 50,
        "logo": "https://www.i-igrushki.ru/upload/iblock/ae3/ae33911e7a4f5aa2ea81acbb22bc818d.jpg"
    },
    "pedals": {
        "name": "Педали",
        "description": f"<b>Педали</b>\n"
                       "Педали крепятся к шатунам и передают усилие от ноги на трансмиссию велосипеда. "
                       "От качества педалей зависит, как процент передаваемого усилия и КПД педалирования, "
                       "так и ваша безопасность, управляемость и контроль велосипеда в целом."
                       f"{hide_link('https://skltn.ru/uploads/source/products/1624275432-311.jpg')}\n\n"
                       "Цена: <b>60</b>",
        "price": 60,
        "logo": "https://skltn.ru/uploads/source/products/1624275432-311.jpg"
    },
    "wheels": {
        "name": "Колёса",
        "description": f"<b>Колесо</b>\n"
                       "Колесо́ — движитель, свободно вращающийся или закреплённый на вращающейся оси диск, "
                       "позволяющий поставленному на него телу катиться, а не скользить."
                       f"{hide_link('https://skltn.ru/uploads/source/products/1624275432-311.jpg')}\n\n"
                       "Цена: <b>60</b>",
        "price": 70,
        "logo": "https://homeandgarden.store/image/catalog/1dasd/katalogi/kolesadljasadovo-stroitelnyhtachekigruzovyhtelezhek.jpg"
    },
}