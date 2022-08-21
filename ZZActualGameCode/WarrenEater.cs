using System.Collections;

public class WarrenEater : SpecialCardBehaviour
{
	public override IEnumerator OnPlayFromHand()
	{
		if ((bool)BoardManager.instance.LastSacrificesInfo.Find((CardInfo x) => x.HasTrait(Trait.FeedsStoat)))
		{
			base.Card.Displayer.SetName("Bloated " + base.Card.Info.displayedName);
			base.Card.SwitchToAlternatePortrait();
			base.Card.AddHealth(1);
		}
		yield break;
	}
}
