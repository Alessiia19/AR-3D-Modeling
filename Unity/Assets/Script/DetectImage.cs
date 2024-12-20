using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using TMPro;

public class DetectImage : MonoBehaviour
{
    [SerializeField]
    ARTrackedImageManager trackedImageManager;  // Manages AR tracked images

    [SerializeField] 
    private TextMeshProUGUI imageNameText;  // UI element to display the name of the detected image

    [SerializeField]
    private GameObject scanCorners;     // UI element indicating the scanning corners

    [SerializeField]
    private GameObject instructionPanel;    // Panel displaying instructions

    [SerializeField] 
    private GameObject[] prefabs;   // Array of prefabs to instantiate for each tracked image

    private Dictionary<string, GameObject> trackedImages = new Dictionary<string, GameObject>();    // Maps image names to their prefabs


    // Called when the script instance is being loaded
    void Awake() {

        // Initialize the tracked image manager
        trackedImageManager = GetComponent<ARTrackedImageManager>();

        // Instantiate prefabs at runtime and deactivate them
        foreach (GameObject prefab in prefabs) {
            GameObject newPrefab = Instantiate(prefab, Vector3.zero, Quaternion.identity);
            newPrefab.name = prefab.name;
            newPrefab.SetActive(false); 
            trackedImages.Add(newPrefab.name, newPrefab);
        }
    }

    // Called when the object becomes enabled and active
    void OnEnable() => trackedImageManager.trackedImagesChanged += OnChanged;

    // Called when the object becomes disabled or inactive
    void OnDisable() => trackedImageManager.trackedImagesChanged -= OnChanged;

    // Called whenever the tracking status changes
    void OnChanged(ARTrackedImagesChangedEventArgs eventArgs)
    {
        // Handle newly added tracked images
        foreach (ARTrackedImage trackedImage in eventArgs.added)
        {
            UpdateImage(trackedImage);
        }

        // Handle newly added tracked images
        foreach (ARTrackedImage trackedImage in eventArgs.updated)
        {
            // Update tracked image if fully tracked
            if (trackedImage.trackingState == UnityEngine.XR.ARSubsystems.TrackingState.Tracking)
            {
                UpdateImage(trackedImage);  
            }

            // Deactivate prefab if tracking is lost
            else if (trackedImage.trackingState == UnityEngine.XR.ARSubsystems.TrackingState.None || 
                     trackedImage.trackingState == UnityEngine.XR.ARSubsystems.TrackingState.Limited)
            {
                trackedImages[trackedImage.referenceImage.name].SetActive(false);
            }
        }

        CheckForTrackedImages();    // Update UI based on tracking status
    }

    // Updates the UI and places the prefab corresponding to the tracked image
    void UpdateImage(ARTrackedImage trackedImage)
    {
        // Display the name of the tracked image in the UI
        imageNameText.text = trackedImage.referenceImage.name;

        // Place the corresponding prefab at the location of the tracked image
        PlacePrefab(trackedImage.referenceImage.name, trackedImage.transform);
    }

    
    // Checks if any images are currently being tracked and updates the UI accordingly
    void CheckForTrackedImages()
    {
        bool anyTracked = false;

        // Check if any tracked images are active
        foreach (var prefab in trackedImages.Values)
        {
            if (prefab.activeSelf)
            {
                anyTracked = true;
                break;
            }
        }

        // No images tracked: update UI to show instructions
        if (!anyTracked)
        {
            imageNameText.text = "No image detected";
            ChangeCornersColor(Color.black);
            instructionPanel.SetActive(true);
        }

        // Images are tracked: update UI to indicate success
        else
        {
            ChangeCornersColor(Color.green);
            instructionPanel.SetActive(false);
        }
    }

    // Place the prefab corresponding to the tracked image name
    void PlacePrefab(string name, Transform parentTransform) {
        if (trackedImages.ContainsKey(name))
        {
            GameObject prefab = trackedImages[name];
            prefab.transform.SetParent(parentTransform, true);  // Attach to the tracked image's transform

            // Activate the prefab
            prefab.SetActive(true);
            prefab.transform.rotation = Quaternion.Euler(0f, 180f, 0f); // Adjust rotation to face the user

        }
    }

    // Change the color of the corner indicators
    private void ChangeCornersColor(Color color)
    {
        var cornerImages = scanCorners.GetComponentsInChildren<UnityEngine.UI.Image>();
        foreach (var image in cornerImages)
        {
            image.color = color;
        }
    }


}
