from django.shortcuts import render
from django.views import generic
from django import http
from django.conf import settings
import json

# from .forms import ImageForm
from network import Network

# Create your views here.
class NetworkView(generic.TemplateView):
	template_name = 'th_pixiv_network/th_pixiv_network.html'
	network = Network()
		
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

	# label to name
	# label ID から名前を返す
	def label_to_name(self, labels, chara_table):
		# intかstrのとき
		if type(labels) == int or type(labels) == str:
			name = ""
			try:
				for k, v in chara_table.items():
					if v['id'] == int(labels):
						name = k
						break
			except ValueError:
				pass
			return name
		# str以外のイテラブルの場合
		elif hasattr(labels, '__iter__'):
			names = []
			for label in labels:
				hit = False
				try:
					for k, v in chara_table.items():
						if v['id'] == int(label):
							names.append(k)
							hit = True
							break
					if not hit:
						names.append("")
				# int()でintに変換出来ないとき
				except ValueError:
					names.append("")
			return names
		# その他のとき
		else:
			return ""

	def post(self, request, *args, **kwargs):
		form = ImageForm(request.POST, request.FILES)
		if not form.is_valid():
			context = self.get_context_data()

			# Only file size <= 50MB is acceptable
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

		# Character name string
		# table_file = 'classifier/static/classifier/chara_table.json'
		table_file = settings.STATIC_ROOT + '/classifier/chara_table.json'
		chara_table = dict()
		with open(table_file, "r") as f:
			chara_table = json.load(f)

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
			top_labels[self.label_to_name(int(idx), chara_table)] = value
			value_pre = value
		self.kwargs['pred'] = top_labels
		self.kwargs['done'] = True

		return render(request, self.template_name, context=self.kwargs)