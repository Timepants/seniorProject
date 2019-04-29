
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading;
using System.Timers;

using UnityEditor;

using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using Crosstales.FB;

public class MainMenu : MonoBehaviour
{
    private bool inAnim = false;
    public GameObject Main;
    public GameObject ScriptMenu;
    public GameObject ModelMenu;
    public GameObject TrainMenu;
    public GameObject ModelButton;
    public GameObject GUI;
    public GameObject SpdInput;
    public RawImage RoadImage;
    public InputField SpeedInputField;
    private string BasePath = Directory.GetParent(Directory.GetCurrentDirectory()).ToString();
    AsyncOperation asyncLoadLevel;
    string[] imagesToFind = {"jpg", "png"};
    private string roadImageString;
    
    



    public void Awake()
    {
        //keep it processing even when not in focus.
        Application.runInBackground = true;

        //Set desired frame rate as high as possible.
        Application.targetFrameRate = 60;
        if (!DataManager.BackFromTrain && !DataManager.BackFromNN)
        {
            Main.SetActive(true);
            ModelMenu.SetActive(false);
            TrainMenu.SetActive(false);
            RoadImage.enabled = false;
            SpdInput.SetActive(false);
            print("THIS IS BOOL -- " + DataManager.BackFromTrain);
        } else if (!DataManager.BackFromNN)
        {
            print("THIS IS BOOL -- " + DataManager.BackFromTrain);
            Main.SetActive(false);
            ModelMenu.SetActive(false);
            TrainMenu.SetActive(true);
            RoadImage.enabled = true;
            SpdInput.SetActive(false);
            RoadImage.texture = DataManager.RoadTexture;
            TrainMenu.transform.GetChild(0).GetComponent<Text>().text = DataManager.Env_Name;
            DataManager.BackFromTrain = false;

        } else
        {
            Main.SetActive(false);
            ModelMenu.SetActive(true);
            TrainMenu.SetActive(false);
            RoadImage.enabled = false;
            SpdInput.SetActive(false);
            DataManager.BackFromNN = false;
        }


        


    }

    public void OpenModelMenu()
    {
        
        Main.SetActive(false);
        ModelMenu.SetActive(true);

    }

    public void BackToMainMenu()
    {
        ModelMenu.SetActive(false);
        Main.SetActive(true);
        
    }

    public void OpenTrainMenu()
    {
        ModelMenu.SetActive(false);
        TrainMenu.SetActive(true);
    }

    public void BackToModelMenu()
    {
        TrainMenu.SetActive(false);
        ModelMenu.SetActive(true);
        

    }


    public void TestData()
    {
        SceneManager.LoadScene(1);
    }

    

    public void OpenModels()
    {
            string itemPath = BasePath + "\\src\\models\\"; //Maybe to be replaced with something else?
            itemPath = itemPath.Replace(@"/", @"\");   // explorer doesn't like front slashes
            System.Diagnostics.Process.Start("explorer.exe", itemPath);
        
    }

    public void OpenScripts()
    {
        string itemPath = BasePath + "\\src\\";
       // print(itemPath);
        System.Diagnostics.Process.Start("explorer.exe", itemPath);

    }

    public void OpenCFolder()
    {
        string itemPath = "C:\"";
        itemPath = itemPath.Replace(@"/", @"\");   // explorer doesn't like front slashes
        System.Diagnostics.Process.Start("explorer.exe", "/select," + itemPath); 

    }

    public void OnTrain()
    {
        //print(Directory.GetCurrentDirectory());
        string directory = BasePath + "\\src\\models\\";
        //string model = EditorUtility.SaveFilePanel("Save Your model", directory, "Test_Model", "h5");
        string model = FileBrowser.SaveFile("Save your model", directory, "TestModel", "h5");
       // print(model);
        if (!string.IsNullOrEmpty(model))
        {
            OnPrepareData();
            Thread.Sleep(2000);
            TrainModel(model);
            
        }
        else
        {
            //EditorUtility.DisplayDialog("Error!", "Please enter something in the correct format", "Ok");
            
        }

    }

    private void TrainModel(string modelToSave)
    {
        
        string path = BasePath + "\\src\\";
        Process p = new Process();
        ProcessStartInfo startInfo = new ProcessStartInfo();

        //startInfo.FileName = "cmd.exe";
        //startInfo.Arguments = "/c \"python " + path + "\\train.py\" " + modelToSave;

        startInfo.FileName = DataManager.AnacondaLocation;
        startInfo.Arguments = " & python " + BasePath + "\\src\\train.py " + modelToSave + " && exit";
        p.StartInfo = startInfo;
        p.Start();

    }

    public void OnPrepareData()
    {

        string path = BasePath + "\\src\\prepare_data.py";
        Process p = new Process();
        ProcessStartInfo startInfo = new ProcessStartInfo();

        //tartInfo.FileName = "cmd.exe";
        //startInfo.Arguments = "/c \"python " + path + "\\prepare_data.py\"";
        startInfo.FileName = DataManager.AnacondaLocation;
        startInfo.Arguments = " & python " + BasePath + "\\src\\prepare_data.py & exit";
        p.StartInfo = startInfo;
        p.Start();
        //OnTrain();
    }

    public void OpenWebserver()
    {
        var SSID = GetSSID();
        if (SSID == "Curiopo")
        {
            //EditorUtility.DisplayDialog("Error!", "You have to be on the \"Curiopo\" Network", "Ok");
        } else
        {
            OpenURL();
        }

        EventSystem.current.SetSelectedGameObject(null);

    }

    private void OpenURL()
    {
        Application.OpenURL("https://old.reddit.com");
    }

    private string GetSSID()
    {
        var process = new Process
        {
            StartInfo =
                    {
                    FileName = "netsh.exe",
                    Arguments = "wlan show interfaces",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true
                    }
        };
        process.Start();

        var output = process.StandardOutput.ReadToEnd();
        var line = output.Split(new[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries).FirstOrDefault(l => l.Contains("SSID") && !l.Contains("BSSID"));
        if (line == null)
        {
            return string.Empty;
        }
        var ssid = line.Split(new[] { ":" }, StringSplitOptions.RemoveEmptyEntries)[1].TrimStart();
        return ssid;
    }

    public void ChooseModel()
    {
        //string path = Directory.GetParent(Directory.GetCurrentDirectory()).ToString();
        //print(path);
        string modelFolder =  BasePath + "\\src\\models\\";
        //modelFolder = modelFolder.Replace(@"/", @"\");
        //print(modelFolder);
        //string modelpath = EditorUtility.OpenFilePanel("Choose model?? to deploy", modelFolder, "h5");
        string modelpath = FileBrowser.OpenSingleFile("Choose model to deploy", modelFolder, "h5");
        // print("Modelpath here " + modelpath.ToString());
        if (modelpath.ToString() != null && modelpath != modelFolder && modelpath != "")
        {


            DataManager.ModelToRun = modelpath;
            print(modelpath.ToString());
            OnStartPredictServer(modelpath);
            SceneManager.LoadScene(2);
        } else
        {
            //EditorUtility.DisplayDialog("Error", "Please choose a proper file type!", "Ok", "No");
        }
        EventSystem.current.SetSelectedGameObject(null);
    }

    private void OnStartPredictServer(string modelPath)
    {
        
        if (modelPath != null)
        {

            
            Process p = new Process();
            ProcessStartInfo startInfo = new ProcessStartInfo();
            
            startInfo.FileName = DataManager.AnacondaLocation;

            startInfo.Arguments = " & python " + BasePath + "\\src\\predict_server.py " + modelPath + " & exit";
            p.StartInfo.CreateNoWindow = true;
            p.StartInfo = startInfo;
            //print(p.ProcessName);
            p.Start();
            
        }
        else
        {
            //EditorUtility.DisplayDialog("Error", "Please choose a proper file type!","Ok", "No");
        }
         EventSystem.current.SetSelectedGameObject(null);
    }


    string env;
   

    public void StartTrain()
    {
        if (DataManager.Env_Name != null && DataManager.Road != null && DataManager.TrainingSpeed != 0)
        {

            string SceneToLoad = "Scenes/TrainingScenes/" + DataManager.Env_Name;
            //LoadLevel(SceneToLoad);
            SceneManager.LoadSceneAsync(SceneToLoad, LoadSceneMode.Single);

            print("Non error");
        } else
        {
            print("error");
        }


    }

    public IEnumerator LoadLevel(string LevelToLoad)
    {
        print("HIT ME DAD");
        asyncLoadLevel = SceneManager.LoadSceneAsync(LevelToLoad, LoadSceneMode.Single);
        while (!asyncLoadLevel.isDone)
        {
            print("Loading the Scene");
            yield return null;
        }
    }


    public void ChooseEnv()
    {
        //print(Directory.GetCurrentDirectory());
        
        string modelFolder = BasePath + "\\sdsim\\Assets\\Scenes\\TrainingScenes";
        //modelFolder = modelFolder.Replace(@"/", @"\");
        //print(modelFolder);
        //string modelpath = EditorUtility.OpenFilePanel("Choose Scene to Use", modelFolder, "unity");
        string modelpath = FileBrowser.OpenSingleFile("Choose Scene to Use", modelFolder, "unity");

        if (modelpath != null)
        {
            env = modelpath;
            string env_name = Path.GetFileNameWithoutExtension(modelpath);
            DataManager.Env_Name = env_name;
            
            TrainMenu.transform.GetChild(0).GetComponent<Text>().text = env_name;
        }
        else
        {
            //EditorUtility.DisplayDialog("Error", "Please choose a proper file type!", "Ok", "No");
        }


        EventSystem.current.SetSelectedGameObject(null);
    }

    public void ChooseRoad()
    {
        //print(Directory.GetCurrentDirectory());
        
        string modelFolder = BasePath + "\\sdsim\\Assets\\Textures\\roads";
        //print(modelFolder);
        //modelFolder = modelFolder.Replace(@"/", @"\");
        //string modelpath = EditorUtility.OpenFilePanel("Choose Scene to Use", modelFolder, "jpg,png");
        string modelpath = FileBrowser.OpenSingleFile("Choose Scene to Use", modelFolder, imagesToFind);
        print(modelpath);
        if (modelpath != null && modelpath != "")
        {
            DataManager.Road = modelpath;
            RoadImage.enabled = true;
            byte[] fileData = File.ReadAllBytes(modelpath);
            Texture2D tex = new Texture2D(2, 2);
            tex.LoadImage(fileData); //..this will auto-resize the texture dimensions
            DataManager.RoadTexture = tex;
            RoadImage.texture = tex;
            roadImageString = modelpath;
            


        } else if (roadImageString != null)
        {

        }
        else
        {
            //EditorUtility.DisplayDialog("Error", "Please choose a proper file type!", "Ok", "No");
            RoadImage.enabled = false;
        }
        EventSystem.current.SetSelectedGameObject(null);
    }

    public void ChooseSpeed()
    {
        print("Y U no worky");
        SpdInput.SetActive (true);
        EventSystem.current.SetSelectedGameObject(null);

    }
    public void SpdSubmit()
    {
        string speed = SpeedInputField.text;
        int.TryParse(speed, out int Spd);
        //print("Speed-- " + Spd);
        if (Spd > 3)
        {
            Spd = 3;
        }
        else if (Spd < 1)
        {
            Spd = 1;
        }
        DataManager.TrainingSpeed = Spd;
        print(DataManager.TrainingSpeed);
       // print(DataManager.TrainingSpeed);
    }

    public void ChooseAnacondaEnv()
    {
        string anaconda = FileBrowser.OpenSingleFile("Choose Anaconda Shortcut", "C:\\", "lnk");
        //string anaconda = EditorUtility.OpenFilePanel("Choose Anaconda Shortcut", "C:\\", "lnk");
        if (Path.GetExtension(anaconda) != ".lnk")
        {
            print("hullo");
        } else
        {
            DataManager.AnacondaLocation = anaconda;
            print(anaconda);
        }
        print(Path.GetExtension(anaconda));
    }
}
