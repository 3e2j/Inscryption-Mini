using System.Collections;
using UnityEngine;

public class SacrificeToken : MonoBehaviour
{
	[SerializeField]
	private Texture satisfiedTexture;

	[SerializeField]
	private Texture notSatisfiedTexture;

	[SerializeField]
	private Renderer coinRenderer;

	private bool isSatisfied;

	public void ResetTexture()
	{
		coinRenderer.material.mainTexture = notSatisfiedTexture;
	}

	public void Show()
	{
		ResetTexture();
		StopAllCoroutines();
		base.gameObject.SetActive(value: true);
		GetComponentInChildren<Animator>().SetTrigger("enter");
	}

	public void Hide()
	{
		if (base.gameObject.activeSelf)
		{
			GetComponentInChildren<Animator>().SetTrigger("exit");
			StartCoroutine(WaitThenDisable());
		}
	}

	private IEnumerator WaitThenDisable()
	{
		yield return new WaitForSeconds(0.25f);
		base.gameObject.SetActive(value: false);
	}

	public void SetSatisfied(bool satisfied)
	{
		if (satisfied && !isSatisfied)
		{
			GetComponentInChildren<Animator>().SetTrigger("flip_satisfied");
		}
		if (satisfied || isSatisfied)
		{
		}
		isSatisfied = satisfied;
	}

	private void KF_SwitchTextureSatisfied()
	{
		coinRenderer.material.mainTexture = satisfiedTexture;
	}
}
