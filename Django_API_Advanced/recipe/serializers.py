from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """ Serializador para objeto tag """
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    """ Serializador para objeto ingredient """
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializador para objeto recipe """

    ingredients = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'price', 'time_minutes', 'link',)
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """ Serializador para objeto recipe con detalles """
    ingredients = IngredientSerializer(many = True, read_only = True)
    tags = TagSerializer(many = True, read_only = True)