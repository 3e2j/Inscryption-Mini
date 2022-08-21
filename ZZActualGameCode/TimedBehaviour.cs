using UnityEngine;

public class TimedBehaviour : MonoBehaviour
{
	[Header("Timer Parameters")]
	public float originalFrequency;

	public float volatility;

	protected float timer;

	private float frequency;

	protected virtual bool Paused => false;

	public void AddDelay(float delay)
	{
		timer -= delay;
	}

	private void LateUpdate()
	{
		if (!Paused)
		{
			if (frequency <= 0f)
			{
				frequency = originalFrequency;
			}
			timer += Time.deltaTime;
			if (timer > frequency)
			{
				float num = (-0.5f + Random.value) * volatility;
				frequency = originalFrequency + num;
				Reset();
				OnTimerReached();
			}
		}
	}

	protected void Reset()
	{
		timer = 0f;
	}

	protected virtual void OnTimerReached()
	{
	}
}
