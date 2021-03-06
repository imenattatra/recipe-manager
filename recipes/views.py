from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ingredients.models import Ingredient
from recipes.forms import RecipeForm, RecipeIngredientForm
from recipes.models import Recipe, RecipeIngredient
from django.http import JsonResponse


"""
Recipe CRUD views in this order: 
-RecipeList
-RecipeCreate
-RecipeDelete
-RecipeDetail
"""
class RecipeList(ListView):
    model = Recipe
    template_name = "all_recipes.html"
    context_object_name = "all_recipes"
    def get_context_data(self, **kwargs):
        context = super(RecipeList, self).get_context_data(**kwargs)
        context['title'] = 'Recipes List'
        return context

class RecipeCreate(CreateView):
    model = Recipe
    template_name = "add_recipe.html"
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(RecipeCreate, self).get_context_data(**kwargs)
        context['title'] = 'Add Recipe'
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong")
        return self.render_to_response(
        self.get_context_data(request=self.request, form=form))

    def form_valid(self, form):
        c=form.save()
        messages.success(self.request, "You can now add ingredients to your recipe")
        #we redirect to the "edit recipe" so the user can add ingrediants
        id=c.id
        return HttpResponseRedirect('/recipes/'+str(id)+'/edit/')

class RecipeDelete(DeleteView):
    model = Recipe
    def get_success_url(self):
        messages.success(self.request, "Recipe deleted successfully")
        return reverse('all_recipes')

class RecipeEdit(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'edit_recipe.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super(RecipeEdit, self).get_context_data(**kwargs)
        context['title'] = 'Edit Recipe'
        context['all_recipe_ingredients'] = RecipeIngredient.objects.filter(recipe_id=self.kwargs.get('pk'))
        #hide ingredients that are already in recipe from selection
        existing_ingredients=Ingredient.objects.filter(recipeingredient__in=context['all_recipe_ingredients'] )
        context['all_ingredients'] = Ingredient.objects.all()
        context['not_already_existing_ingredients'] = Ingredient.objects.exclude(id__in=existing_ingredients)
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Something went wrong")
        return self.render_to_response(
        self.get_context_data(request=self.request, form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Recipe modified successfully")
        return HttpResponseRedirect('/recipes/')

class RecipeDetail(DetailView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'view_recipe.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetail, self).get_context_data(**kwargs)
        context['title'] = 'Detail Recipe'
        context['all_ingredients'] = Ingredient.objects.all()
        context['all_recipe_ingredients'] = RecipeIngredient.objects.filter(recipe_id=self.kwargs.get('pk'))
        return context

"""
Recipe Ingredient= ingredient + amount of this ingredient in the recipe

Recipe Ingredient CRUD views in this order:
-create_recipe_ingredient: add ingredient and its amount to a recipe
-edit_recipe_ingredient: edit the ingredient or its amount in a recipe
-RecipeIngredientDelete: remove an ingredient from a recipe
"""

def create_recipe_ingredient(request,recipe_id):
    #FIXME : apply createView with modal to keep the same coding logic
    if request.method == "POST":

        ingredient =Ingredient.objects.get(id=request.POST.get("ingredient"))
        recipe=Recipe.objects.get(id=recipe_id)
        amount = request.POST.get("amount")
        try :
            RecipeIngredient(recipe=recipe,ingredient=ingredient,amount=amount).save()
            messages.success(request, "Ingredient addedd successfully to the recipe.")
        except:
            messages.error(request, "Something went wrong.")
    return HttpResponseRedirect('/recipes/' + str(recipe_id) + '/edit/')

def edit_recipe_ingredient(request,recipe_id,pk):
    #FIXME : apply editView with modal to keep the same coding logic
    if request.method == "POST":

        ingredient =Ingredient.objects.get(id=request.POST.get("ingredient"))
        amount = request.POST.get("amount")
        try :
            ing=RecipeIngredient.objects.filter(id=pk).update(ingredient=ingredient,amount =amount )

            messages.success(request, "Recipe's ingredient updated successfully.")
        except :
            messages.error(request, "Something went wrong.")
    return HttpResponseRedirect('/recipes/' + str(recipe_id) + '/edit/')
class RecipeIngredientDelete(DeleteView):
    model = RecipeIngredient
    def get_success_url(self):
        messages.success(self.request, "Ingredient deleted successfully from the recipe")
        return reverse('edit_recipe', kwargs={'pk': self.kwargs.get('recipe_id')})


"""
Function that check existence of recipe while creating: 
-check_recipe_by_name
"""
def check_recipe_by_name(request):
    name = request.GET.get('name', None)  
    data = {
        'is_taken': Recipe.objects.filter(name__iexact=name).exists(),
    }
    return JsonResponse(data)