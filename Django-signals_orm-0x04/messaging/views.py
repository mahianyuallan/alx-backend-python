from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout


@csrf_exempt
def delete_user(request, user_id):
    """
    View to delete a user account and all related data.
    """
    if request.method == "DELETE":
        user = get_object_or_404(User, id=user_id)
        username = user.username
        user.delete()  # This triggers the post_delete signal
        logout(request)
        return JsonResponse({"message": f"User '{username}' and related data deleted successfully."}, status=200)

    return JsonResponse({"error": "Only DELETE method is allowed."}, status=405)
