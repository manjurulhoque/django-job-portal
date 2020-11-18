def update_user(backend, user, response, *args, **kwargs):
    user.role = "employee"
    user.save()
