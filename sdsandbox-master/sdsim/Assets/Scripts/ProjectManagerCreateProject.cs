using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class ProjectManagerCreateProject : EditorWindow
{
    [MenuItem("Example/ShowPopup Example")]
    static void Init()
    {
        ProjectManagerCreateProject window = ScriptableObject.CreateInstance<ProjectManagerCreateProject>();
        window.position = new Rect(Screen.width / 2, Screen.height / 2, 250, 150);
        window.ShowPopup();
    }

    void OnGUI()
    {
        EditorGUILayout.LabelField("This is an example of EditorWindow.ShowPopup", EditorStyles.wordWrappedLabel);
        GUILayout.Space(70);
        if (GUILayout.Button("Agree!")) this.Close();
    }
}
