from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control

# Create your views here.

# ==================================== LOG IN ======================================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    error_message = None
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user is not None:
            auth_login(request, user)
            return render(request, 'home.html',{'username':username})
        else:
            error_message = 'Please Enter Valid Username and Password'

    return render(request, 'login.html',{'error_message':error_message})

# ============================================== END ==============================================================================

# ============================================== SIGN UP ============================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        Name = request.POST['Name'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        cpassword = request.POST['cpassword'].strip()

        if len(Name) > 20:
            messages.error(request, 'Name Must Be Under 10 Characters')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Exist!')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Registered')
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request, 'Username Must Be Under 10 Characters')
            return redirect('signup')
        
        if password != cpassword:
            messages.error('Password Didnt Match')
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = Name
        myuser.save()
    
        # user_obj = Userdetails(username=username, name=Name, email=email, password=password)
        # user_obj.save()

        messages.success(request, "Your Account has been successfully created")

        return redirect('login')

    return render(request, 'login.html')

# ======================================================= END ==============================================================================

# ====================================================== HOME ===============================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        messages.error(request, "Bad Credentials")
        return redirect('login')
    
# ========================================================= END ==============================================================================

# ====================================================== ADMINPANEL =====================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminpanel(request):
        if 'is_authenticated' in request.session:
            search_querry = request.GET.get('search','')
            if search_querry :
                users = User.objects.filter(username__istartswith=search_querry)
            else:
                users = User.objects.all()
            return render(request, 'admin.html',{'users':users,'search_querry':search_querry})
        else:
            return redirect('admin')
        
# ===================================================== END ==============================================================================
        
# ==================================================== ADMIN ================================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin(request):
    if 'is_authenticated' in request.session:
        return redirect('adminpanel')
    
    Username = 'admin'
    Password = 'admin'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if Username == username and Password == password:
            request.session['is_authenticated']=True
            return redirect('adminpanel')
    
    return render(request, 'adminlogin.html')

# ====================================================== END ==============================================================================

# ================================================== CREATE USER ========================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createuser(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        Name = request.POST['Name'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password1'].strip()
        cpassword = request.POST['password2'].strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Exist!')
            return redirect('createuser')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Registered')
            return redirect('createuser')
        
        if len(username)>10:
            messages.error(request, 'Username Must Be Under 10 Characters')
            return redirect('createuser')
        
        if password != cpassword:
            messages.error('Password Didnt Match')
            return redirect('createuser')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = Name
        myuser.save()
    
        # user_obj = Userdetails(username=username, name=Name, email=email, password=password)
        # user_obj.save()

        messages.success(request, "Your Account has been successfully created")

        return redirect('createuser')

    return render(request, 'createuser.html')

# ========================================================= END ==============================================================================

# ===================================================== ADMIN DELETE ================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_delete(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('adminpanel')  # Redirect to admin panel after deletion
    users = User.objects.all()
    return render(request, 'admin.html', {'users': users})

# ======================================================== END ==============================================================================

# ====================================================== ADMIN EDIT ===================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_edit(request,user_id):
    if 'is_authenticated' in request.session:
         
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('admin')

        if request.method == 'POST':
            Username = request.POST['username']
            Name = request.POST['Name']
            Email = request.POST['email']
            Password1 = request.POST['password1']
            Password2 = request.POST['password2']

            if Password1 != Password2:
                messages.error(request, 'Passwords do not match')
                return redirect('edit',user_id=user.id)

            if User.objects.filter(username=Username).exclude(id=user_id).exists():
                messages.error(request, 'Username already exists')
                return redirect('edit',user_id=user.id)
            
            if User.objects.filter(first_name=Name).exclude(id=user_id):
                messages.error(request, 'Username already exists')
                return redirect('edit',user_id=user.id)

            if User.objects.filter(email=Email).exclude(id=user_id).exists():
                messages.error(request, 'Email already exists')
                return redirect('edit',user_id=user.id)

            user.username = Username
            user.first_name = Name
            user.email = Email
            user.password = Password1
            user.save()

            messages.success(request, 'User updated successfully')
            return redirect('adminpanel')
                
        return render(request, 'edit.html', {'user': user})
    
    else:
        return render(request, 'adminlogin.html')

# ========================================================== END ==============================================================================

# ========================================================= LOG OUT HOME =================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logouthome(request):
    logout(request)
    return redirect('login')

# ========================================================= END ==============================================================================

# ========================================================== LOG OUT ADMIN ==================================================================

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutadmin(request):
    if 'is_authenticated' in request.session:
        request.session.flush()
        return redirect('admin')
    
# ================================================================= END ==============================================================================
