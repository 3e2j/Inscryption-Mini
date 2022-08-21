using System.Collections;
using UnityEngine;

public class SpecialCardBehaviour : MonoBehaviour
{
	protected Card Card => GetComponent<Card>();

	public virtual IEnumerator OnPlayFromHand()
	{
		yield break;
	}

	public virtual IEnumerator OnResolveOnBoard()
	{
		yield break;
	}

	public virtual IEnumerator OnOtherCardResolve(Card otherCard)
	{
		yield break;
	}

	public virtual IEnumerator OnSacrifice()
	{
		yield break;
	}

	public virtual IEnumerator OnSlotTargetedForAttack()
	{
		yield break;
	}

	public virtual IEnumerator OnUpkeep()
	{
		yield break;
	}
}
