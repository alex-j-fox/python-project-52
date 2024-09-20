from django.utils.translation import gettext_lazy as _


def navbar(request):
    """
    Provides the navbar items for the navigation bar.

    It checks if the user is authenticated and returns the corresponding
    navbar items. If the user is authenticated, it returns the links to the
    users, statuses, labels, and tasks pages. If the user is not authenticated,
    it returns the links to the login and registration pages.

    :param request: The HTTP request.
    :type request: HttpRequest
    :return: A dictionary containing the navbar items.
    :rtype: dict
    """
    user = request.user
    navbar_items = [{
        'label': _('Users'),
        'url': '/users/',
        'class': 'nav-link',
        'align': ''
    }]
    if request.user.is_authenticated:
        # Add the links to the users, statuses, labels, and tasks pages
        navbar_items.append({
            'label': _('Statuses'),
            'url': '/statuses/',
            'class': 'nav-link',
            'align': ''
        })
        navbar_items.append({
            'label': _('Labels'),
            'url': '/labels/',
            'class': 'nav-link',
            'align': ''
        })
        navbar_items.append({
            'label': _('Tasks'),
            'url': '/tasks/',
            'class': 'nav-link',
            'align': ''
        })
        # Add the link to the user's profile
        navbar_items.append({
            'label': _('Wellcome') + ', ' + user.username,
            'class': 'nav-link',
            'align': 'ms-auto'
        })
        # Add the logout button
        navbar_items.append({
            'label': _('Logout'),
            'url': '/logout/',
            'form': True,
            'class': 'btn nav-link',
            'align': ''
        })
    else:
        # Add the links to the login and registration pages
        navbar_items.append({
            'label': _('Login'),
            'url': '/login/',
            'class': 'nav-link ms-auto',
            'align': 'ms-auto'
        })
        navbar_items.append({
            'label': _('Registration'),
            'url': '/users/create/',
            'class': 'nav-link ms-auto',
            'align': ''
        })

    return {'navbar_items': navbar_items}
