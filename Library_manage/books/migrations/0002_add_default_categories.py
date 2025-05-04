from django.db import migrations

def add_default_categories(apps, schema_editor):
    Category = apps.get_model('books', 'Category')
    
    default_categories = [
        ('Fiction', 'Works of fiction including novels and short stories'),
        ('Non-Fiction', 'Factual works including biographies, history, and science'),
        ('Mystery', 'Books involving crime, detective work, and suspense'),
        ('Drama', 'Books focusing on character development and emotional themes'),
        ('Romance', 'Books focusing on romantic relationships and love stories'),
        ('Science Fiction', 'Books exploring futuristic concepts and technology'),
        ('Fantasy', 'Books featuring magical elements and imaginary worlds'),
        ('Biography', 'Books about real people\'s lives'),
        ('History', 'Books about historical events and periods'),
        ('Self-Help', 'Books providing personal development and improvement advice'),
        ('Poetry', 'Books containing poems and verse'),
        ('Children', 'Books written for young readers'),
        ('Young Adult', 'Books written for teenage readers'),
        ('Thriller', 'Books with suspenseful and exciting plots'),
        ('Horror', 'Books designed to scare and unsettle readers'),
        ('Comedy', 'Books with humorous content'),
        ('Classic', 'Books of enduring literary significance'),
        ('Contemporary', 'Books from the current era'),
        ('Academic', 'Books for educational and research purposes'),
        ('Reference', 'Books providing information and facts'),
    ]
    
    for name, description in default_categories:
        Category.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )

def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('books', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, remove_default_categories),
    ] 