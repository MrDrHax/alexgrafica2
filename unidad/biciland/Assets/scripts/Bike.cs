using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bike : MonoBehaviour
{
    public AgentInfo info;

    [SerializeField]
    Vector3 destination;
    [SerializeField]
    Vector3 destinationStart;

    [SerializeField]
    Quaternion rotation;
    Quaternion rotationStart;

    public static float timeToDestination;
    public static float timeToRotate;

    [SerializeField]
    float timeToDestinationStart;

    Animator anim;

    private void Start() {
        anim = gameObject.GetComponent<Animator>();
        destination = transform.position;
        rotation = transform.rotation;
    }

    public void Update(){
        // move towards destination only if bike has not arrived yet
        if (Vector3.Distance(transform.position, destination) > 0.001f){
            transform.position = Vector3.Lerp(destinationStart, destination, Mathf.Clamp01((Time.time - timeToDestinationStart) / timeToDestination));
            anim.SetBool("moving", true);
        }
        else{
            anim.SetBool("moving", false);
        }

        // rotate towards destination only if bike is not rotated yet
        if (Quaternion.Angle(transform.rotation, rotation) > 1f){
            var lerpValue = Mathf.Clamp01((Time.time - timeToDestinationStart) / timeToRotate);
            transform.rotation = Quaternion.Lerp(rotationStart, rotation, lerpValue);
        }
    }

    public void SetDestination(Vector2Int pos){
        info.pos = pos;

        destinationStart = transform.position;
        destination = tilemaps.fromxyToPos(pos.x, pos.y);
        rotationStart = transform.rotation;
        rotation = Quaternion.LookRotation(transform.position - destination, Vector3.forward);
        rotation = Quaternion.Euler(0, rotation.eulerAngles.y, 0);
        timeToDestinationStart = Time.time;
    }

    public void kill(){
        // TODO add death animation
        Destroy(gameObject);
    }
}
