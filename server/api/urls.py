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
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views.alidrive import AliyunDriveView, AliyunDriveQRView
from api.views.download import DownloadView
from api.views.files import FileInfoView, ManyView
from api.views.share import ShareCodeView
from api.views.short import ShortView
from api.views.upload import AliyunDriveUploadView
from api.views.userinfo import LoginView, UserInfoView

router = SimpleRouter(False)
router.register('drive', AliyunDriveView)
router.register('file', FileInfoView)
router.register('download', DownloadView)
router.register('share', ShareCodeView)
urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login', LoginView.as_view(), name='login'),
    path('userinfo', UserInfoView.as_view(), name='userinfo'),
    path('qrdrive', AliyunDriveQRView.as_view(), name='qrdrive'),
    path('upload', AliyunDriveUploadView.as_view(), name='upload'),
    path('short', ShortView.as_view(), name='short'),
    re_path(r'^many/(?P<name>\w+)$', ManyView.as_view(), name='many'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))

]
