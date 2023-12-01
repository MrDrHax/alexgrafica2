/*
Andrea Alexandra Barrón Córdova A01783126
Alejandro Fernández del Valle Herrera A01024998

Specific conection for fast-automata.
*/

using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

[System.Serializable]
public class ResponseDefault
{
    public Tuple<int, int, int> board; // Board dimensions
    public AgentsModel agents; // Agent models
    public Dictionary<string, object> values; 
    public Dictionary<string, int> summary;
}

[System.Serializable]
public class AgentsModel
{
    public List<AgentInfo> simulated;
    public List<AgentInfo> statics;
    public int total; //Record holder
}