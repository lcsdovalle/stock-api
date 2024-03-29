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

            # Handle special field types (e.g., DecimalField, DateTimeField)
            if isinstance(field_value, models.DecimalField):
                field_value = float(field_value)
            elif isinstance(field_value, models.DateTimeField):
                field_value = field_value.strftime("%Y-%m-%d %H:%M:%S")
            # Add more special cases as needed

            data[field_name] = field_value
        return data

    class Meta:
        abstract = True  # Make sure this model is not created in the database
