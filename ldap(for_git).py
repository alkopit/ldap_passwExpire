
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL, NTLM
import re
import datetime
print('')
print('')
print('')
print('')
print('		 █████╗     ██╗   ██╗     ██████╗ ')
print('		██╔══██╗    ██║   ██║    ██╔════╝ ')
print('		███████║    ██║   ██║    ██║  ███╗')
print('		██╔══██║    ╚██╗ ██╔╝    ██║   ██║')
print('		██║  ██║     ╚████╔╝     ╚██████╔╝')
print('		╚═╝  ╚═╝      ╚═══╝       ╚═════╝ ')
print('')
print('')
print('')

AD_SEARCH = int(input('	Выберите OU пользователей:\n	1. Users1\n	2. Users2\n	3. Users3\n	4. Users4\n	5. Users5\n	6. Все \n \n	Ввод: '))

if AD_SEARCH == 1:
    AD_SEARCH_TREE = 'OU=Users1,DC=domain,DC=local'
elif AD_SEARCH == 2:
    AD_SEARCH_TREE = 'OU=Users2,DC=domain,DC=local'
elif AD_SEARCH == 3:
    AD_SEARCH_TREE = 'OU=Users3,DC=domain,DC=local'
elif AD_SEARCH == 4:
    AD_SEARCH_TREE = 'OU=Users4,DC=domain,DC=local'
elif AD_SEARCH == 5:
    AD_SEARCH_TREE = 'OU=Users5,DC=domain,DC=local'
elif AD_SEARCH == 6:
    AD_SEARCH_TREE = 'DC=domain,DC=local'
else:
    print('\n	Введено некорректное значение')
    #break
print('')
try:
    print('	Выбрано OU:',AD_SEARCH_TREE)
except NameError:
    print('	Выход из программы\n')
    exit()
print('')
	

AD_SERVER = 'dc.domain.local' # DNS имя сервера Active Directory
AD_USER = 'domain\\adsync' # Пользователь AD, два \\ обязательно
AD_PASSWORD = 'Password' # Пароль
#AD_SEARCH_TREE = 'DC=domain,DC=local' # Начальное дерево поиска
#AD_SEARCH_TREE = 'OU=Dismissed,OU=Users,OU=Insigma (office),DC=domain,DC=local' # Начальное дерево поиска

server = Server(AD_SERVER) # Строка сервера
conn = Connection(server, user=AD_USER, password=AD_PASSWORD, authentication=NTLM) # Строка соединения

if not conn.bind():
    print('	ERROR IN BIND', conn.result) # Статус соединения ошибка
else:
    print('	Соединение с DC... - OK') # Статус соединения ОК
	
print('') # разрыв строк
print('') # разрыв строк

uAC_66048 = 66048 # Атрибут userAccountControl - Учетка Включена, срок действия пароля не ограничен
uAC_66050 = 66050 # Атрибут userAccountControl - Учетка Отключена, срок действия пароля не ограничен
uAC_512 = 512 # Атрибут userAccountControl - Учетная запись по умолчанию. Представляет собой типичного пользователя
uAC_514 = 514 # Атрибут userAccountControl - Учетка Отключена

#ADUser = input('Введите имя пользователя: ') # вводим нужного пользователя
#conn.search(AD_SEARCH_TREE, "(&(objectCategory=Person)(sAMAccountName=" + ADUser + "))", SUBTREE, attributes =['cn','sAMAccountName','displayName','pwdLastSet','userAccountControl']) # ищем пользака в AD_SEARCH_TREE, читаем атрибуты

conn.search(AD_SEARCH_TREE,'(&(objectCategory=Person)(sAMAccountName=*))', SUBTREE, attributes =['cn','sAMAccountName','displayName','pwdLastSet','userAccountControl']) # Ищем всех пользователей в AD_SEARCH_TREE, читаем атрибуты

for entry in conn.entries:
    if entry.userAccountControl == uAC_66048:
        print('	Пользователь:',entry.cn,'| Cрок действия пароля не ограничен')
        print('') # разрыв строк
    elif entry.userAccountControl == uAC_66050:
        print('	Пользователь:',entry.cn,'| Учетная запись отключена, срок действия пароля неограничен')
        print('') # разрыв строк
    elif entry.userAccountControl == uAC_514:
        print('	Пользователь:',entry.cn,'| Учетная запись отключена')
        print('') # разрыв строк
    else:
	
        pwdLastSet = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',str(entry.pwdLastSet)) # вытаскиваем дату установки пароля
						#  год   мес   день  час   мин	 сек	

        print('	Пользователь:',entry.cn,'| Cрок действия пароля 42 дня')
        print('	Пароль был установлен:',str(pwdLastSet)[2:21]) # отладочное

        date_1 = datetime.datetime.strptime(str(pwdLastSet)[2:21], "%Y-%m-%d %H:%M:%S") # получаем "дату" из pwdLastSet 
        end_date = date_1 + datetime.timedelta(days=42) # вычисляем дату окончания действия пароля
        print('	Действие пароля закончится:',end_date) # выводим на экран
        print('') # разрыв строк
		
i = 0 # подсчитать их количество
for entry in conn.entries:
	i = i + 1
print('	Всего пользователей:', int(i))
print('')
print('')
