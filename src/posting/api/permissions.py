from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Object lever permission to only allow owners of an object to edit it. 
	Assumes the model instance has an 'owner' attribute
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are alowed to any requests,
		#so we'll always allow GET, HEAD or OPTIONS request.

		if request.method in permissions.SAFE_METHODS:
			return True
		# Instance must have an attribute named owner 
		return obj.owner == request.user 