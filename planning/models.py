from django.db import models
from django.contrib.auth.models import User


class Template(models.Model):
    """
    Template is just a set of fields with some attributes,
    which describe these fields. Because of count of fields
    is different and there attributes are different too, model
    includes dynamic JsonField. Structure below model fields.
    """

    title = models.CharField(max_length=150, verbose_name='Название', default='Untitled')
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    fields = models.JSONField(verbose_name="Поля")

    # fields: [{
    #   field_id: 1,
    #   attrs:{
    #       label: 'Возраст',
    #       check_count: none,
    #       max_val: 100,
    #       min_val: 12,
    #       max_length: none,
    #       options: none,
    #       default: 20,
    #       blank: False,
    #   }
    # },{
    #   field_id: 1,
    #   attrs:{
    #        label: 'Цвет',
    #        check_count: none,
    #        max_val: none,
    #        min_val: none,
    #        max_length: 100,
    #        options: [{
    #           title: 'Синий',
    #           value: 'Blue'
    #        },{
    #           title: 'Зелёный',
    #           value: 'Green'
    #        }],
    #        default: 'Green',
    #        blank: True,
    #        }
    # }
    # ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'


class Plan(models.Model):
    """ Plan cards include JsonField with data of this plan.
        Data in this field is dynamic, so count of field is dynamic too.
        Structure of Json below model fields
    """
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    template = models.ForeignKey(Template, verbose_name="Шаблон", on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True, verbose_name='Дата')
    data = models.JSONField(verbose_name="Данные")

    # data:{
    #   is_important: True(False),
    #   data:{
    #       field_1: val,
    #       ...
    #       field_x: val,
    #   }
    # }

    class Meta:
        verbose_name = 'План'
        verbose_name_plural = 'Планы'


class Field(models.Model):
    """
    Field outputted when the template is creating and when plan is creating.
    """
    title = models.CharField(max_length=150, verbose_name='Название')
    type_of_data = models.ForeignKey('Type', verbose_name='Тип данных', on_delete=models.PROTECT)
    input_name = models.ForeignKey('Input', verbose_name="Имя поля", on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'


class Type(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тип')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Input(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тип')
    css_class = models.CharField(max_length=150, verbose_name="CSS Класс")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ввод'
        verbose_name_plural = 'Вводы'

