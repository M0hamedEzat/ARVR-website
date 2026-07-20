from django.contrib import admin

from .models import Annotation


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
	list_display = ('title', 'has_audio', 'has_image', 'created_at', 'id')
	list_filter = ('created_at',)
	search_fields = ('title', 'instruction', 'id')
	readonly_fields = ('id', 'created_at')

	def has_audio(self, obj):
		return bool(obj.audio_file)

	has_audio.boolean = True
	has_audio.short_description = 'Audio'

	def has_image(self, obj):
		return bool(obj.image_file)

	has_image.boolean = True
	has_image.short_description = 'Image'
