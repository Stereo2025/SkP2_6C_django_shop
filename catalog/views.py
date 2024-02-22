from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Contact, Category


def home_page(request):
    """Контроллер домашней страницы"""
    products = Product.objects.all().order_by('id')

    context = {
        'product_list': products,
    }

    return render(request, 'catalog/home_page.html', context=context)


def contacts(request):
    """Контроллер страницы контактов"""
    contacts = Contact.objects.all()
    data = {
        'contact_list': contacts,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have a message from {name}({phone}): {message}')
    return render(request, 'catalog/contact.html', context=data)


def products(request):
    """Контроллер страницы товаров"""
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 6)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
        'product_list': page_obj,
    }
    return render(request, 'catalog/products.html', context=context)


def user_product(request):
    """Контроллер страницы добавления товара от пользователя"""
    category_list = Category.objects.all()
    context = {
        'category_list': category_list,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        category = Category.objects.get(name=request.POST.get('category'))
        print(f'1 - {name}, 2 - {description}, 3 - {image}, 4 - {price}, 5 - {category}')
        Product.objects.create(name=name, description=description, image=image, price=price, category=category)
    return render(request, 'catalog/user_product.html', context=context)


def view_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'catalog/view_product.html', context=context)
