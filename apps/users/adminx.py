import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


"""xadminの見た目テーマの設定"""
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    """タイトル設定"""
    site_title = "スクール管理システム"
    """フッター設定"""
    site_footer = "制作者Aki"
    menu_style = "accordion"



class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index']


#model関連付け登録
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

#xadminの見た目テーマviewとの関連付け
xadmin.site.register(views.BaseAdminView, BaseSetting)
#タイトルなどの設定
xadmin.site.register(views.CommAdminView, GlobalSettings)

