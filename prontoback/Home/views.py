from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import load_workbook
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from datetime import datetime
from django.core.mail import send_mail



def HomePageView (request):
    return render(request, 'index.html')

def MenuView(request):
    """Renders the menu view.
    
    This function retrieves the categories and menu items from the database. It first fetches all the categories and their associated menu items using the `prefetch_related` method. The categories are then ordered by their name.
    
    If a `category` parameter is provided in the request, the function filters the menu items based on the selected category. It uses the `filter` method to retrieve the menu items whose category name matches the selected category (case-insensitive). If no `category` parameter is provided, it retrieves all the menu items.
    
    The menu items are then paginated using the `Paginator` class, with 8 items per page. The current page number is retrieved from the request's query parameters.
    
    Finally, the function creates a context dictionary with the categories, paginated menu items, and the selected category. It renders the 'menu.html' template with this context."""
    categories = Category.objects.prefetch_related(
        'menu_items').order_by('name')
    selected_category = request.GET.get('category')

    if selected_category:
        menu_items = MenuItem.objects.filter(
            category__name__iexact=selected_category)
    else:
        menu_items = MenuItem.objects.all()

    paginator = Paginator(menu_items, 8)
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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        persons = request.POST.get('persons')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        try:
            booking = Reservation.objects.create(
                name=name,
                email=email,
                date=date,
                time=time,
                persons=persons,
                phone=phone,
                message=message
            )
            booking.save()

            
            subject = f'New Booking: {name}'
            message = f'Name: {name}, Email: {email}, Date: {date}, Time: {time}, Persons: {persons}, Phone: {phone}, Message: {message}'
            send_mail(subject, message, 'admin@example.com', ['admin@example.com'])

            return render(request, 'book_success.html')

        except Exception as e:
            print(f'Error saving booking: {str(e)}')

    return render(request, 'book.html')

def event_list(request):
    events = Event.objects.all()
    if not events:
        events = [Event(
            name='Placeholder Event',
            description='This is a placeholder event.',
            date=datetime.now().date(),
            time=datetime.now().time(),
            location='Placeholder Location',
        )]
    return render(request, 'events.html', {'events': events})


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

