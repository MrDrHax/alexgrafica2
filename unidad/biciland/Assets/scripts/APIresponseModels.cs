using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

[System.Serializable]
public class ResponseDefault
{
    public Tuple<int, int, int> board;
    public AgentsModel agents;
    public Dictionary<string, object> values;
    public Dictionary<string, int> summary;
}

[System.Serializable]
public class AgentsModel
{
    public List<AgentInfo> simulated;
    public List<AgentInfo> statics;
    public int total;
}