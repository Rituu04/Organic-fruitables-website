from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Order, OrderItem, Product, Cart, Contact
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def index(request):
  return render(request,'index.html')

def shop(request):
  pro=Product.objects.all()
  return render(request,'shop.html',{'pros':pro})

def contact(request):
  if request.method == "POST":
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    Contact.objects.create(
      name=name,
      email=email,
      subject=subject,
      message=message
    )

    messages.success(request, "Message sent successfully!")
    return redirect('contact')

  return render(request, "contact.html")

def cart(request):
  return render(request,'cart.html')

def testimonial(request):
  return render(request,'testimonial.html')

from django.contrib import messages
from .models import Cart

def checkout(request):
  if not request.user.is_authenticated:
    messages.error(request, "Please login to continue checkout")
    return redirect('/login/')

  cart = Cart.objects.filter(user=request.user)

  if not cart:
    messages.warning(request, "Your cart is empty!")
    return redirect('/cart/')

  total = sum(item.subtotal() for item in cart)
  shipping = 50
  grand_total = total + shipping

  context = {
    "cart": cart,
    "total": total,
    "shipping": shipping,
    "grand_total": grand_total
  }

  return render(request, "checkout.html", context)

def login(request):
  if request.method == 'POST':
    un=request.POST['uname']
    p1=request.POST['pass1']
    user=auth.authenticate(username=un,password=p1)
        
    if user is not None:
      auth.login(request,user)
      messages.success(request,"Login successful!")
      return redirect('/')
    else:
      messages.error(request,"Invalid username or password!")
      redirect('/login/')

  return render(request,'login.html')

def logout(request):
  auth.logout(request)
  messages.success(request, "Logout successful!")
  return redirect('/')

def register(request):
  if request.method == 'POST':
    fn=request.POST['fname']   
    ln=request.POST['lname']
    em=request.POST['email']
    un=request.POST['uname']
    p1=request.POST['pass1']
    p2=request.POST['pass2']
    if p1 != p2:
      messages.error(request, "Password't doesn't Match!")
      return redirect('/register/')

    if User.objects.filter(username=un).exists():
      messages.error(request, "Username already exists! Try another Username")
      return redirect('/register/')
    if User.objects.filter(email=em).exists():
      messages.error(request, "Email already exists! Try Again")
      return redirect('/register/')

    User.objects.create_user(
      first_name=fn,
      last_name=ln,
      email=em,
      username=un,
      password=p1
    )
  
    messages.success(request,"UserId created Successfully")
    return redirect('/login/')

  return render(request, 'register.html')

def add_to_cart(request, pid):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first.")
        return redirect('/login/')

    product = get_object_or_404(Product, pid=pid)

    # Check if product already in cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.pname} added to cart")
    return redirect('/shop/')
  
def cart_page(request):
    if not request.user.is_authenticated:
      messages.error(request, "Please login to view your cart")
      return redirect('/login/')

    cart = Cart.objects.filter(user=request.user)
    
    total = sum(item.subtotal() for item in cart)

    return render(request, "cart.html", {"cart": cart, "total": total})

def remove_cart(request, cid):
  item = Cart.objects.get(id=cid)
  item.delete()
  return redirect('/cart/')

def place_order(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        pincode = request.POST.get("pincode")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")

        payment_method = request.POST.get("payment_method")

        if not payment_method:
            messages.error(request, "Please choose a payment method.")
            return redirect("checkout")

        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect("checkout")

        if not all([first_name, last_name, address, city, country, pincode, mobile, email]):
            messages.error(request, "Please fill all the billing details.")
            return redirect("checkout")
          
        # Total calculate
        total = sum(item.product.pprice * item.quantity for item in cart_items)

        # Order create
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            country=country,
            pincode=pincode,
            mobile=mobile,
            email=email,
            payment_method=payment_method,
            total=total
        )

        # Order items save
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.pprice
            )

        cart_items.delete()

        # Redirect to bill page
        return redirect("bill_page", order_id=order.id)

    return redirect("checkout")
  
def bill_page(request, order_id):
    order = Order.objects.get(id=order_id)
    items = OrderItem.objects.filter(order=order)

    return render(request, "bill.html", {
        "order": order,
        "items": items
    })

def search(request):
    query = request.GET.get('q')
    pros = Product.objects.all()

    if query:
        q = query.lower()

        if 'veg' in q:
            pros = Product.objects.filter(cat__cname__icontains='veg')

        elif 'fruit' in q:
            pros = Product.objects.filter(cat__cname__icontains='fruit')

        else:
            pros = Product.objects.filter(
                Q(pname__icontains=query) |
                Q(cat__cname__icontains=query)
            )

    return render(request, 'shop.html', {
        'pros': pros,
        'query': query
    })
