from django.db.models import Sum, Avg, Max, Min, Count
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Expense, Transaction
from .serializers import CategorySerializer, ExpenseSerializer, UserSerializer, TransactionSerializer
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import csv
import io
import pandas as pd
from datetime import datetime



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





class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """
        This view returns a list of all transactions for the currently authenticated user.
        """
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        This view returns a list of all categories for the currently authenticated user.
        """
        user = self.request.user
        return Category.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spending_summary(request):
    """
    Get spending summary data grouped by category.
    """
    user = request.user

    # Get query parameters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Filter transactions by date if parameters are provided
    transactions = Transaction.objects.filter(user=user)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Aggregate by category
    category_summary = transactions.values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Calculate total spending
    total_spending = transactions.aggregate(total=Sum('amount'))['total'] or 0

    return Response({
        'categories': category_summary,
        'total_spending': total_spending
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_spending(request):
    """
    Get spending data grouped by month.
    """
    user = request.user

    # Get query parameters for year
    year = request.query_params.get('year', datetime.now().year)

    # Filter transactions for the specified year
    transactions = Transaction.objects.filter(
        user=user,
        date__year=year
    )

    # Extract month from date and group by month
    monthly_data = {}
    for month in range(1, 13):
        month_transactions = transactions.filter(date__month=month)
        total = month_transactions.aggregate(total=Sum('amount'))['total'] or 0
        month_name = datetime(2000, month, 1).strftime('%B')
        monthly_data[month_name] = total

    return Response(monthly_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """
    Upload transactions from a CSV file.
    Expected CSV format: date,description,amount,category
    """
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)

    # Read the CSV file
    try:
        data = csv_file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(data))

        # Validate required columns
        required_columns = ['date', 'description', 'amount', 'category']
        for col in required_columns:
            if col not in df.columns:
                return Response(
                    {'error': f'Missing required column: {col}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Process each row
        transactions_created = 0
        for _, row in df.iterrows():
            # Parse date
            try:
                date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            except ValueError:
                try:
                    date = datetime.strptime(row['date'], '%m/%d/%Y').date()
                except ValueError:
                    continue  # Skip rows with invalid dates

            # Get or create category
            category_name = row['category']
            category, _ = Category.objects.get_or_create(
                name=category_name,
                user=request.user
            )

            # Create transaction
            Transaction.objects.create(
                user=request.user,
                date=date,
                description=row['description'],
                amount=float(row['amount']),
                category=category
            )
            transactions_created += 1

        return Response({
            'success': True,
            'transactions_created': transactions_created
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get the current user's profile information.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the current user's profile information.
    """
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """
        This view returns a list of all transactions for the currently authenticated user.
        """
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        This view returns a list of all categories for the currently authenticated user.
        """
        user = self.request.user
        return Category.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spending_summary(request):
    """
    Get spending summary data grouped by category.
    """
    user = request.user

    # Get query parameters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Filter transactions by date if parameters are provided
    transactions = Transaction.objects.filter(user=user)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Aggregate by category
    category_summary = transactions.values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Calculate total spending
    total_spending = transactions.aggregate(total=Sum('amount'))['total'] or 0

    return Response({
        'categories': category_summary,
        'total_spending': total_spending
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_spending(request):
    """
    Get spending data grouped by month.
    """
    user = request.user

    # Get query parameters for year
    year = request.query_params.get('year', datetime.now().year)

    # Filter transactions for the specified year
    transactions = Transaction.objects.filter(
        user=user,
        date__year=year
    )

    # Extract month from date and group by month
    monthly_data = {}
    for month in range(1, 13):
        month_transactions = transactions.filter(date__month=month)
        total = month_transactions.aggregate(total=Sum('amount'))['total'] or 0
        month_name = datetime(2000, month, 1).strftime('%B')
        monthly_data[month_name] = total

    return Response(monthly_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """
    Upload transactions from a CSV file.
    Expected CSV format: date,description,amount,category
    """
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)

    # Read the CSV file
    try:
        data = csv_file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(data))

        # Validate required columns
        required_columns = ['date', 'description', 'amount', 'category']
        for col in required_columns:
            if col not in df.columns:
                return Response(
                    {'error': f'Missing required column: {col}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Process each row
        transactions_created = 0
        for _, row in df.iterrows():
            # Parse date
            try:
                date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            except ValueError:
                try:
                    date = datetime.strptime(row['date'], '%m/%d/%Y').date()
                except ValueError:
                    continue  # Skip rows with invalid dates

            # Get or create category
            category_name = row['category']
            category, _ = Category.objects.get_or_create(
                name=category_name,
                user=request.user
            )

            # Create transaction
            Transaction.objects.create(
                user=request.user,
                date=date,
                description=row['description'],
                amount=float(row['amount']),
                category=category
            )
            transactions_created += 1

        return Response({
            'success': True,
            'transactions_created': transactions_created
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get the current user's profile information.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the current user's profile information.
    """
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def register(request):
    """
    Register a new user.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})