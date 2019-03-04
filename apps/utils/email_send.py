from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM


#ランダムの文字列を作り方
def random_str(randomlength=8):
    str = ''
    chars ="AaBaCcDdEeFfGgHhIiJjKkMmNnLlOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    #メール発送前の内容入力
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "デベロッパー新規登録"
        email_body = "以下のリンクをクリックしてください:http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "デベロッパーパスワードリセット"
        email_body = "以下のリンクをクリックしてパスワードリセットしてください:http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

