from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content', 'is_completed']
        widgets = {'title': forms.TextInput(attrs={'placeholder': '어떤 일을 할까요?'}),
                   'content': forms.Textarea(attrs={'rows': 5, 'placeholder': '필요한 내용을 적어 주세요 (선택)'})}
        error_messages = {'title': {'required': '할 일 제목을 입력해 주세요.',
                                    'max_length': '제목은 200자 이내로 입력해 주세요.'}}
