from django.utils.translation import gettext_lazy as _


def navbar(request):
    user = request.user
    navbar_items = [{
        'label': _('Users'),
        'url': '/users/',
        'class': 'nav-link',
        'align': ''
    }]
    if request.user.is_authenticated:
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
        navbar_items.append({
            'label': _('Wellcome') + ', ' + user.username,
            'class': 'nav-link',
            'align': 'ms-auto'
        })
        navbar_items.append({
            'label': _('Logout'),
            'url': '/logout/',
            'form': True,
            'class': 'btn nav-link',
            'align': ''
        })
    else:
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
