from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages


#Allowed users decorator logic:
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):


            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Access Denied")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        return wrapper_func
    return decorator


#"Admin" group only decorator logic (not used yet, useful to have here just in case I need it):
# def admin_only(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         group = None
#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name

#         if group == 'customer':
#             return redirect('dashboard')
        
#         if group == 'admin':
#             return view_func(request, *args, **kwargs)
    
#     return wrapper_func