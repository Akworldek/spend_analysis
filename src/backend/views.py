from django.db.models import Sum, Avg, Max, Min, Count
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer, UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)

        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                pass

        # Filter by category if provided
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category__name=category)

        # Filter by search query if provided
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(description__icontains=search)

        return queryset

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get spending summary statistics
        """
        # Default to current month if no date range specified
        today = timezone.now().date()
        start_date = request.query_params.get('start_date', (today.replace(day=1)).strftime('%Y-%m-%d'))
        end_date = request.query_params.get('end_date', today.strftime('%Y-%m-%d'))

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        # Base queryset with date filters
        queryset = Expense.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date
        )

        # Filter by category if provided
        category = request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(category__name=category)

        # Filter by search query if provided
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(description__icontains=search)

        # Calculate statistics
        stats = queryset.aggregate(
            total=Sum('amount'),
            avg=Avg('amount'),
            max=Max('amount'),
            min=Min('amount'),
            count=Count('id')
        )

        # Get category breakdown
        categories = []
        for category in Category.objects.filter(user=request.user):
            category_total = queryset.filter(category=category).aggregate(total=Sum('amount'))['total'] or 0
            categories.append({
                'name': category.name,
                'amount': category_total
            })

        # Sort categories by amount (descending)
        categories.sort(key=lambda x: x['amount'], reverse=True)

        return Response({
            'total_spending': stats['total'] or 0,
            'avg_transaction': stats['avg'] or 0,
            'max_expense': stats['max'] or 0,
            'min_expense': stats['min'] or 0,
            'transaction_count': stats['count'] or 0,
            'categories_used': queryset.values('category').distinct().count(),
            'spending_by_category': categories
        })

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        """
        Get monthly spending totals for the last 6 months
        """
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=180)  # Approximately 6 months

        # Get all expenses in date range
        expenses = Expense.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date
        )

        # Group by month and calculate totals
        monthly_data = {}
        for expense in expenses:
            month_key = expense.date.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    'month': expense.date.strftime('%b %Y'),
                    'amount': 0
                }
            monthly_data[month_key]['amount'] += float(expense.amount)

        # Convert to list and sort by month
        result = list(monthly_data.values())
        result.sort(key=lambda x: datetime.strptime(x['month'], '%b %Y'))

        return Response(result)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        token, created = Token.objects.get_or_create(user=user)

        # Create some default categories for the user
        default_categories = ['Food', 'Utilities', 'Transportation', 'Entertainment', 'Shopping']
        for category_name in default_categories:
            Category.objects.create(name=category_name, user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({
            'error': 'Username already exists'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    if request.user.is_authenticated:
        request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)