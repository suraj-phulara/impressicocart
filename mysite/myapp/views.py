
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from mysite.form import createuserform, createcustomerform
from .document import ProductDocument, AggregatedIndex
from .models import AggregatedCategory, Product, Image
from elasticsearch_dsl import Q

from django.shortcuts import render
from elasticsearch_dsl import Search
from .document import AggregatedIndex

def home(request):
    search = Search(using=AggregatedIndex._index._using, index=AggregatedIndex._index._name)

    response = search[:100].execute()

    main_categories_with_subcategories = {}
    for hit in response:
        main_category = hit.main_category
        sub_category = hit.sub_category
        if main_category not in main_categories_with_subcategories:
            main_categories_with_subcategories[main_category] = set()
        main_categories_with_subcategories[main_category].add(sub_category)

    data = [{'main_category': main_category, 'sub_categories': list(sub_categories)}
            for main_category, sub_categories in main_categories_with_subcategories.items()]

    return render(request, 'customapp/home.html', {'data': data})

def product_search_view(request):
    print("request--->", request)
    selected_main_category = request.GET.get('main_category', '')
    selected_subcategory = request.GET.get('subcategory', '')
    search_query = Q('bool', must=[
        Q('term', main_category=selected_main_category),
        Q('term', sub_category=selected_subcategory)
    ])
    print("search query main category = ",selected_main_category, "   ***   sub category == ", selected_subcategory)
    search = Search(using=ProductDocument._index._using, index=ProductDocument._index._name).query(search_query)
    response = search.execute()
    products = []
    for hit in response:
        product_data = {
            'name': hit.name,
            'actual_price': hit.actual_price,
            'discount_price': hit.discount_price,
            'ratings': hit.ratings,
            'no_of_ratings': hit.no_of_ratings,
            'link': hit.link,
        }
        products.append(product_data)

    return render(request, 'customapp/products.html', {'products': products})



def search_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        search = ProductDocument.search().query("multi_match", query=query, fields=['name', 'main_category.name', 'sub_category.name'])
        results = search.execute()
        results = [hit.to_dict() for hit in results]
    return render(request, 'customapp/search.html', {'results': results})



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        customer_form = createcustomerform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            customer_form = createcustomerform(request.POST)
            if form.is_valid() and customer_form.is_valid():
                user = form.save()
                customer = customer_form.save(commit=False)
                customer.user = user
                customer.save()
                return redirect('login')
        context = {
            'form': form,
            'customer_form': customer_form,
        }
        return render(request, 'customapp/register.html', context)


def about_us(request):
    return render(request, 'cu/about_us.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'customapp/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('/')

