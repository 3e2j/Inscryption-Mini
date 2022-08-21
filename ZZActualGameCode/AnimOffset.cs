using System.Collections;
using UnityEngine;

public class AnimOffset : MonoBehaviour
{
	public string defaultState;

	public bool adjustSpeed;

	private void Awake()
	{
		Animator component = GetComponent<Animator>();
		if ((bool)component)
		{
			component.Play(defaultState, 0, (float)Random.Range(0, 100) * 0.01f);
			if (adjustSpeed)
			{
				component.speed = (float)Random.Range(90, 100) * 0.01f;
			}
		}
		if ((bool)GetComponent<Animation>())
		{
			StartCoroutine(WaitThenPlay());
		}
	}

	private IEnumerator WaitThenPlay()
	{
		if (!string.IsNullOrEmpty(defaultState))
		{
			GetComponent<Animation>().Play();
			GetComponent<Animation>()[defaultState].time = Random.value * GetComponent<Animation>().clip.length;
		}
		else
		{
			yield return new WaitForSeconds(Random.value * GetComponent<Animation>().clip.length);
			GetComponent<Animation>().Play();
		}
	}
}
