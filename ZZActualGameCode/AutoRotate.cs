using UnityEngine;

public class AutoRotate : MonoBehaviour
{
	public float rotateSpeed;

	public bool rotateClockwise;

	public float slowSpeed;

	public bool unscaledTime;

	[SerializeField]
	private bool local;

	[Header("Incremental")]
	public bool byIncrement;

	public float increment;

	[Header("Rotate Between")]
	public bool rotateBetween;

	public float minRotation;

	public float maxRotation;

	private float tickTimer;

	private void Update()
	{
		if (byIncrement)
		{
			tickTimer += ((!unscaledTime) ? Time.deltaTime : Time.unscaledDeltaTime);
			if (tickTimer > rotateSpeed)
			{
				SetZRotation(base.transform.rotation.eulerAngles.z + increment * ((!rotateClockwise) ? (-1f) : 1f));
				tickTimer = 0f;
			}
			return;
		}
		rotateSpeed = Mathf.Max(rotateSpeed - ((!unscaledTime) ? Time.deltaTime : Time.unscaledDeltaTime) * slowSpeed, 0f);
		if (rotateSpeed != 0f)
		{
			SetZRotation(base.transform.rotation.eulerAngles.z + Time.deltaTime * rotateSpeed * ((!rotateClockwise) ? (-1f) : 1f));
		}
		if (rotateBetween)
		{
			if (base.transform.rotation.eulerAngles.z > maxRotation)
			{
				rotateClockwise = false;
			}
			else if (base.transform.rotation.eulerAngles.z < minRotation)
			{
				rotateClockwise = true;
			}
		}
	}

	private void SetZRotation(float zrot)
	{
		if (local)
		{
			base.transform.localRotation = Quaternion.Euler(0f, 0f, zrot);
		}
		else
		{
			base.transform.rotation = Quaternion.Euler(0f, 0f, zrot);
		}
	}
}
