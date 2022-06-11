from django.conf import settings
import torch
import torchvision
from torchvision import transforms
from PIL import Image
import timm

from . import fill_image


def init_model():
    # モデルpath
    model_path = settings.STATIC_ROOT + '/classifier/model/model.pth'
    # デバイス
    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # クラス数 = キャラ数 + 1
    num_classes = 177
    # モデル
    model = timm.create_model('efficientnet_b0', pretrained=False, num_classes=num_classes)
    # # 元モデルのfc層入力 -> ラベル数+1出力
    # num_ftrs = model.fc.in_features
    # model.fc = torch.nn.Linear(num_ftrs, num_classes)
    # デバイス適用
    # model = model.to(device)

    # 保存したモデルパラメータの読み込み
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    return model
    
# 予測
def pred(image_path, model=None):
    if model is None:
        model = init_model()

    image_PIL = Image.open(image_path).convert('RGB')
    
    # transform
    # 正方形256*256に変形
    transform = transforms.Compose([
        transforms.Lambda(fill_image.fill_image_mean),
        transforms.Resize((256, 256)),
        # transforms.normalize([], []),
        transforms.ToTensor(),
    ])

    image = transform(image_PIL)
    image = torch.unsqueeze(image, dim=0)

    output = model(image)

    return torch.sigmoid(output[0]).detach().numpy()