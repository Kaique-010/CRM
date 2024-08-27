from django.shortcuts import render
from licencas.models import Licencas

def listar_licencas(request):
    if request.user.is_authenticated:
        licencas = Licencas.objects.filter(usuarios=request.user)
    else:
        licencas = Licencas.objects.none()  # Nenhuma licença se o usuário não estiver autenticado

    return render(request, 'licencas/lista.html', {'licencas': licencas})
