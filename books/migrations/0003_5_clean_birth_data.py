# Data migration to clean invalid birth data before migration 0004
from django.db import migrations, connection

def clean_birth_data(apps, schema_editor):
    """پاک کردن مقادیر نامعتبر birth قبل از تغییر فیلد"""
    # استفاده از SQL مستقیم برای پاک کردن مقادیر نامعتبر
    with connection.cursor() as cursor:
        # در SQLite، تمام مقادیر birth که عدد معتبر نیستند را NULL می‌کنیم
        # ابتدا تمام مقادیر blob (bytes) را NULL می‌کنیم
        try:
            cursor.execute("""
                UPDATE books_publisher 
                SET birth = NULL 
                WHERE typeof(birth) = 'blob'
            """)
        except Exception as e:
            # اگر خطا داد، ادامه می‌دهیم
            print(f"Warning: {e}")
        
        # همچنین مقادیری که نمی‌توان آن‌ها را به integer تبدیل کرد را NULL می‌کنیم
        # در SQLite، بهتر است همه مقادیر غیر integer را NULL کنیم
        try:
            # ابتدا بررسی می‌کنیم که آیا فیلد birth وجود دارد
            cursor.execute("PRAGMA table_info(books_publisher)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'birth' in columns:
                # تمام مقادیر غیر integer را NULL می‌کنیم
                cursor.execute("""
                    UPDATE books_publisher 
                    SET birth = NULL 
                    WHERE typeof(birth) != 'integer' 
                    AND typeof(birth) != 'null'
                """)
        except Exception as e:
            print(f"Warning: {e}")


def reverse_clean(apps, schema_editor):
    # عملیات معکوس لازم نیست
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_publisher_address_remove_publisher_website_and_more'),
    ]

    operations = [
        migrations.RunPython(clean_birth_data, reverse_clean),
    ]

