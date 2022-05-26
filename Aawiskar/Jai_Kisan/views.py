from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views import View
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Customer, Item, Product,Booked,Vendor
from .forms import CustomerRegistrationForm, CustomerProfileForm,VenderRegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

class VenderRegistrationView(View):
	def get(self, request):
		form = VenderRegistrationForm()
		return render(request, 'Jai_Kisan/venderregistration.html', {'form': form})
	def post(self, request):
		form = VenderRegistrationForm(request.POST)
		if form.is_valid():
			print("manodd")
			user = User.objects.create_user(username=form.cleaned_data.get('User_name'),email=form.cleaned_data.get('email'),password=form.cleaned_data.get('password'))
			user.is_active = True
			user.save()
			print("mudd")
			User_name=form.cleaned_data.get('User_name')
			First_name=form.cleaned_data.get('First_name')
			Last_name=form.cleaned_data.get('Last_name')
			email=form.cleaned_data.get('email')
			phone=form.cleaned_data.get('phone'),
			state=form.cleaned_data.get('state')
			city=form.cleaned_data.get('city')
			locality=form.cleaned_data.get('locality')
			zipcode=form.cleaned_data.get('zipcode')
			vendor_data=Vendor(user=user, User_name=User_name,First_name=First_name,Last_name=Last_name,email= email,phone=phone,
							   state=state,city=city,locality=locality,zipcode=zipcode)
			print("maff")
			messages.success(request, 'Congratulations!! Registered Successfully.')
			vendor_data.save()
			# new_user = authenticate(username=form.cleaned_data.get('user_name'),
			# 						password=form.cleaned_data.get('password'))
			# login(request, new_user)


            # form.save()
			return render(request,'Jai_Kisan/venderregistration.html',{'form': form})

			# return HttpResponseRedirect('Jai_Kisan/venderregistration.html',{'form': form})
        # return render(request, 'Jai_kisan/venderregistration.html', {'form': form})

def index(request):

    # allProds = []
    # catprods = Product.objects.values('category', 'id')
    # cats = {item['category'] for item in catprods}
    # for cat in cats:
    #     prod = Product.objects.filter(category=cat)
    #     n = len(prod)
    #     nSlides = n // 4 + ceil((n / 4) - (n // 4))
    #     allProds.append([prod, range(1, nSlides), nSlides])
    # params = {'allProds':allProds}
    return render(request, 'Jai_Kisan/home.html')
class ProductView(View):
	def get(self, request):
		totalitem = 0
		tracter = Product.objects.filter(category='T')
		boring_machine = Product.objects.filter(category='BM')
		harvestor = Product.objects.filter(category='H')
		if request.user.is_authenticated:
			totalitem = len(Item.objects.filter(user=request.user))
		return render(request, 'Jai_Kisan/home.html', {'tracter':tracter, 'boring_machine':boring_machine, 'harvestor':harvestor, 'totalitem':totalitem})


class ProductDetailView(View):
	def get(self, request, pk):
		totalitem = 0
		product = Product.objects.get(pk=pk)
		print(product.id)
		item_already_in_cart=False
		if request.user.is_authenticated:
			totalitem = len(Item.objects.filter(user=request.user))
			item_already_in_cart = Item.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'Jai_Kisan/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required()
def add_to_cart(request):
	user = request.user
	item_already_in_cart1 = False
	product = request.GET.get('prod_id')
	item_already_in_cart1 = Item.objects.filter(Q(product=product) & Q(user=request.user)).exists()
	if item_already_in_cart1 == False:
		product_title = Product.objects.get(id=product)
		Item(user=user, product=product_title).save()
		messages.success(request, 'Product Added to Cart Successfully !!' )
		return redirect('/cart')
	else:
		return redirect('/cart')

@login_required
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Item.objects.filter(user=request.user))
		user = request.user
		cart = Item.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 70.0
		totalamount=0.0
		cart_product = [p for p in Item.objects.all() if p.user == request.user]
		print(cart_product)
		if cart_product:
			for p in cart_product:
				tempamount = (p.duration * p.product.discounted_price)
				amount += tempamount
			totalamount = amount+shipping_amount
			return render(request, 'Jai_Kisan/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
		else:
			return render(request, 'Jai_Kisan/emptycart.html', {'totalitem':totalitem})
	else:
		return render(request, 'Jai_Kisan/emptycart.html', {'totalitem':totalitem})

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Item.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.duration +=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Item.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.duration * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'duration':c.duration,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Item.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.duration-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Item.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.duration * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'duration':c.duration,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def checkout(request):
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Item.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount = 70.0
	totalamount=0.0
	cart_product = [p for p in Item.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.duration * p.product.discounted_price)
			amount += tempamount
		totalamount = amount+shipping_amount
	return render(request, 'Jai_Kisan/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount})

@login_required
def Booked_placed(request):
	op = Booked.objects.filter(user=request.user)
	return render(request, 'Jai_Kissan/booked.html', {'Booked':op})

def tracter(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Item.objects.filter(user=request.user))
	if data==None :
			tracter = Product.objects.filter(category='T')
	elif data == 'Ambani' or data == 'Tata':
			tracter = Product.objects.filter(category='T').filter(brand=data)
	return render(request, 'Jai_Kisan/tracter.html', {'tracter':tracter, 'totalitem':totalitem})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'Jai_kisan/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
        return render(request, 'Jai_kisan/customerregistration.html', {'form': form})

@login_required
def address(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Item.objects.filter(user=request.user))
	add = Customer.objects.filter(user=request.user)
	return render(request, 'Jai_Kisan/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})


def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Item.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Item.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.duration * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Item.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'Jai_Kisan/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})

    def post(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Item.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully.')
        return render(request, 'Jai_Kisan/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})

@login_required
def payment_done(request):
	print("murli")
	custid = request.GET.get('custid')
	print("Customer ID", custid)
	user = request.user
	cartid = Item.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	# for cid in cartid:
	# 	Booked(user=user,product=cid.product, quantity=cid.duration).save()
	# 	print("Order Saved")
	# 	cid.delete()
	# 	print("Cart Item Deleted")
	return render(request, 'Jai_Kisan/home.html')
	# return redirect("Booked")