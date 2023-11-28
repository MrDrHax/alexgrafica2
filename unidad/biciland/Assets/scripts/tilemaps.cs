using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class tilemaps : MonoBehaviour
{
    
    public Vector3 gridStartingPos;
    public Vector2 tileSize;

    public TileGrid grid;

    // roads
    public GameObject roadPrefab;
    public GameObject buildingPrefab;
    public GameObject stoplightPrefab;
    public GameObject destinationPrefab;

    public GameObject parents;

    public void Start(){
        grid = new TileGrid(25, 25);

        string data = "v<<<<<<<<<<<<<<<<<s<<<<<\nvv<<<<<<<<<<<<<<<<s<<<<^\nvv#D#########vv#SS###D^^\nvv###########vv#^^####^^\nvv##########Dvv#^^D###^^\nvv#D#########vv#^^####^^\nvv<<<<<<s<<<<vv#^^####^^\nvv<<<<<<s<<<<vv#^^####^^\nvv####SS#####vv#^^####^^\nvvD##D^^####Dvv#^^####^^\nvv####^^#####vv#^^D###^^\nSS####^^#####vv#^^####^^\nvvs<<<<<<<<<<<<<<<<<<<^^\nvvs<<<<<<<<<<<<<<<<<<<^^\nvv##########vv###^^###^^\nvv>>>>>>>>>>>>>>>>>>>s^^\nvv>>>>>>>>>>>>>>>>>>>s^^\nvv####vv##D##vv#^^####SS\nvv####vv#####vv#^^####^^\nvv####vv#####vv#^^###D^^\nvv###Dvv####Dvv#^^####^^\nvv####vv#####vv#^^####^^\nvv####SS#####SS#^^#D##^^\nv>>>>s>>>>>>s>>>>>>>>>^^\n>>>>>s>>>>>>s>>>>>>>>>>^";

        grid.getFromString(data);
        createFromData();
    }

    public void createFromData(){
        for (int x = 0; x < grid.width; x++){
            for (int y = 0; y < grid.height; y++){
                char c = grid.getTile(x, y);
                switch (c) {
                    case 'v':
                        createRoadTile(x, y);
                        break;
                    case 's':
                        createStoplightTile(x, y);
                        createRoadTile(x, y);
                        break;
                    case 'D':
                        createDestinationTile(x, y);
                        break;
                    case '#':
                        createBuildingTile(x, y);
                        break;
                    case '^':
                        createRoadTile(x, y);
                        break;
                    case 'S':
                        createStoplightTile(x, y);
                        createRoadTile(x, y);
                        break;
                }
            }
        }
    }

    public void createRoadTile(int x, int y){
        var spawned = GameObject.Instantiate(roadPrefab, fromxyToPos(x, y), Quaternion.identity);
        spawned.transform.parent = parents.transform;
    }

    public void createBuildingTile(int x, int y){
        var spawned = GameObject.Instantiate(buildingPrefab, fromxyToPos(x, y), Quaternion.identity);
        spawned.transform.parent = parents.transform;
    }

    public void createStoplightTile(int x, int y){
        var spawned = GameObject.Instantiate(stoplightPrefab, fromxyToPos(x, y), Quaternion.identity);
        spawned.transform.parent = parents.transform;
    }

    public void createDestinationTile(int x, int y){
        var spawned = GameObject.Instantiate(destinationPrefab, fromxyToPos(x, y), Quaternion.identity);
        spawned.transform.parent = parents.transform;
    }

    public Vector3 fromxyToPos(int x, int y){
        return new Vector3(gridStartingPos.x + x * tileSize.x, gridStartingPos.y, gridStartingPos.z + y * tileSize.y);
    }
}


public class TileGrid{
    public int width;
    public int height;
    public char[,] grid;

    public TileGrid(int width, int height){
        this.width = width;
        this.height = height;
        grid = new char[width, height];
    }

    public void setTile(int x, int y, char tile){
        grid[x, y] = tile;
    }

    public char getTile(int x, int y){
        return grid[x, y];
    }

    public void getFromString(string data){
        int x = 0;
        int y = 0;
        foreach(char c in data){
            if(c == '\n'){
                x = 0;
                y++;
            }else{
                grid[x, y] = c;
                x++;
            }
        }
    }
}