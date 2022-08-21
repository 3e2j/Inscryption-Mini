using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OpponentAI : MonoBehaviour
{
	public static OpponentAI instance;

	private Deck deck;

	private List<Card> queuedCards = new List<Card>();

	public AIPlayMode Mode { get; set; }

	public virtual bool QueueFirstCardBeforePlayer => true;

	private void Start()
	{
		instance = this;
		deck = GetComponentInChildren<Deck>();
	}

	public virtual IEnumerator DoPlayPhase()
	{
		if (queuedCards.Count > 0)
		{
			PlayQueuedCards();
			yield return new WaitForSeconds(0.5f);
		}
		QueueNewCards();
	}

	public void QueueNewCards(bool doTween = true)
	{
		List<CardSlot> list = BoardManager.instance.OpponentSlots.FindAll((CardSlot x) => x.Card == null);
		list.RemoveAll((CardSlot x) => queuedCards.Find((Card y) => y.QueuedSlot) == x);
		if (list.Count > 0)
		{
			Card card = deck.DrawCard();
			if (card != null)
			{
				card.SetIsOpponentCard();
				CardSlot cardSlot = PickSlot(list);
				card.transform.position = cardSlot.transform.position + Vector3.forward * 6f + Vector3.up * 2f;
				card.transform.rotation = Quaternion.Euler(130f, 0f, 180f);
				BoardManager.instance.QueueCardForSlot(card, cardSlot, 2.5f, doTween);
				queuedCards.Add(card);
			}
		}
	}

	protected void PlayQueuedCards(float playSpeed = 1f)
	{
		List<Card> list = new List<Card>();
		foreach (Card queuedCard in queuedCards)
		{
			if (queuedCard.QueuedSlot.Card == null)
			{
				BoardManager.instance.AssignCardToSlot(queuedCard, queuedCard.QueuedSlot, playSpeed);
				queuedCard.QueuedSlot = null;
				AudioController.Instance.PlaySoundWithPitch("card", 0.9f + Random.value * 0.2f, 0.15f);
				list.Add(queuedCard);
			}
		}
		queuedCards.Clear();
	}

	private CardSlot PickSlot(List<CardSlot> validSlots)
	{
		CardSlot cardSlot = null;
		List<CardSlot> list = null;
		switch (Mode)
		{
		case AIPlayMode.PickEmpty:
			list = validSlots.FindAll((CardSlot x) => x != null && x.opposingSlot.Card == null);
			break;
		case AIPlayMode.PickStrongest:
			list = validSlots.FindAll((CardSlot x) => x != null && x.opposingSlot.Card != null);
			break;
		case AIPlayMode.PickWeakest:
			list = validSlots.FindAll((CardSlot x) => x != null && x.opposingSlot.Card != null);
			break;
		}
		if (list != null && list.Count > 0)
		{
			cardSlot = list[Random.Range(0, list.Count)];
		}
		if (cardSlot == null)
		{
			cardSlot = validSlots[Random.Range(0, validSlots.Count)];
		}
		return cardSlot;
	}
}
