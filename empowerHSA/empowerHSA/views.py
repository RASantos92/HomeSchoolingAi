from django.http import JsonResponse
from django.views import View
from .models.Lesson import Lesson
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from bson import ObjectId

@method_decorator(csrf_exempt, name='dispatch')
class LessonListCreateView(View):
    def get(self, request):
        print("here")
        lessons = Lesson.objects.all()
        
        print(lessons[len(lessons)-1]._id)
        lessons_json = [
            {
                "id": str(lesson._id),
                "title": lesson.title,
                "content": lesson.content,
                "created_at": lesson.created_at
            } 
            for lesson in lessons
        ]
        return JsonResponse(lessons_json, safe=False)

    def post(self, request):
        print("in the post method")
        try:
            data = json.loads(request.body.decode('utf-8'))
            lesson = Lesson.objects.create(
                title=data.get('title'),
                content=data.get('content')
            )
            return JsonResponse({
                'id': str(lesson._id),
                'title': lesson.title,
                'content': lesson.content,
                'created_at': lesson.created_at
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LessonRetrieveUpdateDestroyView(View):
    def get(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
            return JsonResponse({
                'id': str(lesson._id),
                'title': lesson.title,
                'content': lesson.content,
                'created_at': lesson.created_at
            })
        except Lesson.DoesNotExist:
            return JsonResponse({'error': 'Lesson not found'}, status=404)

    def put(self, request, pk):
        try:
            data = json.loads(request.body.decode('utf-8'))
            lesson = Lesson.objects.get(pk=pk)
            lesson.title = data.get('title', lesson.title)
            lesson.content = data.get('content', lesson.content)
            lesson.save()
            return JsonResponse({
                'id': str(lesson._id),
                'title': lesson.title,
                'content': lesson.content,
                'created_at': lesson.created_at
            })
        except Lesson.DoesNotExist:
            return JsonResponse({'error': 'Lesson not found'}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
            lesson.delete()
            return JsonResponse({'message': 'Lesson deleted successfully'}, status=204)
        except Lesson.DoesNotExist:
            return JsonResponse({'error': 'Lesson not found'}, status=404)