using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StartNN : MonoBehaviour
{
    public MenuHandler menuHandler;

    // Start is called before the first frame update
    void Start()
    {
        menuHandler.NetworkSteering.SetActive(true);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
