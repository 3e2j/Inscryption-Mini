using Pixelplacement;
using UnityEngine;

public class FlickerLight : TimedBehaviour
{
	[SerializeField]
	private float baseIntensity = 4.75f;

	[SerializeField]
	private float intensityChange = 0.5f;

	protected override void OnTimerReached()
	{
		float endValue = baseIntensity + Random.value * intensityChange;
		Tween.LightIntensity(GetComponent<Light>(), endValue, 0.2f, 0f, Tween.EaseInOut);
	}
}
