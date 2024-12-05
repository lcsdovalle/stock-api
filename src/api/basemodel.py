from django.db import models


class BaseModel(models.Model):
    def to_dict(self):
        """
        Returns a dict representation of the model instance, including all fields.
        """
        data = {}
        for field in self._meta.fields:
            field_name = field.name
            field_value = getattr(self, field_name)

            if isinstance(field_value, models.DecimalField):
                field_value = float(field_value)
            elif isinstance(field_value, models.DateTimeField):
                field_value = field_value.strftime("%Y-%m-%d %H:%M:%S")

            data[field_name] = field_value
        return data

    class Meta:
        abstract = True
