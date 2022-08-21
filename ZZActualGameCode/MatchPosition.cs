using UnityEngine;

public class MatchPosition : MonoBehaviour
{
	public Transform target;

	public bool x = true;

	public bool y = true;

	public bool z = true;

	public bool destroyIfTargetNull;

	private void LateUpdate()
	{
		if (target != null)
		{
			Vector3 position = new Vector3((!x) ? base.transform.position.x : target.transform.position.x, (!y) ? base.transform.position.y : target.transform.position.y, (!z) ? base.transform.position.z : target.transform.position.z);
			base.transform.position = position;
		}
		else if (destroyIfTargetNull)
		{
			Object.Destroy(base.gameObject);
		}
	}
}
