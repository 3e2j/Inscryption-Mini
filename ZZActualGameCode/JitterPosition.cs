using UnityEngine;

public class JitterPosition : MonoBehaviour
{
	[SerializeField]
	private bool onlyX;

	[SerializeField]
	private float jitterSpeed = 5f;

	[SerializeField]
	private float jitterFrequency = 0.1f;

	private Vector2 currentJitterValue;

	private Vector2 intendedJitterValue;

	private float jitterTimer;

	private Vector2 originalPos;

	public float amount = 0.05f;

	private void Start()
	{
		originalPos = base.transform.localPosition;
	}

	private void Update()
	{
		jitterTimer += Time.deltaTime;
		if (jitterTimer > jitterFrequency)
		{
			SetNewIntendedValue();
			jitterTimer = 0f;
		}
		currentJitterValue = Vector2.Lerp(currentJitterValue, intendedJitterValue, Time.deltaTime * jitterSpeed);
		ApplyJitter(currentJitterValue);
	}

	public void Stop()
	{
		base.enabled = false;
		base.transform.localPosition = originalPos;
	}

	private void SetNewIntendedValue()
	{
		intendedJitterValue = Random.insideUnitCircle;
	}

	private void ApplyJitter(Vector2 jitterValue)
	{
		base.transform.localPosition = new Vector2(originalPos.x + jitterValue.x * amount, originalPos.y + ((!onlyX) ? (jitterValue.y * amount) : 0f));
	}
}
