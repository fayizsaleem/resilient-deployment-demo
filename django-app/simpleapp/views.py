from django.http import JsonResponse
def health(request):
    # Return status OK (change to 500 later to simulate failure)
    return JsonResponse({"status": "error","message": "simulated failure"}, status=500)

