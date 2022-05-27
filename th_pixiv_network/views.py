from django.shortcuts import render
from django.views import generic
from django import http
from django.conf import settings
import json

from .forms import NumberForm
from .network import Network

# Create your views here.
class NetworkView(generic.TemplateView):
	template_name = 'th_pixiv_network/th_pixiv_network.html'
	network = Network()
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		self.network = Network()
 
		context['form'] = NumberForm()
		context['nodes'] = json.dumps(self.network.nodes)
		context['edges'] = json.dumps(self.network.edges)
		context['threshold'] = self.network.threshold

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
		form = NumberForm(request.POST, request.FILES)
		if not form.is_valid():
			context = self.get_context_data()
			return render(request, self.template_name, context=context)

		threshold = form.cleaned_data['threshold']

		# set threshold
		self.network.set_threshold(threshold)
		self.kwargs['nodes'] = json.dumps(self.network.nodes)
		self.kwargs['edges'] = json.dumps(self.network.edges)
		self.kwargs['threshold'] = self.network.threshold

		return render(request, self.template_name, context=self.kwargs)