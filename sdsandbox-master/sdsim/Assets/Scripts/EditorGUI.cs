using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

public class EditorGUI : EditorWindow
{
    //public GameObject ModelBtn = GameObject;
    [MenuItem("Window/Example")]
    static void Do()
    {
        GetWindow<EditorGUI>();
        
    }

    Object currentObject = null;
    Object selectedObject = null;

   public void OnGUI()
    {
        //ObjectPickerを開く
        if (GUILayout.Button("ShowObjectPicker"))
        {

            int controlID = EditorGUIUtility.GetControlID(FocusType.Passive);
            //CameraのコンポーネントをタッチしているGameObjectを選択する
            EditorGUIUtility.ShowObjectPicker<Text>(null, true, "", controlID);
        }

        string commandName = Event.current.commandName;
        if (commandName == "ObjectSelectorUpdated")
        {
            currentObject = EditorGUIUtility.GetObjectPickerObject();
            Debug.Log(currentObject.ToString());
            //ObjectPickerを開いている間はEditorWindowの再描画が行われないのでRepaintを呼びだす
            Repaint();
           
        }
        else if (commandName == "ObjectSelectorClosed")
        {
            selectedObject = EditorGUIUtility.GetObjectPickerObject();
        }

        EditorGUILayout.ObjectField(currentObject, typeof(Object), true);
        EditorGUILayout.ObjectField(selectedObject, typeof(Object), true);
    }
}
