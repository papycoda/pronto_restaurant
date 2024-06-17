from django.shortcuts import render, redirect
from django.http import HttpResponse
from openpyxl import load_workbook
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from datetime import datetime
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime, timedelta
from django.db import transaction



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
    """
    Handles table booking requests for the restaurant.
    
    This view processes the POST request from the booking form, validates the data,
    checks table availability, creates a reservation, and sends a notification email
    to the admin. It also handles errors and provides appropriate feedback to the user.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: The HTTP response object with the booking page or a success message.
    """
    if request.method == 'POST':
        # Extract form data from the POST request
        customer_name = request.POST.get('customer_name')
        contact_info = request.POST.get('contact_info')
        email = request.POST.get('email')
        date_time = request.POST.get('date_time')
        number_of_people = request.POST.get('number_of_people')
        table_id = request.POST.get('table')

        try:
            # Parse the date and time from the form input and make it timezone-aware
            start_time = timezone.make_aware(datetime.strptime(date_time, "%Y-%m-%dT%H:%M"), timezone.get_current_timezone())
            duration = timedelta(hours=2)

            # Define restaurant operating hours (make them timezone-aware)
            restaurant_opening_time = timezone.make_aware(datetime.combine(start_time.date(), datetime.strptime("10:00", "%H:%M").time()), timezone.get_current_timezone())
            restaurant_closing_time = timezone.make_aware(datetime.combine(start_time.date(), datetime.strptime("22:00", "%H:%M").time()), timezone.get_current_timezone())
            
            # Validate the reservation time is within operating hours
            if not (restaurant_opening_time <= start_time <= restaurant_closing_time and 
                    restaurant_opening_time <= (start_time + duration) <= restaurant_closing_time):
                raise ValueError("Reservation time is outside of operating hours.")

            # Retrieve the selected table from the database
            table = Table.objects.get(id=table_id)

            # Check if the table is available for the requested time
            if table.is_reserved and table.reserved_until > start_time:
                raise ValueError("The selected table is not available for the requested time.")

            # Create a new reservation
            booking = Reservation.objects.create(
                customer_name=customer_name,
                contact_info=contact_info,
                email=email,
                date_time=start_time,
                table=table,
                status='Pending'
            )
            booking.save()

            # Update the table's reservation status
            table.is_reserved = True
            table.reserved_until = start_time + duration
            table.save()

            # Send an email notification to the admin
            subject = f'New Booking: {customer_name}'
            message_content = (
                f'Name: {customer_name}\n'
                f'Contact Info: {contact_info}\n'
                f'Email: {email}\n'
                f'Date and Time: {date_time}\n'
                f'Number of People: {number_of_people}\n'
                f'Table Group: {table.table_group}'
            )
            send_mail(subject, message_content, 'your-email@example.com', ['admin@example.com'])

            # Display success message and redirect to home page
            messages.success(request, 'Reservation successful! An admin will reach out to you to confirm the reservation.')
            return redirect('index')

        except Exception as e:
            # Handle any errors that occur and display an error message
            messages.error(request, f'Error saving booking: {str(e)}')
            return render(request, 'book.html', {'tables': Table.objects.all()})

    # Render the booking page with the available tables
    return render(request, 'book.html', {'tables': Table.objects.all()})

def event_list(request):
    events = Event.objects.all()

    for event in events:
        if event.recurrence:
            event.next_occurrence = event.recurrence.after(timezone.now())
        else:
            event.next_occurrence = None  # or any other default value
    
    context = {
        'events': events
    }
    return render(request, 'event_list.html', context)


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

