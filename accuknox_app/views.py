from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from .serializers import *



# register user api
@api_view(['POST'])
def user_registration_api(request):
    serializer = UserModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# login user api
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # if check_password(password, user.password):
        if user.password == password:
        # if ph.verify(user.password, password):
            refresh = RefreshToken.for_user(user)
            return Response({'message': 'Login successful', 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Both email and password are required'}, status=status.HTTP_400_BAD_REQUEST)



# API to search other users by email and name
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET.get('query', '')
    page_number = request.GET.get('page', 1)

    try:
        print('try')
        exact_user = UserModel.objects.get(email=query)
        results = [{
            'name': exact_user.name,
            'email': exact_user.email
        }]
        return Response({
            'results': results,
            'page': 1,
            'total_pages': 1
        })

    except UserModel.DoesNotExist:
        print('except')
        users = UserModel.objects.filter(
            Q(email__icontains=query) | Q(name__icontains=query)
        )

        paginator = Paginator(users, 10)  # 10 records per page
        page_obj = paginator.get_page(page_number)

        results = [
            {
                'name': user.name,
                'email': user.email
            }
            for user in page_obj
        ]

        return Response({
            'results': results,
            'page': page_number,
            'total_pages': paginator.num_pages
        })



# API to send friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id')

    if sender_id == receiver_id:
        return JsonResponse({'error': 'Cannot send friend request to yourself'}, status=400)

    sender = UserModel.objects.get(id=sender_id)
    receiver = UserModel.objects.get(id=receiver_id)

    # check if the sender has sent more than 3 friend requests in the last minute
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    recent_requests_count = FriendRequestModel.objects.filter(
        sender=sender, timestamp__gte=one_minute_ago
    ).count()

    if recent_requests_count >= 3:
        return Response({'error': 'You have sent too many friend requests. Please wait a moment before sending more.'}, status=429)

    friend_request, created = FriendRequestModel.objects.get_or_create(sender=sender, receiver=receiver)

    if not created:
        if friend_request.status == 'pending':
            return Response({'error': 'Friend request already sent'}, status=400)
        else:
            friend_request.status = 'pending'
            friend_request.save()

    return Response({'message': 'Friend request sent successfully'})



# API to accept friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
    request_id = request.data.get('request_id')
    try:
        friend_request = FriendRequestModel.objects.get(id=request_id, status='pending')
        friend_request.status = 'accepted'
        friend_request.save()

        return Response({'message': 'Friend request accepted'})

    except FriendRequestModel.DoesNotExist:
        return Response({'error': 'Friend request not found or already handled'}, status=400)



# API to Reject friend request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request):
    request_id = request.data.get('request_id')
    try:
        friend_request = FriendRequestModel.objects.get(id=request_id, status='pending')
        friend_request.status = 'rejected'
        friend_request.save()

        return Response({'message': 'Friend request rejected'})

    except FriendRequestModel.DoesNotExist:
        return Response({'error': 'Friend request not found or already handled'}, status=400)



# API to list friends(list of users who have accepted friend request
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    try:
        user_id = request.GET.get('user_id')
        user = UserModel.objects.get(id=user_id)
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    sent_requests = FriendRequestModel.objects.filter(sender=user, status='accepted').select_related('receiver')
    sent_friends = [req.receiver for req in sent_requests]

    received_requests = FriendRequestModel.objects.filter(receiver=user, status='accepted').select_related('sender')
    received_friends = [req.sender for req in received_requests]

    friends = sent_friends + received_friends

    # Serialize the results
    results = [
        {
            'id': friend.id,
            'name': friend.name,
            'email': friend.email
        }
        for friend in friends
    ]

    return Response({
        'friends': results
    })



# List pending friend requests(received friend request)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    try:
        user_id = request.GET.get('user_id')
        user = UserModel.objects.get(id=user_id)
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    pending_requests = FriendRequestModel.objects.filter(receiver=user, status='pending').select_related('sender')

    results = [
        {
            'request_id': req.id,
            'sender_id': req.sender.id,
            'sender_name': req.sender.name,
            'sender_email': req.sender.email
        }
        for req in pending_requests
    ]

    return Response({
        'pending_requests': results
    })