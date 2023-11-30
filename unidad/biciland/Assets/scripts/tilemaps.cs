using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class tilemaps : MonoBehaviour
{
    
    public Vector3 gridStartingPos;
    public Vector2 tileSize;

    public static tilemaps singleton;

    public TileGrid grid;

    // roads
    public GameObject buildingPrefab;
    public GameObject destinationPrefab;

    public GameObject parents;

    public void Start(){
        singleton = this;

        grid = new TileGrid(25, 25);

        string data = "vv<<<<<<<<<S<<<<<<<<<<<<\nvvv<<<<<<<<S<<<<<<<<<<<<\nvv##D#vv#ss##D#vv#####<^\nvv####vv#^^####vv#####^^\nvv####vv#^^D###vv####D^^\nvv#D##vv#^^####SS#####^^\nvv<<<<vv#^^<<<<<<s<<<<^^\nvv<<<<vv#^^<<<<<<s<<<<^^\nvv####vv#^^####vv#####^^\nvvD###vv#^^####vv####D^^\nvv###Dvv#^^D###vvD####^^\nSS####vv#^^####vv#####^^\nvvs<<<<<<<<<<<<<<<<<<<^^\nvvs<<<<<<<<<<<<<<<<<<<^^\nvv###vv###^^##########^^\nvv>>>>>>>>>>>>>>>>>>>s^^\nvv>>>>>>>>>>>>>>>>>>>s^^\nvv####vv#^^####vv##D##SS\nvvD###vv#^^D###vv#####^^\nvv####vv#^^####vv<<<<<^^\nvv###Dvv#^^####vv#####^^\nvv####vv#^^###Dvv####D^^\nv>####ss#^^####ss#####^^\n>>>>>S>>>>>>>>S>>>>>>^^^\n>>>>>S>>>>>>>>S>>>>>>>^^";

        grid.getFromString(data);
        createFromData();
    }

    public void createFromData(){
        for (int x = 0; x < grid.width; x++){
            for (int y = 0; y < grid.height; y++){
                char c = grid.getTile(x, grid.height - y - 1);
                switch (c) {
                    case '^':
                    case '<':
                    case '>':
                    case 'v':
                        createRoadTile(x, y, c);
                        break;
                    case 's':
                    case 'S':
                        createStoplightTile(x, y, c);
                        break;
                    case 'D':
                        createDestinationTile(x, y);
                        break;
                    case '#':
                        createBuildingTile(x, y);
                        break;
                }
            }
        }
    }

    public void createRoadTile(int x, int y, char c){
        RoadPlacer.loadAndPlace(c, parents.transform, fromxyToPos(x, y));
    }

    public void createBuildingTile(int x, int y){
        var spawned = GameObject.Instantiate(buildingPrefab, fromxyToPos(x, y), Quaternion.identity);
        spawned.transform.parent = parents.transform;
    }

    public void createStoplightTile(int x, int y, char c){
        createRoadTile(x, y, c);
        // TODO add stoplight object
    }

    public void createDestinationTile(int x, int y){
        var spawned = GameObject.Instantiate(destinationPrefab, fromxyToPos(x, y), Quaternion.identity);
        spawned.transform.parent = parents.transform;
    }

    public static Vector3 fromxyToPos(int x, int y){
        return new Vector3(singleton.gridStartingPos.x + x * singleton.tileSize.x, singleton.gridStartingPos.y, singleton.gridStartingPos.z + y * singleton.tileSize.y);
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