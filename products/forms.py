import os
import secrets

from django import forms
from django.conf import settings

from PIL import Image as PIL_Image

from .models import Image


class ImageAdminForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

    def clean_thumb(self):
        thumb = self.cleaned_data.get('thumb')

        if thumb:
            original_filename, original_extension = os.path.splitext(
                thumb.name)

            with PIL_Image.open(thumb) as image:

                original_format = image.format

                aspect_ratio = (1, 1)
                output_size = (500, 500)

                width, height = image.size
                target_width = width
                target_height = int(
                    target_width * (aspect_ratio[1] / aspect_ratio[0]))

                if target_height > height:
                    target_height = height
                    target_width = int(
                        target_height * (aspect_ratio[0] / aspect_ratio[1]))

                left = (width - target_width) / 2
                top = (height - target_height) / 2
                right = (width + target_width) / 2
                bottom = (height + target_height) / 2

                image = image.crop((left, top, right, bottom))
                image = image.resize(output_size, PIL_Image.ANTIALIAS)

                resized_thumb_name = "_".join(
                    [original_filename, secrets.token_urlsafe(6), original_extension])

                output_filename = os.path.join(
                    settings.MEDIA_ROOT, resized_thumb_name)

                image.save(output_filename,
                           format=original_format)

                self.cleaned_data['thumb'] = resized_thumb_name

                thumb = self.cleaned_data.get('thumb')

        return thumb
