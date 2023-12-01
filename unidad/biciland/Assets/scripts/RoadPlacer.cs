/*
Andrea Alexandra Barrón Córdova A01783126
Alejandro Fernández del Valle Herrera A01024998

Code used to load the appropriate road prefab based on the given direction
*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class RoadPlacer
{
    public static void loadAndPlace(char direction, Transform parent, Vector3 position){
        GameObject roadPrefab;
        switch (direction){
            case '^':
                roadPrefab = Resources.Load("road_top") as GameObject;
                break;
            case '<':
                roadPrefab = Resources.Load("road_left") as GameObject;
                break;
            case '>':
                roadPrefab = Resources.Load("road_right") as GameObject;
                break;
            case 'v':
                roadPrefab = Resources.Load("road_down") as GameObject;
                break;
            case 's':
                roadPrefab = Resources.Load("stoplight2") as GameObject;
                break;
            case 'S':
                roadPrefab = Resources.Load("stoplight1") as GameObject;
                break;
            default:
                roadPrefab = Resources.Load("road_top") as GameObject;
                break;
        }

        //Instantiate the roads
        var placed = GameObject.Instantiate(roadPrefab, position, Quaternion.identity);
        placed.transform.parent = parent;
        placed.transform.name = position.ToString();
    }
}
