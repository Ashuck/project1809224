from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class TypeSpecies(models.Model):
    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы живых существ на сайте"
    
    title = models.CharField("Название раздела", max_length=64) 
    short_description = models.TextField("Короткое описание")
    description = models.TextField("Описание")
    photo = models.ImageField("Фотография")

    def __str__(self):
        return self.title
    

class HabitatAreas(models.Model):
    class Meta:
        verbose_name = "Район обитания"
        verbose_name_plural = "Районы обитания"
    
    title = models.CharField("Название", max_length=64)
    description = models.TextField("Описание")
    iframe_map = models.TextField("Код карты")

    def __str__(self):
        return self.title


class Squads(models.Model):
    class Meta:
        verbose_name = "Отряд/отдел/порядок"
        verbose_name_plural = "Отряд/отдел/порядок"
    
    title = models.CharField("Название Отрядa/отделa/порядкa", max_length=64)
    international_name = models.CharField("Муждународное название", default="", max_length=64)

    def __str__(self):
        return self.title


class Families(models.Model):
    class Meta:
        verbose_name = "Семейство"
        verbose_name_plural = "Семейства"
    
    title = models.CharField("Название семейства", max_length=64)
    international_name = models.CharField("Муждународное название", default="", max_length=64)

    def __str__(self):
        return self.title


class RedBookSpecies(models.Model):
    class Meta:
        verbose_name = "Вид"
        verbose_name_plural = "Виды, занесенные в красную книгу"
    
    title = models.CharField("Название", max_length=64)
    type = models.ForeignKey(TypeSpecies, models.PROTECT, verbose_name="Тип")
    main_photo = models.ImageField("Фотография", upload_to="SpeciesGallery")
    photo_autor = models.CharField("Автор фото", max_length=100, default="")
    
    international_name = models.CharField("Муждународное название", default="", max_length=120)
    squad = models.ForeignKey(Squads, verbose_name="Отряд/отдел/порядок", on_delete=models.PROTECT, default=None, null=True)
    family = models.ForeignKey(Families, verbose_name="Семейство", on_delete=models.PROTECT, default=None, null=True)

    status = models.TextField("Статус", default="")
    spreading = models.TextField("Распространение", default="")
    pop_count = models.TextField("Численность", default="")
    habitat_features = models.TextField("Особенности обитания", default="")
    limit_features = models.TextField("Лимитирующие факторы", default="")
    protect_step = models.TextField("Принятые меры охраны", default="")
    state_change = models.TextField("Изменение состояния", default="")
    necessary_measures = models.TextField("Необходимые меры охраны", default="")
    sources = models.TextField("Источники", default="")
    autor = models.TextField("Автор", default="")
    additional_info = models.TextField("Дополнительная информация", default="", blank=True)

    actual_date = models.DateField("данные актуальны на", default=datetime.now)

    iframe_map = models.TextField("Код карты")
    habitat_area = models.ManyToManyField(HabitatAreas, verbose_name="Районы обитания", related_name='red_book_species')

    def __str__(self):
        return self.title


class SpeciesGallery(models.Model):
    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Галерея фотографий"

    specie = models.ForeignKey(RedBookSpecies, models.PROTECT, verbose_name="Вид", related_name="gallery")
    photo = models.ImageField("Фотография", upload_to="SpeciesGallery")
    autor = models.CharField("Автор", max_length=100, default="")

    def __str__(self):
        return self.specie.title
    

class UserInfo(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи проекта"
    
    user = models.OneToOneField(User, models.PROTECT, verbose_name="Пользователь", related_name='user_info')

    ROLES = (
        ("admin", "Админ"),
        ("user", "Пользователь")
    )

    role = models.CharField("Роль", max_length=32, choices=ROLES, default="user")

    first_name = models.CharField("Имя", max_length=32)
    second_name = models.CharField("Фамилия", max_length=32)
    email = models.EmailField("E-mail", unique=True)
    favorite_species = models.ManyToManyField(RedBookSpecies, verbose_name="Фавориты из книги", related_name="user_favorities", blank=True)
    avatar = models.ImageField("Фотография", upload_to="UserAvatar", blank=True, null=True, default=None)
    
    def __str__(self):
        return f"{self.first_name} {self.second_name} ({self.user.username})"


class UserGallery(models.Model):
    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Галерея пользовательских фото"
    
    STATUS = (
        ("new", "Новая"),
        ("approved", "Одобрена"),
        ("rejected", "Отклонена"),
    )
    

    specie = models.ForeignKey(RedBookSpecies, models.PROTECT, verbose_name="Вид")
    photo = models.ImageField("Фотография", upload_to="UserGallery")
    status = models.CharField("Статус", max_length=32, choices=STATUS, default="new")
    user = models.ForeignKey(UserInfo, models.PROTECT, verbose_name="Пользователь", related_name='user_gallery')

    def __str__(self):
        return f"{self.specie.title} ({self.specie.type.title})"