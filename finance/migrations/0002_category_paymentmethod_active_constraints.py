from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="paymentmethod",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name="category",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="paymentmethod",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("user", "name", "kind"),
                name="unique_category_per_user_kind",
            ),
        ),
        migrations.AddConstraint(
            model_name="paymentmethod",
            constraint=models.UniqueConstraint(
                fields=("user", "name"),
                name="unique_payment_method_per_user",
            ),
        ),
    ]
