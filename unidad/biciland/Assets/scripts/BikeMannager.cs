/*
Andrea Alexandra Barrón Córdova A01783126
Alejandro Fernández del Valle Herrera A01024998
*/

using System;
using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using UnityEngine.Networking;

public class BikeMannager : MonoBehaviour
{
    public List<Bike> bikes; // Active bikes

    public GameObject bikePrefab;

    public float timeToDestination;
    public float timeToRotatePercentage;

    public float UpdateInterval; // Time before the new state

    public string baseUrl; 

    private HttpClient client;

    public void Start(){
        client = new HttpClient();
        bikes = new List<Bike>();

        //Corrutines for bike update
        Bike.timeToDestination = timeToDestination;
        Bike.timeToRotate = timeToDestination * timeToRotatePercentage;        

        StartCoroutine(UpdateBikesCoroutine());
    }


    private IEnumerator UpdateBikesCoroutine(){
        //Periodically update bikes
        yield return new WaitForEndOfFrame();
        var requestString = baseUrl + "/state";

        ResponseDefault initialBoardState;

        using (UnityWebRequest webRequest = UnityWebRequest.Get(requestString))
        {
            webRequest.SetRequestHeader("Accept", "application/json");
            webRequest.SetRequestHeader("Content-Type", "application/json");

            yield return webRequest.SendWebRequest();

            if (!(webRequest.result == UnityWebRequest.Result.Success))
            {
                //Check for succesful request
                throw new Exception("Error updating board");
            }

            var content = webRequest.downloadHandler.text;

            initialBoardState = JsonUtility.FromJson<ResponseDefault>(content);
        }

        //Separate stoplights and bikes

        var stoplights = (from agent in initialBoardState.agents.simulated
                          where agent.state.Contains("stoplight")
                          select agent).ToList();

        var bikes = (from agent in initialBoardState.agents.simulated
                     where agent.state.Contains("Car")
                     select agent).ToList();

        if (bikes.Count != 0){
            //update bikes if there are any
            List<AgentInfo> newContext = bikes;
            UpdateBikes(newContext); 
        }

        while (true){
            var startTime = Time.time;

            requestString = baseUrl + "/step"; //Request the next step

            ResponseDefault boardState;

            using (UnityWebRequest webRequest = UnityWebRequest.Post(requestString, ""))
            {
                webRequest.SetRequestHeader("Accept", "application/json");
                webRequest.SetRequestHeader("Content-Type", "application/json");

                yield return webRequest.SendWebRequest();

                if (!(webRequest.result == UnityWebRequest.Result.Success))
                {
                    throw new Exception("Error updating board");
                }

                var content = webRequest.downloadHandler.text;

                boardState = JsonUtility.FromJson<ResponseDefault>(content);
            }

            stoplights = (from agent in boardState.agents.simulated
                          where agent.state.Contains("stoplight")
                          select agent).ToList();
            
            bikes = (from agent in boardState.agents.simulated
                        where agent.state.Contains("Car")
                        select agent).ToList();

            // wait to update next call
            yield return new WaitForSecondsRealtime(Mathf.Clamp(UpdateInterval - (Time.time - startTime), 0, UpdateInterval));

            UpdateBikes(bikes);
        }
    }

    private IEnumerator spawnBike(AgentInfo info){
        // Coroutine for spawning a bike based on agent
        var spawned = GameObject.Instantiate(bikePrefab, tilemaps.fromxyToPos(info.pos.x, info.pos.y), Quaternion.identity);
        spawned.transform.parent = transform;
        var bike = spawned.GetComponent<Bike>();
        yield return new WaitForEndOfFrame();
        bike.info = info;
        bikes.Add(bike);
    }

    public void UpdateBikes(List<AgentInfo> newContext){
        // update bikes
        foreach (AgentInfo info in newContext){
            Bike bike = bikes.Find(b => b.info.id == info.id);
            if (bike == null){
                // create new bike
                StartCoroutine(spawnBike(info));
            } else {
                // update bike
                bike.SetDestination(info.pos);
            }
        }

        // remove bikes that are not in the new context
        List<Bike> bikesToRemove = new List<Bike>();
        foreach (Bike bike in bikes){
            if (!newContext.Exists(info => info.id == bike.info.id)){
                bikesToRemove.Add(bike);
            }
        }

        foreach (Bike bike in bikesToRemove){
            bikes.Remove(bike);
            bike.kill();
        }
    }
}
