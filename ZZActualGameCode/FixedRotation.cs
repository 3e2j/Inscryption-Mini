using UnityEngine;

public class FixedRotation : MonoBehaviour
{
	public float rotation;

	private void Update()
	{
		base.transform.rotation = Quaternion.Euler(0f, 0f, rotation);
	}
}
