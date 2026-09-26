import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="option",
            name="option_name",
            field=models.CharField(
                db_column="optionName",
                default="",
                max_length=255,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="option",
            name="list",
            field=models.ForeignKey(
                db_column="listID",
                on_delete=models.deletion.CASCADE,
                related_name="options",
                to="lists.list",
            ),
        ),
    ]
