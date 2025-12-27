from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    time_opening_restoran = models.DateField()
    title = models.TextField()
    contact_admin = models.CharField(max_length=30, verbose_name="Контакт адміністратора")
    opening_time = models.TextField(verbose_name="Час відкриття")
    closing_time = models.TimeField(verbose_name="Час закриття")

    def __str__(self):
        return f"{self.name} - {self.address} - {self.time_opening_restoran} - {self.contact_admin}"
    
    class Meta:
        db_table = 'restaurant'
        ordering = ['name']
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

class Comments(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=300)
    data = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.author} - {self.text} - {self.rating}"
    
    class Meta:
        db_table = 'comments'
        ordering = ['author']
    

class Workers(models.Model):

    ROLE_CHOICES = [
        ("admin", "Адміністрато"),
        ("bartender", "Бармен"),
        ("waiter", "Офіціант"),
    ]


    name = models.CharField(max_length=100)
    data_came_work = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='workers/',blank=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default="waiter")
    rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        default=0, 
        validators= [MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.name} - {self.rating }"


    class Meta:
        db_table = 'workers'
        ordering = ['name']

    
class Menu(models.Model):
    
    STATUS_CHOICES = [
        ("breakfast", "Сніданок"),
        ("lunch", "Обід"),
        ("dinner", "Вечеря"),
    ]

    MENU_CHOICES = [
        ("burgers", "Бургери"),
        ("salads", "Салати"),
        ("soups", "Супи"),
        ("main_dishes", "Основні страви"),
        ("pizza", "Піца"),
        ("pasta", "Паста"),
        ("cold_appetizers", "Холодні закуски"),
        ("hot_appetizers", "Гарячі закуски"),
        ("desserts", "Десерти"),
        ("drinks", "Напої"),
    ]

    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=100, choices=STATUS_CHOICES, default="lunch")
    type2 = models.CharField(max_length=100, choices=MENU_CHOICES, default="main_dishes")
    title = models.CharField(max_length=300)
    photo = models.ImageField(upload_to='menu/', blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        db_table = 'menu'
        ordering = ['name']

#----------------------------------------------------------------------------------------------
class MenuOrder(models.Model):
    
    STATUS_CHOICES = [
        ("breakfast", "Сніданок"),
        ("lunch", "Обід"),
        ("dinner", "Вечеря"),
    ]

    STATUS_CHOICES2 = [
        ("pending", "Очікує підтвердження"),
        ("confirmed", "Підтверджено"),
        ("cancelled", "Скасовано"),
    ]

    MENU_CHOICES = [
        ("burgers", "Бургери"),
        ("salads", "Салати"),
        ("soups", "Супи"),
        ("main_dishes", "Основні страви"),
        ("pizza", "Піца"),
        ("pasta", "Паста"),
        ("cold_appetizers", "Холодні закуски"),
        ("hot_appetizers", "Гарячі закуски"),
        ("desserts", "Десерти"),
        ("drinks", "Напої"),
    ]

    PAY_CHOICES = [
        ("online", "Онлайн"),
        ("upon receipt", "При отримані"),
    ]

    menu_items = models.ForeignKey(Menu, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=100, choices=STATUS_CHOICES, default="lunch")
    type2 = models.CharField(max_length=100, choices=MENU_CHOICES, default="main_dishes")

    customer = models.CharField(max_length=50)
    phone = models.CharField(max_length=25, unique=True)
    street = models.CharField(max_length=100)
    pay = models.CharField(max_length=100, choices=PAY_CHOICES, default="online")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES2, default="pending", verbose_name="Статус")
    


    def __str__(self):
        return f"{self.name}"
    
#----------------------------------------------------------------------------------------------

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Адміністратор"),
        ("user", "Користувач"),
        ("waiter", "Офіціант"),
    ]

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="admin")
    phone = models.CharField(max_length=25, unique=True)
    favorite = models.ManyToManyField("Menu", blank=True, null=True, related_name="favorite_user")

    def __str__(self):
        return self.username

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Очікує підтвердження"),
        ("confirmed", "Підтверджено"),
        ("cancelled", "Скасовано"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="Година та день бронювання столика")
    phone = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)
    guests_count = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(10)], verbose_name="Кількість гостей")


    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.time.strftime('%d.%m.%Y %H:%M')}"
    
    class Meta:
        db_table = 'orders'
        ordering = ['-time']
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"











class Special(models.Model):
    user = models.ForeignKey(CustomUser,null=True, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu,null=True, on_delete=models.CASCADE)


    def __str__(self):
        return  f"{self.user.username} - {self.menu.name}"
    