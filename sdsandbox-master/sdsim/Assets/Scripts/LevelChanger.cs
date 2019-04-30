using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class LevelChanger : MonoBehaviour
{
    public Animator anim;
    private int levelToLoad;

    // Update is called once per frame
    void Update()
    {
        
    }

    public void FadeToLevel(int Index)
    {
        levelToLoad = Index;
        anim.SetTrigger("FadeOut");
    }

    public void OnFadeComplete()
    {
        SceneManager.LoadScene(levelToLoad);
    }
}
