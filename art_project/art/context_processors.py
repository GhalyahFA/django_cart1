from .models import Category

def get_navbar(request):
    return {"categories": Category.objects.all()}
