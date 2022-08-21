using System.Collections;

public class Cub : SpecialCardBehaviour
{
	public override IEnumerator OnSlotTargetedForAttack()
	{
		if (base.Card.Info.HasTrait(Trait.Juvenile))
		{
			Trait typeTrait = ((!base.Card.Info.HasTrait(Trait.Bear)) ? Trait.Wolf : Trait.Bear);
			Card protector = BoardManager.instance.CardsOnBoard.Find((Card x) => x.Info.HasTrait(Trait.ProtectsCub) && x.Info.HasTrait(typeTrait));
			if (protector != null)
			{
				yield return StartCoroutine(BoardManager.instance.SwitchSlotsOfCards(base.Card, protector, 3f));
			}
		}
	}
}
