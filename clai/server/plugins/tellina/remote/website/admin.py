from django.contrib import admin

from .models import Annotation, AnnotationUpdate, Command, CommandAdmin, NLRequest, \
    Translation, URL, URLTag, User, UserAdmin

admin.site.register(Command, CommandAdmin)

admin.site.register(URL)
admin.site.register(User, UserAdmin)
admin.site.register(NLRequest)
admin.site.register(Translation)
admin.site.register(Annotation)
admin.site.register(AnnotationUpdate)
admin.site.register(URLTag)
