from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "error"}, status=500)

