from io import BytesIO

import qrcode
from qrcode.image.svg import SvgImage

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, DetailView, ListView

from reportlab.lib.pagesizes import A6
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .forms import AnnotationForm
from .models import Annotation


def build_qr_svg(payload: str) -> str:
	qr = qrcode.QRCode(
		error_correction=qrcode.constants.ERROR_CORRECT_M,
		box_size=8,
		border=2,
	)
	qr.add_data(payload)
	qr.make(fit=True)

	buffer = BytesIO()
	qr.make_image(image_factory=SvgImage).save(buffer)
	return mark_safe(buffer.getvalue().decode('utf-8'))


def build_qr_svg_bytes(payload: str) -> bytes:
	qr = qrcode.QRCode(
		error_correction=qrcode.constants.ERROR_CORRECT_M,
		box_size=8,
		border=2,
	)
	qr.add_data(payload)
	qr.make(fit=True)

	buffer = BytesIO()
	qr.make_image(image_factory=SvgImage).save(buffer)
	return buffer.getvalue()


def build_qr_pdf_bytes(payload: str, title: str, instruction: str, audio_url: str | None, image_url: str | None) -> bytes:
	qr = qrcode.QRCode(
		error_correction=qrcode.constants.ERROR_CORRECT_M,
		box_size=8,
		border=2,
	)
	qr.add_data(payload)
	qr.make(fit=True)
	image = qr.make_image(fill_color='black', back_color='white').convert('RGB')
	image_reader = ImageReader(image)

	buffer = BytesIO()
	page_width, page_height = A6
	document = canvas.Canvas(buffer, pagesize=A6)

	document.setTitle(f'Annotation {payload}')
	document.setFont('Helvetica-Bold', 14)
	document.drawString(24, page_height - 32, title)
	document.setFont('Helvetica', 9)
	document.drawString(24, page_height - 46, f'Asset ID: {payload}')

	qr_side = 150
	document.drawImage(image_reader, 24, page_height - 220, width=qr_side, height=qr_side, preserveAspectRatio=True, mask='auto')

	text_y = page_height - 240
	document.setFont('Helvetica-Bold', 9)
	document.drawString(24, text_y, 'Instruction')
	document.setFont('Helvetica', 9)
	text_y -= 12
	for line in wrap_text(instruction, 38):
		document.drawString(24, text_y, line)
		text_y -= 11

	if audio_url:
		text_y -= 4
		document.setFont('Helvetica-Bold', 9)
		document.drawString(24, text_y, 'Audio')
		document.setFont('Helvetica', 9)
		text_y -= 12
		for line in wrap_text(audio_url, 38):
			document.drawString(24, text_y, line)
			text_y -= 11

	if image_url:
		text_y -= 4
		document.setFont('Helvetica-Bold', 9)
		document.drawString(24, text_y, 'Image')
		document.setFont('Helvetica', 9)
		text_y -= 12
		for line in wrap_text(image_url, 38):
			document.drawString(24, text_y, line)
			text_y -= 11

	document.showPage()
	document.save()
	return buffer.getvalue()


def wrap_text(text: str, width: int) -> list[str]:
	words = text.split()
	lines: list[str] = []
	current = ''

	for word in words:
		candidate = f'{current} {word}'.strip()
		if len(candidate) <= width:
			current = candidate
		else:
			if current:
				lines.append(current)
			current = word

	if current:
		lines.append(current)

	return lines or ['']


class AnnotationListView(ListView):
	model = Annotation
	template_name = 'website/annotation_list.html'
	context_object_name = 'annotations'

	def get_queryset(self):
		return super().get_queryset().order_by('-created_at')


class AnnotationCreateView(CreateView):
	model = Annotation
	form_class = AnnotationForm
	template_name = 'website/annotation_form.html'


class AnnotationDetailView(DetailView):
	model = Annotation
	template_name = 'website/annotation_detail.html'
	context_object_name = 'annotation'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['qr_svg'] = build_qr_svg(str(self.object.id))
		context['qr_download_url'] = reverse('website:annotation-qr-download', kwargs={'pk': self.object.pk})
		return context


@require_GET
def annotation_qr_download_view(request, pk):
	annotation = get_object_or_404(Annotation, pk=pk)
	response = HttpResponse(
		build_qr_pdf_bytes(
			str(annotation.id),
			annotation.title,
			annotation.instruction,
			request.build_absolute_uri(annotation.audio_file.url) if annotation.audio_file else None,
			request.build_absolute_uri(annotation.image_file.url) if annotation.image_file else None,
		),
		content_type='application/pdf',
	)
	response['Content-Disposition'] = f'attachment; filename="annotation-{annotation.id}.pdf"'
	return response


@require_GET
def annotation_api_view(request, pk):
	annotation = get_object_or_404(Annotation, pk=pk)
	return JsonResponse(
		{
			'id': str(annotation.id),
			'title': annotation.title,
			'instruction': annotation.instruction,
			'created_at': annotation.created_at.isoformat().replace('+00:00', 'Z'),
			'audio_file': request.build_absolute_uri(annotation.audio_file.url) if annotation.audio_file else None,
			'image_file': request.build_absolute_uri(annotation.image_file.url) if annotation.image_file else None,
		}
	)
