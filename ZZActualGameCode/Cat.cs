using System.Collections;
using UnityEngine;

public class Cat : SpecialCardBehaviour
{
	private int sacrificeCount;

	public override IEnumerator OnSacrifice()
	{
		sacrificeCount++;
		if (sacrificeCount >= 9)
		{
			yield return new WaitForSeconds(0.25f);
			CardInfo undeadCat = Resources.Load<CardInfo>("Data/Cards/CatUndead");
			yield return StartCoroutine(base.Card.TransformIntoCard(undeadCat));
		}
	}
}
