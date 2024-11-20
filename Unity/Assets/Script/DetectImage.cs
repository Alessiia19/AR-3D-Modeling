using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using TMPro;

public class DetectImage : MonoBehaviour
{
    [SerializeField]
    ARTrackedImageManager trackedImageManager;

    [SerializeField] 
    private TextMeshProUGUI imageNameText;

    [SerializeField]
    private GameObject scanCorners;

    [SerializeField]
    private GameObject instructionPanel;

    [SerializeField] 
    private GameObject[] prefabs;

    private Dictionary<string, GameObject> trackedImages = new Dictionary<string, GameObject>();

    void Awake() {
        trackedImageManager = GetComponent<ARTrackedImageManager>();

        // Instantiate prefabs at runtime and deactivate them
        foreach (GameObject prefab in prefabs) {
            GameObject newPrefab = Instantiate(prefab, Vector3.zero, Quaternion.identity);
            newPrefab.name = prefab.name;
            newPrefab.SetActive(false); 
            trackedImages.Add(newPrefab.name, newPrefab);
        }
    }

    void OnEnable() => trackedImageManager.trackedImagesChanged += OnChanged;

    void OnDisable() => trackedImageManager.trackedImagesChanged -= OnChanged;

    void OnChanged(ARTrackedImagesChangedEventArgs eventArgs)
    {
        foreach (ARTrackedImage trackedImage in eventArgs.added)
        {
            UpdateImage(trackedImage);
        }

        foreach (ARTrackedImage trackedImage in eventArgs.updated)
        {
            if (trackedImage.trackingState == UnityEngine.XR.ARSubsystems.TrackingState.Tracking)
            {
                UpdateImage(trackedImage);
            }
            else if (trackedImage.trackingState == UnityEngine.XR.ARSubsystems.TrackingState.None || 
                     trackedImage.trackingState == UnityEngine.XR.ARSubsystems.TrackingState.Limited)
            {
                trackedImages[trackedImage.referenceImage.name].SetActive(false);
            }
        }

        CheckForTrackedImages();
    }

    void UpdateImage(ARTrackedImage trackedImage)
    {
        imageNameText.text = trackedImage.referenceImage.name;
        PlacePrefab(trackedImage.referenceImage.name, trackedImage.transform);
    }

    void CheckForTrackedImages()
    {
        bool anyTracked = false;
        foreach (var prefab in trackedImages.Values)
        {
            if (prefab.activeSelf)
            {
                anyTracked = true;
                break;
            }
        }

        if (!anyTracked)
        {
            imageNameText.text = "No image detected";
            ChangeCornersColor(Color.black);
            instructionPanel.SetActive(true);
        }
        else
        {
            ChangeCornersColor(Color.green);
            instructionPanel.SetActive(false);
        }
    }

    void PlacePrefab(string name, Transform parentTransform) {
        if (trackedImages.ContainsKey(name))
        {
            GameObject prefab = trackedImages[name];
            prefab.transform.SetParent(parentTransform, true);
            prefab.SetActive(true);
            prefab.transform.rotation = Quaternion.Euler(0f, 180f, 0f);

        }
    }

    private void ChangeCornersColor(Color color)
    {
        var cornerImages = scanCorners.GetComponentsInChildren<UnityEngine.UI.Image>();
        foreach (var image in cornerImages)
        {
            image.color = color;
        }
    }


}
