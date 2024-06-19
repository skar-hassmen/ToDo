from django import forms
from personal_area.models import Tasks
from datetime import datetime


class DateInput(forms.DateInput):
    input_type = 'date'
    

class CreateTaskForm(forms.ModelForm):
    CHOICES_P = [(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий')]
    title = forms.CharField(label='Заголовок задачи',
                            widget=forms.TextInput(attrs={'class': 'form__data'}),
                            max_length=50,
                            required=True)
    description = forms.CharField(label='Описание задачи',
                                  widget=forms.Textarea(attrs={'class': 'form__data form__area__text'}),
                                  required=True)
    date_deadline = forms.DateField(label='Дата дедлайна',
                                    widget=DateInput(attrs={'class': 'form__date width__field'}),
                                    initial=datetime.today().date(),
                                    required=True)
    priority = forms.IntegerField(label='Приоритет',
                                widget=forms.Select(attrs={'class': 'form__data width__field select__field'}, choices=CHOICES_P),
                                required=True,
                                initial=1,
                                min_value=1,
                                max_value=3)  

    def clean_date_deadline(self):
        date_deadline = self.cleaned_data.get('date_deadline')
        if date_deadline < datetime.today().date():
            raise forms.ValidationError("Запрещено вводить прошедшую дату!")
        return date_deadline

    class Meta:
        model = Tasks
        fields = ['title', 'date_deadline', 'description', 'priority']


    

class EditTaskForm(forms.ModelForm):
    CHOICES_S = [(0, 'Не выполнена'), (1, 'Выполнена'), (2, 'Просрочена')]
    CHOICES_P = [(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий')]
    title = forms.CharField(label='Заголовок задачи',
                            widget=forms.TextInput(attrs={'class': 'form__data'}),
                            max_length=50,
                            required=True)
    description = forms.CharField(label='Описание задачи',
                                  widget=forms.Textarea(attrs={'class': 'form__data form__area__text'}),
                                  required=True)
    date_deadline = forms.DateField(label='Дата дедлайна',
                                    widget=DateInput(attrs={'class': 'form__date width__field'}),
                                    initial=datetime.today().date(),
                                    required=True)                         
    status = forms.IntegerField(label='Статус',
                                widget=forms.Select(attrs={'class': 'form__data width__field select__field'}, choices=CHOICES_S),
                                required=True,
                                min_value=0,
                                max_value=2)
    priority = forms.IntegerField(label='Приоритет',
                                widget=forms.Select(attrs={'class': 'form__data width__field select__field'}, choices=CHOICES_P),
                                required=True,
                                min_value=1,
                                max_value=3)  
    
    def clean_date_deadline(self):
            date_deadline = self.cleaned_data.get('date_deadline')
            if date_deadline < datetime.today().date():
                raise forms.ValidationError("Запрещено вводить прошедшую дату!")
            return date_deadline

    class Meta:
        model = Tasks
        fields = ['title', 'date_deadline', 'description', 'status', 'priority']

    
