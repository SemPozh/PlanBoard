from django.test import TestCase
from planning.models import Template, Plan, Field, Type, Input
from django.contrib.auth.models import User


class TemplateModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        fields = {'fields': [{
          'field_id': 1,
          'attrs':{
              'label': 'Возраст',
              'check_count': None,
              'max_val': 100,
              'min_val': 12,
              'max_length': None,
              'options': None,
              'default': 20,
              'blank': False,
              }
          }]
        }
        user = User.objects.create(username='testuser', password='')
        Template.objects.create(title='TestTemplate', user=user, fields=fields)


    def test_title_label(self):
        template = Template.objects.get(id=2)
        field_label = template._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_user_label(self):
        template = Template.objects.get(id=2)
        field_label = template._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Пользователь')

    def test_fields_label(self):
        template = Template.objects.get(id=2)
        field_label = template._meta.get_field('fields').verbose_name
        self.assertEqual(field_label, 'Поля')

    def test_title_max_length(self):
        template = Template.objects.get(id=2)
        field_max_length = template._meta.get_field('title').max_length
        self.assertEqual(field_max_length, 150)


class PlanModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        fields = {'fields': [{
            'field_id': 2,
            'attrs': {
                'label': 'Возраст',
                'check_count': None,
                'max_val': 100,
                'min_val': 12,
                'max_length': None,
                'options': None,
                'default': 20,
                'blank': False,
            }
        }]
        }

        user = User.objects.create(username='testuser2', password='')
        template = Template.objects.create(title='TestTemplate2', user=user, fields=fields)

        data = {
            'data':{
              'is_important': True,
              'data':{
                  'field_1': 1,
                  'field_2': 2,
                  'field_3': 3,
                  'field_4': 4,
              }
            }
        }

        Plan.objects.create(user_id=user.id, template_id=template.id, data=data)

    def test_user_label(self):
        plan = Plan.objects.get(id=1)
        field_label = plan._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'Пользователь')

    def test_template_label(self):
        plan = Plan.objects.get(id=1)
        field_label = plan._meta.get_field('template').verbose_name
        self.assertEqual(field_label, 'Шаблон')

    def test_data_label(self):
        plan = Plan.objects.get(id=1)
        field_label = plan._meta.get_field('data').verbose_name
        self.assertEqual(field_label, 'Данные')

    def test_date_auto_now_add(self):
        plan = Plan.objects.get(id=1)
        field_add = plan._meta.get_field('date').auto_now_add
        self.assertTrue(field_add)


class FieldModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        type_of_data = Type.objects.create(title='String')
        input_name = Input.objects.create(title='TextInput', css_class='Some_css')
        Field.objects.create(title='Обычное поле', type_of_data_id=type_of_data.id, input_name_id=input_name.id)


    def test_field_title_label(self):
        field = Field.objects.get(id=1)
        field_label = field._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_field_title_max_length(self):
        field = Field.objects.get(id=1)
        field_max_length = field._meta.get_field('title').max_length
        self.assertEqual(field_max_length, 150)

    def test_field_type_of_data_label(self):
        field = Field.objects.get(id=1)
        field_label = field._meta.get_field('type_of_data').verbose_name
        self.assertEqual(field_label, 'Тип данных')

    def test_field_input_name_label(self):
        field = Field.objects.get(id=1)
        field_label = field._meta.get_field('input_name').verbose_name
        self.assertEqual(field_label, 'Имя поля')

    def test_type_title_label(self):
        field = Type.objects.get(id=1)
        field_label = field._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Тип')

    def test_type_title_max_length(self):
        field = Type.objects.get(id=1)
        field_label = field._meta.get_field('title').max_length
        self.assertEqual(field_label, 100)

    def test_input_title_label(self):
        field = Input.objects.get(id=1)
        field_label = field._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Тип')

    def test_input_title_max_length(self):
        field = Input.objects.get(id=1)
        field_label = field._meta.get_field('title').max_length
        self.assertEqual(field_label, 100)

    def test_input_css_class_label(self):
        field = Input.objects.get(id=1)
        field_label = field._meta.get_field('css_class').verbose_name
        self.assertEqual(field_label, 'CSS Класс')

    def test_input_css_class_max_length(self):
        field = Input.objects.get(id=1)
        field_label = field._meta.get_field('css_class').max_length
        self.assertEqual(field_label, 150)



