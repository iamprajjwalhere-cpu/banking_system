from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Account.objects.create(user=user, acc_no=f"ACC{user.id}", balance=0)
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

@login_required
def dashboard(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
    return render(request, "dashboard.html", {"account": account, "transactions": transactions})

@login_required
def deposit(request):
    account = Account.objects.get(user=request.user)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, type="Deposit", amount=amount)
            return redirect("dashboard")
    else:
        form = DepositForm()
    return render(request, "deposit.html", {"form": form})

@login_required
def withdraw(request):
    account = Account.objects.get(user=request.user)
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, type="Withdraw", amount=amount)
                return redirect("dashboard")
    else:
        form = WithdrawForm()
    return render(request, "withdraw.html", {"form": form})
