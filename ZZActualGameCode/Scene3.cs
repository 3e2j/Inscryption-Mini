using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Scene3 : SceneSequencer
{
	private bool playedWarrenMessage;

	private int turnNumber;

	[SerializeField]
	private Knife knife;

	[SerializeField]
	private GameObject eyeCover;

	private bool showedKnife;

	private bool knifeSequence;

	private static bool seenDialogue;

	public override IEnumerator Intro()
	{
		GameStats.lostEye = false;
		yield return new WaitForSeconds(1f);
		ViewManager.instance.FadeIn();
		if (!seenDialogue)
		{
			yield return new WaitForSeconds(1f);
			TextDisplayer.instance.ShowMessage("You told me you were the only survivor of the crash.");
			yield return new WaitForSeconds(4f);
			TextDisplayer.instance.ShowMessage("If that is true, then who is that behind you?");
			CustomCoroutine.WaitThenExecute(3f, TextDisplayer.instance.Clear);
			seenDialogue = true;
		}
	}

	public override IEnumerator PlayerTurnStart()
	{
		turnNumber++;
		if (LifeManager.instance.Balance < 0 && !showedKnife)
		{
			showedKnife = true;
			TextDisplayer.instance.ShowMessage("You are losing.");
			yield return new WaitForSeconds(1f);
			ViewManager.instance.SwitchToView(View.Default);
			yield return new WaitForSeconds(1f);
			knife.gameObject.SetActive(value: true);
			AudioController.Instance.PlaySound("sacrifice");
			yield return new WaitForSeconds(1f);
			TextDisplayer.instance.ShowMessage("But I will allow you to tip the scales.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.Clear();
		}
	}

	public override IEnumerator OpponentTurnStart()
	{
		if (turnNumber == 1)
		{
			yield return new WaitForSeconds(1f);
			TextDisplayer.instance.ShowMessage("You dare lie to me? In my forest?", Emotion.Anger);
			yield return new WaitForSeconds(1f);
			CustomCoroutine.WaitThenExecute(2.5f, TextDisplayer.instance.Clear);
		}
	}

	public override void OnKnifeUsed()
	{
		StartCoroutine(KnifeSequence());
	}

	private IEnumerator KnifeSequence()
	{
		knifeSequence = true;
		ViewManager.instance.LockState = ViewLockState.Locked;
		PlayerHand.instance.PlayingLocked = true;
		Cursor3D.instance.InteractionDisabled = true;
		knife.gameObject.SetActive(value: false);
		BodySacrifice selection = BodySacrifice.None;
		yield return StartCoroutine(FirstPersonKnife.instance.ShowKnifeAndWaitForSelection(delegate(BodySacrifice sacrifice)
		{
			selection = sacrifice;
		}, BodySacrifice.RightEye));
		if (selection == BodySacrifice.None)
		{
			knife.gameObject.SetActive(value: true);
			AudioController.Instance.PlaySound("placeitem");
			yield return new WaitForEndOfFrame();
		}
		else
		{
			AudioController.Instance.PlaySound("sacrifice");
			AudioController.Instance.PlaySound("suspense_1");
			ViewManager.instance.FadeOutRed();
			GameStats.lostEye = true;
			eyeCover.SetActive(value: true);
			yield return new WaitForSeconds(1.5f);
			yield return StartCoroutine(LifeManager.instance.ShowDamageSequence(3, toPlayer: false, isEye: true));
			yield return new WaitForSeconds(1f);
			TextDisplayer.instance.ShowMessage("That ought to even things out.");
			CustomCoroutine.WaitThenExecute(2.5f, TextDisplayer.instance.Clear);
			yield return new WaitForSeconds(1f);
		}
		ViewManager.instance.SwitchToView(View.Default);
		ViewManager.instance.LockState = ViewLockState.Unlocked;
		PlayerHand.instance.PlayingLocked = false;
		Cursor3D.instance.InteractionDisabled = false;
		knifeSequence = false;
	}

	public override IEnumerator End(bool playerWon)
	{
		knife.gameObject.SetActive(value: false);
		if (playerWon)
		{
			GameStats.sceneProgress = 3;
			TextDisplayer.instance.ShowMessage("You win again.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("Choose.");
			yield return StartCoroutine(RewardsSequence());
			TextDisplayer.instance.Clear();
			yield return new WaitForSeconds(1.5f);
			ViewManager.instance.FadeOut();
			yield return new WaitForSeconds(1.5f);
			TextDisplayer.instance.ShowMessage("One more round, human.");
			yield return new WaitForSeconds(1.5f);
		}
		else
		{
			TextDisplayer.instance.ShowMessage("You lose.");
			yield return new WaitForSeconds(3f);
			ViewManager.instance.FadeOut();
		}
		yield return new WaitForSeconds(1.5f);
		SceneManager.LoadScene(SceneManager.GetActiveScene().name);
	}
}
