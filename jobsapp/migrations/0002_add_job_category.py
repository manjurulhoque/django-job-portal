import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
        ("jobsapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="jobs",
                to="categories.category",
            ),
        ),
        migrations.AddIndex(
            model_name="job",
            index=models.Index(fields=["category"], name="jobsapp_job_category_idx"),
        ),
    ]
