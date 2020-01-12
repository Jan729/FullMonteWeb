# Generated by Django 2.2.6 on 2020-01-12 01:41

from django.db import migrations
from application.models import Optical, Material


def load_properties(application, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.

    #air
    m = Material(material_name='Air')
    m.save()
    o=Optical(property_name="Scattering Coefficient", property_value=1,material=m)
    o.save()
    o=Optical(property_name="Absorbtion Coefficient", property_value=2,material=m)
    o.save()
    o=Optical(property_name="Refractive Index", property_value=3,material=m)
    o.save()
    o=Optical(property_name="Anisotropy", property_value=4,material=m)
    o.save()
    #muscle
    m = Material(material_name='Tumour')
    m.save()
    o=Optical(property_name="Scattering Coefficient", property_value=4,material=m)
    o.save()
    o=Optical(property_name="Absorbtion Coefficient", property_value=3,material=m)
    o.save()
    o=Optical(property_name="Refractive Index", property_value=2,material=m)
    o.save()
    o=Optical(property_name="Anisotropy", property_value=1,material=m)
    o.save()
    #tumor
    m = Material(material_name='Muscle')
    m.save()
    o=Optical(property_name="Scattering Coefficient", property_value=2,material=m)
    o.save()
    o=Optical(property_name="Absorbtion Coefficient", property_value=2,material=m)
    o.save()
    o=Optical(property_name="Refractive Index", property_value=2,material=m)
    o.save()
    o=Optical(property_name="Anisotropy", property_value=2,material=m)
    o.save()

class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial')

    ]

    operations = [
        migrations.RunPython(load_properties)
    ]
