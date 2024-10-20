using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using TMPro;

public class DetectImage : MonoBehaviour
{
    [SerializeField]
    ARTrackedImageManager m_TrackedImageManager;

    [SerializeField] 
    private TextMeshProUGUI imageNameText;

    [SerializeField] 
    private GameObject[] prefabs;

    private Dictionary<string, GameObject> trackedImages = new Dictionary<string, GameObject>();

    void Awake() {
        m_TrackedImageManager = GetComponent<ARTrackedImageManager>();

        // Instantiate prefabs at runtime and deactivate them
        foreach (GameObject prefab in prefabs) {
            GameObject newPrefab = Instantiate(prefab, Vector3.zero, Quaternion.identity);
            newPrefab.name = prefab.name;
            newPrefab.SetActive(false); 
            trackedImages.Add(newPrefab.name, newPrefab);
        }
    }

    void OnEnable() => m_TrackedImageManager.trackedImagesChanged += OnChanged;

    void OnDisable() => m_TrackedImageManager.trackedImagesChanged -= OnChanged;

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
        PlacePrefab(trackedImage.referenceImage.name, trackedImage.transform.position);
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
        }
    }

    void PlacePrefab(string name, Vector3 position) {
        if (trackedImages.ContainsKey(name))
        {
            
            trackedImages[name].SetActive(true);
            trackedImages[name].transform.position = position;

            trackedImages[name].transform.rotation = Quaternion.Euler(0f, 180f, 0f);

        }
    }
}
