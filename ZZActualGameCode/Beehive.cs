using System.Collections;
using UnityEngine;

public class Beehive : SpecialCardBehaviour
{
	public override IEnumerator OnResolveOnBoard()
	{
		yield return new WaitForSeconds(0.15f);
		foreach (CardSlot playerSlot in BoardManager.instance.PlayerSlots)
		{
			CheckForAttraction(playerSlot);
		}
	}

	public override IEnumerator OnOtherCardResolve(Card otherCard)
	{
		yield return new WaitForSeconds(0.15f);
		CheckForAttraction(otherCard.Slot);
	}

	private void CheckForAttraction(CardSlot slot)
	{
		if (!(slot != null) || !(slot.Card != null) || !slot.Card.Info.HasTrait(Trait.LikesHoney))
		{
			return;
		}
		if (BoardManager.instance.SlotIsLeftOfSlot(slot, base.Card.Slot, BoardManager.instance.PlayerSlots))
		{
			CardSlot adjacent = BoardManager.instance.GetAdjacent(base.Card.Slot, adjacentOnLeft: true);
			if (adjacent.Card == null)
			{
				AttractHoneyLover(slot.Card, adjacent);
			}
		}
		else
		{
			CardSlot adjacent2 = BoardManager.instance.GetAdjacent(base.Card.Slot, adjacentOnLeft: false);
			if (adjacent2.Card == null)
			{
				AttractHoneyLover(slot.Card, adjacent2);
			}
		}
	}

	private void AttractHoneyLover(Card honeyLover, CardSlot slot)
	{
		BoardManager.instance.AssignCardToSlot(honeyLover, slot);
		honeyLover.SwitchToAlternatePortrait();
	}
}
