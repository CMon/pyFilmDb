from django.core.management.base import BaseCommand
from lxml import etree
import django.db.models
import sys

class Command(BaseCommand):
    args = '<modelName> [<export To>]'
    help = 'export a given model (not only movies)'

    def handle(self, *args, **options):
        modelName = None
        exportTo = None
        if len(args) >= 1:
            modelName = str(args[0])

        if len(args) == 2:
            exportTo = str(args[1])
        elif len(args) > 2 or len(args) < 1:
            print "Wrong usage"
            sys.exit(1)

        noModelExported = True
        models = django.db.models.get_models()
        for model in models:
            if modelName == model._meta.object_name:
                self.exportModel(model, exportTo)
                noModelExported = False
                break
        if noModelExported:
            print "No models were exported. Following will be available:"
            for model in models:
                print model._meta.object_name

    def exportModel(self, model, exportFile = None):
        modelName = model._meta.object_name
        if not exportFile:
            exportFile = modelName + ".xml"

        root = etree.Element(modelName)

        # model._meta.object_name holds the name of the model
        for item in model.objects.all():
            entry = etree.SubElement(root, "item")
            for field in item._meta.fields:
                fieldElement = etree.SubElement(entry, field.name)
                value = getattr(item, field.name)
                if value:
                    if isinstance(value, django.db.models.base.Model):
                        # This field is a foreign key, so save the primary key
                        # of the referring object
                        pk_name = value._meta.pk.name
                        pk_value = getattr(value, pk_name)
                        fieldElement.text = str(pk_value)
                    else:
                        fieldElement.text = str(value)

        print "storing into " + exportFile
        modelFile = open(exportFile, "w")
        modelFile.write(etree.tostring(root, pretty_print=True))
        modelFile.close()
