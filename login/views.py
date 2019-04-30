# """
# """


# import json
# import facebook
# from voluptuous import All, Length, Schema
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.models import Token
# from users.models import Profile


# facebook_validator = Schema({"token": All(str, Length(min=1))}, required=True)


# _FB_FIELDS = (
#     "first_name",
#     "last_name",
#     "name",
#     "id",
#     "hometown",
#     "location",
#     "email",
#     "picture.type(large)",
#     "birthday",
# )


# @csrf_exempt
# def facebook_login(request, **kwargs) -> JsonResponse:
#     """
#     """
#     data = facebook_validator(json.loads(request.body.decode("utf-8")))
#     access_token = data["token"]
#     new_user = False
#     try:
#         graph = facebook.GraphAPI(access_token=access_token)
#         user_info = graph.get_object(id="me", fields=", ".join(_FB_FIELDS))
#     except facebook.GraphAPIError as exc:
#         print(exc)
#         return JsonResponse({"error": "GraphAPI"})
#     print(user_info)
#     try:
#         user = Profile.objects.get(facebook_id=user_info.get("id")).user
#     except Profile.DoesNotExist:
#         password = User.objects.make_random_password()
#         user = User.objects.create_user(
#             first_name=user_info.get("first_name"),
#             last_name=user_info.get("last_name"),
#             email=user_info.get("email", "testing@test.io"),
#             username=user_info.get("email") or user_info.get("last_name"),
#         )
#         user.set_password(password)
#         user.save()
#         profile = user.profile
#         profile.facebook_id = user_info.get("id")
#         profile.name = user_info.get("name")
#         profile.save()
#         new_user = True
#     print(user)
#     token = Token.objects.get(user=user).key
#     if token:
#         return JsonResponse({"auth_token": token, "new_user": new_user})
#     return JsonResponse({"error": "Not able to return token"})

# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from rest_auth.registration.views import SocialLoginView


# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter
