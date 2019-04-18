using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class GroundColorChange : MonoBehaviour
{

    public Color color = Color.white;
    // Start is called before the first frame update
    void Start()
    {
        // //Fetch the Renderer from the GameObject
        // Renderer rend = GetComponent<Renderer>();

        // //Set the main Color of the Material to green
        // rend.material.shader = Shader.Find("_Color");
        // rend.material.SetColor("_Color", color);
        // gameObject.GetComponent<Renderer>().material.color = color;
    }

    // Update is called once per frame
    void Update()
    {
        // color.b = Random.Range(0,255);
        // gameObject.GetComponent<Renderer>().material.color = color;
        // print(color);
    }

    public void setColor(Color col){
        gameObject.GetComponent<Renderer>().material.color = col;
    }
}
