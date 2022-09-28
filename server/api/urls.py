"""xshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from api.views.alidrive import AliyunDriveView, AliyunDriveQRView
from api.views.download import DownloadView
from api.views.files import FileInfoView, ManyView
from api.views.lobby import FileLobbyView
from api.views.share import ShareCodeView
from api.views.short import ShortView
from api.views.upload import AliyunDriveUploadView
from api.views.userinfo import LoginView, UserInfoView, RefreshTokenView, LogoutView, RegisterView

router = SimpleRouter(False)
router.register('drive', AliyunDriveView)
router.register('file', FileInfoView)
router.register('download', DownloadView)
router.register('share', ShareCodeView)
urlpatterns = [
    # path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path('login', LoginView.as_view(), name='login'),
    re_path('register', RegisterView.as_view(), name='register'),
    re_path('logout', LogoutView.as_view(), name='logout'),
    re_path('userinfo', UserInfoView.as_view(), name='userinfo'),
    re_path('qrdrive', AliyunDriveQRView.as_view(), name='qrdrive'),
    re_path('upload', AliyunDriveUploadView.as_view(), name='upload'),
    re_path('short', ShortView.as_view(), name='short'),
    re_path('lobby', FileLobbyView.as_view(), name='lobby'),
    re_path(r'^many/(?P<name>\w+)$', ManyView.as_view(), name='many'),
    re_path('refresh', RefreshTokenView.as_view(), name='refresh'),
    re_path('', include(router.urls))

]
