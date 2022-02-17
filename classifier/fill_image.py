import numpy as np
from PIL import Image

# 短辺を長辺の長さにして正方形にした画像を返す
# ガウシアンノイズ
def fill_image_gaussian(rgb_image):
	# PIL to ndarray
	np_image = np.array(rgb_image)

	# 縦横のサイズ取得
	height, width, _ = np_image.shape
	# 縦横の差
	fill_size = np.abs(height-width)

	# 画像の平均標準偏差取得
	mean = np_image.reshape(-1, 3).mean(axis=0)
	std = np_image.reshape(-1, 3).std(axis=0)
	
	# 縦が小さいとき
	if height < width:
		top_size = fill_size // 2
		bottom_size = fill_size - top_size

		# 端を画像の平均標準偏差から作成
		top = np.random.normal(mean, std, [top_size, width, 3]).astype(np.uint8)
		bottom = np.random.normal(mean, std, [bottom_size, width, 3]).astype(np.uint8)

		# 結合
		np_image = np.concatenate([top, np_image, bottom], axis=0)

	# 横が小さいとき
	elif height > width:
		left_size = fill_size // 2
		right_size = fill_size - left_size
	
		# 端を画像の平均標準偏差から作成
		left = np.random.normal(mean, std, [height, left_size, 3]).astype(np.uint8)
		right = np.random.normal(mean, std, [height, right_size, 3]).astype(np.uint8)

		# 結合
		np_image = np.concatenate([left, np_image, right], axis=1)

	return Image.fromarray(np_image)


# 短辺を長辺の長さにして正方形にした画像を返す
# グラデーション
def fill_image_gradient(rgb_image):
	# PIL to ndarray
	np_image = np.array(rgb_image)

	# 縦横のサイズ取得
	height, width, _ = np_image.shape
	# 縦横の差
	fill_size = np.abs(height-width)

	# 縦が小さいとき
	if height < width:
		top_size = fill_size // 2
		bottom_size = fill_size - top_size

		# 元画像の上下端の色を取得
		top_color = np_image[0]
		bottom_color = np_image[-1]
		# 中間色
		mid_color = (top_color//2 + bottom_color//2)

		# 上下部分を作成
		top = np.linspace(mid_color, top_color, top_size, axis=0, dtype=np.uint8)
		bottom = np.linspace(bottom_color, mid_color, bottom_size, axis=0, dtype=np.uint8)
		# 結合
		np_image = np.concatenate([top, np_image, bottom], axis=0)

	# 横が小さいとき
	elif height > width:
		left_size = fill_size // 2
		right_size = fill_size - left_size
	
		# 元画像の左右端の色を取得
		left_color = np_image[:,0]
		right_color = np_image[:,-1]
		# 中間色
		mid_color = (left_color//2 + right_color//2)

		# 左右部分を作成
		left = np.linspace(mid_color, left_color, left_size, axis=1, dtype=np.uint8)
		right = np.linspace(right_color, mid_color, right_size, axis=1, dtype=np.uint8)

		# 結合
		np_image = np.concatenate([left, np_image, right], axis=1)

	return Image.fromarray(np_image)


# 短辺を長辺の長さにして正方形にした画像を返す
# 端の平均値
def fill_image_mean(rgb_image):
	# PIL to ndarray
	np_image = np.array(rgb_image)

	# 縦横のサイズ取得
	height, width, _ = np_image.shape
	# 縦横の差
	fill_size = np.abs(height-width)

	# 縦が小さいとき
	if height < width:
		top_size = fill_size // 2
		bottom_size = fill_size - top_size

		# 元画像の上下端の色を取得
		top_color = np_image[0]
		bottom_color = np_image[-1]

		# 上下部分を作成
		top = np.empty([top_size, width, 3], dtype=np.uint8)
		top[:,:] = top_color.mean(axis=0)
		bottom = np.empty([bottom_size, width, 3], dtype=np.uint8)
		bottom[:,:] = bottom_color.mean(axis=0)

		# 結合
		np_image = np.concatenate([top, np_image, bottom], axis=0)


	# 横が小さいとき
	elif height > width:
		left_size = fill_size // 2
		right_size = fill_size - left_size
	
		# 元画像の左右端の色を取得
		left_color = np_image[:,0]
		right_color = np_image[:,-1]

		# 左右部分を作成(端の平均)
		left = np.empty([height, left_size, 3], dtype=np.uint8)
		left[:,:] = left_color.mean(axis=0)
		right = np.empty([height, right_size, 3], dtype=np.uint8)
		right[:,:] = right_color.mean(axis=0)

		# 結合
		np_image = np.concatenate([left, np_image, right], axis=1)

	return Image.fromarray(np_image)