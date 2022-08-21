using UnityEngine;

[RequireComponent(typeof(Renderer))]
public class SetSortingLayer : MonoBehaviour
{
	[HideInInspector]
	public int sortingLayerIndex;

	public int sortingOrder;
}
