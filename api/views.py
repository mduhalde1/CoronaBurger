from api.models import Hamburguesa, Ingrediente
from api.serializers import HamburguesaSerializer, IngredienteSerializer, IngredienteSimplifiedSerializer, HamburguesaSimplifiedSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response


url = 'www.coronaburger.com/api/ingrediente/'

@api_view(['GET', 'POST'])
def Hamburguesa_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        hamburguesas = Hamburguesa.objects.all()
        serializer = HamburguesaSerializer(hamburguesas, many=True)
        if hamburguesas.count() > 0:
            for j in range(hamburguesas.count()):
                print('1')
                ingredientes=[]
                for i in serializer.data[j]['ingredientes']:
                    ingredientes.append({"path": url+str(i)})
                serializer.data[j]['ingredientes'] = ingredientes
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HamburguesaSimplifiedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("input invalido", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def Ingrediente_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        ingredientes = Ingrediente.objects.all()
        serializer = IngredienteSimplifiedSerializer(ingredientes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = IngredienteSimplifiedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("Input invalido", status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'GET'])
def Ingrediente_detail(request, numero):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        pk = int(numero)
    except ValueError:
        return Response("id invalido",status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ingrediente = Ingrediente.objects.get(pk=pk)
    except Ingrediente.DoesNotExist:
        return Response("ingrediente inexistente", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_simplified = IngredienteSimplifiedSerializer(ingrediente)
        return Response(serializer_simplified.data)

    elif request.method == 'DELETE':
        serializer = IngredienteSerializer(ingrediente)
        if ingrediente.hamburguesas.count() == 0:
            ingrediente.delete()
            return Response("ingrediente eliminado",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Ingrediente no se puede borrar, se encuentra presente en una hamburguesa", status=status.HTTP_409_CONFLICT)


@api_view(['PATCH', 'DELETE', 'GET'])
def Hamburguesa_detail(request, numero):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        pk = int(numero)
    except ValueError:
        return Response("id invalido",status=status.HTTP_400_BAD_REQUEST)
    try:
        hamburguesa = Hamburguesa.objects.get(pk=pk)
    except Hamburguesa.DoesNotExist:
        return Response("hamburguesa inexistente",status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HamburguesaSerializer(hamburguesa)
        ingredientes=[]
        for i in serializer.data['ingredientes']:
            ingredientes.append({"path": url+str(i)})
        new_data = serializer.data
        new_data['ingredientes'] = ingredientes
        return Response(new_data)
    
    elif request.method == 'PATCH':
        fields_accepted = ['nombre', 'precio', 'descripcion', 'imagen']
        for key in request.data.keys():
            if key not in fields_accepted:
                return Response("Parámetros inválidos",status=status.HTTP_400_BAD_REQUEST)
        serializer = HamburguesaSerializer(hamburguesa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            ingredientes=[]
            for i in serializer.data['ingredientes']:
                ingredientes.append({"path": url+str(i)})
            new_data = serializer.data
            new_data['ingredientes'] = ingredientes
            return Response(new_data)
        return Response("Parámetros inválidos", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hamburguesa.delete()
        return Response("hamburguesa eliminada", status=status.HTTP_200_OK)


@api_view(['DELETE', 'PUT'])
def modify_hamburguesa_ingrediente(request, pk, pk2):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        hamburguesa = Hamburguesa.objects.get(pk=pk)
    except Hamburguesa.DoesNotExist:
        return Response("Id de hamburguesa inválido",status=status.HTTP_404_NOT_FOUND)
    try:
        ingrediente = Ingrediente.objects.get(pk=pk2)
    except Ingrediente.DoesNotExist:
        return Response("Ingrediente inexistente", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = HamburguesaSerializer(hamburguesa)
        if int(pk2) not in serializer.data['ingredientes']:
            serializer.data['ingredientes'].append(int(pk2))
        serializer = HamburguesaSerializer(hamburguesa, data={'ingredientes': serializer.data['ingredientes']}, partial=True)
        if serializer.is_valid():
            serializer.save()
            ingredientes=[]
            for i in serializer.data['ingredientes']:
                ingredientes.append({"path": url+str(i)})
            new_data = serializer.data
            new_data['ingredientes'] = ingredientes
            return Response(new_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        serializer = HamburguesaSerializer(hamburguesa)
        if int(pk2) in serializer.data['ingredientes']:
            serializer.data['ingredientes'].remove(int(pk2))
        serializer = HamburguesaSerializer(hamburguesa, data={'ingredientes': serializer.data['ingredientes']}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("ingrediente retirado", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)