from django.core.management.base import BaseCommand, CommandError
from movies.models import Movie, Scene
from lxml import etree

class Command(BaseCommand):
    args = '<xml file>'
    help = 'imports data from xml file (default fixtures.xml)'

    def handle(self, *args, **options):
        fixtureFile = "fixtures.xml"
        if len(args) > 0:
            fixtureFile = args[0]
        self.stdout.write("Reading " + fixtureFile + "\n")

        # read xml file and add movie and scene
        try:
            tree = etree.parse(fixturesFile)
        except:
            raise CommandError("xml parse error of file: " + fixtureFile)

        for element in tree.xpath("/fixtures/entry"):
            # read values
            filename = element.xpath("relpath/text()")
            if len(filename) > 0:
                filename = filename[0]
            hash = element.xpath("hash/text()")
            if len(hash) == 0:
                generateNewEntry("", filename, element)
                return
            else:
                hash = hash[0]

            # check if hash has already a scene entry
            scene = Scene.objects.get(sha256=hash)
            if scene:
                if scene.sceneRelPath != filename:
                    scene.sceneRelPath = filename
                    scene.save()
            else:
                generateNewEntry(hash, filename, element)

    def generateNewEntry(self, hash, filename, element):
        if (hash == ""):
            hash = generateMissingHash()

        movie = Movie(
            title = hash
        )
        movie.save()
        scene = Scene(
            sha256 = hash,
            movie = movie,
            title = os.path.basename(filename),
            animatedImage = element.xpath("animatedImage/text()"),
            stillImage = element.xpath("stillImage/text()"),
            sceneRelPath = filename,
            duration = int(element.xpath("duration/text()"))
        )
        scene.save()
        return
