using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

[System.Serializable]
public class ResponseDefault
{
    /*
    {
  "board": {
    "additionalProp1": [
      0
    ],
    "additionalProp2": [
      0
    ],
    "additionalProp3": [
      0
    ]
  },
  "agents": {
    "simulated": [
      {
        "id": 0,
        "pos": {
          "x": 0,
          "y": 0
        },
        "state": "string",
        "layer": 0
      }
    ],
    "static": [
      {
        "id": 0,
        "pos": {
          "x": 0,
          "y": 0
        },
        "state": "string",
        "layer": 0
      }
    ],
    "total": 0
  },
  "values": {},
  "summary": {
    "additionalProp1": 0,
    "additionalProp2": 0,
    "additionalProp3": 0
  }
}*/
    public Tuple<int, int, int> board;
    public AgentsModel agents;
    public Values values;
    public Summary summary;
    
}

[System.Serializable]
class AgentsModel
{
    public List<AgentInfo> simulated;
    public List<AgentInfo> statics;
    public int total;
}