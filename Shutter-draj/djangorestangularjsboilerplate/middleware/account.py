from djangorestangularjsboilerplate.models import UserStatus

class AccountMiddleware(object):
	"""docstring for AccountMiddleware"""
	def process_request(self, request):
		print 'middleware executed'
		try:
			print request.user
			print UserStatus.objects.get(id=request.user.id).is_active
			return HttpResponse("some response")
		except Exception:
			pass
	

	def process_response(self, request, response):
		print "AccountMiddleware process_response executed"
		return response