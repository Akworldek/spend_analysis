from rest_framework import serializers
from .models import Category, Expense, Transaction
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        category = Category.objects.create(user=user, **validated_data)
        return category


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'date', 'category', 'category_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_category_name(self, obj):
        if obj.category:
            return obj.category.name
        return None

    def create(self, validated_data):
        user = self.context['request'].user
        expense = Expense.objects.create(user=user, **validated_data)
        return expense


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'description', 'amount', 'category', 'category_name', 'category_color']
        read_only_fields = ['user']