using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerHand : MonoBehaviour
{
	public static PlayerHand instance;

	private List<Card> cardsInHand = new List<Card>();

	private Deck deck;

	[SerializeField]
	private Transform cardsParent;

	[SerializeField]
	private CardPile pile;

	private bool choosingSlot;

	private Card choosingSlotCard;

	private const float PLACEMENT_X_RANGE = 1.75f;

	public bool PlayingLocked { get; set; }

	public List<Card> CardsInHand => cardsInHand;

	public Deck Deck
	{
		get
		{
			return deck;
		}
		set
		{
			deck = value;
			pile.SpawnCards(deck.CardsInDeck);
		}
	}

	private void Awake()
	{
		instance = this;
	}

	private void Update()
	{
		if (cardsInHand.Count > 0)
		{
			SetCardPositions();
		}
	}

	public IEnumerator Draw()
	{
		yield return StartCoroutine(Draw(null));
	}

	public IEnumerator Draw(CardInfo specificCard)
	{
		Card card2 = null;
		card2 = ((!(specificCard != null)) ? deck.DrawCard() : deck.DrawSpecificCard(specificCard));
		if (card2 != null)
		{
			ParentCardToHand(card2, Vector3.up * 8f + Vector3.right * 5f);
			if (specificCard == null)
			{
				pile.Draw();
				yield return new WaitForSeconds(0.15f);
			}
			cardsInHand.Add(card2);
			OnCardInspected(card2);
			SetCardPositions();
		}
		else
		{
			TextDisplayer.instance.ShowMessage("You're out of cards. Good luck.");
			yield return new WaitForSeconds(3.5f);
			TextDisplayer.instance.Clear();
		}
	}

	public void ParentCardToHand(Card card, Vector3 startPositionOffset)
	{
		card.transform.SetParent(cardsParent);
		card.transform.position = base.transform.position + startPositionOffset;
	}

	public void OnCardInspected(Card card)
	{
		AudioController.Instance.PlaySoundWithPitch("card", 0.9f + Random.value * 0.2f, 0.15f);
		int num = cardsInHand.IndexOf(card);
		foreach (Card item in cardsInHand)
		{
			if (item != card)
			{
				int num2 = cardsInHand.IndexOf(item);
				int num3 = cardsInHand.Count - 1 - Mathf.Abs(num2 - num);
				item.transform.localPosition = new Vector3(item.transform.localPosition.x, item.transform.localPosition.y, -0.02f * (float)num3);
			}
		}
		card.transform.localPosition = new Vector3(card.transform.localPosition.x, card.transform.localPosition.y, -0.25f);
	}

	public void OnCardSelected(Card card)
	{
		if (!choosingSlot && CanPlay(card))
		{
			StartCoroutine(SelectSlotForCard(card));
		}
	}

	private bool CanPlay(Card card)
	{
		return card.Info.cost <= BoardManager.instance.PlayerAvailableSacrifices && !PlayingLocked;
	}

	private IEnumerator SelectSlotForCard(Card card)
	{
		BoardManager.instance.CancelledSacrifice = false;
		CombatBell.instance.Enabled = false;
		choosingSlot = true;
		choosingSlotCard = card;
		BoardManager.instance.ShowCardNearBoard(card, showNearBoard: true);
		bool cardWasPlayed = false;
		bool hasCost = card.Info.cost > 0;
		if (hasCost)
		{
			List<CardSlot> occupiedSlots = BoardManager.instance.PlayerSlots.FindAll((CardSlot x) => x.Card != null);
			yield return StartCoroutine(BoardManager.instance.ChooseSacrificesForCards(occupiedSlots, card));
		}
		if (!BoardManager.instance.CancelledSacrifice)
		{
			List<CardSlot> emptySlots = BoardManager.instance.PlayerSlots.FindAll((CardSlot x) => x.Card == null);
			yield return StartCoroutine(BoardManager.instance.ChooseSlot(emptySlots, !hasCost));
			CardSlot slot = BoardManager.instance.LastSelectedSlot;
			if (slot != null)
			{
				cardWasPlayed = true;
				cardsInHand.Remove(card);
				BoardManager.instance.AssignCardToSlot(card, slot);
				if (cardsInHand.Count > 0)
				{
					OnCardInspected(cardsInHand[0]);
				}
			}
			yield return StartCoroutine(card.Play());
			yield return StartCoroutine(card.ResolveOnBoard());
			foreach (Card c in BoardManager.instance.CardsOnBoard)
			{
				yield return StartCoroutine(c.OtherCardResolve(card));
			}
		}
		if (!cardWasPlayed)
		{
			BoardManager.instance.ShowCardNearBoard(card, showNearBoard: false);
		}
		choosingSlot = false;
		choosingSlotCard = null;
		CombatBell.instance.Enabled = true;
	}

	private void SetCardPositions()
	{
		float num = 1.75f / (float)cardsInHand.Count;
		float num2 = -1.9f;
		foreach (Card item in cardsInHand)
		{
			if (item != null && choosingSlotCard != item)
			{
				int num3 = cardsInHand.IndexOf(item);
				float num4 = num2 + num * (float)num3;
				float num5 = Mathf.Abs(num4 - num2) / 1.75f;
				num5 = num5 * 2f - 1f;
				float z = num5 * -11f;
				float num6 = 1.1f + 0.1f * (0f - Mathf.Abs(num5));
				if (Cursor3D.instance.CurrentInteractable == item)
				{
					num6 += 0.1f;
				}
				item.UpdateHandPosition(new Vector3(num4, num6, item.transform.localPosition.z));
				item.transform.localRotation = Quaternion.Euler(5.5f, 0f, z);
			}
		}
	}
}
