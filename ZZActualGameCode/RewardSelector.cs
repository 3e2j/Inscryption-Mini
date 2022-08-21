using System.Collections;
using System.Collections.Generic;
using Pixelplacement;
using UnityEngine;

public class RewardSelector : MonoBehaviour
{
	public static RewardSelector instance;

	[SerializeField]
	private List<RewardCard> rewards;

	[SerializeField]
	private CardPile pile;

	private RewardCard chosenReward;

	private void Awake()
	{
		instance = this;
	}

	public IEnumerator ChooseReward(List<CardInfo> options)
	{
		ViewManager.instance.LockState = ViewLockState.Locked;
		ViewManager.instance.SwitchToView(View.Choices);
		SetCollidersEnabled(collidersEnabled: false);
		foreach (CardInfo option in options)
		{
			RewardCard card2 = rewards[options.IndexOf(option)];
			card2.gameObject.SetActive(value: true);
			card2.GetComponent<CardAnimationController>().SetFlipped(flipped: true, immediate: true);
			card2.SetInfo(option);
			AudioController.Instance.PlaySoundWithPitch("card", 0.9f + Random.value * 0.2f, 0.2f);
			Vector3 cardPos = card2.transform.position;
			card2.transform.position = card2.transform.position + Vector3.forward * 5f + new Vector3(-0.5f + Random.value * 1f, 0f, 0f);
			Tween.Position(card2.transform, cardPos, 0.3f, 0f, Tween.EaseInOut);
			Tween.Rotate(card2.transform, new Vector3(0f, 0f, Random.value * 1.5f), Space.Self, 0.4f, 0f, Tween.EaseOut);
			yield return new WaitForSeconds(0.2f);
			ParticleSystem.EmissionModule emission = card2.GetComponentInChildren<ParticleSystem>().emission;
			emission.rateOverTime = 0f;
		}
		yield return new WaitForSeconds(0.4f);
		SetCollidersEnabled(collidersEnabled: true);
		chosenReward = null;
		yield return new WaitUntil(() => chosenReward != null);
		yield return new WaitForSeconds(0.5f);
		foreach (RewardCard card in rewards)
		{
			if (card != chosenReward)
			{
				Tween.Position(card.transform, card.transform.position + Vector3.forward * 20f, 0.5f, 0f, Tween.EaseInOut);
				Object.Destroy(card.gameObject, 0.5f);
				yield return new WaitForSeconds(0.1f);
			}
		}
		GameStats.playerDeck.Add(chosenReward.Info);
		ViewManager.instance.LockState = ViewLockState.Unlocked;
	}

	public void OnRewardChosen(RewardCard card)
	{
		chosenReward = card;
		SetCollidersEnabled(collidersEnabled: false);
		card.GetComponent<CardAnimationController>().SetFlipped(flipped: true);
		Tween.Position(card.transform, pile.transform.position + Vector3.up * 1f, 0.5f, 0f, Tween.EaseInOut);
		Tween.Position(card.transform, pile.TopCardPosition, 0.25f, 0.75f, Tween.EaseInOut);
	}

	private void SetCollidersEnabled(bool collidersEnabled)
	{
		foreach (RewardCard reward in rewards)
		{
			reward.GetComponent<Collider>().enabled = collidersEnabled;
		}
	}
}
