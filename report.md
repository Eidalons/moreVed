# Отчёт о выполнении задачи "Дрон МореВед"

- [Отчёт о выполнении задачи "Дрон мореВед"](#отчёт-о-выполнении-задачи-name)
  - [Постановка задачи](#постановка-задачи)
  - [Известные ограничения и вводные условия](#известные-ограничения-и-вводные-условия)
    - [Цели и Предположения Безопасности (ЦПБ)](#цели-и-предположения-безопасности-цпб)
  - [Архитектура системы](#архитектура-системы)
    - [Контекст работы системы](#контекст-работы-системы)
    - [Компоненты](#компоненты)
    - [Алгоритм работы решения](#алгоритм-работы-решения)
    - [Описание Сценариев (последовательности выполнения операций), при которых ЦБ нарушаются](#описание-сценариев-последовательности-выполнения-операций-при-которых-цб-нарушаются)
    - [Переработанная архитектура](#переработанная-архитектура)
    - [Указание "доверенных компонент" на архитектурной диаграмме.](#указание-доверенных-компонент-на-архитектурной-диаграмме)
    - [Проверка негативных сценариев](#проверка-негативных-сценариев)
    - [Политики безопасности](#политики-безопасности)
  - [Запуск приложения и тестов](#запуск-приложения-и-тестов)
    - [Запуск приложения](#запуск-приложения)
    - [Запуск тестов](#запуск-тестов)

## Постановка задачи

Центр контроля экологической обстановки (ЦЕКЭОБ) создаёт дрон для мониторинга экологической обстановки водной поверхности, где не всегда есть связь,а также может быть опасно для живых организмов, поэтому нужна функция автономного выполнения задачи.  ЦЕКЭОБ ставит задачу на исследование заданного района, далее к месту проверки выдвигается бригада запуска судна(люди перевозящие судно с места хранения к месту выполнения задачи).
МореВед должен идти в контролируемом водном пространстве, координацию движения в котором осуществляет система организации водного движения (ОрВД). Судно портативное - небольшая лодка которую можно перевозить в наземном транспорте. Далее после запуска судна, контролем заниматся специалист из ЦЕКЭОБ. Во время выполнения задания судно отправляет телеметрию в центр в реальном времени. После исследования, бригада запуска забирает судно и перевозит его к месту храниния

Ценности, ущербы и неприемлемые события

|Ценность|Негативное событие|Оценка ущерба|Комментарий|
|:-:|:-:|:-:|:-:|
|Безэкипажное Судно|В результате атаки потерпел крушение или был угнан|Средний|Безэпижаное судно застраховано|
|Люди|Из-за неверно оценненной обстановки люди могут оказаться в зоне повышенной опасности|Высокий||
|Данные мониторинга|Из-за нарушения целостности данных приняты неправильные решения на стороне центра управления|Средний|Внутренние издержки: Людей не отправили на устранение проблемы. Людей отправили не туда|
|Данные мониторинга|Данные о радиационной обстановке оказались доступны злоумышленикам, что привело к рассекречиванию военных испытаний|Высокий|Нарушение закона о защите секретной информации|
|Инфраструктура|Судно врезалось в объект водной навигации|Высокий||
|Имущество третьих лиц|Судно врезалось в корабль|Высокий|
|Данные мониторинга|Злоумышленник получил данные с судна и распространил их|Высокий|Репутационниые риски|


## Известные ограничения и вводные условия

- По условиям организаторов должна использоваться микросервисная архитектура и брокер сообщений для реализации асинхронной работы сервисов.
- Между собой сервисы cудна общаются через брокер сообщений, а все внешнее взаимодействие происходит в виде REST запросов.
- Графический интерфейс для взаимодействия с пользователем не требуется, достаточно примеров REST запросов.

### Список используемых сокращений
- Организация водного движения (далее ОрВД)
- Центр контроля экологической обстановки (далее ЦЕКЭОБ)
- 

### Цели и Предположения Безопасности (ЦПБ)

Цели безопасности:
1. Выполняются только авторизованные системой ЦЕКЭОБ задания.
2. Задания выполняются только в авторизованном районе.
3. ОрВД всегда должен знать реальные координаты судна
4. ЦЕКЭОБ должнен получать только аутентичные показания с датчиков
5. Данные с датчиков должны быть конфиденциальны
6. ЦЕКЭОБ должнен знать реальные координаты аутентичные судна

Предположения безопасности:
1. Аутентичная система ОрВД благонадёжна
2. ЦЕКЭОБ благонадежен.
3. Бригада запуска судно благонадежна и обладает необходимой квалификацией
5. Монитор безопасности и брокер сообщений доверенные модули

## Архитектура системы

### Взаимодействие системы

![Контекст](images/kontekst_diagram.jpg)

### Сценарий работы

![Сценарий работы](images/base_scenarij.jpg)

### Компоненты

Базовая архитектура

![Базовая архитектура](images/BaseSchema.jpg)

Базовая диаграмма последовательности

![Диаграмма последовательности](images/baseDiagram.jpg)

[Cсылка на исходник диаграммы](https://www.plantuml.com/plantuml/uml/lLPDQjj05DxFAOQi4cWku4K9pRAqNUG4QYg2ePQCB0UoQvosIN31j50AMJYOGdS5LPKIHRQLAxovKJyz3N5dEdQrA5quGffvty-RxmtP6yHU50zxhqKVp-vXj-y5iToYR_IPhkWxJUdZblG6Sl_fYoVIsZDLR-WJPRp-B3psUtuGxuT178MC9eIrVqQ5EbKZocb1YLIdbAe9tLBH48IztZ3e7dfnDmms5vxHFPWJIccEJqiiJZG4Sn-S36A_jn62bbnUq4zAr7igj8Rdtd7tY0Kq6F9l1dvG1IN0kwUAIc3UuWT1T2Sf0_H8dUEbn6BA10T-C0WZ2xoroPecnqVimFEo-Lo_6IVWHh-2qX5gAvgh3nB28OuI1hlZyfTU7FlHYH17KJZiI_MMhIseuA9K-yebMuItHf8G78pTtSTs0cH7rfGFBagO0XmerGL-PpMzi6eOXm4xJKipx4hPymqujTy_OVpWrKg74II72jk1DemmZfbpZk-vqwpSfXdE9SDRjIE4xXYJ6j5hrFD9SGhEGQfHbcgita5I7PwAZxjI4oOh93QK7A85IEPgmelSV65wQaDekpJs6-UrWlXgHOuxaF6StAp29eHLwPHplUxqd266G8T2Org0-OKILeZ6ILJn12wvJy1rpA0m09moPni1B4tET4sDT5a73Q7sFI24VSkubTcuV3EK2Fmb5K1cCCG3y0NeGD56xBKT4jG-JBg-2UjqWhDgSauBEm85gXozSdlbqJHa63DkZMPBM0UWVP7yExFRd5EUL7qzLAlLdJNU_X-_lhsuOJnhwcBDxTMYQnr7hDHudKVtxaU_JG3bVFvx-8F_C7u1)

|Компонент|Назначение|
|:--|:--|
|1. Связь|отвечает за взаимодействие с ЦЕКЭОБ и системой организации водного движения (ОрВД)|
|2. Система анализов|собирает и анализирует данные фото-видеофиксации|
|3. Центральная система управления|осуществляет общее управление судном, контролирует выполнение задания|
|4. Система навигация|предоставляет спутниковые координаты дрона|
|5. Контроль батареи|предоставляет статус остаточного заряда батареи и оценку продолжительности полёта в текущем режиме энергопотребления|
|6. Система перемещения|осуществляет контроь над двигателями и поворотными устройствами|
### Алгоритм работы решения

### Негативные сценарии
|Название сценария|Описание|
|---|----------------------|
|НС-1| При компрометации модуля системы управления в ЦЕКЭОБ были направлены невалидные данные о судне (нарушение ЦБ 4, 6)|
|НС-2| При компрометации модуля системы управления в ОрВД были направлены невалидные координаты (нарушение ЦБ 3)|
|НС-3| При компрометации модуля связи на судне было полученно неправильное задание (нарушено ЦБ 1)|
|НС-4| При компрометации модуля связи на судне был получен неправильный маршрут (Нарушено ЦБ 2)|
|НС-5| При компрометации модуля связи ОрВд не получил / получил недостоверные координаты судна (Нарушено ЦБ 3)|
|НС-6| При компрометации модуля связи ЦЕКЭОБ не получил / получил недостоверные координаты судна (Нарушено ЦБ 6)|
|НС-7| При компрометации модуля связи ЦЕКЭОБ не получил / получил недоствоверные данные с датчиков (Нарушено ЦБ 4)|
|НС-8| При компрометации модуля связи злоумышленник получил доступ к данным с датчиков (Нарушено ЦБ 5)|
|НС-9| При компрометации модуля датчиков ЦЕКЭОБ получил недостоверные данные с датчиков (Нарушено ЦБ 4)|
|НС-10| При компрометации модуля перемещения ОрВД получил недостоверные координаты судна (Нарушено ЦБ 3)|
|НС-11| При компрометации модуля перемещения судно вышло за пределы авторизированного района (Нарушено ЦБ 2)|
|НС-12| При компрометации модуля перемещения ЦЕКЭОБ не получил / получил недоствоверные координаты (Нарушено ЦБ 4)|
|НС-13| При компрометации модуля навигации ОрВД получил недостоверные координаты судна (Нарушено ЦБ 3)|
|НС-14| При компрометации модуля навигации ЦЕКЭОБ получил недостоверные координаты судна (Нарушено ЦБ 6)|
|НС-15| При компрометации модуля системы управления злоумышленник получил доступ к данным с датчиков (Нарушено ЦБ 5)|

### Описание Сценариев (последовательности выполнения операций), при которых ЦБ нарушаются

Нарушение ЦБ (Целей безопасности) в базовом решении

Напоминание ЦБ:

1. Выполняются только аутентичные задания на мониторинг
2. Выполняются только авторизованные системой ОрВД задания
3. Все манёвры выполняются согласно ограничениям в полётном задании (высота, полётная зона/эшелон)
4. Только авторизованные получатели имеют доступ к сохранённым данным фото-видео фиксации
5. В случае критического отказа дрон снижается со скоростью не более 1 м/с
6. Для запроса авторизации вылета к системе ОрВД используется только аутентичный идентификатор дрона
7. Только авторизованные получатели имеют доступ к оперативной информации

|Атакованный компонент|ЦБ1|ЦБ2|ЦБ3|ЦБ4|ЦБ5|ЦБ6|Кол-во нарушений|
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|1. Связь|🔴|🔴|🔴|🔴|🟢|🟢|4/6|
|2. Система анализов|🟢|🟢|🟢|🔴|🟢|🟢|1/6|
|3. Центральная система управления|🟢|🟢|🔴|🔴|🔴|🔴|4/6|
|4. Система навигация|🟢|🟢|🔴|🟢|🟢|🔴|2/6|
|5. Система перемещения|🟢|🔴|🔴|🔴|🟢|🟢|3/6|

🟢 - ЦБ не нарушена 🔴 - ЦБ нарушена

**Негативный сценарий - НС-1:**

![НС-1](/images/neg1.jpg)

**Негативный сценарий - НС-2:**

![НС-2](/images/neg2.jpg)

**Негативный сценарий - НС-3:**

![НС-3](/images/neg3.jpg)


**Негативный сценарий - НС-4:**

![НС-4](/images/neg4.jpg)



**Негативный сценарий - НС-5:**

![НС-5](/images/neg5.jpg)


**Негативный сценарий - НС-6:**

![НС-6](/images/neg6.jpg)


**Негативный сценарий - НС-7:**

![НС-7](/images/neg7.jpg)


**Негативный сценарий - НС-8:**

![НС-8](/images/neg8.jpg)


**Негативный сценарий - НС-9:**

![НС-9](/images/neg9.jpg)


**Негативный сценарий - НС-10:**

![НС-10](/images/neg10.jpg)



**Негативный сценарий - НС-11:**

![НС-11](/images/neg11.jpg)


**Негативный сценарий - НС-12:**

![НС-12](/images/neg12.jpg)


**Негативный сценарий - НС-13:**

![НС-13](/images/neg13.jpg)

**Негативный сценарий - НС-14:**
![НС-13](/images/neg14.jpg)

**Негативный сценарий - НС-15:**
![НС-13](/images/neg15.jpg)

## Переработанная архитектура

![Переработанная архитектура](docs/images/drone-inspector_rework-arch.png)

Описание декомпозиции

<table>
    <thead>
        <tr>
            <th align="center">Исходный компонент</th>
            <th align="center">Декомпозиция</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=3 align="center">Центральная система упраления</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">Оркестратор задач</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">Аварийный блок</td>
        </tr>
        <tr>
            <td rowspan=3 align="center">Навигация</td>
            <td rowspan=1 align="center">Комплексирование</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">Навигация ИНС</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">Навигация GNSS</td>
        </tr>
        <tr>
            <td rowspan=2 align="center">Хранение данных</td>
            <td rowspan=1 align="center">Хранение данных</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">Блок защиты данных</td>
        </tr>
        <tr>
            <td rowspan=2 align="center">Приводы</td>
            <td rowspan=1 align="center">Приводы</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">Аварийные приводы</td>
        </tr>
        <tr>
            <td rowspan=2 align="center">Контроль батареи</td>
            <td rowspan=1 align="center">Контроль батареи</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">Критичный заряд батареи</td>
        </tr>
        <tr>
            <td rowspan=3 align="center">Связь</td>
            <td rowspan=1 align="center">Блок шифрования каналов</td>
        </tr>
        <tr>
            <td rowspan=1 align="center">Данные о дроне</td>
        </tr>
    </tbody>
</table>

### Таблица новых компонентов

|Компонент|Описание|Комментарий|
|:---|:--|:--|
|2. Блок шифрования каналов|Расшифрование/шифрование принимаемых/отправляемых пакетов данных.|Работает при помощи SSL протокола. В рамках хакатона протокол не реализуется. Предполагается что в ОрВД и Системе планирование полетов тоже реализован данный функционал. Если это 5G сети то там используется ECIES+5G-AKA.|
|3. Оркестратор задач|Распределение задач.|Записывает индефикатор дрона в блок Данные о дроне, потом полученный токен от ОрВД при инициализации. В аварийный блок отправляет параметры полетного задания: зона полета, высота и так же отправляет, если приходят команды об аварийной остановке от ОрВД или Системы управления полетов. Все остальные команды и задания отправляет в Центральную систему управления.|
|4. Данные о дроне|Хранит индентификатор дрона и токен ОрВД|При отправке данных дописывает индентификатор/токен к пакету данных|
|5. Аварийный блок|Перехватывает управление дроном при возникновении аварийной ситуации.|Следит за тем чтобы дрон не вышел из полетный зоны или высотой указанной в полётном задании, следит за зарядом аккумулятора чтобы хватило на аварийную посадку, при нарушении совершает аварийную посадку (снижение вниз до земли)|
|6. Центральная система управления|Выполнение бизнес-логики и полетного задания, исполнение команд поступающих из ОрВД и Системы планирования полетов.||
|7. Блок защиты данных|Шифрование данных оперативных данных (проанализированные данные) и первичные данные (фото и видео).|Аппратный модуль шифрования рядом с хранилищем занимающейся криптографией. Отправляет зашифрованные данные дальше при необходимости. Используется AES-256 (если нужен отечественный то Магма), но в рамках хакатона не реализуется. Ключ находится в Системе планирования полетов. Как пример реализация модуля: флешка с аппаратной криптографией.|
|14. Комплексирование|Комплексирование навигационных данных.||
|15. Навигация ИНС|Физический модуль ИНС дающий координаты дроны.||
|16. Навигация GNSS|Физический модуль GNSS дающий координаты дроны.||
|17. Аварийные приводы|Группа приводов достаточных для совершения аварийной посадки.|Нужное количество для совершение аварийной посадки, это выбранные приводы из приводов имующихся в дроне. (не добавление ещё дополнительных приводов)|
|18. Критичный заряд батареи|Проверяет остаток зарядки аккумулятора.|По пороговому значению (которого хватит для аварийной посадки дрона) отправляет срабатывание(меньше порогового значения). При реализации в продуктовой системе это физический модуль, подключается к системе управления в обход самодиагностики сигнальным проводом.|

### Диаграмма последовательности

#### Выполнения задания

Общая схема выполнения задания, за счёт того что она большая нельзя сохранить картинкой. Прикрепляем ссылку.

Ниже будет каждый этап.

[Выполнение задания](http://www.plantuml.com/plantuml/svg/xLbFRnD75B_lfrXnCgAkIak1eghYrbilN96YnIo9LNjjsHiaUiAXQOgCI458HPNw1wdjUPFOZMCIvolCVAE-tzl9UDwm6tkZA9Mg75eHp_lztfltvysysRlzDEgbw-rMa3RJLXnUKQ_rK1shcNglZjIO_fkeSQZsLQP6AiEVUljA44JhQITPRp-8Uq6NyCr6inibAQ7VaS10Rn3oK6Nt4s9wRs1FYNFNKeHHFtpKxNletqZgjNh3gr7Q3kJozOz3uj_LssfVls2PHgVTNa-QZIXjTX8f_2a9loBbCpMzduJwHzBwlRI1VbPJ_YDZkTsSSgtPNVEtzHcHaMqaFiRkw5yPxN6cduB3-4PlCVvXb4OhKHArddmNIv8RHFA6zHsHYyU0pa8rWb5mTOxkTP9u1HmIUvEmVoCSK0vxzGlOpPlG0-dpK3zJnoorI_iQEmvlarsh_jwkVqBSloFW-XMHmBO32jmKLa4RLi2Zdp878jzjjZgfnt8TB2Gz8QqpsjMGfVjnxt6d7tgoYCqxikyGaeJ8r1vPEUDDJ10JqZy9iGpZuMacFb9xJBeMHwrqRQMn5ZU-zPWHg5zSo_KB-7c7uvNHJsCrOOu7KPh6lISU_3RWq0L3z1QYhQQa-G1H9ZYbtkXKlfL6hqbyKSiZlc7iEaH146Yg1xOakCIO98aUUxZF2VSh8aaoUwJm1yGoL6_fntSCQIPz3tAp4FBrD_VkCM0rwNk8snoD7JWvXDjDHH1yd-8mEibOlSduRg_JYFlzPh8gMMwvzSRUUWutwc7u0SN3-D5AF-tqA1SbnnV4yHTdhcqz1HOKGk6edr3Rd2a7UHeZK6mHu-9st5kDauOVz5i5KAxEOv7EWcBb9B63rLvdlSiUrrjv8mcfHGqHPQH8G4sk_fLiL7Suc_oMPEkPI-yGFs7hDLgTKXw_97hRZYSanictfoQs8PdSs9KDONmr4Ch96DFYhbsxQ4ECud1kmvsG4GDX0pK0HrHqLBAuo8eI6m8NobIslUPRLySCuHunuMroYuKjt8XCb-UkQZjr5infn5P8TCDsNWABp2U6scawX8PYL_bEae4DlwoVYDRh9P6rgJsQ_rd1AgcGRCCXNPv6O2UugxcACk8sAigoH8WicuOILC8eIwPUOOTX3PiXBjfYQUbLAZn9U0ubDEUhK20EYhZZvA5jVMzHXl2sutFP0DrCEPxVDDJCkrgQu2pTBsViS2wuVOIVH63UZ7wKj3MzYLKl7iA9vwJYd29KGP_n6CwPUX4I0QZeqaLHgkJ62hJduBg5Ebpf0iSFY9-kkjo-Sm-hhB872qfuaDyNzKPv3fwTyLpyLaxl--naZa0zLtMtlK4j0QwXZr14PZ253cWXZrO9UNDO1EO2JZh4V82Gyausz3Cz2DmbPoUGClF7J6_dsdDj8_Vm2FnRljYHL5Mp4yC_UHrU3Pe9qWYtV6mU3kVBnOZFHC260MxdHgP4WbQaGC58ORqFOMbYEQTrHhrU8XOO0KVMvjaMeWANeNZudDNFJsRF_BHeTJfT31gmTUHQYICQBEe0mImS-rJcwhOZgCcX36YenC6lXsLMM9ZWa3iGixFUrYzvYjaKrI68p8GBIugWQYoWvCHSVex4ZRRenQL4eNGzYU-JMffoJU8D9PlP-cLrd5OTvrOUbiUlkMEZ65dfpmM5HUKZC0NRzn5up3nWEVqI3NGFzmHRIkQUvYXmXdVuk62KGagHWWbIhwGIJI7_GLfsJ6iM1Kmi9S2vTcdBdR1Xdn_k9-81GhfA4ZZF2FKwziDPkYdV3oI10_4Ol54WMm9jaKLwfR187dzCn9QzWr-CZNAAh1LLVQ77Bu_51ON_tzQzhKinTi45_a1PfFKZMbWgE11S-YsWOdfTbIyXSdh46R_ZFaARMwohy73Xmulp8i2sucWDtQyCiAxa8mEJYxdL4fWF3SKlEUWc2rvpBl1zHhAOKQ_OmD8k8cqdlA4f7HCMYnJSFh1KaYgI4853KfWh6sA5I5L8lVANg3CwfUfhKt73wAHns7bCQG7HW9-Ezta3tEpO5XY7RPlkm6NoVdwckpDE5d3wibjsvB5qb7iFwSn8dFu7ZDK3lX9CrGI7VmYJWgNk627QS_uXp7xno5V94TQwGwwy0KbCoYyNXXpD5vuqL_3IYu5zIVfPQYpuz8XkPjowwtEZlj5na4ANuyBbkF1_l3M8XzS_YSxUbEtZgooOybk6V6lviDndPpdSvJFI-F9uFzlnVd67--8iA3ffB-wSNMmVbyHT-jzwk_Kl)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/xLbFRnD75B_lfrXnCgAkIak1eghYrbilN96YnIo9LNjjsHiaUiAXQOgCI458HPNw1wdjUPFOZMCIvolCVAE-tzl9UDwm6tkZA9Mg75eHp_lztfltvysysRlzDEgbw-rMa3RJLXnUKQ_rK1shcNglZjIO_fkeSQZsLQP6AiEVUljA44JhQITPRp-8Uq6NyCr6inibAQ7VaS10Rn3oK6Nt4s9wRs1FYNFNKeHHFtpKxNletqZgjNh3gr7Q3kJozOz3uj_LssfVls2PHgVTNa-QZIXjTX8f_2a9loBbCpMzduJwHzBwlRI1VbPJ_YDZkTsSSgtPNVEtzHcHaMqaFiRkw5yPxN6cduB3-4PlCVvXb4OhKHArddmNIv8RHFA6zHsHYyU0pa8rWb5mTOxkTP9u1HmIUvEmVoCSK0vxzGlOpPlG0-dpK3zJnoorI_iQEmvlarsh_jwkVqBSloFW-XMHmBO32jmKLa4RLi2Zdp878jzjjZgfnt8TB2Gz8QqpsjMGfVjnxt6d7tgoYCqxikyGaeJ8r1vPEUDDJ10JqZy9iGpZuMacFb9xJBeMHwrqRQMn5ZU-zPWHg5zSo_KB-7c7uvNHJsCrOOu7KPh6lISU_3RWq0L3z1QYhQQa-G1H9ZYbtkXKlfL6hqbyKSiZlc7iEaH146Yg1xOakCIO98aUUxZF2VSh8aaoUwJm1yGoL6_fntSCQIPz3tAp4FBrD_VkCM0rwNk8snoD7JWvXDjDHH1yd-8mEibOlSduRg_JYFlzPh8gMMwvzSRUUWutwc7u0SN3-D5AF-tqA1SbnnV4yHTdhcqz1HOKGk6edr3Rd2a7UHeZK6mHu-9st5kDauOVz5i5KAxEOv7EWcBb9B63rLvdlSiUrrjv8mcfHGqHPQH8G4sk_fLiL7Suc_oMPEkPI-yGFs7hDLgTKXw_97hRZYSanictfoQs8PdSs9KDONmr4Ch96DFYhbsxQ4ECud1kmvsG4GDX0pK0HrHqLBAuo8eI6m8NobIslUPRLySCuHunuMroYuKjt8XCb-UkQZjr5infn5P8TCDsNWABp2U6scawX8PYL_bEae4DlwoVYDRh9P6rgJsQ_rd1AgcGRCCXNPv6O2UugxcACk8sAigoH8WicuOILC8eIwPUOOTX3PiXBjfYQUbLAZn9U0ubDEUhK20EYhZZvA5jVMzHXl2sutFP0DrCEPxVDDJCkrgQu2pTBsViS2wuVOIVH63UZ7wKj3MzYLKl7iA9vwJYd29KGP_n6CwPUX4I0QZeqaLHgkJ62hJduBg5Ebpf0iSFY9-kkjo-Sm-hhB872qfuaDyNzKPv3fwTyLpyLaxl--naZa0zLtMtlK4j0QwXZr14PZ253cWXZrO9UNDO1EO2JZh4V82Gyausz3Cz2DmbPoUGClF7J6_dsdDj8_Vm2FnRljYHL5Mp4yC_UHrU3Pe9qWYtV6mU3kVBnOZFHC260MxdHgP4WbQaGC58ORqFOMbYEQTrHhrU8XOO0KVMvjaMeWANeNZudDNFJsRF_BHeTJfT31gmTUHQYICQBEe0mImS-rJcwhOZgCcX36YenC6lXsLMM9ZWa3iGixFUrYzvYjaKrI68p8GBIugWQYoWvCHSVex4ZRRenQL4eNGzYU-JMffoJU8D9PlP-cLrd5OTvrOUbiUlkMEZ65dfpmM5HUKZC0NRzn5up3nWEVqI3NGFzmHRIkQUvYXmXdVuk62KGagHWWbIhwGIJI7_GLfsJ6iM1Kmi9S2vTcdBdR1Xdn_k9-81GhfA4ZZF2FKwziDPkYdV3oI10_4Ol54WMm9jaKLwfR187dzCn9QzWr-CZNAAh1LLVQ77Bu_51ON_tzQzhKinTi45_a1PfFKZMbWgE11S-YsWOdfTbIyXSdh46R_ZFaARMwohy73Xmulp8i2sucWDtQyCiAxa8mEJYxdL4fWF3SKlEUWc2rvpBl1zHhAOKQ_OmD8k8cqdlA4f7HCMYnJSFh1KaYgI4853KfWh6sA5I5L8lVANg3CwfUfhKt73wAHns7bCQG7HW9-Ezta3tEpO5XY7RPlkm6NoVdwckpDE5d3wibjsvB5qb7iFwSn8dFu7ZDK3lX9CrGI7VmYJWgNk627QS_uXp7xno5V94TQwGwwy0KbCoYyNXXpD5vuqL_3IYu5zIVfPQYpuz8XkPjowwtEZlj5na4ANuyBbkF1_l3M8XzS_YSxUbEtZgooOybk6V6lviDndPpdSvJFI-F9uFzlnVd67--8iA3ffB-wSNMmVbyHT-jzwk_Kl)

#### Начало вылета

![Диаграмма последовательности](docs/images/sd/sd-1.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/lLFBQjj05DtFLmnUkGGL-bY5Kl8XWJ1rr4PWZOGzMhIhkFHHQ6XeoRQ5_e5mFSGuiVmBT_wePqOHqdMhKa7fHcXcxZdtdFiucXirCqKw5IOnqrYEw2kLxZsLT4ELfANxY1_hNbCv4a8L9jD5-YoUYHoeP9BaIXjWljFQBH1awPRAOqqxW4hQulQSAbhU_L-Ef9hBv_by3_qDKL_eAhmgamh-_E2-1F_INTArkmWnaonD2vrCb4aopOCV8lYpbqwROotT1sHzmpNWcZR-K5kaPKrvbkHd-xOUWGpQ46wzE_oLy5YvSyzn3VpAbohWJvLH9qghwSjNCITv39Aha6-BMbf0VLrNGTIMR8sUPJe-yHn2l9XbHIvxko1GlkWfBy5XKFEBMJXix5Pq6wuWU8pN3TsuJw2tlYHa9QqH1gIb7-1ehBxpvK9owHQTzjfxWYNtOkhY7HpyTo5rOjbgE9G1iM0QqEvEAEiL5FzEHOy6qOM2gjEusZhj0kJ2crq7c-24NcZ1UTFCZz-HTWPAqT8mArGXVEV3QnE0D8Fate9X_ASSB4DFgVQAn1ihdqHDQ1JrTROPwLLx7AAA9uGsh7__67bsmBkPXoG3zrsAlYbX8NyxXWpKnyXN9XhWK8wz6N31Ok_g3LeyHlWlLgZb6x8WBGhSiJuLuWZV8ft-1000)

#### Инициация вылета

![Диаграмма последовательности](docs/images/sd/sd-2.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/hLRDJjjC5DtFKrYiWX2VFYX55OkANNVTi4MAJ70Jgx4JEGuINH5eIokGKYeMg59RiUdQ3N4nAPXNc7cZdZCsaSTAIOFOc67cd7D_xjmxMU-4TX1slQO8tR3fM7FoJDx8HBsNYOpuLNrB3jIH_2rZjI-ZEI7iRjZokzwM4uWsk6xDRTj-2EOvq3s0OdajeqrVte8KQRKzcSf1lkxFMNR7UjNkbDZVWFeiJ_Mf7Nh2F5xwpuB-GFNbfJhMc5hByxg-MxD3j-MRu6M0Js0ybQDDtr8VOFMjwGEsvKZ_4sdS89DikEr6EQmd48DlWCUC3gi8CQPgZngNu0-nSQZvstPeLstVRkw-SKoH5OYSQdito6LCQch98Pt2NfonWvRlLAbXSbV1_I5ZC66S_gfZ-gs3K3qpvvOwaBSQDM352Wdtu5Uz7DlI_z3-BbDeda24lbsXS2FiQ6iyqPNVqngiVDjjjiAIoX9LW4vWDKLKHnhTSOATLiSgOPTr8IDvJIGOaRo0bwaE8c5DO3-nU4pdcMaAOtsXHHkEtGmRrLh3gRqkARDGNugUgsFc-QUkLuIjM2PQOyiEGoVOBT6VaKvRT4GTijfo1CjNh3Bek7h3U_MgjS25djqi2Q_aVbsp8K0QGJXl2OQOLz-tTqgyf-1zrPLCaADnCvvXyrnJNBzJegnEfBnukR6X2NM_KsBGnYV06Gv2pMu0OzJDeqcEvmHrnw_j2b4FMjssDML22BIsjVYSFRomi6OXwF7rmYeUzqmMkm0CQBERrpIetBSP7oNGz_kI1G0avZOsJTcAUiVJUM7eqb3Uuuzf8bCqnCbNFKCULxi0DMR5sapsyemXpOkBavWimAmfdLQbwMbycEmZf6wQZI9wGk9xqCTyemqhox2C7fJ14LkSMxHTqVECKsD_-XsSNV4nydQFV3bdTuy7-ddcT8_7np-GAvmZg4XALooPc7YyUCIdNCB7VEh2Xl4eiAGwadrre7gYU5I8XAZiqS6tdrdFh0sBJweeZtOZ8jDKPVnC_ChwS5vWG8F0qSxWTSBvcWtvdcdQaU18pZ5_GU3404nyH_844cowUAzcdWoCaSamaGCAsF4zEsHLc38s3rA5ln_lVd08nzyMw_XqlUOV)

#### Следование в район мониторинга

![Диаграмма последовательности](docs/images/sd/sd-3.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/dPM_JXj14CRxVOgLgqI8AEGFYYWYkdHfQ2sXmpc15NjjsGSI7GSYA3AAaowA54KqgI_c3Ww3pwym-qRvPh8-xbQO8Ws2sVb-ysU_FJQ7KJ28zhiT5RMZJgWRT46tb55A1KqeeHdbb6cQQ7k4lsuGdMcweu8Fx34L2EVu_PAIXbB1VjGp-zsTSA3weBPRxNvW8jrOVwRfDw0pUooOMtiEJMB7JQDj350CL0Pime4JcalMH1hXEkE63eQw6vXWrqUlFGVx5nLWVWDaPaTqqpGqfS9Lmmbpx94mkCD-kzEBFCeQKsIM2HIf7KdsC1mSz8RQots1t0jAP0if50ccdr4XG-GqvI4eVt190jqBWqwqjztQ2riVFV9Ba7zKExVdM0ZzeGIK1A6CSc7i154K3Wuz-HkMSorkn9vXw9Ycg7oZwPhbTapfexpjrg0DNj3nmAzSNtSqbpkPygL1pXOHWmZ410UUxZLqF-KcStQ8_SHtgUaxWXSYQPkX9rb_KFBk_TQM27RDq5DmZQz8npWywZy7y8otQ6ygeh0R3dP3qpfKgjFhzVL_Mrmv2-hLj_TEMbdPq3IN-ko9ZE_EZZYKoOOvz7bXP5NAQemDgGq7dR6BQq_0ZkqNw7DxgiNLTz9nMWCvewAJ1wMKrQHsf9onIoKcc61lS_OSKZAtasK5eNERaCOpkaPPc9LTXV577isDhfpBKBRs2C28dVB4ngfwf6kLOlV82Zjs3KgDjFe9KRwL6L4Qe5xgIVaihgJ9ugc28La0A_CoUNwv_rGS8BCfjg3BMPA1atg2_suglbiaLtjy3EgsiRgw94sL76zmchl2S2MKYOOCFV1xiQUbiQlxzXLDGsdvcRjQN2kYsE82XlnBAfhc_YbHeaBpGMtY1_xB_0K0)

#### Работа в районе мониторинга

![Диаграмма последовательности](docs/images/sd/sd-4.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/fLPDRzj64BtlhrZuP2DHKQTfaWf5aLjllUHgG61anY8gaO986KXFLjqqBMpKJP53KQ0VERHdIYMZZrZINzZzHvqtN5FSDLMepKMWkFFUVBoPuJwE4s-G37jTaGH9rvTxwW-Lgh5QwQzLAjL4wZFwFrShjLIvLDVyCAF35HtCwFblbUu9uGsJA1psdle3qIU-e1tqlJ0XjZTaF2BpdA3fKQZMwfrAcUACg2Rc-MfFUh5yreyTz6zazPDwpQTUqXFsyU47alWd-afDzINRjADURnW6RIy9ej0slaV6hyZvIYsEGgc_8w_Vs37GQxNWFodRJGhAJj3lk6bzH6I8RQ5oP8SQ5IK1nvJm6RruoVXZB_5QNkXrdt_bsoJtYUGr-rlg2vK3kf8g8p8kTe4UHA7V0eUDVK3OlwYeIpX7lFeISNCIUcJNNEfpjMQh2UMLLmhUexXEtDmEFoJktzMAE5yH2MARat0BUiFUS08UVSOSKBuVTAF4OJa42_V8X12Plc3hs1-SHh5qRE-na2btLqQ8bBfggLQSn0oQaFzPRVCnQSVtkacdrUxuxIyTPWZrIpLoVOawZrclb5xbQiOSJxqayGVF7VWZmE4BWUYNK5ijoFESL0QSMY_xLxvMUn0GdzTrYE-RkAxLcZLP4B4P2QHer0-zKmVtCU5-PILdc3pzBRIKwcTw-OOXGHWxa0UraC-_UFA40ITXx20UiHfZ55cYx6OY23ub7RARZjKl6DyVH6q_ZeFmn6PvM9qthjRtAAE-aBSeZlrdhJY91jIBDiSdnF4dEXVpKDIb9e9QA0hr8sQREsLUj364ueWOv_VymOaVjbtH7zP0UJhNLZjR5AsRnXPcfcJZiqffxjnfIW8kgFz-e3OokKZkbxTgXZdTibj5DuhwydyiPR7nRiVIbErItAFGajUInYQeYjHe81yz8f8NjZesGGNYC3IT1Rm3kaJM-NMDZGYDHbEYQENwurN2i-luDqvnc5N_xhD4KtsEpO7gSmVNL_n023Fr58Arb12q0P_haQWULQ8rgOsOzUgc96kqMtMb2tUrWA9iHDlLVhcctdAfLWU25WG0j5eW8gzrv91n5foUm4emDbiiwCGsiFQOhIgCxH2tSjhIrPk9aiSbNHk_EN-OKqj9Qout7rKkGMPzW_VhlDwbWvt4kRkzlPZUzlRVskj0R0Atqq0I11bNF_65jqNLuJNUW2qhRWu8iVY-6a_fvlgHSgmKrfMitk4GtPOh79DBC15Z3egIm5pZdFZDpGhRn1rJLprZMa7P6mG8OLt-vAUDZOFcxfhOB718jzBQ0BTl4JjsmXkQfWHSZzp8Tp2Hjni5H_MjOXD2E3G5cUQu1K4hLchtrhjT52_flLTH26zejcLicTGlZ2ZnPNHARG5JmH_cAIV0ouvZGN18ssm77fDtnNbHXtLvqKq5jo-NPMn_bfP5zT3EZ5pIyPonUaHM6Uw4mW-F9KAoLervhDbEMCz4Hw_A-sHnIeKeexl6v66_5FpYCVqCUzr_0000)

#### Финализация задания и завершение задания

![Диаграмма последовательности](docs/images/sd/sd-5.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/fLRFRzn45BxFNp7g2LI2I2bjYH3gZHkNNYkjNCVTjTYrLxQtKZdjafI0DY8KLG8X0Qe4d9sjJPqbyVuBC_yHttjsPprJBq7Y4cLdtlUzx_ruptC_pRmacqt68WkpSI1lg1zLhbQgr7FzZIhLbQfKATLh71Ogfv_wJAfAwcDSNE7aRrNHhVwQRsp36q9uiooEPfD7GIAcS1JwuTIBChXv2OE5_WekBbN-C58RC3MmkQhLob18BvMFfwc3_XLMFwWNVEjb4s5VxxylmR_IP-grFcKRFvvCPb7eUraOHxRnBHW_X_DQhHz64a5N-jZMW6ErvXyvswqQob4u7RbXVGWoQ8DvIT7XlnmnrdfE76rkz0dZ3xtC6tYHDtxwPM2Jt0R92_PtfPUg96WjLK6YS5Osw2IEWW5nsDWxmFv9TMFdqAjFIJS7eHTspgK-KXksMY6kifFm2NGDtTZsFm3tRwe6vtEGaBOB56wD4_P6DyIZvyn1bP-6upXpMFQ91TOLlDQ8QidMQP0yYLFfsDxYGkQG2qiWSlKAAciEegAQm7yb-Ph4SwQvBrynwIZmnjbeu8y2_mk7cGhrSrUvFgKydtEzSXoLgcAEHrwM1SbJ1twFuEIBXEWJgZRaLEg2gWmuMg_uLxw1duJWyyOEyUrMroKFHAdMUc56WcUHIIBlYOFx2BXVk98LScJ6yISSlcH86AKEv4ulvBFF7pnWm31A7SGzhiOv9PbM0A1c0Q0EnPkErSyOFqrYFqZJC1hQB7UxyyRP-fRIg9VoBOh3uF4WpU84lMXpV0oEF_ISpTiTrQEW5qg9-fvccplbecbZAXGhObmm2P9X4FbkqUywK3ET6wkTBOh1cyOMxKp9lKyxgJbWCDTvpfbee-djQPKBCKpYsLHkbtIuOqU_HxgW2AShbnfLuyx4TZpgoZ8JU_CcwU8uQVPAcX6zfAEInUA8-TYJC32Buq2osuK-eMrXhHfzfh_ZeZ-Jl3qkMNHX4pLvWv9Ug2ejg5wAndwBH0Ghr6V3MybqoKw7mBMPOE4bvOQM0aylDwV3ng6BTfhXrbesu5Yqo2Ez4DqhQNbQjCkircUjGFPHT5UrS5S6KPW6irszOzRFNoooVbTWy06WbS5bHVpSKGNt5CScQDHRcnqMkB4CUlTJteJ0nhR4tPmc6NjxEyo4uN59D-oNnm38tDeV8eWEpRJy_X_UAfr1w7nSaJBBZkVCUI3LOcjleu4jeF2y-uLjDiRQQaG-Ouq56V4tvRZvmBNpds-__pdP5ZGAilk8uldiVqCnkIGcC9P4OGZQTvGJ0Jzjg2GSVWraEu1lfxarxQ0Ex3SK4C9wVSbFzhOEcknQ0ElTKsn_EYnmY6TXdxn-GeYrbGFTafXLvUYsJAxl0bSVFKp_XpwW3Kc_FilaUdqy4lVn1w_zVm00)

#### Аварийная посадка

![Диаграмма последовательности](docs/images/sd/sd-6.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/fPFF2jD04CRl-nHBJtfGK46X1-c326LDWmqacv1iX7fggb2bOgnu5do361hwfpPzXPatSdO3jTC6BrxADlc-ttxpJJlAZ4fD7eN212RqvG2-GWqLpc47UpZHgPHmXXOBg6031wW6GgZSn3gFNlkfICWTU46Yj27l3_9zW-y3gJAfJ2JuwoUF9Vo46alOucUdyU8eodNWAHF4cekVadWDHsZXy4fB_0Wx_43qrgQ34tqhwR7DOqCwNTqXfq4olGtsZ62KZUGD5hYWKuKB6cfk6LitMOLBvvyeeyPAgt3spkUGvmHXvU0AzX9-TI6TsO_yz8sllTdDu2zwh8sz--mUr0JOu8eZnfcVleqpAOIWAkMZbxojeGj-ryk9JitLLBOgQ1xm5JuK3ENONMt_IUqWZEUwBXYHj5TIrlXGSYODV_sQv7yB8ctbykt_yMiLOHmdhFn-sONAhhZ4Bt29Qrn8V6zNvkuzOebVy9D5IaAqyDlrGdkyXV653diO58WnN21kwqL9g75b9u4ZsPfkBNTfz4ICw8F-v7y0)

## Указание "доверенных компонент" на архитектурной диаграмме

![Переработанная архитектура](docs/images/drone-inspector_security-arch.png)

#### Таблица доверенных компонентов

|Компонент|Уровень доверия|Обоснование|Комментарий|
|:--|:--|:--|:--|
|1. Связь|$\textcolor{red}{\textsf{Недоверенный}}$|||
|2. Блок шифрования каналов|$\textcolor{orange}{\textsf{Доверенный}}$|Соблюдение ЦБ 1, 2, 3, 4, 6, 7|Смотри Негативный сценарий 2, 3, 5. Введение такого модуля позволяет нам изолироваться от Среды передачи данных, убирает возможность реализации атаки Evil Twin, Человек по середине, любую прослушку данных в каналах связи и соотвественно не дает изменять информацию от наших систем. А так как системы доверенные то получаемые данные от них автоматически авторизированные и аутентичные.|
|3. Оркестратор задач|$\textcolor{green}{\textsf{Доверенный}}$|Соблюдение ЦБ 1, 2, 3, 6|Нужен для реализации аварийного блока и данных о дроне.|
|4. Данные о дроне|$\textcolor{orange}{\textsf{Доверенный}}$|Соблюдение ЦБ 6|Смотри Негативный сценарий 3|
|5. Аварийный блок|$\textcolor{green}{\textsf{Доверенный}}$|Соблюдение ЦБ 1, 2, 3, 5|Смотри Негативный сценарий 1, 4, 6, 8, 9, 10, 11|
|6. Центральная система управления|$\textcolor{red}{\textsf{Недоверенный}}$|||
|7. Блок защиты данных|$\textcolor{orange}{\textsf{Доверенный}}$|Соблюдение ЦБ 4, 7|Смотри Негативный сценарий 2 и 7|
|8. Сбор и анализ данных|$\textcolor{red}{\textsf{Недоверенный}}$|||
|9. Хранение данных|$\textcolor{red}{\textsf{Недоверенный}}$|||
|10. Полетный контроллер|$\textcolor{red}{\textsf{Недоверенный}}$|||
|11. Приводы|$\textcolor{red}{\textsf{Недоверенный}}$|||
|12. Самодиагностика и мониторинг|$\textcolor{red}{\textsf{Недоверенный}}$|||
|13. Контроль батареи|$\textcolor{red}{\textsf{Недоверенный}}$|||
|14. Комплексирование|$\textcolor{orange}{\textsf{Доверенный}}$|Соблюдение ЦБ 1, 2, 3|Смотри Негативный сценарий 6|
|15. Навигация ИНС|$\textcolor{red}{\textsf{Недоверенный}}$|||
|16. Навигация GNSS|$\textcolor{red}{\textsf{Недоверенный}}$|||
|17. Аварийные приводы|$\textcolor{green}{\textsf{Доверенный}}$|Соблюдение ЦБ 5|Смотри Негативный сценарий 11|
|18. Критичный заряд батареи|$\textcolor{green}{\textsf{Доверенный}}$|Соблюдение ЦБ 3, 5|Смотри Негативный сценарий 12 и 13|

#### Качественная оценка доменов

|Компонент|Доверие|Оценка|Кол-во входящих интерфейсов|Комментарий|
|:--|:-:|:-:|:-:|:--|
|1. Связь|$\textcolor{red}{\textsf{Недоверенный}}$|CL|3|Апаратно-программный модуль который отвечает за приём и отправку данных, может быть реализован как и радиоканал, GSM связь, 5G, спутниковая связь и т.д.|
|2. Блок шифрования каналов|$\textcolor{orange}{\textsf{Доверенный}}$|SM|2|Программный модуль реализующий в себе криптографические функции|
|3. Оркестратор задач|$\textcolor{green}{\textsf{Доверенный}}$|SS|1|Программный модуль занимающейся только первичной инициализацией и отправкой команд в модули|
|4. Данные о дроне|$\textcolor{orange}{\textsf{Доверенный}}$|SS|2|Программный модуль сохраняющий в себе индентификацию дрона и добавляет их к отправляемым данным|
|5. Аварийный блок|$\textcolor{green}{\textsf{Доверенный}}$|SM|3|Программный модуль отвечающий за аварийную посадку дрона, снижает высоту вниз с заданной скоростью, проверяет данные высоты и полетной зоны с координатами|
|6. Центральная система управления|$\textcolor{red}{\textsf{Недоверенный}}$|CL|5|Апаратно-программный модуль содержащий в себе кучу функций|
|7. Блок защиты данных|$\textcolor{orange}{\textsf{Доверенный}}$|SS|2|Программный модуль реализующий криптографические функции|
|8. Сбор и анализ данных|$\textcolor{red}{\textsf{Недоверенный}}$|CL|1|Апаратно-программный модуль содержащий ИИ, камеры, лидары и т.д. для выполнения мониторинга|
|9. Хранение данных|$\textcolor{red}{\textsf{Недоверенный}}$|SS|1|Флешка, SD карта, eeprom, HDD, SSD и еще что может хранить данные|
|10. Полетный контроллер|$\textcolor{red}{\textsf{Недоверенный}}$|CXL|1|Апаратно-программный модуль занимающийся управлением движения всего дрона, может иметь ИИ, наличие доп датчиков для определения движения и тд.|
|11. Приводы|$\textcolor{red}{\textsf{Недоверенный}}$|SS|1|Сервоприводы и драйверы|
|12. Самодиагностика и мониторинг|$\textcolor{red}{\textsf{Недоверенный}}$|MM|1|Программный модуль опроса компонентов|
|13. Контроль батареи|$\textcolor{red}{\textsf{Недоверенный}}$|SS|1|Аппаратный модуль считывающий батарею|
|14. Комплексирование|$\textcolor{orange}{\textsf{Доверенный}}$|SS|2|Программный модуль занимающийся комплексированием координат от двух систем навигации|
|15. Навигация ИНС|$\textcolor{red}{\textsf{Недоверенный}}$|MM|0|Аппаратный модуль инерциальная навигационная система|
|16. Навигация GNSS|$\textcolor{red}{\textsf{Недоверенный}}$|MM|0|Аппаратный модуль спутниковой системы связи|
|17. Аварийные приводы|$\textcolor{green}{\textsf{Доверенный}}$|SS|1|Сервоприводы и драйверы|
|18. Критичный заряд батареи|$\textcolor{green}{\textsf{Доверенный}}$|SS|0|Аппаратный модуль считывающий батарею|

### Проверка негативных сценариев

|Название сценария|Описание|
|---|---------|
|НС-1|Тест Негативного сценария 1. Модуль связи скомпрометирован и пытается изменить данные, что приводит к измению пакета из за чего Блок шифрования данных не может его расшифровать, ЦБ не нарушены|
|НС-2|Тест Негативного сценария 2. Злоумышленник начал прослушивать данные с канала связи, но не смог прочесть данные, ЦБ не нарушены. Аналогично для Негативного сценария 5|
|НС-3|Тест Негативного сценария 3. Модуль связи скомпрометирован и пытается изменить данные, что приводит к измению пакета из за чего ОрВД не может его расшифровать, ЦБ не нарушены|
|НС-4|Тест Негативного сценария 4, 6, 8, 10. При компроментации модулей в этих сценариях, дрон совершает аварийную посадку, ЦБ не нарушены|
|НС-5|Тест Негативного сценария 7. Злоумышленник изымает модуль хранения, но данные внутри него зашифрованы, он не может их прочесть, при попытках взлома модуля, после 3 попыток он стирает данные, ЦБ не нарушены|
|НС-6|Тест Негативного сценария 9, 11, 12, 13. При компроментации модулей в этих сценариях, дрон совершает аварийную посадку с заданной скоростью не более 1 м/с, ЦБ не нарушены |

**Негативный сценарий - НС-1:**

![НС-1](/docs/images/test_ns/ns-1.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/rLF1pj906BplKspmyXki2Huv4Dv3F5Ieq8HkcxAz0r5YeWd1UF2YnZVOW9lM5kehVFj6pcvfOj74wCcVX8LytypipAGThwIVoYnQCXdAPS1xzDcigQOZQVoMf3Xz94qdKcPB1SONB4zKSxCnEomkf80hp9uFUepvcOn55ZqFKfP0Dfo6YIyaHBzG0S8MX3EfYQ3lL942kMWkk_xVzxY_uY-IrGtx4r3lwBtR-Z9YtVNWCOV-qUmfDsyTPXf7KIR2gI_3MF07QJ3hCfw0SO23cig9uEOrhdxPDOAn3M_ZETonqLs4oGBPy9cdSPPm-k3WEpIZSDeQOEGDA1fX5KCKxesivtv_o96wfieSiB8jQauvvBysTv9cW07TTJzqe5yiEZvCOgGenwa1qNQCOLVsphoosuUisuhtrFRoRDI6QktXUxPKfFXcHufA6uPTOPOtJuD0T9WNqiwAsTmuhHvnf8L6KsVvaoA7kHntQMUpegBDZz8yR_YRQBREloteJvt_zwNyI-QozMk3tjaN3-YrsTw3Pu2nGCpO64SMBNy0)

**Негативный сценарий - НС-2:**

![НС-2](/docs/images/test_ns/ns-2.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/vLTDRzj64BtlhrWu5nknYiPDarGeYjnwwoN7fX0OcP68IgH0qWRIarKtSGiRLLFaK1HeqXpQCsr94QNeuo_i_gFE6r8qTqCLAdpinPAryzw-cJSxN3wCOYUCZxeT4NjnnvKxweq-KKjrfSRqELE9L0irLaELwEzLIZylQ76ebbBtzGjQMAY4ub8za0SxGZX7SU0VTP-ueUWHhTVqUeuV4-bR2kaJmrZDLVBOLolrNYK4JlFDik-37Ub4ycalij2lAUfNzOfNdRWhR79Q7giHjAvODl-ZprGgrOYf5_fSFsTu5Bg7Zhn5VosMEnz9Kdcb1sgYBpYq6NIxHxxNT68lyCtW0mf-IIairUonB_MFfFq7CnFw6TL3VJZkAgDiUxssNPnFYEmr5tkC6j4tr7gfJy0n8Jmdm_X39tOQZkzqddtdcYHtYUJLEbSr1dH9sKCK3CpGOU2x3N2Os7k4_HjUOdFerHVGpKdelkcSrATgnL5NbDUuP5kNTBNitEvyJDnlr98uNn89j4t9_XbKOJUiW4UVC0Vwf-TrWjXYWJdeIpJWah8wpxnqm-CWabRi0HkPg3aY2P6e8PgMaqZX2UsVIYn3F5SQn0irPDAswtJYTgFPTflVMimmwlUoSds1Eb-oNmdtNSeSJvmuTiDd5lm1uDWBGlGPt2OvgPh2PO9Jwut-bQ_H33tYSpeMyTrSrrojs9CPcyRjY1HpzttdsC9zIhW_sCcK3_WBFiVgD_hnBKCyFx8WzoeXNtxrw143Mdva8Hwm6vSeiaJPynD1y0dvO9_ENXWqtIZo_9R9ShzythXQFw6C-lp30txeFcr4SH1IBveSdn77N-XS7cXSbme5bL0KwXUSRUwKQTR6C8eLCSxjkc7BzPkswVShe7mwLqOx6nIDTMEB_4p9sXUbqjo-NPS4d57__OmsodAHt2_lL8fpMjdUAX6T8EX9zQTAu0YQZ8WarsJAyUDDmElTJIrrsIpCHLObUmrhB8AIIRKQyj5z8dbkkcCIb20MGzqQm5kW2sJLldPmRaAjLfSeMZ7-U9JmsRNtppR5ugZyxovRDD6dc1oeFdTmTSNtXCXFFKamXX94v-1JtHVbfPBQFBK-imxM9LcXtSeZNTYZ1HH58vfRxHPZwXsNQhadQ40G0AC59l9OHmuZpeBJ4nW9USo625en0gmvPhYAO4lY9axBkiemKV3Of2lp5cGuMJwNfOSgbs1aF8DtgtRTfuMjpDdVt5vCR-tsdzfhJrmBDzD04WIvB3_YizrcvGtd-0Lie-pc08dPypNVARc-VYIibMGDPFac27KRBe9CBi64Qn4e2eByCcZfpszMc2RsCRNTur2Oz_MjLkYw_ZS5sfmaG0hZ4YW_NqDgrnlMj_V8OYi9u6jffVJDyyNCYXb0IPzhGihdZEYgvYafmyJJfzdj4iTvNw9fuF8C7xoEHaK33IKawRwX10rsaMrSoWNtTzXmWro8GTQOg5wnBwYs294V7WSiLHu8Yn0rG-jJw1XtFNGaz-Fs1-p_ORKJTszeDJ786XDjyj48gHxsGUpAu9YED485Nwecd0i_g5WBnC7CVBBpY7kVhMVkhegNb4Jmw66pByqhnIBh2OmY855ADMMixbFK2FTvuVg74fACnqJ-jUB9WaThzefOl0jagrI8GjsSfsQV8fXVFAG_zDB-3m00)

**Негативный сценарий - НС-3:**

![НС-3](/docs/images/test_ns/ns-3.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/PPB1Ji9054NtxojUOAicwiw5uJ_KHOK6cj1fKwPxC8QOQ48qBjoeyGycI4C5gRzmvu-yAIoeRcRcJU-zxxn9EoCRP3QFXs8ZEmorXNS_HeKv2kuhECKh2dp2-HkKlDwWObMfd_Wf2fQEkjBFzBGb4kGsCNby7MQICZRgHcbWB4FVA7h2Sqk3aGOsbkRduoF51-P-XgL_g3NT98vp4tK36oL6srdOQpfEw7Z4cYohIwF-ZWItEsv79lBm6gkwSBLkliqTHEc0TDBFaZnLlDJYAITpN6bJOjpJK71S9pkv7bwq-raOcglp9jcPOWdth_s64L-AaiS5-4RCee0rWNYk_5YngFMaa-QiRCLfsOZFnFWVL3N-DzmkbbUEGGGKIlRGjeOD2cMqyvC_MEi3PMzQbMvkUq54nP8jYChJ6gL8Q7hIuS8_unS0)

**Негативный сценарий - НС-4:**

![НС-4](/docs/images/test_ns/ns-4.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/hLN1Jjj04BtlLwpIIoj81IsbY0FYrbil79iAcM05gyucSXoataXGGLLGGszLfGfnwTaDDZWGExym-qUTcIp6CQQvz998i_FUpBnzuztk-9RdTvkky1tVjMK5BlGHf3222Fzl8P2GG0HN4EW-n1XEz41_aRgdJp2SOFW8mn6CvDgoN5-M6yjoTQKYXDNrMwhRtBCzqSO2JjrfMygNbVMN4duJKlSH6S2TFcEMOKqXASH8tCVZ2GGKE8OfPutWZZ1uFAn8goERbh8QjYUVUVR-FF_g2XQuW1I9loCJTWlZci91KbCIJuXC7p4HjTbst9PVHhLAL3pV266X7Z2aOtk7hKvP_YlClyHk9vIDg01bIo3baMBI4Xk99HtpA7r8cJo1AoO-i2tNFzYj7zZrJx90_HgfV-Pdq6Ue3_pXQw4xY21caZtBzstlSm6-GN0gHfteKno_X_t4C9PmGt0zXF2VVBjrpq4-ooqGhvc-9Z3bAxgbEpG6IiWOJAAimmBk3U9-ySN6xAqJkbe9Fp1uoH17bKgyNefxztvdXr4DrIc3KRLp61cpZcUke6dliD5RHjfDsslOgbvKxcq9D2AffWLZv2XsZKM4S5kjDdg2fGbPb60cYyI5OMUFwL9BFG61kBTvzGFDz77hmQvBIvlO0dT5Vel85dg08LxRY4DVxrT6PB0Ifatk0prwIWipjt9wgByXIupxpWiquUx3ChhPnDXLAG54SmHw86RvHJpED49zfxoa2RUFs0N5grlIwCIZH723BU1-i97xUl2OaoGHnjWIuVd5GuwUGHxhdfZRoRbAFRFOgHwQDhb6cF-8YUBs44Lca_bIpxDDlEOcqnV2KJc5S8TGNjQ2FHAoItX2mRRFPpwHXoUKrl1iM-KIozVNEBK8olU_k4YcMBNwHBh8-FAeV95fyK4AkJT-Y1QZW_poqaE3X7HrU10IdTdHyqLfvOKAAy--8DckC_FobvQ6Dk-0X9WToGOY0OeS_vrVxJ_-a9Z0OtLh2a93bLMXnvdSUIyyvbz1MbCF7p08kCms_dIRxby0)

**Негативный сценарий - НС-5:**

![НС-5](/docs/images/test_ns/ns-5.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/bL8zKy904EtlL-o44cEBKZZy3t6S64xC2859GXzHHALWh2mT2_lumN23vdx3xZzoBp2OapHMoUtjUs_Vssl5YHSbetvF947Ia-3WCwMeyHqN_5rX1fZZ0Zymep4gBkUe-QI1hkYMBtA-I57H71gE4Due6OIZ_fcCn91f0pyOUc42pi4-u0k-eQOKK05c1eTVg73P3l6pEESqeua3NWp3QE3BE0x2hitIO9P7HcbSCMh9olUiFAOPx51qvFbfd0mYhojjZaFcUANKj1VJArnKJ509nIUZJTVupNrt_B_6hmh4XUTVogWMoOuGl_E3UrHoqmH_cq4xj5Am7FmXA7bntNgzoT6ZfebjmYOeGS0zhdKZASCJYwa9R47HpMRPsJzODgNgEOHO9s4074QvtVYa1vhJk93Q8fM9W5UPxK3NPnQQCgRAAA-EbNabNACfPdjWdiMECorQCkpm8_y1)

**Негативный сценарий - НС-6:**

![НС-6](/docs/images/test_ns/ns-6.png)

[Cсылка на исходник диаграммы](//www.plantuml.com/plantuml/uml/hLLDJzjQ4DtVNt6LjtbFa2S2BMrPLEowwuPbgP09LeYQE95ZaDWHK45LK4DtLQKAiUdQ1HkSxxymzn_rpFW2nZ9XquKXcZldpCpn6T_rJk3umLwpeO9wq71rYIxC8KtfYcBy7rAeQK8nNLDeZYX1U69wvhCsNNE2y0JXGuHZkj9l5dMbWcSPpqf9AMSlQ7bxpMtNLssKg5VhRSSBT6drVqs_66kEW0rfPCw4fx_fWPOIK1_XU4mX1uvfnbaeF68CZlibxNHqq_6SMfwwiWJk2vg2ynj8q2eDDZrCCRNLSC8yvb0ukCDslT4Az3--kvEZgZ2L37S5M6Hw0kcu_dwhKvI_ZFnBD3hcRA12Q3QXgKoJi91e9D5oZ2aGd0hvXAw5UDTr6i7kLdNNhNugeby1_O_C750Dyj1lUIyXGZ4bGhJj187h7nHnl6OEhiejcLFeq4LZ2GqqtJA7wLCqbtIhwjV1vpHon2ziSsEQoMiQWZYnDfgmFOJ4S_Ppk9V0_PINcuZ3JlZrQlgEuAL0wbv7vp2hXPXtxpSs157pEda8Lpb7VchLGMeBddA41eU2SfkkNtEzwa6ksAi2QCmIpNBEo51iMOyerMYrsZ25I1A9664gXyQwYAi7Y4uAJK6XiXRNvRSFJbrOM4DnxaUi5hCRJ0yXMTTOGb_k5aKz6BpyWVtmCSEq9Xt0dgUyAuyMpVJDLx0as7FPdR7q7HNHfREYgq82YhC4K4gb-Ndy6WI1iZFsDH9ZgzByuf35AiIZ07IB5h0MR5t8qYlWX2JAMlcXXUpcWQbhySUcgx97Tu1irQxTxwdfsvQbNfJzZAdyxZ1HpNTT3rJtfdbS-5yHybOsyaPQ3nUrhHNII7wTwUMbr8VJz5ECCrZiFyKx0ssmRM8MQ2YkYiHNeepY9R4vJsJW99jGlDhMpNV9cMdcabhzokKdqjGzpnDIqIn_HKNIYrnDpwF3x4BpnGD2bXG74TFPlJr_Bcr-8ViP49UmJ3VtjaPWA4FRoq5J8buLEx40UOw_pk_joBEEFxZv_m00)

|Компонент|Соответствие|
|-----|-----|
|1. Связь|communication|
|2. Блок шифрования каналов|chipher|
|3. Оркестратор задач|data_analyze|
|4. Данные о дроне|drone_data|
|5. Аварийный блок|emergency|
|6. Центральная система управления|manager|
|7. Блок защиты данных|def_storage|
|8. Сбор и анализ данных|processing|
|9. Хранение данных|storage|
|10. Полетный контроллер|autopilot|
|11. Приводы|servos|
|12. Самодиагностика и мониторинг|health_check|
|13. Контроль батареи|battery|
|14. Комплексирование|nav|
|15. Навигация ИНС|ins|
|16. Навигация GNSS|gnss|
|17. Аварийные приводы|emergency_servos|
|18. Критичный заряд батареи|battery_critical|
|ОрВД|atm|
|Система планирования полётов|fps|

### Политики безопасности

```python {lineNo:true}
policies = (
    {"src": "communication", "dst": "chipher", "opr": "initiate"},
    {"src": "communication", "dst": "chipher", "opr": "register"},
    {"src": "communication", "dst": "chipher", "opr": "set_token"},
    {"src": "communication", "dst": "chipher", "opr": "task_status_change"},
    {"src": "communication", "dst": "chipher", "opr": "start"},
    {"src": "communication", "dst": "chipher", "opr": "stop"},
    {"src": "communication", "dst": "chipher", "opr": "sign_out"},
    {"src": "communication", "dst": "chipher", "opr": "clear_flag"},
    {"src": "communication", "dst": "chipher", "opr": "set_task"},
    {"src": "chipher", "dst": "data-analyze", "opr": "process_command"},
    {"src": "data-analyze", "dst": "drone-data", "opr": "set_password"},
    {"src": "data-analyze", "dst": "drone-data", "opr": "set_token"},
    {"src": "data-analyze", "dst": "drone-data", "opr": "set_hash"},
    {"src": "data-analyze", "dst": "emergency", "opr": "stop"},
    {"src": "data-analyze", "dst": "manager", "opr": "process_command"},
    {"src": "drone-data", "dst": "communication", "opr": "send_response"},
    {"src": "drone-data", "dst": "communication", "opr": "send_error"},
    {"src": "manager", "dst": "drone-data", "opr": "send_response"},
    {"src": "manager", "dst": "drone-data", "opr": "send_error"},
    {"src": "manager", "dst": "autopilot", "opr": "move"},
    {"src": "autopilot", "dst": "servos", "opr": "move"},
    {"src": "autopilot", "dst": "manager", "opr": "set_move"},
    {"src": "manager", "dst": "processing", "opr": "get_data"},
    {"src": "processing", "dst": "def-storage", "opr": "get_data"},
    {"src": "def-storage", "dst": "storage", "opr": "get_data"},
    {"src": "storage", "dst": "def-storage", "opr": "send_data"},
    {"src": "def-storage", "dst": "manager", "opr": "send_data"},
    {"src": "data-analyze", "dst": "drone-data", "opr": "send_response"},
    {"src": "data-analyze", "dst": "drone-data", "opr": "send_error"},
    {"src": "drone-data", "dst": "chipher", "opr": "send_response"},
    {"src": "drone-data", "dst": "chipher", "opr": "send_error"},
    {"src": "chipher", "dst": "communication", "opr": "send_response"},
    {"src": "chipher", "dst": "communication", "opr": "send_error"},

    {"src": "data-analyze", "dst": "drone-data", "opr": "register"},
    {"src": "drone-data", "dst": "chipher", "opr": "register"},

    {"src": "manager", "dst": "drone-data", "opr": "sign_out"},

    {"src": "ins", "dst": "nav", "opr": "set_ins_coords"},
    {"src": "gnss", "dst": "nav", "opr": "set_gnss_coords"},
    {"src": "nav", "dst": "data-gruber", "opr": "set_coords"},
    {"src": "data-gruber", "dst": "health-check", "opr": "check"},
    {"src": "health-check", "dst": "battery", "opr": "get_battery"},
    {"src": "battery", "dst": "health-check", "opr": "set_battery"},
    {"src": "health-check", "dst": "data-gruber", "opr": "set_battery"},
    {"src": "battery-critical", "dst": "data-gruber", "opr": "low_power"},
    {"src": "data-gruber", "dst": "emergency", "opr": "stop"},
    {"src": "emergency", "dst": "emergency-servos", "opr": "land"},
    {"src": "data-gruber", "dst": "manager", "opr": "set_data"},
    {"src": "autopilot", "dst": "servos", "opr": "move"}
)

def check_operation(id, details) -> bool:
    """ Проверка возможности совершения обращения. """
    src: str = details.get("source")
    dst: str = details.get("deliver_to")
    opr: str = details.get("operation")

    if not all((src, dst, opr)):
        return False

    print(f"[info] checking policies for event {id},  {src}->{dst}: {opr}")

    return {"src": src, "dst": dst, "opr": opr} in policies
```
## P.S.

Код весь реализован за исключения центральной системы управления, так как не хватило времени
data-gruber - Остаток от приведущей архитектуры, в решении был использован шина данных и она была доверенной, собирала параметры. В ветке documents если посмотреть коммиты то можно увидеть как это было реализовано.

## Запуск приложения и тестов

### Запуск приложения

см. [инструкцию по запуску](README.md)

### Запуск тестов

_Предполагается, что в ходе подготовки рабочего места все системные пакеты были установлены._

Запуск примера: открыть окно терминала в Visual Studio code, в папке с исходным кодом выполнить

**make all**

запуск тестов:

**make test**
