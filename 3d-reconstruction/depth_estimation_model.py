import pytorch_lightning as pl
from transformers import GLPNImageProcessor, GLPNForDepthEstimation
from transformers import AutoImageProcessor, AutoModelForDepthEstimation
import torch

class DepthEstimationModel(pl.LightningModule):
    def __init__(self):
        super(DepthEstimationModel, self).__init__()
        self.glpn_processor = GLPNImageProcessor.from_pretrained("vinvino02/glpn-nyu")
        self.glpn_model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")
        self.depth_anything_processor = AutoImageProcessor.from_pretrained("depth-anything/Depth-Anything-V2-Large-hf")
        self.depth_anything_model = AutoModelForDepthEstimation.from_pretrained("depth-anything/Depth-Anything-V2-Large-hf")

    def forward(self, img):
        # GLPN Model
        glpn_inputs = self.glpn_processor(images=img, return_tensors="pt")
        with torch.no_grad():
            glpn_depth = self.glpn_model(**glpn_inputs).predicted_depth

        # Depth-Anything Model
        da_inputs = self.depth_anything_processor(images=img, return_tensors="pt")
        with torch.no_grad():
            da_depth = self.depth_anything_model(**da_inputs).predicted_depth

        if glpn_depth.shape != da_depth.shape:
            da_depth = da_depth.unsqueeze(0)
            da_depth = torch.nn.functional.interpolate(da_depth, size=glpn_depth.shape[1:], mode='bilinear', align_corners=False)

        combined_depth = (0.97 * glpn_depth + 0.03 * da_depth)  
        return combined_depth

    def predict(self, img):
        combined_depth = self.forward(img)
        return combined_depth
