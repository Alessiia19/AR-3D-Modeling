import pytorch_lightning as pl
from transformers import GLPNImageProcessor, GLPNForDepthEstimation
from transformers import AutoImageProcessor, AutoModelForDepthEstimation
import torch

# Pytorch Lightning module for depth estimation using two pre-trained models
class DepthEstimationModel(pl.LightningModule):

    # Initializes the models
    def __init__(self):
        super(DepthEstimationModel, self).__init__()

        # Load GLPN model
        self.glpn_processor = GLPNImageProcessor.from_pretrained("vinvino02/glpn-nyu")
        self.glpn_model = GLPNForDepthEstimation.from_pretrained("vinvino02/glpn-nyu")

        # Load Depth-Anything model
        self.depth_anything_processor = AutoImageProcessor.from_pretrained("depth-anything/Depth-Anything-V2-Large-hf")
        self.depth_anything_model = AutoModelForDepthEstimation.from_pretrained("depth-anything/Depth-Anything-V2-Large-hf")

    def forward(self, img):
        # GLPN depth estimation 
        glpn_inputs = self.glpn_processor(images=img, return_tensors="pt")
        with torch.no_grad():
            glpn_depth = self.glpn_model(**glpn_inputs).predicted_depth

        # Depth-Anything depth estimation
        da_inputs = self.depth_anything_processor(images=img, return_tensors="pt")
        with torch.no_grad():
            da_depth = self.depth_anything_model(**da_inputs).predicted_depth

        # Ensure both depth maps have the same shape
        if glpn_depth.shape != da_depth.shape:
            da_depth = da_depth.unsqueeze(0)
            da_depth = torch.nn.functional.interpolate(da_depth, size=glpn_depth.shape[1:], mode='bilinear', align_corners=False)

        # Combine Depth Maps
        # Weighted average of GLPN (97%) and Depth-Anything (3%) outputs
        combined_depth = (0.97 * glpn_depth + 0.03 * da_depth)  
        return combined_depth


    # Runs the forward method to predict the depth map for a given input image
    # Returns the combined depth map as a torch.Tensor
    def predict(self, img):
        combined_depth = self.forward(img)
        return combined_depth
