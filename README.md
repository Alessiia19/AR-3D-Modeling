# AR Analysis of Museum Environments
Augmented reality (AR) application that allows users to visualize 3D reconstructions of paintings through a mobile device (Android). 
The application recognizes specified paintings and displays corresponding 3D models directly in front of the them.

## Technologies Used
- **Unity**: For developing and managing the AR environment.
- **Python**: For generating 3D models from 2D images using deep learning.
- **Blender**: For refining and finalizing the 3D models generated.

## Software Versions Used
The following are the versions of the software, libraries, and packages used during the development of this project:
- **Python**: 3.11.10
- **PyTorch**: Version 2.4.1
- **PyTorch Lightning**: Version 2.4.0
- **Pillow**: Version 10.4.0
- **NumPy**: Version 1.26.4
- **Matplotlib**: Version 3.9.2
- **Open3D**: Version 0.18.0
- **Unity**: Version 2022.3.48f1
- **Blender**: Version 4.2.2
- **Transformers**: Version 4.45.2

> Note: The versions above indicate the exact versions used during the project. Compatibility with other versions has not been tested.

## Unity Setup
1. Install the necessary packages:
   - **AR Foundation**
   - **ARCore XR Plugin**
2. Switch to Android Platform:
	- In **File > Build Settings > Android**, select **Switch Platform**
3. Configure project settings.
   In **File > Build Settings > Player Settings**:
   - **Minimum API level**: 24
   - Uncheck **Auto Graphic API**
   - Make sure you have **IL2CPP** as **Scripting Backend**
   - Enable both **ARMv7** and **ARM64** as **Target Architectures**
   - In **XR Plug-in Management > *Android Icon*** make sure **ARCore** is checked. 

## Run the project

### Python: 3D Reconstruction Workflow
The Python script creates 3D meshes from 2D images using deep learning techniques.
You can run the script using the following:
`python main.py --image_path "path/to/your/image.jpg"`

### Unity: AR Application Setup
1. Import the generated `.obj` file from the Python script output into Unity’s **Assets** folder.
2. Add to the **Reference Image Library** the paintings you want the AR application to recognize.
3. Link the prefab representing the 3D model to the recognized image:
   - Use the XR Origin's inspector to associate the 3D model prefab with the respective image in the scene.
   - Test the application on the mobile device to verify the AR interaction and model placement.
   > Note: Make sure you have selected your device in **File > Build Settings > Run Device**.

## Project Structure

### 3D-Reconstruction (Python)
Contains python scripts responsible for 3D reconstruction:
  - **main.py**: Main script for running the 3D reconstruction process.
  - **image_processing**: Loads and resizes the input image to ensure compatibility with the depth estimation model.
  - **depth_estimation_model.py**: Handles depth map generation using pre-trained models.
  - **depth_processing.py**: Normalizes and post-processes the depth map output from the model to prepare it for point cloud generation.
  - **point_cloud.py**: Converts depth data into a 3D point cloud.
  - **mesh.py**: Generates the 3D mesh from the point cloud.
  - **utils.py**: Contains utility functions.

### Unity
- **/Assets**: Contains all Unity assets, including C# scripts, prefabs and image libraries.
- **/Packages**: Contains Unity packages used in the project, like AR Foundation and ARCore.
- **/ProjectSettings**: Contains project-wide settings such as input configurations, graphics settings, and AR settings necessary for the application to run correctly.

## Additional Notes
- **Blender Refinement**: The generated models can be further refined in Blender for improved quality.

