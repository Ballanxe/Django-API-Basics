from django.db.models import Q
from rest_framework import generics, mixins

from .permissions import IsOwnerOrReadOnly
from posting.models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostAPIView(mixins.CreateModelMixin,generics.ListAPIView):

	lookup_field		= 'pk'
	serializer_class	= BlogPostSerializer # This add a serializer to the view 
	# permission_classes  = [IsOwnerOrReadOnly] 

	def get_queryset(self):

		qs = BlogPost.objects.all()
		query = self.request.GET.get("q")
		if query is not None:
			qs = qs.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()

		return qs

	def perform_create(self,serializer):
		"""This asign the user logged in to the post created user field """
		serializer.save(user=self.request.user)

	def post(self,request,*args,**kwargs):
		"""This allow the ListAPIView to have a post method in
		the view thanks to the CreateModelMixin  """
		return self.create(request, *args, **kwargs)

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}



class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field		= 'pk'
	serializer_class	= BlogPostSerializer
	# permission_classes	= [IsOwnerOrReadOnly]


	def get_queryset(self):
		return BlogPost.objects.all()

	def get_serializer_context(self, *args, **kwargs):
		return {"request":self.request}

