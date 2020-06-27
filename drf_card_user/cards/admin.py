from django.contrib import admin

# Register your models here.
from cards.models import Card


def report(modeladmin, request, queryset):
    ids = [x.id for x in queryset.all()]
    count = queryset.update(is_required=True)
    print("here:", ids, 'COUNT', count)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ['id', 'user', 'date', 'content', '_user']
    list_filter = ['date']
    search_fields = ['content', 'date', 'user_username']  # or 조건과 contain!  엄청 느림!
    # autocomplete_fields =
    actions = (report,)

    #  유저 커스텀 list_display 안에 있어서 각각이 object를 호출한다..
    #  그래서 메소드면 첫번재 인자로 오브젝트가 온다!
    def _user(self, obj):
        print(obj)
        return str(obj.user.id) + "user!!"
