using System.Collections;

public class NoPlayQueueOpponent : OpponentAI
{
	public override bool QueueFirstCardBeforePlayer => false;

	public override IEnumerator DoPlayPhase()
	{
		QueueNewCards(doTween: false);
		PlayQueuedCards(4f);
		yield break;
	}
}
