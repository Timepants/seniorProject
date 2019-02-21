using System.Collections;
using System.Collections.Generic;
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
}
