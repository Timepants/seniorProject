using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class PopupDialog : MonoBehaviour
{
   public void CallErrorPopup()
    {
        EditorUtility.DisplayDialog("Error", "Please choose a proper file type!", "Ok", "No");
    }
}
