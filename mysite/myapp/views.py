from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from .forms import ExpensesForm
from .models import Expenses
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime,timedelta

def index(request):

    if request.method == 'POST':
        expense_form = ExpensesForm(request.POST)
        if expense_form.is_valid():
            expense_form.save()
            messages.success(request, "Expense added successfully!")
            return redirect('index')   # reset form
    else:
        expense_form = ExpensesForm()

    # ✅ ALWAYS fetch data
    expenses = Expenses.objects.all()
    total_expense=Expenses.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    print(total_expense)


    #yearly sum

    last_year=datetime.today()-timedelta(days=365)
    data=Expenses.objects.filter(date__gt=last_year)
    yearly_sum=data.aggregate(Sum('amount'))['amount__sum'] or 0

    #monthly sum
    last_month=datetime.today()-timedelta(days=30)
    data=Expenses.objects.filter(date__gt=last_month)
    monthly_sum=data.aggregate(Sum('amount'))['amount__sum'] or 0

    #weekly sum
    last_week=datetime.today()-timedelta(days=7)
    data=Expenses.objects.filter(date__gt=last_week)
    weekly_sum=data.aggregate(Sum('amount'))['amount__sum'] or 0

    #calculating daily sum
    daily_expense=Expenses.objects.filter().values('date').order_by('date').annotate(Sum('amount'))
    print(daily_expense)

    #category sum
    category_expense=Expenses.objects.values('category').annotate(Sum('amount'))

    return render(request, 'myapp/index.html', {
        'expense_form': expense_form,
        'expenses': expenses,
        'total': total_expense,
        'monthly_sum': monthly_sum,
        'yearly_sum': yearly_sum,
        'weekly_sum': weekly_sum,
        'daily_expense': daily_expense,
        "category_expense":category_expense
    })

def edit_expense(request,id):
    expense=Expenses.objects.get(id=id)
    expense_form=ExpensesForm(instance=expense)
    if request.method == 'POST':
        expense_form=ExpensesForm(request.POST,instance=expense)
        if expense_form.is_valid():
            expense_form.save()
            return redirect('index')
    else:
        expense_form=ExpensesForm(instance=expense)
    return render(request, 'myapp/edit_expense.html', {'expense_form': expense_form})

def delete_expense(request,id):
    expense=Expenses.objects.get(id=id)
    if request.method == 'POST':
        expense.delete()
        return redirect('index')