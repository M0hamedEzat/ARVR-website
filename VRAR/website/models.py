from io import BytesIO
import uuid

import qrcode
from qrcode.image.svg import SvgImage

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class Annotation(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=200)
	instruction = models.TextField()
	audio_file = models.FileField(upload_to='annotation-audio/', blank=True, null=True)
	image_file = models.ImageField(upload_to='annotation-images/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.title

	def get_absolute_url(self):
		return reverse('website:annotation-detail', kwargs={'pk': self.pk})

	@property
	def qr_svg(self):
		qr = qrcode.QRCode(
			error_correction=qrcode.constants.ERROR_CORRECT_M,
			box_size=8,
			border=2,
		)
		qr.add_data(str(self.id))
		qr.make(fit=True)

		buffer = BytesIO()
		qr.make_image(image_factory=SvgImage).save(buffer)
		return mark_safe(buffer.getvalue().decode('utf-8'))
