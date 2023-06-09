from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core_routes.models import *
from core_routes.serializers import *
from rest_framework.views import APIView
from core_routes.helpers.helper_functions import *

"""
This file holds all view classes related to the RecettesIngredients, SousRecettes,
and RecettesProgressionElements models. 
"""
class RecetteIngredientsDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecettesIngredients item.
    """
    def get_object(self, pk):
        try:
            return RecetteIngredient.objects.get(pk=pk)
        except Recette.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = GetRecetteIngredientSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteIngredientSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        serializer = CreateRecetteIngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SousRecettesDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a SousRecette item.
    """
    def get_object(self, pk):
        try:
            return SousRecette.objects.get(pk=pk)
        except Recette.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SousRecetteSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        serializer = SousRecetteSerializer(data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class RecetteProgressionDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecettesIngredients item.
    """
    def get_object(self, pk):
        try:
            return RecetteProgressionElement.objects.get(pk=pk)
        except Recette.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        print(request.data)
        snippet = self.get_object(pk)
        current_section = snippet.section
        current_rank = snippet.rank
        if 'section' in request.data:
            request.data['rank'] = self.get_rank_in_new_section(request.data['section'])
        serializer = RecetteProgressionElementUpdateSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            self.update_rank_in_old_section(current_section,current_rank)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_rank_in_new_section(self, section_id):
        section_items = RecetteProgressionElement.objects.filter(section= section_id).order_by('rank')
        print(section_items)
        if len(section_items) >0:
            max_rank = section_items[len(section_items)-1].rank
            print(f"max rank bcs there was: {max_rank}")
        else:
            max_rank =0
        return max_rank + 1

    def update_rank_in_old_section(self,section,rank):
        following_elements = RecetteProgressionElement.objects.filter(section=section).filter(rank__gt =rank)
        for element in following_elements:
            element.rank -=1
            element.save()

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        all_progression_elements_of_same_section = RecetteProgressionElement.objects.filter(section=snippet.section)
        for progression_element in all_progression_elements_of_same_section:
            if progression_element.rank> snippet.rank:
                progression_element.rank = progression_element.rank - 1
                progression_element.save()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        serializer = RecetteProgressionElementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class IncrementProgressionElementRank(APIView):
    def put(self, request,progression_element_id, format=None):
        progression_element = RecetteProgressionElement.objects.get(id=progression_element_id)
        try: 
            progression_element_above = RecetteProgressionElement.objects.get(section=progression_element.section,rank=progression_element.rank-1)
            if progression_element_above:
                progression_element_above.rank = progression_element_above.rank +1
                progression_element_above.save()
                progression_element.rank = progression_element.rank -1
                progression_element.save()
                return Response(status=status.HTTP_200_OK) 
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE) 
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE) 
     
class DecrementProgressionElementRank(APIView):
    def put(self, request,progression_element_id, format=None):
        progression_element = RecetteProgressionElement.objects.get(id=progression_element_id)
        try: 
            progression_element_below = RecetteProgressionElement.objects.get(section=progression_element.section,rank=progression_element.rank+1)
            if progression_element_below:
                progression_element_below.rank = progression_element_below.rank -1
                progression_element_below.save()
                progression_element.rank = progression_element.rank +1
                progression_element.save()
                return Response(status=status.HTTP_200_OK) 
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE) 
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE) 


class RecetteSectionDetailAPIView(APIView):
    """
    Retrieve, update or delete a snippet a RecettesIngredients item.
    """
    def get_object(self, pk):
        try:
            return RecetteSection.objects.get(pk=pk)
        except Recette.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RecetteSectionSerializer(snippet, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        serializer = RecetteSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
