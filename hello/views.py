from django.shortcuts import render
from .entities.user import User

# Create your views here.
def index(request):
    users = User.get_all()
    return render(request, 'hello/index.html', {'users': users})
