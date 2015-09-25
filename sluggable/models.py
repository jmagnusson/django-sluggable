from django.utils import six
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template.defaultfilters import slugify


class SluggableModel(models.Model):
    slug = models.SlugField()

    def _get_queryset_for_slug(self):
        """
        Returns a queryset that will be filtered on to check for conflicting
        slugs. This can be overridden for more advanced implementations.
        """
        return self.__class__._default_manager

    def _generate_slug(self):
        """
        Generate a unique slug for this model.
        """
        # Create the keyword arguments for a new queryset based on the values
        # of this model's "unique_together" fields when they include the "slug"
        # field.
        filter_kwargs = {}
        unique_together = self._meta.unique_together

        # Normalize
        if len(unique_together) and \
           isinstance(unique_together[0], six.string_types):
            unique_together = (unique_together, )

        for combo in unique_together:
            if 'slug' in combo:
                for field in combo:
                    if field == 'slug':
                        continue
                    filter_kwargs[field] = getattr(self, field)

        queryset = self._get_queryset_for_slug().filter(**filter_kwargs)
        base_slug = self._generate_base_slug()

        try:
            slug = base_slug
            queryset.get(slug=slug)

            # If no ObjectDoesNotExist exception is thrown, a model with the
            # current slug already exists. We need to create a new unique slug
            # until we can find one that is truly unique.
            i = 1
            while True:
                slug = '%s-%s' % (base_slug, i)
                queryset.get(slug=slug)
                i = i + 1

        except ObjectDoesNotExist:
            # If the object does not exist, there are no naming conflicts and
            # the current value of the "slug" variable is safe to use.
            pass

        return slug[0:50]

    def _generate_base_slug(self):
        """
        Generate the base slug for this model.

        If you'd like to use something other than this model's __unicode__
        representation to generate the base slug, override this method in your
        model class to return a slugified string.
        """
        return slugify(u'%s' % self)

    def save(self, *args, **kwargs):
        self.slug = self._generate_slug()

        return super(SluggableModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
