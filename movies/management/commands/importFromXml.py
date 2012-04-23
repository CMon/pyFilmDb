from django.core.management.base import BaseCommand, CommandError
from movies.models import Movie, Scene
from lxml import etree
import os

class Command(BaseCommand):
    args = '<xml file>'
    help = 'imports data from xml file (default fixtures.xml)'

    def handle(self, *args, **options):
        fixtureFile = "fixtures.xml"
        if len(args) > 0:
            fixtureFile = str(args[0])
        self.stdout.write("Reading " + fixtureFile + "\n")

        # read xml file and add movie and scene
        try:
            tree = etree.parse(fixtureFile)
        except:
            raise CommandError("xml parse error of file: " + fixtureFile + ". Error: " + e)

        for element in tree.xpath("/fixtures/entry"):
            # read values
            filename = element.xpath("relpath/text()")
            if len(filename) > 0:
                filename = filename[0]
            hash = element.xpath("hash/text()")
            if len(hash) == 0:
                self.generateNewEntry("", filename, element)
                return
            else:
                hash = hash[0]

            # check if hash has already a scene entry
            scenes = Scene.objects.filter(sha256=hash)
            if len(scenes) > 1:
                print "ERROR: found an invalid entry (duplicate hash: " + hash + ")"
            elif len(scenes) == 1:
                scene = scenes[0]
                if scene.sceneRelPath != filename:
                    scene.sceneRelPath = filename
                    scene.save()
            else:
                self.generateNewEntry(hash, filename, element)

    def generateNewEntry(self, hash, filename, element):
        print "Adding: " + hash + " File: " + filename
        if hash == "":
            print " file skipped, because no hash was found"
            return

        movie = Movie(
            title = hash,
            slug = hash
        )
        movie.save()
        scene = Scene(
            sha256 = hash,
            movie = movie,
            title = os.path.basename(filename),
            animatedImage = hash + ".gif",
            stillImage = hash + ".png",
            sceneRelPath = filename,
            duration = int(element.xpath("duration/text()")[0])
        )
        scene.save()
        return
