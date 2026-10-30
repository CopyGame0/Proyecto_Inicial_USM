from django.shortcuts import render

def pagina_principal(request):
    return render(request, 'inicio/index.html')
def formulario_view(request):
    return render(request, 'inicio/formulario.html')