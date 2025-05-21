def detectuser(user):
    if user.role == 1:
        return 'vendorDashboard'  # Must match the URL name in urls.py
    elif user.role == 2:
        return 'customerDashboard'
    elif user.role is None and user.is_superadmin:
        return 'admin'
    return 'home'  # Default fallback