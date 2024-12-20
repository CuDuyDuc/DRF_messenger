import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models

from message_be.apps.models_container.user import User
from message_be.apps.models_container.message import Message