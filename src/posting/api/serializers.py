from rest_framework import serializers

from posting.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
	url 				= serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = BlogPost
		fields = [
			'url',
			'pk', # If you have url stuff dont need anymore the pk
			'user',
			'title',
			'content',
			'timestamp',

		]

		# read_only_fields = ['user'] # This prevents the change via PUT 


	def get_url(self,obj):

		request = self.context.get("request")
		return obj.get_api_url(request=request)	


	def validate_title(self,value):
		"""This validates the title because it has to be unique"""


		qs = BlogPost.objects.filter(title__iexact=value)
		if self.instance:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise serializers.ValidationError("This title has already been used")
		return value
