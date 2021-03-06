from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from geonode.api.resourcebase_api import CommonModelApi, CommonMetaApi
from geonode.base.models import ResourceBase, resourcebase_post_save
from geonode.people.models import Profile

from agon_ratings.models import OverallRating

class Analysis(ResourceBase):
    """ Class representing an analysis, it inherits GeoNode's base resource class """
    data = models.TextField()

    def get_absolute_url(self):
        """ Returns the absolute url of this analysis """
        return reverse('analytics.views.analysis_detail', None, [str(self.id)])

    @property
    def class_name(self):
        return self.__class__.__name__

class GeoMondrianRole(models.Model):
    """ Class used to connect users to GeoMondrian roles """
    rolename = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(Profile, related_name="geomondrianrole")

class AnalysisResource(CommonModelApi):
    """ Class to be used in the search API of GeoNode """
    class Meta(CommonMetaApi):
        queryset = Analysis.objects.distinct().order_by('-date')
        resource_name = 'analysis'

def pre_delete_analysis(instance, sender, **kwrargs):
    """ Function called before the deletion of an analysis """
    ct = ContentType.objects.get_for_model(instance)
    OverallRating.objects.filter(
        content_type=ct,
        object_id=instance.id).delete()

signals.pre_delete.connect(pre_delete_analysis, sender=Analysis)
signals.post_save.connect(resourcebase_post_save, sender=Analysis)
