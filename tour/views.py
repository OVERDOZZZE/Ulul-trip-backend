from django.forms import model_to_dict
from rest_framework.response import Response
from tour.models import Review, Tour
from rest_framework.views import APIView
class tour_reviews(APIView):
    def get(self, request):
        tour = Tour.objects.get(id=id)
        reviews = Review.objects.filter(tour_id=id)
        return Response({
            'tour': tour,
            'categories': tour.categories.name,
            'reviews': reviews,
        })
    def post(self, request):
        tour = Tour.objects.get(id=id)
        review_new = Review.objects.create(
            text=request.data['text'],

        )
        return Response({
            'tour': tour,
            'categories': tour.categories.name,
            'reviews': model_to_dict(review_new),
            'autor': request.user(request)
        })



