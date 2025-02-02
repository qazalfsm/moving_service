from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomerForm, MoverForm, UserLoginForm, OrderForm, PhotoUploadForm
from .models import Customer, Mover, Order, DetectedItem
from geopy.distance import geodesic
from ultralytics import YOLO

def nearest_movers(request, order_id):
    order = Order.objects.get(id=order_id)
    movers = Mover.objects.all()
    order_location = tuple(map(float, order.origin_location.split(",")))

    nearest_movers = []
    for mover in movers:
        mover_location = tuple(map(float, mover.location.split(",")))
        distance = geodesic(order_location, mover_location).kilometers
        nearest_movers.append((mover, distance))

    nearest_movers.sort(key=lambda x: x[1])
    return render(request, 'users/nearest_movers.html', {'nearest_movers': nearest_movers})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ثبت‌نام با موفقیت انجام شد!")
            return redirect('dashboard')
    else:
        form = CustomerForm()
    return render(request, 'users/register_customer.html', {'form': form})

def register_mover(request):
    if request.method == 'POST':
        form = MoverForm(request.POST)
        if form.is_valid():
            mover = form.save(commit=False)
            mover.location = request.POST.get('location_map')
            mover.save()
            messages.success(request, "ثبت‌نام راننده با موفقیت انجام شد!")
            return redirect('dashboard')
    else:
        form = MoverForm()
    return render(request, 'users/register_mover.html', {'form': form})

def dashboard(request):
    return render(request, 'users/dashboard.html')

def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        photo_form = PhotoUploadForm(request.POST, request.FILES)
        if order_form.is_valid() and photo_form.is_valid():
            order = order_form.save()
            photos = photo_form.save(commit=False)
            yolo_model = YOLO('yolov8l.pt')

            for photo in photos:
                results = yolo_model(photo.image.path)
                for result in results:
                    for box in result.boxes.data:
                        DetectedItem.objects.create(
                            order=order,
                            item_class=int(box.cls.item()),
                            confidence=float(box.conf.item()),
                            bbox={
                                'x1': float(box.xyxy[0].item()),
                                'y1': float(box.xyxy[1].item()),
                                'x2': float(box.xyxy[2].item()),
                                'y2': float(box.xyxy[3].item())
                            }
                        )
            messages.success(request, "سفارش با موفقیت ثبت شد!")
            return redirect('dashboard')
    else:
        order_form = OrderForm()
        photo_form = PhotoUploadForm()
    return render(request, 'users/create_order.html', {'order_form': order_form, 'photo_form': photo_form})

def mover_dashboard(request):
    orders = Order.objects.filter(items_detected__isnull=False).distinct()
    return render(request, 'users/mover_dashboard.html', {'orders': orders})

def home(request):
    return render(request, 'users/home.html')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomerForm, MoverForm, UserLoginForm, OrderForm, PhotoUploadForm
from .models import Customer, Mover, Order, DetectedItem
from geopy.distance import geodesic
from ultralytics import YOLO

def nearest_movers(request, order_id):
    order = Order.objects.get(id=order_id)
    movers = Mover.objects.all()
    order_location = tuple(map(float, order.origin_location.split(",")))

    nearest_movers = []
    for mover in movers:
        mover_location = tuple(map(float, mover.location.split(",")))
        distance = geodesic(order_location, mover_location).kilometers
        nearest_movers.append((mover, distance))

    nearest_movers.sort(key=lambda x: x[1])
    return render(request, 'users/nearest_movers.html', {'nearest_movers': nearest_movers})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ثبت‌نام با موفقیت انجام شد!")
            return redirect('dashboard')
    else:
        form = CustomerForm()
    return render(request, 'users/register_customer.html', {'form': form})

def register_mover(request):
    if request.method == 'POST':
        form = MoverForm(request.POST)
        if form.is_valid():
            mover = form.save(commit=False)
            mover.location = request.POST.get('location_map')
            mover.save()
            messages.success(request, "ثبت‌نام راننده با موفقیت انجام شد!")
            return redirect('dashboard')
    else:
        form = MoverForm()
    return render(request, 'users/register_mover.html', {'form': form})

def dashboard(request):
    return render(request, 'users/dashboard.html')

def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        photo_form = PhotoUploadForm(request.POST, request.FILES)
        if order_form.is_valid() and photo_form.is_valid():
            order = order_form.save()
            photos = photo_form.save(commit=False)
            yolo_model = YOLO('yolov8l.pt')

            for photo in photos:
                results = yolo_model(photo.image.path)
                for result in results:
                    for box in result.boxes.data:
                        DetectedItem.objects.create(
                            order=order,
                            item_class=int(box.cls.item()),
                            confidence=float(box.conf.item()),
                            bbox={
                                'x1': float(box.xyxy[0].item()),
                                'y1': float(box.xyxy[1].item()),
                                'x2': float(box.xyxy[2].item()),
                                'y2': float(box.xyxy[3].item())
                            }
                        )
            messages.success(request, "سفارش با موفقیت ثبت شد!")
            return redirect('dashboard')
    else:
        order_form = OrderForm()
        photo_form = PhotoUploadForm()
    return render(request, 'users/create_order.html', {'order_form': order_form, 'photo_form': photo_form})

def mover_dashboard(request):
    orders = Order.objects.filter(items_detected__isnull=False).distinct()
    return render(request, 'users/mover_dashboard.html', {'orders': orders})

def home(request):
    return render(request, 'users/home.html')
