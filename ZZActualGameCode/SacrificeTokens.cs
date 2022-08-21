using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SacrificeTokens : MonoBehaviour
{
	[SerializeField]
	private List<SacrificeToken> tokens = new List<SacrificeToken>();

	public IEnumerator ShowTokens(int numTokens)
	{
		if (numTokens >= 2)
		{
			for (int i = 0; i < numTokens; i++)
			{
				tokens[i].Show();
				yield return new WaitForSeconds(0.1f);
			}
		}
	}

	public void SetTokensFlipped(int numFlipped)
	{
		for (int i = 0; i < tokens.Count; i++)
		{
			if (tokens[i].gameObject.activeSelf)
			{
				tokens[i].SetSatisfied(i < numFlipped);
			}
		}
	}

	public void HideTokens()
	{
		for (int i = 0; i < tokens.Count; i++)
		{
			tokens[i].Hide();
		}
	}
}
