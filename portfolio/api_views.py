from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Profile, Skill
from .serializers import ProfileSerializer, SkillSerializer


class ProfileAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        profile = Profile.objects.filter(is_active=True).first()
        if profile:
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response(serializer.data)
        return Response({})


class SkillListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)
