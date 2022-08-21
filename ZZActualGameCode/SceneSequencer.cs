using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneSequencer : MonoBehaviour
{
	public static SceneSequencer instance;

	[SerializeField]
	private List<CardInfo> cardRewardChoices = new List<CardInfo>();

	private void Start()
	{
		instance = this;
	}

	private void Update()
	{
	}

	public virtual IEnumerator Intro()
	{
		yield return new WaitForSeconds(0.2f);
		ViewManager.instance.FadeIn();
	}

	public virtual IEnumerator End(bool playerWon)
	{
		yield break;
	}

	public virtual IEnumerator PlayerTurnStart()
	{
		yield break;
	}

	public virtual IEnumerator PlayerDuringTurn()
	{
		yield break;
	}

	public virtual IEnumerator OpponentTurnStart()
	{
		yield break;
	}

	public virtual IEnumerator PlayerCombatStart()
	{
		yield break;
	}

	public virtual IEnumerator PlayerCombatEnd()
	{
		yield break;
	}

	public virtual IEnumerator OpponentCombatStart()
	{
		yield break;
	}

	public virtual IEnumerator OpponentCombatEnd()
	{
		yield break;
	}

	public virtual IEnumerator OnCardTransform(Card card)
	{
		if (card.Info.HasTrait(Trait.ProtectsCub) && !GameStats.playedCubMessage)
		{
			GameStats.playedCubMessage = true;
			TextDisplayer.instance.ShowMessage("They grow up so fast.", Emotion.Laughter);
			yield return new WaitForSeconds(3f);
			TextDisplayer.instance.Clear();
		}
	}

	public virtual void OnKnifeUsed()
	{
	}

	protected virtual IEnumerator FadeOutAndReload()
	{
		ViewManager.instance.FadeOut();
		yield return new WaitForSeconds(1.5f);
		SceneManager.LoadScene(SceneManager.GetActiveScene().name);
	}

	protected IEnumerator RewardsSequence()
	{
		ViewManager.instance.LockState = ViewLockState.Locked;
		PlayerHand.instance.PlayingLocked = true;
		yield return StartCoroutine(BoardManager.instance.ClearBoard());
		ViewManager.instance.SwitchToView(View.Choices);
		yield return new WaitForSeconds(0.5f);
		yield return StartCoroutine(RewardSelector.instance.ChooseReward(cardRewardChoices));
	}
}
