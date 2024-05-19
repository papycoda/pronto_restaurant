from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import load_workbook
from .models import MenuItem,Category
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator


def HomePageView (request):
    return render(request, 'index.html')

def MenuView (request):
    categories = Category.objects.prefetch_related('menu_items').order_by('name')
    selected_category = request.GET.get('category')
    all_items = MenuItem.objects.all() 

    if selected_category:
        menu_items = all_items.filter(category__name__iexact=selected_category)
    else:
        menu_items = all_items

    paginator = Paginator(all_items, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'page_obj': page_obj,
        'selected_category': selected_category,
    }
    return render(request, 'menu.html', context) 

def AboutView(request):
    return render(request, 'about.html')

def BookView(request):
    return render(request, 'book.html')


@user_passes_test(lambda u: u.is_superuser)
def import_from_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        wb = load_workbook(excel_file)
        ws = wb.active

        # Iterate starting from the second row (min_row=2)
        for row in ws.iter_rows(min_row=2, values_only=True): 
            try:
                category_name, item, description, price = row
                category, created = Category.objects.get_or_create(name=category_name)
                description = description or ""
                price = price or 0.00

                # create new menu item
                MenuItem.objects.create(
                    name=item,
                    description=description,
                    price=price,
                    category=category  
                )
            except ValueError:  
                print(f"Error processing row: {row}")

        return render(request, 'import_success.html')

    return render(request, 'import_form.html') 

