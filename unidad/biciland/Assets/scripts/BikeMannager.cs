using System;
using System.Collections.Generic;
using System.Collections;
using UnityEngine;
using System.Linq;

public class BikeMannager : MonoBehaviour
{
    public List<Bike> bikes;
    //public List<AgentInfo> stoplights;

    public GameObject bikePrefab;

    public float timeToDestination;
    public float timeToRotatePercentage;

    public float UpdateInterval;

    public void Start(){
        bikes = new List<Bike>();
        //stoplights = new List<AgentInfo>();

        Bike.timeToDestination = timeToDestination;
        Bike.timeToRotate = timeToDestination * timeToRotatePercentage;

        StartCoroutine(UpdateBikesCoroutine());
    }

    private IEnumerator UpdateBikesCoroutine(){
        

        while (true){
            if (dummyData.Count == 0){
                break;
            }
            List<AgentInfo> newContext = dummyData[0];
            dummyData.RemoveAt(0);
            UpdateBikes(newContext);

            // wait to update next call
            yield return new WaitForSecondsRealtime(UpdateInterval);
        }
    }

    private IEnumerator spawnBike(AgentInfo info){
        var spawned = GameObject.Instantiate(bikePrefab, new Vector3(info.pos.x, info.pos.y, 0), Quaternion.identity);
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
