from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import generate_access_token, is_auth, generate_refresh_token
from .models import User, Transaction
from .serializers import UserSerializer


class UserView(APIView):
    def get(self, request):

        return Response({"status": "success", "data": "Login successful"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    try:
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return Response({'error': 'Username Not found'}, status=status.HTTP_404_NOT_FOUND)

    if not (user.check_password(password)):
        return Response({'error': 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)
    if user:
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        # token =Token.objects.get_or_create(user_id=user.id)
        # token.key = access_token
        # token.save()
        user.is_login = True  # Set login is True
        user.is_active = True  # Setting user is active or not
        user.token = str(access_token)
        user.save()

        user_data = UserSerializer(user).data
        user_data.update({
            "token": access_token,
            "token": refresh_token
        })
        return Response(user_data, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# This code is consider from a video
@api_view(['POST'])
@is_auth
def user_logout(request):
    print("user_id==>", request.user_id)
    usr = User.objects.get(id=request.user_id)
    usr.is_login = False
    usr.token = ""
    usr.save()
    return Response({"message": "you are logged out successfully"}, status=status.HTTP_200_OK)


# Before


# try:
#     # Get the token from the request
#     username = request.username
#     user = User.objects.get(username = username)
#     if username.is_authenticated:
#         return Response({'message': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

#     #Performing logout
#     user_logout(request)


#          # Remove the user's token
#     token = Token.objects.filter(username=username).first()
#     if token:
#         token.delete()

#     return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

# except Exception as e:
#     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@is_auth
def deposit_amount(request):
    try:
        user_id = request.user_id  # This should be set by the is_auth decorator
        deposit_amount = request.data.get('deposit_amount')

        if not isinstance(deposit_amount, (int, float)) or deposit_amount <= 0:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        user_instance = User.objects.get(id=user_id)

        # Update the user's initial amount  
        current_amount = user_instance.initial_amount
        new_initial_amount = current_amount + deposit_amount
        user_instance.initial_amount = new_initial_amount

        transaction = Transaction.objects.create(user_id=user_instance, deposit_amount=deposit_amount,
                                                 withdraw_amount=0, transaction_type="Deposit")
        transaction.save()
        user_instance.save()

        return Response({"message": "Amount deposited successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@is_auth
def withdraw_amount(request):
    try:
        user_id = request.user_id  # This should be set by the is_auth decorator

        withdraw_amount = request.data.get('withdraw_amount')

        if not isinstance(withdraw_amount, (int, float)) or withdraw_amount <= 0:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        user_instance = User.objects.get(id=user_id)

        # Update the users initial amount
        current_amount = user_instance.initial_amount
        new_initial_amount = current_amount - withdraw_amount
        user_instance.initial_amount = new_initial_amount
        transaction = Transaction.objects.create(user_id=user_instance, deposit_amount=0,
                                                 withdraw_amount=withdraw_amount, transaction_type="Withdraw")
        transaction.save()
        user_instance.save()

        return Response({"message": "Amount Withdraw successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error>>': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@is_auth
def get_balance(request):
    try:
        user_id = request.user_id
        user_instance = User.objects.get(id=user_id)
        balance = user_instance.initial_amount
        transaction = Transaction.objects.create(user_id=user_instance, deposit_amount=0, withdraw_amount=0,
                                                  get_balance=balance)
        user_instance.save()
        transaction.save()
        return Response({"balance": balance}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error>>': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

