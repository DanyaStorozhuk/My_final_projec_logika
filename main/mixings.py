from django.contrib.auth.mixins import UserPassesTestMixin



class UserAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'admin'
    
