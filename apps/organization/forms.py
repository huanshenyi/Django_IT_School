from django import forms
from operation.models import UserAsk
import re


class UserAskForm(forms.ModelForm):
      class Meta:
          model = UserAsk
          #exclude =['add_time']
          fields = ['name', 'mobile', 'course_name']

      def clean_mobile(self):
          mobile = self.cleaned_data.get('mobile')
          re_phone = "0[89]0\d{8}$"
          p = re.compile(re_phone)
          if p.match(mobile):
              return mobile
          else:
              raise forms.ValidationError('携帯番号ではない!', code='mobile_invalid')


          # error_messages={
          #     'name': {
          #         'required': 'お名前を入力してください',
          #         'max_length': '20文字以内入力してください'
          #     },
          #     'mobile': {
          #         'max_length': '20文字以内入力してください',
          #         'required': '番号を入力してください',
          #     },
          #     'course_name': {
          #         'max_length': '50文字以内入力してください',
          #         'required': 'コース名を入力してください'
          #     }
          # }
