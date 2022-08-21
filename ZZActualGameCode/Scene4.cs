using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Scene4 : SceneSequencer
{
	private int turnNumber;

	[SerializeField]
	private Knife knife;

	[SerializeField]
	private GameObject newEyeEffect;

	[SerializeField]
	private GameObject choices;

	private bool showedKnife;

	private static bool seenDialogue;

	private bool madeChoice;

	private bool choseChild;

	public override IEnumerator Intro()
	{
		if (GameStats.lostEye)
		{
			newEyeEffect.SetActive(value: true);
		}
		yield return new WaitForSeconds(1f);
		ViewManager.instance.FadeIn();
		if (!seenDialogue)
		{
			if (GameStats.lostEye)
			{
				yield return new WaitForSeconds(0.5f);
				TextDisplayer.instance.ShowMessage("How is your new eye?");
				yield return new WaitForSeconds(2.5f);
				TextDisplayer.instance.ShowMessage("Its previous owner won't miss it.", Emotion.Laughter);
				yield return new WaitForSeconds(2f);
			}
			yield return new WaitForSeconds(1f);
			TextDisplayer.instance.ShowMessage("I see your child there behind you.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("It also looks hungry.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("If you beat me now, we will eat.");
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
			TextDisplayer.instance.ShowMessage("I will offer my knife to you again.");
			yield return new WaitForSeconds(1f);
			ViewManager.instance.SwitchToView(View.Default);
			yield return new WaitForSeconds(1f);
			knife.gameObject.SetActive(value: true);
			AudioController.Instance.PlaySound("sacrifice");
			yield return new WaitForSeconds(1f);
			TextDisplayer.instance.ShowMessage("Be careful when you use it.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("You will not have a great hand after.", Emotion.Laughter);
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.Clear();
		}
	}

	public override void OnKnifeUsed()
	{
		StartCoroutine(KnifeSequence());
	}

	private IEnumerator KnifeSequence()
	{
		ViewManager.instance.LockState = ViewLockState.Locked;
		PlayerHand.instance.PlayingLocked = true;
		Cursor3D.instance.InteractionDisabled = true;
		knife.gameObject.SetActive(value: false);
		BodySacrifice selection = BodySacrifice.None;
		yield return StartCoroutine(FirstPersonKnife.instance.ShowKnifeAndWaitForSelection(delegate(BodySacrifice sacrifice)
		{
			selection = sacrifice;
		}, BodySacrifice.Hand));
		if (selection == BodySacrifice.None)
		{
			knife.gameObject.SetActive(value: true);
			AudioController.Instance.PlaySound("placeitem");
			yield return new WaitForEndOfFrame();
			ViewManager.instance.LockState = ViewLockState.Unlocked;
			PlayerHand.instance.PlayingLocked = false;
			Cursor3D.instance.InteractionDisabled = false;
			yield break;
		}
		AudioController.Instance.PlaySound("sacrifice");
		AudioController.Instance.PlaySound("suspense_1");
		ViewManager.instance.FadeOutRed();
		knife.gameObject.SetActive(value: false);
		Object.Destroy(PlayerHand.instance.gameObject);
		yield return new WaitForSeconds(1.5f);
		yield return StartCoroutine(LifeManager.instance.ShowDamageSequence(4, toPlayer: false, isEye: false, isHand: true));
		yield return new WaitForSeconds(1f);
		if (LifeManager.instance.Balance < 5)
		{
			TextDisplayer.instance.ShowMessage("A heavy hand.", Emotion.Laughter);
			CustomCoroutine.WaitThenExecute(2.5f, TextDisplayer.instance.Clear);
			yield return new WaitForSeconds(1f);
			ViewManager.instance.SwitchToView(View.Default);
			ViewManager.instance.LockState = ViewLockState.Unlocked;
		}
		Cursor3D.instance.InteractionDisabled = false;
	}

	public override IEnumerator End(bool playerWon)
	{
		knife.gameObject.SetActive(value: false);
		if (playerWon)
		{
			GameStats.sceneProgress = 4;
			yield return new WaitForSeconds(1f);
			TextDisplayer.instance.ShowMessage("You've done it.");
		}
		else
		{
			TextDisplayer.instance.ShowMessage("You lose.");
		}
		yield return new WaitForSeconds(3f);
		ViewManager.instance.FadeOut();
		if (playerWon)
		{
			TextDisplayer.instance.ShowMessage("It's time to eat.");
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.ShowMessage("Please, choose our menu.");
			yield return new WaitForSeconds(1f);
			choices.SetActive(value: true);
			ViewManager.instance.FadeIn();
			ViewManager.instance.SwitchToView(View.Choices, immediate: true);
			ViewManager.instance.LockState = ViewLockState.Locked;
			yield return new WaitUntil(() => madeChoice);
			ViewManager.instance.FadeOut();
			if (choseChild)
			{
				TextDisplayer.instance.ShowMessage("Very well.");
				yield return new WaitForSeconds(3f);
				TextDisplayer.instance.ShowMessage("Let's eat.");
				yield return new WaitForSeconds(3f);
				Application.Quit();
			}
			else
			{
				TextDisplayer.instance.ShowMessage("How very noble.");
				yield return new WaitForSeconds(3f);
				TextDisplayer.instance.ShowMessage("Much like the stoat.");
				yield return new WaitForSeconds(3f);
				AudioController.Instance.PlaySound("sacrifice");
				yield return new WaitForSeconds(0.4f);
				Application.Quit();
			}
		}
		else
		{
			yield return new WaitForSeconds(1.5f);
			SceneManager.LoadScene(SceneManager.GetActiveScene().name);
		}
	}

	public void MakeChoice(bool child)
	{
		madeChoice = true;
		choseChild = child;
	}
}
