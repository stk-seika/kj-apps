from django.shortcuts import render
from django.views import generic
from django import http
from PIL import Image
import io
import base64

from .forms import ImageForm
from classifier import classifier

# Create your views here.
class ClassifierView(generic.TemplateView):
	template_name = 'classifier/classifier.html'
	classifier_model = classifier.init_model()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = ImageForm()
		context['pred'] = ''
		context['done'] = False
		context['image'] = None
		context['alert'] = None
		self.classifier_model = classifier.init_model()
		return context

	def get(self, request, *args, **kwargs) -> http.HttpResponse:
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form = ImageForm(request.POST, request.FILES)
		if not form.is_valid():
			context = self.get_context_data()

			# Only file size <= 50MB
			if 'File size over' in form.errors['image']:
				context['alert'] = '50MB以下のファイルのみ実行します'
			else:
				context['alert'] = 'ファイルを正常に読み込めませんでした'

			# raise ValueError('invalid form')
			return render(request, self.template_name, context=context)

		image = form.cleaned_data['image']

		# Preview image
		with io.BytesIO() as buf:
			Image.open(image, mode='r').save(buf, format='PNG')
			img = buf.getvalue()
		img = base64.b64encode(img)	# encode the buffer valuess by base64
		img = img.decode("utf-8")	# decode to image
		self.kwargs['image'] = img

		# Generate return values
		preds = classifier.pred(image, model=self.classifier_model)
		top_labels = {}
		value_pre = 1.0
		for n, idx in enumerate(reversed(preds.argsort())):
			value = preds[idx]
			# 最低3つ、スコア0.1以上は表示する
			# 一つ前の半分以下か差が0.005以下なら表示しない
			if (n > 3) and (value < 0.1) and (((value_pre / value) > 2.0) or (value_pre - value < 0.005)):
				break
			top_labels[str(idx)] = value
			value_pre = value
		self.kwargs['pred'] = top_labels
		self.kwargs['done'] = True

		return render(request, self.template_name, context=self.kwargs)