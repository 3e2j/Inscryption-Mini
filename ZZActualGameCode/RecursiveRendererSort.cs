using UnityEngine;

public class RecursiveRendererSort : MonoBehaviour
{
	public int sortOrder;

	private void Start()
	{
		ChangeSortingOrder(sortOrder);
	}

	public void ChangeSortingOrder(int order)
	{
		Renderer[] componentsInChildren = GetComponentsInChildren<Renderer>();
		for (int i = 0; i < componentsInChildren.Length; i++)
		{
			componentsInChildren[i].sortingOrder += order;
		}
	}

	public void SetSortingOrder(int order)
	{
		Renderer[] componentsInChildren = GetComponentsInChildren<Renderer>();
		foreach (Renderer renderer in componentsInChildren)
		{
			renderer.sortingOrder = order;
		}
	}
}
