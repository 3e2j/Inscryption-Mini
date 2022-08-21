using UnityEngine;

public class showcasecam : MonoBehaviour
{
	public Transform rotationPoint;

	private void Start()
	{
	}

	private void Update()
	{
		base.transform.RotateAround(rotationPoint.position, Vector3.up, 20f * Time.deltaTime);
	}
}
