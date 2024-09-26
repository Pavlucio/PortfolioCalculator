import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from portfolio_project import settings
from .models import Portfolio, Item
from .forms import CurrencyForm, ItemForm, PortfolioForm, ItemUpdateForm
from .utils import Calculator
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView
import yfinance as yf


# Create your views here.


class PortfolioListView(LoginRequiredMixin, generic.ListView, FormView):
    """
    Generates vie of the list of Portfolios for each users
    """
    model = Portfolio
    template_name = 'my_portfolios.html'
    form_class = PortfolioForm
    success_url = reverse_lazy('myportfolios')

    def get_queryset(self):
        """
        Method returns all portfolio objects which belong to current user
        :return: returns objects filtered by user
        """
        return Portfolio.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """
        Method adds user to the form instance and passes it to the parent class method
        :param form: is provided by Django when the form is submitted and validated successfully
        :return: passes form instance with user to the parent class method (HttpResponse class object)
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Method gets context data for the view
        :param kwargs: additional keyword arguments passed to the method.
        :return: dictionary containing the context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class PortfolioUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """
    Generates view to update Portfolio
    """
    model = Portfolio
    fields = ['title']
    template_name = 'update_portfolio.html'
    success_url = reverse_lazy('myportfolios')

    def form_valid(self, form):
        """
        Method adds user to the form instance and passes it to the parent class method
        :param form: is provided by Django when the form is submitted and validated successfully
        :return: passes form instance with user to the parent class method (HttpResponse class object)
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Checks if the current user is the owner of the portfolio
        :return: boolean True or False
        """
        portfolio = self.get_object()
        return self.request.user == portfolio.user


class PortfolioDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    Generates view to delete Portfolio
    """
    model = Portfolio
    template_name = 'delete_portfolio.html'
    success_url = reverse_lazy('myportfolios')

    def test_func(self):
        """
        Checks if the current user is the owner of the portfolio
        :return: boolean True or False
        """
        portfolio = self.get_object()
        return self.request.user == portfolio.user

@login_required
def portfolio_detail(request, pk):

    """
    Returns view where user can see his portfolio details with all possible methods to initiate (add/update/delete
    Items), perform Current price, history and gain calculations.
    :param request: HttpRequest object that contains metadata about the request
    :param pk: Portfolio primary key, Integer
    :return: returns view of Portfolio details with opportunities to perform actions.
    """

    portfolio = get_object_or_404(Portfolio, pk=pk)

    if portfolio.user != request.user:
        raise PermissionDenied

    form = CurrencyForm(initial={'portfolio_id': pk})
    item_form = ItemForm()


    if request.method == 'POST':
        if 'add_item' in request.POST:
            item_form = ItemForm(request.POST)
            if item_form.is_valid():
                ticker = item_form.cleaned_data['ticker']
                try:
                    check_stock_id = yf.Ticker(ticker)
                    print(check_stock_id.info['currentPrice'])
                    if Item.objects.filter(ticker=ticker, user=request.user, portfolio_id=portfolio.pk).exists():
                        messages.error(request, 'Item with this ticker already exists in your portfolio.')
                    else:
                        new_item = item_form.save(commit=False)
                        new_item.portfolio_id = portfolio
                        new_item.user = request.user
                        new_item.save()
                        messages.success(request, 'Item added to your portfolio successfully.')
                        return redirect('portfolio_detail', pk=pk)
                except:
                    messages.error(request, f'Ticker "{ticker}" does not exist.')
        else:
            form = CurrencyForm(request.POST)
            if form.is_valid():
                base_currency = form.cleaned_data['base_currency']
                portfolio_id = form.cleaned_data['portfolio_id']
                # data = convert_to_data(portfolio, data)
                calculator = Calculator(portfolio, base_currency)
                if 'current' in request.POST:
                    df, df_app, portfolio_value, time_of_request, image_name = calculator.current_portfolio_value()
                    image_url = os.path.join(settings.MEDIA_URL, image_name) if image_name else None
                    context = {
                        'portfolio_id': portfolio_id,
                        'base_currency': base_currency,
                        'portfolio': portfolio.title,
                        'df': df,
                        'df_app': df_app,
                        'portfolio_value': portfolio_value,
                        'pk': portfolio_id,
                        'image_url': image_url,
                        'time_of_request': time_of_request,
                        'df_app_any': df_app.any().any()
                    }
                    return render(request, 'current.html', context)

                elif 'history' in request.POST:
                    portfolio_history, image_1_name, image_2_name = calculator.get_history()
                    image_1_url = os.path.join(settings.MEDIA_URL, image_1_name) if image_1_name else None
                    image_2_url = os.path.join(settings.MEDIA_URL, image_2_name) if image_2_name else None
                    context = {
                        'portfolio_history': portfolio_history,
                        'base_currency': base_currency,
                        'pk': portfolio_id,
                        'portfolio': portfolio.title,
                        'portfolio_history_any': portfolio_history.any().any(),
                        'image_1_url': image_1_url,
                        'image_2_url': image_2_url,
                    }
                    return render(request, 'history.html', context)

                elif 'gain' in request.POST:
                    data_gain_abs, data_gain, image_3_name, image_4_name = calculator.get_gain()
                    image_3_url = os.path.join(settings.MEDIA_URL, image_3_name) if image_3_name else None
                    image_4_url = os.path.join(settings.MEDIA_URL, image_4_name) if image_4_name else None
                    context = {'data_gain': data_gain,
                               'data_gain_any': data_gain.any().any(),
                               'data_gain_abs': data_gain_abs,
                               'data_gain_abs_any': data_gain_abs.any().any(),
                               'base_currency': base_currency,
                               'pk': portfolio_id,
                               'portfolio': portfolio.title,
                               'image_3_url': image_3_url,
                               'image_4_url': image_4_url,
                               }
                    return render(request, 'gain.html', context)

    return render(request, 'portfolio_detail.html',
                  {'portfolio': portfolio, 'form': form, 'item_form': item_form})

@login_required
def update_item(request, pk):
    """
    Function returning the view to update item
    :param request: : HttpRequest object that contains metadata about the request
    :param pk: Item primary key, Integer
    :return: returns view for updating Item
    """
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('portfolio_detail', pk=item.portfolio_id.pk)
    else:
        form = ItemUpdateForm(instance=item)
    return render(request, 'update_item.html', {'form': form})

@login_required
def delete_item(request, pk):
    """
    Function returning the view to delete item
    :param request: HttpRequest object that contains metadata about the request
    :param pk: Item primary key, Integer
    :return: returns view for deleting Item
    """
    item = get_object_or_404(Item, pk=pk)
    portfolio_id = item.portfolio_id.pk
    if request.method == 'POST':
        item.delete()
        return redirect('portfolio_detail', pk=portfolio_id)
    return render(request, 'delete_item.html', {'item': item, 'portfolio_id': portfolio_id})


def index(request):
    """
    Function returning the view to About page (Homepage)
    :param request: HttpRequest object that contains metadata about the request
    :return: returns view of About page (Homepage)
    """
    context = {}
    return render(request, 'index.html', context=context)


@csrf_protect
def register(request):
    """
    Function returning the view to Rigistration page
    :param request: HttpRequest object that contains metadata about the request
    :return: returns view of Registration page
    """
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already exists.')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with email {email} already exists.')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} is registered.')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'register.html')
