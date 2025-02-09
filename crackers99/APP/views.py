from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import Product, Category
from django.core.exceptions import ValidationError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import HttpResponse,JsonResponse
import json

def index(request):
    categories = Category.objects.all()  # Get all categories
    products = Product.objects.all()      # Get all products
    
    # Group products by category
    category_products = {}
    for category in categories:
        category_products[category] = products.filter(category=category)
    
    return render(request, "main/index.htm", {'category_products': category_products})



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')

        sender_email = "kavithacrackershop@gmail.com"
        app_password = "yymuxbahmoljkpet"
        recipient_email = "kavithacrackershop@gmail.com" 
        
        subject = "Enquiry Message from a Customer"
        body = f"""
        Customer Details : 
        Name: {name}
        Mobile: {mobile}
        Message: {message}
        """

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()  
            server.login(sender_email, app_password)  
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()

            # HTML response with JavaScript redirect after 5 seconds
            response_html = """
                <html>
                    <head>
                        <meta http-equiv="refresh" content="5;url=/" />
                    </head>
                    <body>
                        <p>Message sent successfully! You will be redirected to the homepage in 5 seconds...</p>
                    </body>
                </html>
            """
            return HttpResponse(response_html)

        except Exception as e:
            return HttpResponse(f"Failed to send message. Error: {str(e)}")

    return render(request, "main/contact.htm")




def adminn(request):
    if request.session.get('username') == 'babulatha':
        return redirect('addCategory')  

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'babulatharamesh@2025@kavitha' and password == 'babulatharamesh@2025@kavitha':
            request.session['username'] = 'babulatha'
            return redirect('addCategory')  
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, "main/login.htm")



def addCategory(request):
    if request.session.get('username') != 'babulatha':
        return redirect('adminn')  
    
    if request.method == 'POST':
        category_name = request.POST.get('productName')
        description = request.POST.get('description')

        if category_name and Category.objects.filter(name=category_name).exists():
            messages.error(request, "Category name already exists. Please choose a different name.")
        else:
            try:
                new_category = Category(name=category_name, description=description)
                new_category.save()
                messages.success(request, "Category added successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    categories = Category.objects.all()
    return render(request, "main/addCategory.htm",{'categories':categories})





def addProduct(request):
    if request.session.get('username') != 'babulatha':
        return redirect('adminn')  
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        product_name = request.POST.get('productName')
        description = request.POST.get('description')
        old_price = request.POST.get('old_price')
        price = request.POST.get('price')
        in_stock = request.POST.get('in_stock') == 'on'  
        image = request.FILES.get('image')  

        try:
            category = Category.objects.get(id=category_id)
            
            new_product = Product(
                category=category,
                name=product_name,
                description=description,
                old_price=old_price if old_price else None,  
                price=price,
                in_stock=in_stock,
                image=image
            )
            new_product.save()
            
            messages.success(request, "Product added successfully!")
            return redirect('addProduct')  
        
        except Category.DoesNotExist:
            messages.error(request, "Category not found.")
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, "main/addProduct.htm", {'categories': categories,'products':products})


def updateCategory(request, id):
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        category_name = request.POST.get('productName')
        description = request.POST.get('description')
        
        # Check if category name is already taken by another category
        if category_name != category.name and Category.objects.filter(name=category_name).exists():
            messages.error(request, "Category name already exists. Please choose a different name.")
        else:
            try:
                category.name = category_name
                category.description = description
                category.save()
                messages.success(request, "Category updated successfully!")
                return redirect('addCategory')  # Redirect after successful update
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, "main/updateCategory.htm", {'category': category})

def deleteCategory(request,id):
    category = get_object_or_404(Category, id=id)
    
    try:
        # Delete the product
        category.delete()
        
        # Display a success message
        messages.success(request, "Category deleted successfully!")
    except Exception as e:
        # Handle errors if any
        messages.error(request, f"An error occurred: {str(e)}")
    
    # Redirect to the 'addProduct' page after deletion
    return redirect('addCategory')




def updateProduct(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        category_id = request.POST.get('category')
        product_name = request.POST.get('productName')
        description = request.POST.get('description')
        old_price = request.POST.get('old_price')
        price = request.POST.get('price')
        in_stock = request.POST.get('in_stock') == 'on'
        image = request.FILES.get('image')

        try:
            category = Category.objects.get(id=category_id)
            
            product.category = category
            product.name = product_name
            product.description = description
            product.old_price = old_price if old_price else None
            product.price = price
            product.in_stock = in_stock
            if image:
                product.image = image

            product.save()

            messages.success(request, "Product updated successfully!")
            return redirect('addProduct')  # Redirect to a page after successful update

        except Category.DoesNotExist:
            messages.error(request, "Category not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    categories = Category.objects.all()
    return render(request, "main/updateProduct.htm", {'product': product, 'categories': categories})



def deleteProduct(request, id):
    # Fetch the product or return 404 if not found
    product = get_object_or_404(Product, id=id)
    
    try:
        # Delete the product
        product.delete()
        
        # Display a success message
        messages.success(request, "Product deleted successfully!")
    except Exception as e:
        # Handle errors if any
        messages.error(request, f"An error occurred: {str(e)}")
    
    # Redirect to the 'addProduct' page after deletion
    return redirect('addProduct')




def submit_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        total_price = float(request.POST.get('total_price'))
        selected_products = json.loads(request.POST.get('selected_products'))
        print(selected_products)

        # Prepare the email content
        subject = f"New Order from {name}"
        message = f"Name: {name}\nMobile: {mobile}\nAddress: {address}\nTotal Price: ₹{total_price}\n\nSelected Products:\n"
        
        for product in selected_products:
            product_price = float(product['price']) * product['quantity']  # Convert price to float before multiplication
            message += f"Product: {product['name']}, Quantity: {product['quantity']}, Price: ₹{product_price:.2f}\n"  # Format to 2 decimal places
            
        # SMTP setup
        sender_email = "kavithacrackershop@gmail.com"
        sender_password = "yymuxbahmoljkpet"  # Use your app password
        receiver_email = "kavithacrackershop@gmail.com"

        try:
            # Create the MIME message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Setup the server and send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Start TLS for security
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            print(f"Error sending email: {e}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
