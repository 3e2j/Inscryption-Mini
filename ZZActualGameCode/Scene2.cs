using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Scene2 : SceneSequencer
{
	private bool playedCatMessage;

	private bool playedRavenMessage;

	private static bool seenDialogue;

	public override IEnumerator Intro()
	{
		yield return new WaitForSeconds(1f);
		ViewManager.instance.FadeIn();
		if (!seenDialogue)
		{
			yield return new WaitForSeconds(1f);
			TextDisplayer.instance.ShowMessage("You look terrible.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("When did you last eat?");
			CustomCoroutine.WaitThenExecute(2.5f, TextDisplayer.instance.Clear);
			seenDialogue = true;
		}
	}

	public override IEnumerator PlayerDuringTurn()
	{
		while (TurnManager.instance.IsPlayerTurn)
		{
			if (!playedCatMessage && (bool)BoardManager.instance.PlayerSlots.Find((CardSlot x) => x.Card != null && x.Card.Info.name == "Cat"))
			{
				playedCatMessage = true;
				TextDisplayer.instance.ShowMessage("The tenacious Cat.");
				yield return new WaitForSeconds(3f);
				TextDisplayer.instance.ShowMessage("It does not die when sacrificed.");
				yield return new WaitForSeconds(4f);
				TextDisplayer.instance.Clear();
			}
			if (!playedRavenMessage && (bool)PlayerHand.instance.CardsInHand.Find((Card x) => x.Info.name == "Raven"))
			{
				playedRavenMessage = true;
				TextDisplayer.instance.ShowMessage("The Raven.");
				yield return new WaitForSeconds(3f);
				TextDisplayer.instance.ShowMessage("It flies over creatures to attack directly.");
				yield return new WaitForSeconds(4f);
				TextDisplayer.instance.Clear();
			}
			yield return new WaitForEndOfFrame();
		}
	}

	public override IEnumerator End(bool playerWon)
	{
		if (playerWon)
		{
			GameStats.sceneProgress = 2;
			TextDisplayer.instance.ShowMessage("You win this round.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("Choose one.");
			yield return StartCoroutine(RewardsSequence());
			TextDisplayer.instance.Clear();
			yield return new WaitForSeconds(1.5f);
			ViewManager.instance.FadeOut();
			yield return new WaitForSeconds(1.5f);
			TextDisplayer.instance.ShowMessage("I will remind you of my promise.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("If you win the final round...");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("I will feed you.");
			yield return new WaitForSeconds(1.5f);
		}
		else
		{
			TextDisplayer.instance.ShowMessage("You lose.");
			ViewManager.instance.FadeOut();
			yield return new WaitForSeconds(3f);
		}
		yield return new WaitForSeconds(1.5f);
		SceneManager.LoadScene(SceneManager.GetActiveScene().name);
	}
}
