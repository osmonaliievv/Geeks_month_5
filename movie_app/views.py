from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, MovieSerializer, ReviewSerializer
from rest_framework import status


# ---------------- Director --------------
@api_view(http_method_names=['GET', 'POST'])
def director_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data={'directors': data})
    elif request.method == 'POST':
        print(request.data)
        # step 1: Receive data from RequestsBody
        name = request.data.get('name')
        # step 2: Create product
        director = Director.objects.create(name=name)
        # step 3: Return response as data and status
        return Response(data={'director_id': director.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data={'director': data})
    elif request.method == 'PUT':
        director.name = request.data.get('name')
        director.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    data = DirectorSerializer(director).data
    return Response(data=data)


# ---------------- Movie --------------
@api_view(http_method_names=['GET', 'POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieSerializer(movies, many=True).data
        return Response(data={'movies': data})
    elif request.method == 'POST':
        print(request.data)
        # step 1: Receive data from RequestsBody
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')
        # step 2: Create product
        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id,
        )
        # step 3: Return response as data and status
        return Response(data={'movie_id': movie.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data={'movies': data})
    elif request.method == 'PUT':
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
        movie.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    data = MovieSerializer(movie).data
    return Response(data=data)


# ---------------- Review --------------
@api_view(http_method_names=['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data={'reviews': data})
    elif request.method == 'POST':
        print(request.data)
        # step 1: Receive data from RequestsBody
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        stars = request.data.get('stars')
        # step 2: Create product
        review = Review.objects.create(
            text=text,
            movie_id=movie_id,
            stars=stars,
        )
        # step 3: Return response as data and status
        return Response(data={'review_id': review.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data={'movies': data})
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.movie_id = request.data.get('movie_id')
        review.stars = request.data.get('stars')
        review.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    data = ReviewSerializer(review).data
    return Response(data=data)
