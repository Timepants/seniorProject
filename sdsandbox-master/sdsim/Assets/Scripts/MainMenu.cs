using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEditor;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour
{
    public void TestData()
    {
        SceneManager.LoadScene(1);
    }

    public void OpenModels()
    {
            string itemPath = "../../carStuff/src/carModels/"; //Maybe to be replaced with something else?
            itemPath = itemPath.Replace(@"/", @"\");   // explorer doesn't like front slashes
            System.Diagnostics.Process.Start("explorer.exe", itemPath);
        
    }

    public void OpenScripts()
    {
        string itemPath = "../../carStuff/src/";
        itemPath = itemPath.Replace(@"/", @"\");   // explorer doesn't like front slashes
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
        string title = "Train";
        string message = "type in model name";
        string model = EditorUtility.SaveFilePanel("Save Your model", "../../carStuff/src/carModels/", "My_Model", "h5");
        print(model);
        if (!string.IsNullOrEmpty(model))
        {
            OnPrepareData();
            TrainModel(model);
            
        }
        else
        {
            EditorUtility.DisplayDialog("Error!", "Please enter something in the correct format", "Ok");
        }

    }

    private void TrainModel(string modelToSave)
    {
        
        string path = "../../carStuff/src";
        Process p = new Process();
        ProcessStartInfo startInfo = new ProcessStartInfo();

        startInfo.FileName = "cmd.exe";
        startInfo.Arguments = "/c \"python " + path + "\\train.py\" " + modelToSave;
        p.StartInfo = startInfo;
        p.Start();

    }

    public void OnPrepareData()
    {

        string path = "../../carStuff/src";
        Process p = new Process();
        ProcessStartInfo startInfo = new ProcessStartInfo();

        startInfo.FileName = "cmd.exe";
        startInfo.Arguments = "/c \"python " + path + "\\prepare_data.py\"";
        p.StartInfo = startInfo;
        p.Start();
    }

    public void OnStartPredictServer()
    {
        string modelFolder = "../../carStuff/src/carModels/";

        string modelpath = EditorUtility.OpenFilePanel("Choose model?? to deploy", modelFolder, "h5");
        print(modelpath);

        if (modelpath != null)
        {

            string path = "../../carStuff/src";
            Process p = new Process();
            ProcessStartInfo startInfo = new ProcessStartInfo();

            startInfo.FileName = "cmd.exe";
            startInfo.Arguments = "/c \"python " + path + "\\predict_server.py\" " + modelpath;
            p.StartInfo = startInfo;
            p.Start();
        } else
        {
            EditorUtility.DisplayDialog("Error", "Please choose a proper file type!","Ok", "No");
        }
    }
}
