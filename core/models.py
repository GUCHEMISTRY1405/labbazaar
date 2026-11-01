from django.db import models
from django.contrib.auth.models import User


FIELD_CHOICES = [
    ('شیمی', 'شیمی'),
    ('مهندسی پلیمر', 'مهندسی پلیمر'),
    ('مهندسی شیمی', 'مهندسی شیمی'),
    ('شیمی دارویی', 'شیمی دارویی'),
    ('داروسازی', 'داروسازی'),
    ('مهندسی پزشکی', 'مهندسی پزشکی'),
    ('پزشکی', 'پزشکی'),
    ('مهندسی صنایع', 'مهندسی صنایع'),
    ('مهندسی مواد', 'مهندسی مواد'),
]

CHEM_CATEGORIES = [
    ('اسیدها و بازها', 'اسیدها و بازها'),
    ('حلال‌ها', 'حلال‌ها'),
    ('نمک‌ها و مواد معدنی', 'نمک‌ها و مواد معدنی'),
    ('پلیمرها و رزین‌ها', 'پلیمرها و رزین‌ها'),
    ('مواد اولیهٔ دارویی', 'مواد اولیهٔ دارویی'),
    ('افزودنی‌ها و کمک‌فرایندها', 'افزودنی‌ها و کمک‌فرایندها'),
    ('مواد آزمایشگاهی', 'مواد آزمایشگاهی'),
    ('سایر', 'سایر'),
]

STATUS_CHOICES = [
    ('pending', 'در انتظار'),
    ('approved', 'تأیید شده'),
    ('rejected', 'رد شده'),
]


class Profile(models.Model):
    ROLE_CHOICES = [
        ('need', 'شرکت'),
        ('res', 'پژوهشگر'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='res')
    name = models.CharField(max_length=60)
    org = models.CharField(max_length=60, blank=True)
    contact = models.CharField(max_length=120)
    bio = models.TextField(blank=True, max_length=300)
    fields = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class Listing(models.Model):
    KIND_CHOICES = [
        ('need', 'نیاز شرکت'),
        ('res', 'پیشنهاد پژوهشگر'),
        ('chem', 'ماده شیمیایی'),
    ]
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    title = models.CharField(max_length=90)
    org = models.CharField(max_length=60, blank=True)
    extra = models.CharField(max_length=60, blank=True)
    desc = models.TextField(max_length=500, blank=True)
    contact = models.CharField(max_length=120, blank=True)
    fields = models.JSONField(default=list, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    cat = models.CharField(max_length=50, blank=True)
    cas = models.CharField(max_length=20, blank=True)
    grade = models.CharField(max_length=40, blank=True)
    qty = models.CharField(max_length=40, blank=True)
    price = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=30, blank=True)
    ok = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_kind_display()}] {self.title}"