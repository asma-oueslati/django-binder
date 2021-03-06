from binder.permissions.views import PermissionView
from binder.exceptions import BinderForbidden

from ..models import ZooEmployee

# From the api docs
class ZooEmployeeView(PermissionView):
	model = ZooEmployee

	# Override this method so we don't have to deal with actual permissions in testing
	def _require_model_perm(self, perm_type, request, pk=None):
		request._has_permission_check = True
		if request.user.is_superuser:
			return ['all']
		elif perm_type == 'view' and request.user.username == 'testuser2':
			return ['test']
		elif request.user.username == 'testuser3':
			return ['restricted']
		else:
			model = self.perms_via if hasattr(self, 'perms_via') else self.model
			perm = '{}.{}_{}'.format(model._meta.app_label, perm_type, model.__name__.lower())
			raise BinderForbidden(perm, request.user)

	def _scope_view_test(self, request):
		return self.model.objects.none()


	def _scope_view_restricted(self, request):
		return self.model.objects.all()


	def _scope_add_restricted(self, request, obj, values):
		return values.get('name') == 'add okay'


	def _scope_change_restricted(self, request, obj, values):
		return values.get('name') == 'change okay'
