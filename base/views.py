import json
import os
from .forms import InfoRoom, UserRoom
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import datetime

date_today = {}


class Database:
    files = {}
    File = ''

    def database(self, x, file):
        data = {}
        if x:
            with open(file) as f:
                data = json.load(f)
        else:
            with open(file, 'w') as f:
                f.write(json.dumps(self.files))
        self.files = data
        self.File = file
        return self.files, self.File


def home(request):
    return render(request, 'home.html')


def create_account(request):
    value = None
    if request.method == "POST":
        ls = Name(name=request.POST['name'])
        if request.POST['save'] == 'saved':
            if Name.objects.filter(name=request.POST['name']).exists():
                return redirect('home')
            ls.save()
            if request.POST['value'] == 'agree':
                value = True
            else:
                value = False
            ls.information_set.create(name=request.POST['name'],
                                      age=request.POST['age'],
                                      dept=float(request.POST['dept']),
                                      date=datetime.date.today(),
                                      bool=value,
                                      balance=float(request.POST['dept']),
                                      birthday=request.POST['birthday']
                                      )
            ld = NameHistory(name=request.POST['name'])
            ld.save()
        return redirect('home')
    return render(request, 'create_account.html', {"value": value, 'date': datetime.date.today()})


def log_in(request):
    ls = Name.objects.all()
    return render(request, 'log_in.html', {'name': ls})


def account(request, pk):
    global date_today
    ls = Name.objects.get(id=int(pk))
    get = Information.objects.get(name=ls)
    date = [get.date.year, get.date.month, get.date.day]
    hence = datetime.date(date[0], date[1], date[2])
    today = datetime.date.today()
    faith = today - hence
    data = Database()
    if not os.path.exists(f'base\\database\\interest\\{ls}.txt'):
        if not os.path.exists('base\\database\\interest'):
            os.mkdir('base\\database\\interest')
        open(f'base\\database\\interest\\{ls}.txt', 'w').write('{"time": [2022, 2, 22]}')
    data.database(True, f'base\\database\\interest\\{ls}.txt')
    database_time = data.files
    joy_date = datetime.date(database_time['time'][0], database_time['time'][1], database_time['time'][2])
    time = today - joy_date
    day()
    if get.balance < 1:
        ls.information_set.update(dept=0)
    if faith.days > date_today[date[1]]:
        result = (faith.days - date_today[date[1]]) + get.dept
        interest = faith.days - date_today[date[1]]
        if get.interest_bool:
            ls.information_set.update(balance=float(result), interest=interest, interest_bool=False)
    
    if time.days > 0 and get.interest_bool is False:
        balance = get.balance + time.days
        interest_count =get.interest + time.days
        ls.information_set.update(balance=float(balance), interest=interest_count)
        datas = {'time': [today.year, today.month, today.day]}
        data.files = datas
        data.database(False, f'base\\database\\interest\\{ls}.txt')

    return render(request, 'account.html', {'info': ls})


def edit(request, pk):
    ls = Name.objects.get(id=int(pk))
    form = InfoRoom(instance=ls)
    if request.method == 'POST':
        form = InfoRoom(request.POST, instance=ls)
        if form.is_valid():     
            ls.information_set.update(age=request.POST['age'],
                                      birthday=request.POST['birthday'])

            ls.save()
            form.save()
            if not NameHistory.objects.filter(name=ls).exists():
                v = NameHistory(name=ls)

                v.save()

            return redirect('log_in')
    return render(request, 'edit.html', {'form': form})


def day():
    global date_today
    calendar = {}
    today = datetime.date.today()
    for i in range(1, 13):
        if i % 2 == 0 and i != 2:
            calendar[i] = 30
        elif i % 2 == 0 and i == 2:
            if today.year % 2 == 0:
                calendar[i] = 28
            else:
                calendar[i] = 29
        else:
            calendar[i] = 31
    date_today = calendar


def payment(request, pk):
    ls = Name.objects.get(id=int(pk))
    t = ls.information_set.get(name=ls)
    if request.method == 'POST':
        amount = float(request.POST['payment'])
        pay = amount
        balance = t.balance
        interest = t.interest
        dept = t.dept
        date = t.date
        bool = t.interest_bool
        balance_1 = t.balance - amount
        if request.POST['paid'] == 'saved':
            if amount > amount % 3:
                amount = t.balance - amount
                date = datetime.date.today()
                bool = True
            if amount <= 0:
                amount = 0
            if t.interest <= amount:
                interest = 0
            elif balance_1 <= 0:
                dept = 0
            ls.information_set.update(bool=bool, balance=amount, interest=interest, dept=dept, date=date)
            ls.save()

            if balance_1 <= 0:
                ls.information_set.update(date=datetime.date.today(), interest=0, balance=0)
            if History.objects.filter(name=t.name).exists() and os.path.exists(f'base\\database\\{t.name}\\{t.name}.txt'):
                history_ = NameHistory(name=t.name)
                history_.history_set.update(name=f'{t.name}',
                                            age=t.age,
                                            current_balance=balance,
                                            payment=pay,
                                            birthday=t.birthday,
                                            dept=amount,
                                            interest=t.interest,
                                            date=datetime.date.today()
                                            )
                database_history = Database()
                database_history.database(True, f'base\\database\\{t.name}\\{t.name}.txt')
                data = database_history.files
                data_base = {}
                count = 0
                fade = len(data[t.name]['count'])
                data_2 = [t.name, t.age, t.dept,
                          t.interest, balance, pay,
                          str(datetime.date.today()),
                          fade]

                for _, v in data.items():
                    data_base[t.name] = {}
                    for k, b in v.items():
                        data_base[t.name][k] = b.append(data_2[count])
                        count += 1
                database_history.files = data
                database_history.database(False, f'base\\database\\{t.name}\\{t.name}.txt')

            else:
                history_ = NameHistory.objects.get(name=t.name)
                if not os.path.exists(f'base\\database\\{t.name}'):
                    os.mkdir(f'base\\database\\{t.name}')
                open(f"base\\database\\{t.name}\\{t.name}.txt", mode='w').write("{}")

                history_.save()
                pole = NameHistory.objects.get(name=t.name)
                history_.history_set.create(name=t.name,
                                            age=t.age,
                                            current_balance=balance,
                                            payment=pay,
                                            birthday=t.birthday,
                                            dept=amount,
                                            interest=t.interest,
                                            date=datetime.date.today(),
                                            )
                database_history = Database()
                data = {}
                for i in pole.history_set.all():
                    data[i.name] = {'name': [str(t.name)],
                                    'age': [int(t.age)],
                                    'dept': [float(amount)],
                                    'interest': [float(t.interest)],
                                    'current_balance': [float(balance)],
                                    'payment': [float(pay)],
                                    'date': [str(datetime.date.today())],
                                    'count': [0]}
                    print(data)
                database_history.files = data
                database_history.database(False, f'base\\database\\{t.name}\\{t.name}.txt')

        return redirect(f"log_in")

    return render(request, 'payment.html', {'info': ls, 'date': datetime.date.today()})


def history(request, pk):
    get = Name.objects.get(id=pk)
    if NameHistory.objects.filter(name=get).exists() and \
            os.path.exists(f'base\\database\\{get}\\ADD_{get}.txt')\
            or os.path.exists(f'base\\database\\{get}\\{get}.txt'):
        data = Database()
        data.database(True, f'base\\database\\{get}\\{get}.txt')
        bet = {}
        set = {}
        if os.path.exists(f'base\\database\\{get}\\ADD_{get}.txt'):
            data.database(True, f'base\\database\\{get}\\ADD_{get}.txt')
            set = data.files
        elif os.path.exists(f'base\\database\\{get}\\{get}.txt'):
            bet = data.files
        else:
            return HttpResponse("<h1>No history Found :(</h1>")
        return render(request, 'history.html', {'info': bet, 'get': get, 'payment': set})
    else:
        return HttpResponse("<h1>No history Found :(</h1>")


def history_data(request, pk, sk):
    get = Name.objects.get(id=pk)
    if NameHistory.objects.filter(name=get).exists():
        data = Database()
        data.database(True, f'base\\database\\{get}\\{get}.txt')
        bet = data.files
        count = {}
        for _, i in bet.items():
            for k, v in i.items():
                count[k] = v[int(sk)]
        return render(request, 'history_data.html', {'info': count, 'get': get, 'Payment': "Payment"})
    else:
        return HttpResponse("<h1>No history Found :(</h1>")


def add(request, pk):
    ls = Name.objects.get(id=int(pk))
    t = ls.information_set.get(name=ls)
    if request.method == 'POST':
        amount = float(request.POST['payment'])
        pay = amount
        balance = t.balance
        balance_1 = t.balance + amount
        if request.POST['paid'] == 'saved':
            amount = t.balance + amount
            if amount < 0:
                amount = 0
            ls.information_set.update(balance=amount, dept=amount)
            ls.save()

            if balance_1 <= 0:
                ls.information_set.update(date=datetime.date.today(), interest=0, balance=0)
            if History.objects.filter(name=t.name).exists() and os.path.exists(f'base\\database\\{t.name}\\ADD_{t.name}.txt'):
                history_ = NameHistory(name=t.name)
                history_.history_set.update(name=f'{t.name}',
                                            age=t.age,
                                            current_balance=balance,
                                            payment=pay,
                                            birthday=t.birthday,
                                            dept=amount,
                                            interest=t.interest,
                                            date=datetime.date.today()
                                            )
                database_history = Database()
                database_history.database(True, f'base\\database\\{t.name}\\ADD_{t.name}.txt')
                data = database_history.files
                data_base = {}
                count = 0
                fade = len(data[t.name]['count'])
                data_2 = [t.name, t.age, t.dept,
                          t.interest, balance, pay,
                          str(datetime.date.today()),
                          fade]

                for _, v in data.items():
                    data_base[t.name] = {}
                    for k, b in v.items():
                        data_base[t.name][k] = b.append(data_2[count])
                        count += 1
                database_history.files = data
                database_history.database(False, f'base\\database\\{t.name}\\ADD_{t.name}.txt')

            else:
                history_ = NameHistory.objects.get(name=t.name)
                if not os.path.exists(f'base\\database\\{t.name}\\ADD_{t.name}.txt'):
                    if not os.path.exists(f'base\\database\\{t.name}'):
                        os.mkdir(f'base\\database\\{t.name}')
                    open(f"base\\database\\{t.name}\\ADD_{t.name}.txt", mode='w').write("{}")

                history_.save()
                pole = NameHistory.objects.get(name=t.name)
                history_.history_set.create(name=t.name,
                                            age=t.age,
                                            current_balance=balance,
                                            payment=pay,
                                            birthday=t.birthday,
                                            dept=amount,
                                            interest=t.interest,
                                            date=datetime.date.today(),
                                            )
                database_history = Database()
                data = {}
                for i in pole.history_set.all():
                    data[i.name] = {'name': [str(t.name)],
                                    'age': [int(t.age)],
                                    'dept': [float(amount)],
                                    'interest': [float(t.interest)],
                                    'current_balance': [float(balance)],
                                    'payment': [float(pay)],
                                    'date': [str(datetime.date.today())],
                                    'count': [0]}
                database_history.files = data
                database_history.database(False, f'base\\database\\{t.name}\\ADD_{t.name}.txt')

        return redirect(f"log_in")

    return render(request, 'add.html', {'info': ls, 'date': datetime.date.today()})


def history_add(request, pk, sk):
    get = Name.objects.get(id=pk)
    if NameHistory.objects.filter(name=get).exists():
        data = Database()
        data.database(True, f'base\\database\\{get}\\ADD_{get}.txt')
        bet = data.files
        count = {}
        for _, i in bet.items():
            for k, v in i.items():
                count[k] = v[int(sk)]
        return render(request, 'history_data.html', {'info': count, 'get': get, 'Payment': 'Add Payment'})
    else:
        return HttpResponse("<h1>No history Found :(</h1>")


def user_account(request, pk):
    form = UserRoom()
    return render(request, 'user_account.html', {'form': form})


def status(request):
    ls = Name.objects.all()
    return render(request, 'status.html', {'info': ls})