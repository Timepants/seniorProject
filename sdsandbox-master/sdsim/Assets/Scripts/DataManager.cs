using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class DataManager : MonoBehaviour
{
    static public string ModelToRun;
    static public int TrainingSpeed = 1;
    static public string Env_Name;
    static public string Road = Directory.GetCurrentDirectory() + "\\Assets\\Textures\\roads\\road1.png";
    static public Texture2D RoadTexture;
    public static DataManager instance;
    public static bool BackFromTrain = false;
    public static bool BackFromNN = false;
    public static string AnacondaLocation = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Anaconda3 (64-bit)\\Anaconda Prompt (tensorflow).lnk";

    // Start is called before the first frame update
    void Start()
    {
        // If the instance reference has not been set, yet, 
        if (instance == null)
        {
            // Set this instance as the instance reference.
            instance = this;
        }
        else if (instance != this)
        {
            // If the instance reference has already been set, and this is not the
            // the instance reference, destroy this game object.
            Destroy(gameObject);
        }

        // Do not destroy this object, when we load a new scene.
        DontDestroyOnLoad(gameObject);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
