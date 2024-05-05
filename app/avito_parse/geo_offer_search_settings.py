from typing import NamedTuple, Optional

DEFAULT_CITY_URL_SLUG = "moskva"
DEFAULT_CITY = "Москва"
DEFAULT_SEARCH_RADIUS = 200

RU_CITIES_URL_SLUGS = {DEFAULT_CITY: DEFAULT_CITY_URL_SLUG, "Челябинск": "chelyabinsk", 'Абаза': 'abaza', 'Абакан': 'abakan', 'Абдулино': 'abdulino', 'Абинск': 'abinsk', 'Агидель': 'agidel', 'Агрыз': 'agryz', 'Адыгейск': 'adygeysk', 'Азнакаево': 'aznakaevo', 'Азов': 'azov', 'Ак-Довурак': 'ak-dovurak', 'Аксай': 'aksai', 'Алагир': 'alagir', 'Алапаевск': 'alapaevsk', 'Алатырь': 'alatyr', 'Алдан': 'aldan', 'Алейск': 'aleysk', 'Александров': 'aleksandrov', 'Александровск': 'aleksandrovsk', 'Александровск-Сахалинский': 'aleksandrovsk-sakhalinskii', 'Алексеевка': 'alekseevka', 'Алексин': 'aleksin', 'Алзамай': 'alzamay', 'Алупка': 'alupka', 'Алушта': 'alushta', 'Альметьевск': 'almetevsk', 'Амурск': 'amursk', 'Анадырь': 'anadyr', 'Анапа': 'anapa', 'Ангарск': 'angarsk', 'Андреаполь': 'andreapol', 'Анжеро-Судженск': 'anzhero-sudzhensk', 'Анива': 'aniva', 'Апатиты': 'apatity', 'Апрелевка': 'aprelevka', 'Апшеронск': 'apsheronsk', 'Арамиль': 'aramil', 'Аргун': 'argun', 'Ардатов': 'mordoviya_ardatov', 'Ардон': 'ardon', 'Арзамас': 'arzamas', 'Аркадак': 'arkadak', 'Армавир': 'armavir', 'Армянск': 'armyansk', 'Арсеньев': 'arsenev', 'Арск': 'arsk', 'Артем': 'artem', 'Артемовск': 'artemovsk', 'Артемовский': 'artemovskii', 'Архангельск': 'arkhangelsk', 'Асбест': 'asbest', 'Асино': 'asino', 'Астрахань': 'astrakhan', 'Аткарск': 'atkarsk', 'Ахтубинск': 'akhtubinsk', 'Ачинск': 'achinsk', 'Аша': 'asha', 'Бабаево': 'babaevo', 'Бабушкин': 'babushkin', 'Бавлы': 'bavly', 'Багратионовск': 'bagrationovsk', 'Байкальск': 'baikalsk', 'Баймак': 'baymak', 'Бакал': 'bakal', 'Баксан': 'baksan', 'Балабаново': 'balabanovo', 'Балаково': 'balakovo', 'Балахна': 'balakhna', 'Балашиха': 'balashikha', 'Балашов': 'balashov', 'Балей': 'balei', 'Балтийск': 'baltiisk', 'Барабинск': 'barabinsk', 'Барнаул': 'barnaul', 'Барыш': 'barysh', 'Батайск': 'bataysk', 'Бахчисарай': 'bahchysaray', 'Бежецк': 'bezhetsk', 'Белая Калитва': 'belaya-kalitva', 'Белая Холуница': 'belaya-kholunitsa', 'Белгород': 'belgorod', 'Белебей': 'belebei', 'Белев': 'belev', 'Белинский': 'belynsyy', 'Белово': 'belovo', 'Белогорск': 'belogorsk', 'Белозерск': 'belozersk', 'Белокуриха': 'belokurikha', 'Беломорск': 'belomorsk', 'Белоозерский': 'beloozerskii', 'Белорецк': 'beloretsk', 'Белореченск': 'belorechensk', 'Белоусово': 'belousovo', 'Белоярский': 'beloyarskii', 'Белый': 'belyy', 'Бердск': 'berdsk', 'Березники': 'berezniki', 'Березовский': 'berezovskii', 'Беслан': 'beslan', 'Бийск': 'biisk', 'Бикин': 'bikin', 'Билибино': 'bilibino', 'Биробиджан': 'birobidzhan', 'Бирск': 'birsk', 'Бирюсинск': 'biriusinsk', 'Бирюч': 'biriuch', 'Благовещенск': 'amurskaya_oblast_blagoveschensk', 'Благодарный': 'blagodarnyi', 'Бобров': 'bobrov', 'Богданович': 'bogdanovich', 'Богородицк': 'bogoroditsk', 'Богородск': 'bogorodsk', 'Боготол': 'bogotol', 'Богучар': 'boguchar', 'Бодайбо': 'bodaibo', 'Бокситогорск': 'boksitogorsk', 'Болгар': 'bolgar', 'Бологое': 'bologoe', 'Болотное': 'bolotnoe', 'Болохово': 'bolokhovo', 'Болхов': 'bolkhov', 'Большой Камень': 'bolshoy_kamen', 'Бор': 'bor', 'Борзя': 'borzya', 'Борисоглебск': 'borisoglebsk', 'Боровичи': 'borovichi', 'Боровск': 'borovsk', 'Бородино': 'borodino', 'Братск': 'bratsk', 'Бронницы': 'bronnitsy', 'Брянск': 'bryansk', 'Бугульма': 'bugulma', 'Бугуруслан': 'buguruslan', 'Буденновск': 'budennovsk', 'Бузулук': 'buzuluk', 'Буинск': 'buinsk', 'Буй': 'buy', 'Буйнакск': 'buinaksk', 'Бутурлиновка': 'buturlinovka', 'Валдай': 'valday', 'Валуйки': 'valuiki', 'Велиж': 'velizh', 'Великие Луки': 'velikie-luki', 'Великий Новгород': 'velikii-novgorod', 'Великий Устюг': 'velyyy_ustyug', 'Вельск': 'velsk', 'Венев': 'venev', 'Верещагино': 'vereshchagino', 'Верея': 'vereya', 'Верхнеуральск': 'verkhneuralsk', 'Верхний Тагил': 'verkhnii-tagil', 'Верхний Уфалей': 'verhnyy_ufaley', 'Верхняя Пышма': 'verkhnyaya-pyshma', 'Верхняя Салда': 'verhnyaya_salda', 'Верхняя Тура': 'verhnyaya_tura', 'Верхотурье': 'verhoture', 'Верхоянск': 'verkhoyansk', 'Весьегонск': 'vesegonsk', 'Ветлуга': 'vetluga', 'Видное': 'vidnoe', 'Вилюйск': 'viliuisk', 'Вилючинск': 'vylyuchynsk', 'Вихоревка': 'vikhorevka', 'Вичуга': 'vichuga', 'Владивосток': 'vladivostok', 'Владикавказ': 'vladikavkaz', 'Владимир': 'vladimir', 'Волгоград': 'volgograd', 'Волгодонск': 'volgodonsk', 'Волгореченск': 'volgorechensk', 'Волжск': 'volzhsk', 'Волжский': 'volzhskii', 'Вологда': 'vologda', 'Володарск': 'volodarsk', 'Волоколамск': 'volokolamsk', 'Волосово': 'volosovo', 'Волхов': 'volkhov', 'Волчанск': 'volchansk', 'Вольск': 'volsk', 'Воркута': 'vorkuta', 'Воронеж': 'voronezh', 'Ворсма': 'vorsma', 'Воскресенск': 'voskresensk', 'Воткинск': 'votkinsk', 'Всеволожск': 'vsevolozhsk', 'Вуктыл': 'vuktyl', 'Выборг': 'vyborg', 'Выкса': 'vyksa', 'Высоковск': 'vysokovsk', 'Высоцк': 'vysotsk', 'Вытегра': 'vytegra', 'Вышний Волочек': 'vyshnii-volochek', 'Вяземский': 'vyazemskii', 'Вязники': 'vyazniki', 'Вязьма': 'vyazma', 'Вятские Поляны': 'vyatskie_polyany', 'Гаврилов Посад': 'gavrylov_posad', 'Гаврилов-Ям': 'gavrylov_yam', 'Гагарин': 'gagarin', 'Гаджиево': 'gadzhyevo', 'Гай': 'gay', 'Галич': 'galich', 'Гатчина': 'gatchina', 'Гвардейск': 'gvardeysk', 'Гдов': 'gdov', 'Геленджик': 'gelendzhik', 'Георгиевск': 'georgyevs', 'Глазов': 'glazov', 'Голицыно': 'golytsyno', 'Горбатов': 'gorbatov', 'Горно-Алтайск': 'gorno_altaysk', 'Горнозаводск': 'gornozavodsk', 'Горняк': 'gornyak', 'Городец': 'gorodets', 'Городище': 'gorodyshche', 'Городовиковск': 'gorodovikovsk', 'Гороховец': 'gorokhovets', 'Горячий Ключ': 'goryachyy_klyuch', 'Грайворон': 'graivoron', 'Гремячинск': 'gremyachinsk', 'Грозный': 'groznyi', 'Грязи': 'gryazi', 'Грязовец': 'gryazovets', 'Губаха': 'gubakha', 'Губкин': 'gubkin', 'Губкинский': 'gubkinskii', 'Гудермес': 'gudermes', 'Гуково': 'gukovo', 'Гулькевичи': 'gulkevichi', 'Гурьевск': 'gurevsk', 'Гусев': 'gusev', 'Гусиноозерск': 'gusinoozersk', 'Гусь-Хрустальный': 'gus-hrustalnyy', 'Давлеканово': 'davlekanovo', 'Дагестанские Огни': 'dagestanskye_ogny', 'Далматово': 'dalmatovo', 'Дальнегорск': 'dalnegorsk', 'Дальнереченск': 'dalnerechensk', 'Данилов': 'danilov', 'Данков': 'dankov', 'Дегтярск': 'degtyarsk', 'Дедовск': 'dedovsk', 'Демидов': 'demidov', 'Дербент': 'derbent', 'Десногорск': 'desnogorsk', 'Джанкой': 'dzhankoi', 'Дзержинск': 'dzerzhinsk', 'Дзержинский': 'dzerzhinskii', 'Дивногорск': 'divnogorsk', 'Дигора': 'digora', 'Димитровград': 'dimitrovgrad', 'Дмитриев-Льговский': 'dmytryev_lgovskyy', 'Дмитров': 'dmitrov', 'Дмитровск': 'dmitrovsk', 'Дно': 'dno', 'Добрянка': 'dobryanka', 'Долгопрудный': 'dolgoprudnyy', 'Долинск': 'dolinsk', 'Домодедово': 'domodedovo', 'Донецк': 'donetsk', 'Донской': 'donskoi', 'Дорогобуж': 'dorogobuzh', 'Дрезна': 'drezna', 'Дубна': 'dubna', 'Дубовка': 'dubovka', 'Дудинка': 'dudinka', 'Духовщина': 'dukhovshchina', 'Дюртюли': 'diurtiuli', 'Дятьково': 'dyatkovo', 'Евпатория': 'evpatoriya', 'Егорьевск': 'egorevsk', 'Ейск': 'eisk', 'Екатеринбург': 'ekaterinburg', 'Елабуга': 'elabuga', 'Елец': 'elets', 'Елизово': 'elizovo', 'Ельня': 'elnya', 'Еманжелинск': 'emanzhelinsk', 'Емва': 'emva', 'Енисейск': 'eniseisk', 'Ермолино': 'ermolino', 'Ершов': 'ershov', 'Ессентуки': 'essentuki', 'Ефремов': 'efremov', 'Железноводск': 'zheleznovodsk', 'Железногорск': 'krasnoyarskiy_kray_zheleznogorsk', 'Железногорск-Илимский': 'zheleznogorsk-ilimskii', 'Жердевка': 'zherdevka', 'Жигулевск': 'zhigulevsk', 'Жиздра': 'zhizdra', 'Жирновск': 'zhirnovsk', 'Жуков': 'zhukov', 'Жуковка': 'zhukovka', 'Жуковский': 'zhukovskiy', 'Завитинск': 'zavitinsk', 'Заводоуковск': 'zavodoukovsk', 'Заволжск': 'zavolzhsk', 'Заволжье': 'zavolzhe', 'Задонск': 'zadonsk', 'Заинск': 'zainsk', 'Закаменск': 'zakamensk', 'Заозерный': 'zaozernyi', 'Заозерск': 'zaozersk', 'Западная Двина': 'zapadnaya-dvina', 'Заполярный': 'zapolyarnyi', 'Зарайск': 'zaraisk', 'Заречный': 'zarechnyi', 'Заринск': 'zarinsk', 'Звенигово': 'zvenigovo', 'Звенигород': 'zvenigorod', 'Зверево': 'zverevo', 'Зеленогорск': 'zelenogorsk', 'Зеленоградск': 'zelenogradsk', 'Зеленодольск': 'zelenodolsk', 'Зеленокумск': 'zelenokumsk', 'Зерноград': 'zernograd', 'Зея': 'zeya', 'Зима': 'zima', 'Златоуст': 'zlatoust', 'Злынка': 'zlynka', 'Змеиногорск': 'zmeinogorsk', 'Знаменск': 'znamensk', 'Зубцов': 'zubtsov', 'Зуевка': 'zuevka', 'Ивангород': 'ivangorod', 'Иваново': 'ivanovo', 'Ивантеевка': 'ivanteevka', 'Ивдель': 'ivdel', 'Игарка': 'igarka', 'Ижевск': 'izhevsk', 'Избербаш': 'izberbash', 'Изобильный': 'yzobylnyy', 'Иланский': 'ylanskyy', 'Инза': 'inza', 'Иннополис': 'innopolis', 'Инсар': 'insar', 'Инта': 'inta', 'Ипатово': 'ipatovo', 'Ирбит': 'irbit', 'Иркутск': 'irkutsk', 'Исилькуль': 'isilkul', 'Искитим': 'iskitim', 'Истра': 'istra', 'Ишим': 'ishim', 'Ишимбай': 'ishimbai', 'Йошкар-Ола': 'ioshkar-ola', 'Кадников': 'kadnikov', 'Казань': 'kazan', 'Калач': 'kalach', 'Калач-на-Дону': 'kalach-na-donu', 'Калачинск': 'kalachinsk', 'Калининград': 'kaliningrad', 'Калининск': 'kalininsk', 'Калтан': 'kaltan', 'Калуга': 'kaluga', 'Калязин': 'kalyazin', 'Камбарка': 'kambarka', 'Каменка': 'kamenka', 'Каменногорск': 'kamennogorsk', 'Каменск-Уральский': 'kamensk-uralskii', 'Каменск-Шахтинский': 'kamensk-shakhtinskii', 'Камень-на-Оби': 'kamen-na-obi', 'Камешково': 'kameshkovo', 'Камызяк': 'kamyzyak', 'Камышин': 'kamyshin', 'Камышлов': 'kamyshlov', 'Канаш': 'kanash', 'Кандалакша': 'kandalaksha', 'Канск': 'kansk', 'Карабаново': 'karabanovo', 'Карабаш': 'karabash', 'Карабулак': 'karabulak', 'Карасук': 'karasuk', 'Карачаевск': 'karachaevsk', 'Карачев': 'karachev', 'Каргат': 'kargat', 'Каргополь': 'kargopol', 'Карпинск': 'karpinsk', 'Карталы': 'kartaly', 'Касимов': 'kasimov', 'Касли': 'kasli', 'Каспийск': 'kaspiisk', 'Катав-Ивановск': 'katav-ivanovsk', 'Катайск': 'kataisk', 'Качканар': 'kachkanar', 'Кашин': 'kashin', 'Кашира': 'kashira', 'Кедровый': 'edrovyy', 'Кемерово': 'kemerovo', 'Кемь': 'kem', 'Керчь': 'kerch', 'Кизел': 'kizel', 'Кизилюрт': 'kiziliurt', 'Кизляр': 'kizlyar', 'Кимовск': 'kimovsk', 'Кимры': 'kimry', 'Кингисепп': 'kingisepp', 'Кинель': 'kinel', 'Кинешма': 'kineshma', 'Киреевск': 'kireevsk', 'Киренск': 'kirensk', 'Киржач': 'kirzhach', 'Кириллов': 'kirillov', 'Кириши': 'kirishi', 'Киров': 'kirov', 'Кировград': 'kirovgrad', 'Кирово-Чепецк': 'kirovo-chepetsk', 'Кировск': 'kyrovsk', 'Кирс': 'kirs', 'Кирсанов': 'kirsanov', 'Киселевск': 'kiselevsk', 'Кисловодск': 'kislovodsk', 'Клин': 'klin', 'Клинцы': 'klintsy', 'Княгинино': 'knyaginino', 'Ковдор': 'kovdor', 'Ковров': 'kovrov', 'Ковылкино': 'kovylkino', 'Когалым': 'kogalym', 'Кодинск': 'kodinsk', 'Козельск': 'kozelsk', 'Козловка': 'ozlova', 'Козьмодемьянск': 'kozmodemyansk', 'Кола': 'kola', 'Кологрив': 'kologriv', 'Коломна': 'kolomna', 'Колпашево': 'kolpashevo', 'Кольчугино': 'kolchugino', 'Коммунар': 'kommunar', 'Комсомольск': 'komsomolsk', 'Комсомольск-на-Амуре': 'komsomolsk_na_amure', 'Конаково': 'konakovo', 'Кондопога': 'kondopoga', 'Кондрово': 'kondrovo', 'Константиновск': 'konstantinovsk', 'Копейск': 'kopeisk', 'Кораблино': 'korablino', 'Кореновск': 'korenovsk', 'Коркино': 'korkino', 'Королев': 'korolev', 'Короча': 'korocha', 'Корсаков': 'korsakov', 'Коряжма': 'koryazhma', 'Костерево': 'kosterevo', 'Костомукша': 'kostomuksha', 'Кострома': 'kostroma', 'Котельники': 'kotelniki', 'Котельниково': 'kotelnikovo', 'Котельнич': 'kotelnich', 'Котлас': 'kotlas', 'Котово': 'kotovo', 'Котовск': 'kotovsk', 'Кохма': 'kokhma', 'Красавино': 'krasavino', 'Красноармейск': 'krasnoarmeysk', 'Красновишерск': 'rasnovyshers', 'Красногорск': 'moskovskaya_oblast_krasnogorsk', 'Краснодар': 'krasnodar', 'Краснозаводск': 'krasnozavodsk', 'Краснознаменск': 'krasnoznamensk', 'Краснокаменск': 'krasnokamensk', 'Краснокамск': 'krasnokamsk', 'Красноперекопск': 'krasnoperekopsk', 'Краснослободск': 'krasnoslobodsk', 'Краснотурьинск': 'krasnoturinsk', 'Красноуральск': 'krasnouralsk', 'Красноуфимск': 'krasnoufimsk', 'Красноярск': 'krasnoyarsk', 'Красный Кут': 'krasnyi-kut', 'Красный Сулин': 'krasnyy_sulyn', 'Красный Холм': 'rasnyy_holm', 'Кременки': 'kremenki', 'Кропоткин': 'kropotkin', 'Крымск': 'krymsk', 'Кстово': 'kstovo', 'Кубинка': 'kubinka', 'Кувандык': 'kuvandyk', 'Кувшиново': 'kuvshinovo', 'Кудрово': 'kudrovo', 'Кудымкар': 'kudymkar', 'Кузнецк': 'kuznetsk', 'Куйбышев': 'kuibyshev', 'Кукмор': 'kukmor', 'Кулебаки': 'kulebaki', 'Кумертау': 'kumertau', 'Кунгур': 'kungur', 'Купино': 'kupino', 'Курган': 'kurgan', 'Курганинск': 'kurganinsk', 'Курильск': 'kurilsk', 'Курлово': 'kurlovo', 'Куровское': 'kurovskoe', 'Курск': 'kursk', 'Куртамыш': 'kurtamysh', 'Курчалой': 'kurchaloi', 'Курчатов': 'kurchatov', 'Куса': 'kusa', 'Кушва': 'kushva', 'Кызыл': 'kyzyl', 'Кыштым': 'kyshtym', 'Кяхта': 'kyakhta', 'Лабинск': 'labinsk', 'Лабытнанги': 'labytnangi', 'Лагань': 'lagan', 'Ладушкин': 'ladushkin', 'Лаишево': 'laishevo', 'Лакинск': 'lakinsk', 'Лангепас': 'langepas', 'Лахденпохья': 'lakhdenpokhya', 'Лебедянь': 'lebedyan', 'Лениногорск': 'leninogorsk', 'Ленинск': 'leninsk', 'Ленинск-Кузнецкий': 'lenynsk_kuznetskyy', 'Ленск': 'lensk', 'Лермонтов': 'lermontov', 'Лесной': 'sverdlovskaya_oblast_lesnoy', 'Лесозаводск': 'lesozavodsk', 'Лесосибирск': 'lesosibirsk', 'Ливны': 'livny', 'Ликино-Дулево': 'likino-dulevo', 'Липецк': 'lipetsk', 'Липки': 'lipki', 'Лиски': 'liski', 'Лихославль': 'likhoslavl', 'Лобня': 'lobnya', 'Лодейное Поле': 'lodeinoe-pole', 'Лосино-Петровский': 'losino-petrovskii', 'Луга': 'luga', 'Луза': 'luza', 'Лукоянов': 'lukoyanov', 'Луховицы': 'lukhovitsy', 'Лысково': 'lyskovo', 'Лысьва': 'lysva', 'Лыткарино': 'lytkarino', 'Льгов': 'lgov', 'Любань': 'lyuban', 'Люберцы': 'liubertsy', 'Любим': 'lyubym', 'Людиново': 'liudinovo', 'Лянтор': 'lyantor', 'Магадан': 'magadan', 'Магас': 'magas', 'Магнитогорск': 'magnitogorsk', 'Майкоп': 'maikop', 'Майский': 'maiskii', 'Макаров': 'makarov', 'Макарьев': 'makarev', 'Макушино': 'makushino', 'Малая Вишера': 'malaya-vishera', 'Малгобек': 'malgobek', 'Малмыж': 'malmyzh', 'Малоархангельск': 'maloarkhangelsk', 'Малоярославец': 'maloyaroslavets', 'Мамадыш': 'mamadysh', 'Мамоново': 'mamonovo', 'Мантурово': 'manturovo', 'Мариинск': 'mariinsk', 'Мариинский Посад': 'mariinskii-posad', 'Маркс': 'marks', 'Махачкала': 'makhachkala', 'Мглин': 'mglin', 'Мегион': 'megion', 'Медвежьегорск': 'medvezhegorsk', 'Медногорск': 'mednogorsk', 'Медынь': 'medyn', 'Межгорье': 'mezhgore', 'Междуреченск': 'mezhdurechensk', 'Мезень': 'mezen', 'Меленки': 'melenki', 'Мелеуз': 'meleuz', 'Менделеевск': 'mendeleevsk', 'Мензелинск': 'menzelinsk', 'Мещовск': 'meshchovsk', 'Миасс': 'myass', 'Микунь': 'mikun', 'Миллерово': 'millerovo', 'Минеральные Воды': 'mineralnye-vody', 'Минусинск': 'minusinsk', 'Миньяр': 'minyar', 'Мирный': 'myrnyy', 'Михайлов': 'myhaylov', 'Михайловка': 'mikhailovka', 'Михайловск': 'mikhailovsk', 'Мичуринск': 'michurinsk', 'Могоча': 'mogocha', 'Можайск': 'mozhaisk', 'Можга': 'mozhga', 'Моздок': 'mozdok', 'Мончегорск': 'monchegorsk', 'Морозовск': 'morozovsk', 'Моршанск': 'morshansk', 'Мосальск': 'mosalsk', 'Муравленко': 'muravlenko', 'Мураши': 'murashi', 'Мурино': 'murino', 'Мурманск': 'murmansk', 'Муром': 'murom', 'Мценск': 'mtsensk', 'Мыски': 'myski', 'Мытищи': 'mytishchi', 'Мышкин': 'myshkin', 'Набережные Челны': 'naberezhnye_chelny', 'Навашино': 'navashino', 'Наволоки': 'navoloki', 'Надым': 'nadym', 'Назарово': 'nazarovo', 'Назрань': 'nazran', 'Называевск': 'nazyvaevsk', 'Нальчик': 'nalchik', 'Нариманов': 'narimanov', 'Наро-Фоминск': 'naro-fominsk', 'Нарткала': 'nartkala', 'Нарьян-Мар': 'naryan-mar', 'Находка': 'nakhodka', 'Невель': 'nevel', 'Невельск': 'nevelsk', 'Невинномысск': 'nevinnomyssk', 'Невьянск': 'nevyansk', 'Нелидово': 'nelidovo', 'Неман': 'neman', 'Нерехта': 'nerekhta', 'Нерчинск': 'nerchinsk', 'Нерюнгри': 'neriungri', 'Нестеров': 'nesterov', 'Нефтегорск': 'neftegorsk', 'Нефтекамск': 'neftekamsk', 'Нефтекумск': 'neftekumsk', 'Нефтеюганск': 'nefteyugansk', 'Нея': 'neya', 'Нижневартовск': 'nizhnevartovsk', 'Нижнекамск': 'nizhnekamsk', 'Нижнеудинск': 'nizhneudinsk', 'Нижние Серги': 'nizhnie-sergi', 'Нижний Ломов': 'nizhnii-lomov', 'Нижний Новгород': 'nizhnii-novgorod', 'Нижний Тагил': 'nizhnii-tagil', 'Нижняя Салда': 'nyzhnyaya_salda', 'Нижняя Тура': 'nizhnyaya-tura', 'Николаевск': 'nikolaevsk', 'Николаевск-на-Амуре': 'nikolaevsk-na-amure', 'Никольск': 'nikolsk', 'Никольское': 'nykolskoe', 'Новая Ладога': 'novaya-ladoga', 'Новая Ляля': 'novaya_lyalya', 'Новоалександровск': 'novoaleksandrovsk', 'Новоалтайск': 'novoaltaisk', 'Новоаннинский': 'novoannynsyy', 'Нововоронеж': 'novovoronezh', 'Новодвинск': 'novodvinsk', 'Новозыбков': 'novozybkov', 'Новокубанск': 'novokubansk', 'Новокузнецк': 'novokuznetsk', 'Новокуйбышевск': 'novokuibyshevsk', 'Новомичуринск': 'novomichurinsk', 'Новомосковск': 'novomoskovsk', 'Новопавловск': 'novopavlovsk', 'Новоржев': 'novorzhev', 'Новороссийск': 'novorossiisk', 'Новосибирск': 'novosibirsk', 'Новосиль': 'novosil', 'Новосокольники': 'novosokolniki', 'Новотроицк': 'novotroitsk', 'Новоузенск': 'novouzensk', 'Новоульяновск': 'novoulyanovsk', 'Новоуральск': 'novouralsk', 'Новохоперск': 'novokhopersk', 'Новочебоксарск': 'novocheboksarsk', 'Новочеркасск': 'novocherkassk', 'Новошахтинск': 'novoshakhtynsk', 'Новый Оскол': 'novyy_oskol', 'Новый Уренгой': 'novyy_urengoy', 'Ногинск': 'noginsk', 'Нолинск': 'nolinsk', 'Норильск': 'norilsk', 'Ноябрьск': 'noyabrsk', 'Нурлат': 'nurlat', 'Нытва': 'nytva', 'Нюрба': 'nyurba', 'Нягань': 'nyagan', 'Нязепетровск': 'nyazepetrovsk', 'Няндома': 'nyandoma', 'Облучье': 'obluche', 'Обнинск': 'obninsk', 'Обоянь': 'oboyan', 'Обь': 'ob', 'Одинцово': 'odintsovo', 'Озерск': 'ozersk', 'Озеры': 'ozery', 'Октябрьск': 'oktyabrsk', 'Октябрьский': 'bashkortostan_oktyabrskiy', 'Окуловка': 'okulovka', 'Олекминск': 'olekminsk', 'Оленегорск': 'olenegorsk', 'Олонец': 'olonets', 'Омск': 'omsk', 'Омутнинск': 'omutninsk', 'Онега': 'onega', 'Опочка': 'opochka', 'Орел': 'orel', 'Оренбург': 'orenburg', 'Орехово-Зуево': 'orekhovo-zuevo', 'Орлов': 'orlov', 'Орск': 'orsk', 'Оса': 'osa', 'Осинники': 'osinniki', 'Осташков': 'ostashkov', 'Остров': 'ostrov', 'Островной': 'ostrovnoi', 'Острогожск': 'ostrogozhsk', 'Отрадное': 'otradnoe', 'Отрадный': 'otradnyi', 'Оха': 'okha', 'Оханск': 'okhansk', 'Очер': 'ocher', 'Павлово': 'pavlovo', 'Павловск': 'pavlovsk', 'Павловский Посад': 'pavlovskiy_posad', 'Палласовка': 'pallasovka', 'Партизанск': 'partizansk', 'Певек': 'pevek', 'Пенза': 'penza', 'Первомайск': 'pervomaysk', 'Первоуральск': 'pervouralsk', 'Перевоз': 'perevoz', 'Пересвет': 'peresvet', 'Переславль-Залесский': 'pereslavl_zalesskyy', 'Пермь': 'perm', 'Пестово': 'pestovo', 'Петров Вал': 'petrov_val', 'Петровск': 'petrovsk', 'Петровск-Забайкальский': 'petrovsk-zabaykalskiy', 'Петрозаводск': 'petrozavodsk', 'Петропавловск-Камчатский': 'petropavlovsk-kamchatskii', 'Петухово': 'petukhovo', 'Петушки': 'petushy', 'Печора': 'pechora', 'Печоры': 'pechory', 'Пикалево': 'pikalevo', 'Пионерский': 'pionerskii', 'Питкяранта': 'pitkyaranta', 'Плавск': 'plavsk', 'Пласт': 'plast', 'Плес': 'ples', 'Поворино': 'povorino', 'Подольск': 'podolsk', 'Подпорожье': 'podporozhe', 'Покачи': 'pokachi', 'Покров': 'pokrov', 'Покровск': 'pokrovsk', 'Полевской': 'polevskoi', 'Полесск': 'polessk', 'Полысаево': 'polysaevo', 'Полярные Зори': 'polyarnye_zory', 'Полярный': 'polyarnyi', 'Поронайск': 'poronaisk', 'Порхов': 'porkhov', 'Похвистнево': 'pokhvistnevo', 'Почеп': 'pochep', 'Починок': 'pochinok', 'Пошехонье': 'poshekhone', 'Правдинск': 'pravdinsk', 'Приволжск': 'privolzhsk', 'Приморск': 'primorsk', 'Приморско-Ахтарск': 'primorsko-akhtarsk', 'Приозерск': 'priozersk', 'Прокопьевск': 'prokopevsk', 'Пролетарск': 'proletarsk', 'Протвино': 'protvino', 'Прохладный': 'prohladnyy', 'Псков': 'pskov', 'Пугачев': 'pugachev', 'Пудож': 'pudozh', 'Пустошка': 'pustoshka', 'Пучеж': 'puchezh', 'Пушкино': 'pushkino', 'Пущино': 'pushchyno', 'Пыталово': 'pytalovo', 'Пыть-Ях': 'pyt-yah', 'Пятигорск': 'pyatigorsk', 'Радужный': 'raduzhnyi', 'Райчихинск': 'raichikhinsk', 'Раменское': 'ramenskoe', 'Рассказово': 'rasskazovo', 'Ревда': 'revda', 'Реж': 'rezh', 'Реутов': 'reutov', 'Ржев': 'rzhev', 'Родники': 'ivanovskaya_oblast_rodniki', 'Рославль': 'roslavl', 'Россошь': 'rossosh', 'Ростов': 'rostov', 'Ростов-на-Дону': 'rostov-na-donu', 'Рошаль': 'roshal', 'Ртищево': 'rtyshchevo', 'Рубцовск': 'rubtsovsk', 'Рудня': 'rudnya', 'Руза': 'ruza', 'Рузаевка': 'ruzaevka', 'Рыбинск': 'rybinsk', 'Рыбное': 'rybnoe', 'Рыльск': 'rylsk', 'Ряжск': 'ryazhsk', 'Рязань': 'ryazan', 'Саки': 'saki', 'Салават': 'salavat', 'Салаир': 'salair', 'Салехард': 'salekhard', 'Сальск': 'salsk', 'Самара': 'samara', 'Санкт-Петербург': 'sankt-peterburg', 'Саранск': 'saransk', 'Сарапул': 'sarapul', 'Саратов': 'saratov', 'Саров': 'sarov', 'Сасово': 'sasovo', 'Сатка': 'satka', 'Сафоново': 'safonovo', 'Саяногорск': 'sayanogorsk', 'Саянск': 'sayansk', 'Светлогорск': 'svetlogorsk', 'Светлоград': 'svetlograd', 'Светлый': 'kaliningradskaya_oblast_svetlyy', 'Светогорск': 'svetogorsk', 'Свирск': 'svirsk', 'Свободный': 'svobodnyy', 'Себеж': 'sebezh', 'Севастополь': 'sevastopol', 'Северо-Курильск': 'severo-kurilsk', 'Северобайкальск': 'severobaykalsk', 'Северодвинск': 'severodvinsk', 'Североморск': 'severomorsk', 'Североуральск': 'severouralsk', 'Северск': 'seversk', 'Севск': 'sevsk', 'Сегежа': 'segezha', 'Сельцо': 'seltso', 'Семенов': 'semenov', 'Семикаракорск': 'semikarakorsk', 'Семилуки': 'semyluky', 'Сенгилей': 'sengilei', 'Серафимович': 'serafimovich', 'Сергач': 'sergach', 'Сергиев Посад': 'sergyev_posad', 'Сердобск': 'serdobsk', 'Серов': 'serov', 'Серпухов': 'serpukhov', 'Сертолово': 'sertolovo', 'Сибай': 'sibay', 'Сим': 'sim', 'Симферополь': 'simferopol', 'Сковородино': 'skovorodino', 'Скопин': 'skopin', 'Славгород': 'slavgorod', 'Славск': 'slavsk', 'Славянск-на-Кубани': 'slavyansk-na-kubani', 'Сланцы': 'slantsy', 'Слободской': 'slobodskoy', 'Слюдянка': 'slyudyanka', 'Смоленск': 'smolensk', 'Снежинск': 'snezhinsk', 'Снежногорск': 'snezhnogorsk', 'Собинка': 'sobinka', 'Советск': 'sovetsk', 'Советская Гавань': 'sovetskaya-gavan', 'Советский': 'sovetskii', 'Сокол': 'sokol', 'Солигалич': 'soligalich', 'Соликамск': 'solikamsk', 'Солнечногорск': 'solnechnogorsk', 'Соль-Илецк': 'sol-iletsk', 'Сольвычегодск': 'solvychegodsk', 'Сольцы': 'soltsy', 'Сорочинск': 'sorochinsk', 'Сорск': 'sorsk', 'Сортавала': 'sortavala', 'Сосенский': 'sosenskii', 'Сосновка': 'sosnovka', 'Сосновоборск': 'sosnovoborsk', 'Сосновый Бор': 'sosnovyi-bor', 'Сосногорск': 'sosnogorsk', 'Сочи': 'sochi', 'Спас-Деменск': 'spas-demensk', 'Спас-Клепики': 'spas-klepiki', 'Спасск': 'spassk', 'Спасск-Дальний': 'spassk-dalnii', 'Спасск-Рязанский': 'spassk-ryazanskii', 'Среднеколымск': 'srednekolymsk', 'Среднеуральск': 'sredneuralsk', 'Сретенск': 'sretensk', 'Ставрополь': 'stavropol', 'Старая Купавна': 'staraya-kupavna', 'Старая Русса': 'staraya-russa', 'Старица': 'staritsa', 'Стародуб': 'starodub', 'Старый Крым': 'staryi-krym', 'Старый Оскол': 'staryy_oskol', 'Стерлитамак': 'sterlitamak', 'Стрежевой': 'strezhevoi', 'Строитель': 'belgorodskaya_oblast_stroitel', 'Струнино': 'strunino', 'Ступино': 'stupino', 'Суворов': 'suvorov', 'Судак': 'sudak', 'Суджа': 'sudzha', 'Судогда': 'sudogda', 'Суздаль': 'suzdal', 'Сунжа': 'sunzha', 'Суоярви': 'suoyarvi', 'Сураж': 'surazh', 'Сургут': 'surgut', 'Суровикино': 'surovikino', 'Сурск': 'sursk', 'Сусуман': 'susuman', 'Сухиничи': 'sukhinichi', 'Сухой Лог': 'sukhoi-log', 'Сызрань': 'syzran', 'Сыктывкар': 'syktyvkar', 'Сысерть': 'sysert', 'Сычевка': 'sychevka', 'Сясьстрой': 'syasstroy', 'Тавда': 'tavda', 'Таганрог': 'taganrog', 'Тайга': 'taiga', 'Тайшет': 'tayshet', 'Талдом': 'taldom', 'Талица': 'talitsa', 'Тамбов': 'tambov', 'Тара': 'tara', 'Тарко-Сале': 'tarko-sale', 'Таруса': 'tarusa', 'Татарск': 'tatarsk', 'Таштагол': 'tashtagol', 'Тверь': 'tver', 'Теберда': 'teberda', 'Тейково': 'teikovo', 'Темников': 'temnikov', 'Темрюк': 'temryuk', 'Терек': 'terek', 'Тетюши': 'tetiushi', 'Тимашевск': 'timashevsk', 'Тихвин': 'tyhvyn', 'Тихорецк': 'tikhoretsk', 'Тобольск': 'tobolsk', 'Тогучин': 'toguchin', 'Тольятти': 'tolyatti', 'Томари': 'tomari', 'Томмот': 'tommot', 'Томск': 'tomsk', 'Топки': 'topki', 'Торжок': 'torzhok', 'Торопец': 'toropets', 'Тосно': 'tosno', 'Тотьма': 'totma', 'Трехгорный': 'trekhgornyy', 'Троицк': 'troytsk', 'Трубчевск': 'trubchevsk', 'Туапсе': 'tuapse', 'Туймазы': 'tuymazy', 'Тула': 'tula', 'Тулун': 'tulun', 'Туран': 'turan', 'Туринск': 'turinsk', 'Тутаев': 'tutaev', 'Тында': 'tynda', 'Тырныауз': 'tyrnyauz', 'Тюкалинск': 'tiukalinsk', 'Тюмень': 'tyumen', 'Уварово': 'uvarovo', 'Углегорск': 'uglegorsk', 'Углич': 'uglich', 'Удачный': 'udachnyy', 'Удомля': 'udomlya', 'Ужур': 'uzhur', 'Узловая': 'uzlovaya', 'Улан-Удэ': 'ulan-ude', 'Ульяновск': 'ulyanovsk', 'Унеча': 'unecha', 'Урай': 'urai', 'Урень': 'uren', 'Уржум': 'urzhum', 'Урус-Мартан': 'urus-martan', 'Урюпинск': 'uryupyns', 'Усинск': 'usinsk', 'Усмань': 'usman', 'Усолье': 'usole', 'Усолье-Сибирское': 'usole-sibirskoe', 'Уссурийск': 'ussuriisk', 'Усть-Джегута': 'ust-dzheguta', 'Усть-Илимск': 'ust-ilimsk', 'Усть-Катав': 'ust-katav', 'Усть-Кут': 'ust-kut', 'Усть-Лабинск': 'ust-labinsk', 'Устюжна': 'ustyuzhna', 'Уфа': 'ufa', 'Ухта': 'uhta', 'Учалы': 'uchaly', 'Уяр': 'uyar', 'Фатеж': 'fatezh', 'Феодосия': 'feodosiya', 'Фокино': 'fokino', 'Фролово': 'frolovo', 'Фрязино': 'fryazino', 'Фурманов': 'furmanov', 'Хабаровск': 'khabarovsk', 'Хадыженск': 'khadyzhensk', 'Ханты-Мансийск': 'khanty_mansyysk', 'Харабали': 'kharabaly', 'Харовск': 'kharovsk', 'Хасавюрт': 'khasaviurt', 'Хвалынск': 'khvalynsk', 'Хилок': 'khylok', 'Химки': 'khimki', 'Холм': 'holm', 'Холмск': 'kholmsk', 'Хотьково': 'hotkovo', 'Цивильск': 'tsivilsk', 'Цимлянск': 'tsimlyansk', 'Циолковский': 'tsiolkovskii', 'Чадан': 'chadan', 'Чайковский': 'chaikovskii', 'Чапаевск': 'chapaevsk', 'Чаплыгин': 'chaplygin', 'Чебаркуль': 'chebarkul', 'Чебоксары': 'cheboksary', 'Чегем': 'chegem', 'Чекалин': 'chekalin', 'Чердынь': 'cherdyn', 'Черемхово': 'cheremkhovo', 'Черепаново': 'cherepanovo', 'Череповец': 'cherepovets', 'Черкесск': 'cherkessk', 'Чермоз': 'chermoz', 'Черноголовка': 'chernogolovka', 'Черногорск': 'chernogorsk', 'Чернушка': 'chernushka', 'Черняховск': 'chernyakhovsk', 'Чехов': 'moskovskaya_oblast_chehov', 'Чистополь': 'chistopol', 'Чита': 'chita', 'Чкаловск': 'chkalovsk', 'Чудово': 'chudovo', 'Чулым': 'chulym', 'Чусовой': 'chusovoi', 'Чухлома': 'chukhloma', 'Шагонар': 'shagonar', 'Шадринск': 'shadrinsk', 'Шали': 'shali', 'Шарыпово': 'sharypovo', 'Шарья': 'sharya', 'Шатура': 'shatura', 'Шахты': 'shakhty', 'Шахунья': 'shahunya', 'Шацк': 'shatsk', 'Шебекино': 'shebekino', 'Шелехов': 'shelekhov', 'Шенкурск': 'shenkursk', 'Шилка': 'shilka', 'Шимановск': 'shimanovsk', 'Шиханы': 'shikhany', 'Шлиссельбург': 'shlisselburg', 'Шумерля': 'shumerlya', 'Шумиха': 'shumikha', 'Шуя': 'ivanovskaya_oblast_shuya', 'Щекино': 'shchekyno', 'Щелкино': 'schelkino', 'Щелково': 'shchelkovo', 'Щигры': 'shchigry', 'Щучье': 'shchuche', 'Электрогорск': 'elektrogorsk', 'Электросталь': 'elektrostal', 'Электроугли': 'elektrougli', 'Элиста': 'elista', 'Энгельс': 'engels', 'Эртиль': 'ertil', 'Югорск': 'iugorsk', 'Южа': 'iuzha', 'Южно-Сахалинск': 'yuzhno-sahalinsk', 'Южно-Сухокумск': 'iuzhno-sukhokumsk', 'Янаул': 'yanaul', 'Яранск': 'yaransk', 'Яровое': 'yarovoe', 'Ярославль': 'yaroslavl', 'Ярцево': 'yartsevo', 'Ясногорск': 'yasnogorsk', 'Ясный': 'yasnyy', 'Яхрома': 'yakhroma'}


class GeoOfferSearchSettings(NamedTuple):
    city: str
    city_url_slug: str
    radius_search: Optional[int] = None


RU_CITIES_URL_SLUGS_BY_LOWER = {}
for city, slug in RU_CITIES_URL_SLUGS.items():
    city_lower = city.lower()
    RU_CITIES_URL_SLUGS_BY_LOWER[city_lower] = GeoOfferSearchSettings(
        city=city,
        city_url_slug=slug
    )

RU_CITIES_URL_SLUGS_CHOICES = tuple(
    [
        tuple([url_slug, city])
        for city, url_slug in RU_CITIES_URL_SLUGS.items()
    ]
)

RU_CITIES_CHOICES = tuple(
    [
        tuple([city, city])
        for city in RU_CITIES_URL_SLUGS
    ]
)


RUSSIA_REGIONS = {'Алтайский край',
                  'Амурская область',
                  'Архангельская область',
                  'Астраханская область',
                  'Белгородская область',
                  'Брянская область',
                  'Владимирская область',
                  'Волгоградская область',
                  'Вологодская область',
                  'Воронежская область',
                  'Еврейская автономная область',
                  'Забайкальский край',
                  'Ивановская область',
                  'Иркутская область',
                  'Кабардино-Балкарская Республика',
                  'Калининградская область',
                  'Калужская область',
                  'Камчатский край',
                  'Карачаево-Черкесская Республика',
                  'Кемеровская область - Кузбасс',
                  'Кировская область',
                  'Костромская область',
                  'Краснодарский край',
                  'Красноярский край',
                  'Курганская область',
                  'Курская область',
                  'Ленинградская область',
                  'Липецкая область',
                  'Магаданская область',
                  'Москва',
                  'Московская область',
                  'Мурманская область',
                  'Нижегородская область',
                  'Новгородская область',
                  'Новосибирская область',
                  'Омская область',
                  'Оренбургская область',
                  'Орловская область',
                  'Пензенская область',
                  'Пермский край',
                  'Приморский край',
                  'Псковская область',
                  'Республика Адыгея',
                  'Республика Алтай',
                  'Республика Башкортостан',
                  'Республика Бурятия',
                  'Республика Дагестан',
                  'Республика Ингушетия',
                  'Республика Калмыкия',
                  'Республика Карелия',
                  'Республика Коми',
                  'Республика Крым',
                  'Республика Марий Эл',
                  'Республика Мордовия',
                  'Республика Саха (Якутия)',
                  'Республика Северная Осетия – Алания',
                  'Республика Татарстан',
                  'Республика Тыва',
                  'Республика Хакасия',
                  'Ростовская область',
                  'Рязанская область',
                  'Самарская область',
                  'Санкт-Петербург',
                  'Саратовская область',
                  'Сахалинская область',
                  'Свердловская область',
                  'Севастополь',
                  'Смоленская область',
                  'Ставропольский край',
                  'Тамбовская область',
                  'Тверская область',
                  'Томская область',
                  'Тульская область',
                  'Тюменская область',
                  'Удмуртская Республика',
                  'Ульяновская область',
                  'Хабаровский край',
                  'Челябинская область',
                  'Чеченская Республика',
                  'Чувашская Республика',
                  'Чукотский автономный округ',
                  'Ярославская область'
                  }
