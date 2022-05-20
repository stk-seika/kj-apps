from telnetlib import GA
from django.conf import settings
import json
import numpy as np

class Network():
    # グラフ初期化
    def __init__(self, height='600px', width='600px') -> None:
        self.weights = self.__get_weights()
        self.height = height
        self.width = width
        self.threshold = 0.1

        # ノード定義
        self.nodes = [dict() for i in range(len(self.weights))]
        # ノード初期化
        self.init_nodes()

        # エッジ定義
        self.edges = [dict() for i in range(len(self.weights)*len(self.weights))]
        # エッジ初期化
        self.init_edges(self.weights)

    # ラベルファイル読み込み
    def __load_labels(self):
        label_path = settings.STATIC_ROOT + '/th_pixiv_network/labels.json'
        # label_path = './data/labels.json'

        labels = dict()
        with open(label_path, 'r') as f:
            labels = json.load(f)

        # キャララベルが無いデータは落とす
        labels = dict(filter(lambda item: item[1] != [], labels.items()))
        
        return list(labels.values())

    # weights取得
    def __get_weights(self):
        list_labels = self.__load_labels()

        # クラスのラベル最小値最大値
        label_min = len(list_labels)
        label_max = 1
        for labels in list_labels:
            for l in labels:
                if l > label_max:
                    label_max = l
                if l < label_min:
                    label_min = l
        num_classes = label_max - label_min + 1

        # 同時に描かれているイラスト数, 対角成分はキャラのイラスト総数
        mat_charas = np.zeros([num_classes, num_classes], dtype=int)
        for labels in list_labels:
            for l in labels:
                for m in labels:
                    mat_charas[l-1][m-1] += 1

        # 2キャラ以上描かれているイラストのキャラ別割合
        weights = mat_charas.copy().astype(float)
        for l, chara in enumerate(weights):
            chara /= (chara.sum() - chara[l])
            chara[l] = 0.0

        return weights

    # ノードの初期設定
    def init_nodes(self):
        # ノードを画像に
        for i, node in enumerate(self.nodes):
            node['id'] = i+1
            node['label'] = i+1
            # node['title'] = str(self.label_to_name(node['label']))
            node['title'] = str(node['label'])
            node['shape'] = 'image'
            node['image'] = settings.STATIC_ROOT + f'/th_pixiv_network/image/node_{i+1}.gif'
            node['borderWidth'] = 0     # 透過画像なので境界のマージンをなくす
        return 

    # 表示するノードの設定
    def set_visible_node(self, node_idx):
        # 非表示
        for node in self.nodes:
            node['hidden'] = True
            node['physics'] = False
        # 表示
        for idx in node_idx:
            node = self.nodes[idx]
            node['hidden'] = False
            node['physics'] = True
        
        return

    # エッジ初期化設定
    def init_edges(self, weights):
        weighted_edges = []
        for l, chara in enumerate(weights):
            for c, weight in enumerate(chara):
                weighted_edges.append((l, c, weight))
        
        for i, edge in enumerate(self.edges):
            edge['id'] = i
            edge['from'] = weighted_edges[i][0]
            edge['to'] = weighted_edges[i][1]
            edge['width'] = weighted_edges[i][2]
            edge['arrowStrikethrough'] = False
            edge['title'] = edge['width']

        # エッジの閾値設定
        self.set_threshold(self.threshold)

    # 表示するエッジの閾値を設定
    def set_threshold(self, threshold):
        self.threshold = threshold

        for edge in self.edges:
            if abs(edge['width']) < self.threshold:
                edge['value'] = 0
                edge['hidden'] = True
                edge['physics'] = False
            else:
                edge['value'] = abs(edge['width']) * 5.0
                edge['hidden'] = False
                edge['physics'] = True

        return

    # # 描画
    # def draw(self):
    #     self.net.repulsion()
    #     self.net.show('test.html')