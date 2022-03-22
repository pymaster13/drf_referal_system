"""person application URL Configuration"""

from django.urls import path

from .views import (UserGetCodeView, UserAuthorizeView,
                    UserImplementInviteView, profile)

"""
URLs
- get_code/ - first authorization step is entering phone number
              to get code by sms
- authorize/ - second step is entering accepted sms-code and
               getting authorization jwt tokens
- profile/ - get information about user (phone, invite_code,
             invited users) (only for authorized users)
- implement_invite/ - try to realize foreign invite code
                      (only for authorized users)
"""

urlpatterns = [
    path('get_code/', UserGetCodeView.as_view(), name='get_code'),
    path('authorize/', UserAuthorizeView.as_view(), name='authorize'),
    path('profile/', profile, name='profile'),
    path('implement_invite/',
         UserImplementInviteView.as_view(),
         name=' implement_invite'),
]
