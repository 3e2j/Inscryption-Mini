using System.Collections;
using System.Collections.Generic;
using Pixelplacement;
using UnityEngine;

public class BoardManager : MonoBehaviour
{
	public static BoardManager instance;

	[SerializeField]
	private List<CardSlot> playerSlots = new List<CardSlot>();

	[SerializeField]
	private List<CardSlot> opponentSlots = new List<CardSlot>();

	private List<CardSlot> currentValidSlots;

	private List<CardInfo> lastSacrificesInfo = new List<CardInfo>();

	private List<CardSlot> currentSacrifices = new List<CardSlot>();

	[SerializeField]
	private SacrificeTokens tokens;

	private bool viewChangedFromBoard;

	private const float DEFAULT_TRANSITION_SPEED = 0.1f;

	public int PlayerAvailableSacrifices => playerSlots.FindAll((CardSlot x) => x.Card != null).Count;

	public List<CardSlot> PlayerSlots => new List<CardSlot>(playerSlots);

	public int OpponentAvailableSacrifices => opponentSlots.FindAll((CardSlot x) => x.Card != null).Count;

	public List<CardSlot> OpponentSlots => new List<CardSlot>(opponentSlots);

	public List<Card> CardsOnBoard
	{
		get
		{
			List<Card> list = new List<Card>();
			foreach (CardSlot playerSlot in playerSlots)
			{
				if (playerSlot.Card != null)
				{
					list.Add(playerSlot.Card);
				}
			}
			foreach (CardSlot opponentSlot in opponentSlots)
			{
				if (opponentSlot.Card != null)
				{
					list.Add(opponentSlot.Card);
				}
			}
			return list;
		}
	}

	public CardSlot LastSelectedSlot { get; set; }

	public bool ChoosingSlot { get; set; }

	public bool ChoosingSacrifices { get; set; }

	public List<CardInfo> LastSacrificesInfo => lastSacrificesInfo;

	public List<CardSlot> CurrentSacrifices => currentSacrifices;

	public Card CurrentCardToPlay { get; set; }

	public bool CancelledSacrifice { get; set; }

	private void Awake()
	{
		instance = this;
	}

	public IEnumerator ChooseSacrificesForCards(List<CardSlot> validSlots, Card card)
	{
		ViewManager.instance.LockState = ViewLockState.Unlocked;
		ViewManager.instance.SwitchToView(View.Board);
		Cursor3D.instance.SetCursorType(CursorType.Sacrifice);
		viewChangedFromBoard = false;
		currentValidSlots = validSlots;
		ChoosingSacrifices = true;
		CancelledSacrifice = false;
		CurrentCardToPlay = card;
		LastSacrificesInfo.Clear();
		yield return StartCoroutine(tokens.ShowTokens(card.Info.cost));
		while (currentSacrifices.Count != card.Info.cost && !viewChangedFromBoard)
		{
			tokens.SetTokensFlipped(currentSacrifices.Count);
			yield return new WaitForEndOfFrame();
		}
		foreach (CardSlot currentSacrifice in currentSacrifices)
		{
			LastSacrificesInfo.Add(currentSacrifice.Card.Info);
		}
		bool cancelledDueToNoSpaceForCard = !SacrificesCreateRoomForCard();
		if (viewChangedFromBoard || cancelledDueToNoSpaceForCard)
		{
			tokens.HideTokens();
			if (cancelledDueToNoSpaceForCard)
			{
				yield return new WaitForSeconds(0.25f);
			}
			foreach (CardSlot currentSacrifice2 in currentSacrifices)
			{
				currentSacrifice2.Card.Anim.SetMarkedForSacrifice(marked: false);
			}
			ViewManager.instance.SwitchToView(View.Default);
			Cursor3D.instance.SetCursorType(CursorType.Default);
			CancelledSacrifice = true;
		}
		else
		{
			tokens.SetTokensFlipped(currentSacrifices.Count);
			ChoosingSacrifices = false;
			yield return new WaitForSeconds(0.2f);
			tokens.HideTokens();
			foreach (CardSlot s in currentSacrifices)
			{
				yield return StartCoroutine(s.Card.Sacrifice());
				AudioController.Instance.PlaySoundAtLimitedFrequency("sacrifice", 0.1f, 1f, 1f, string.Empty);
			}
		}
		ChoosingSacrifices = false;
		currentSacrifices.Clear();
	}

	public IEnumerator ChooseSlot(List<CardSlot> validSlots, bool canCancel)
	{
		ChoosingSlot = true;
		Cursor3D.instance.SetCursorType(CursorType.Place);
		ViewManager.instance.LockState = ((!canCancel) ? ViewLockState.LockedToBoard : ViewLockState.Unlocked);
		ViewManager.instance.SwitchToView(View.Board);
		viewChangedFromBoard = false;
		currentValidSlots = validSlots;
		LastSelectedSlot = null;
		foreach (CardSlot validSlot in validSlots)
		{
			validSlot.Chooseable = true;
		}
		yield return new WaitUntil(() => LastSelectedSlot != null || (canCancel && viewChangedFromBoard));
		if (canCancel && viewChangedFromBoard)
		{
			ViewManager.instance.SwitchToView(View.Default);
		}
		foreach (CardSlot validSlot2 in validSlots)
		{
			validSlot2.Chooseable = false;
		}
		ViewManager.instance.LockState = ViewLockState.Unlocked;
		ChoosingSlot = false;
		Cursor3D.instance.SetCursorType(CursorType.Default);
	}

	public void OnViewChangedFromBoard()
	{
		viewChangedFromBoard = true;
	}

	public IEnumerator ClearBoard()
	{
		foreach (Card c in CardsOnBoard)
		{
			c.Die(playSound: false);
			yield return new WaitForSeconds(0.05f);
		}
	}

	public IEnumerator SwitchSlotsOfCards(Card card1, Card card2, float switchSpeed = 1f)
	{
		CardSlot card1Slot = card1.Slot;
		CardSlot card2Slot = card2.Slot;
		card1.Slot = null;
		card2.Slot = null;
		AssignCardToSlot(card1, card2Slot, switchSpeed);
		AssignCardToSlot(card2, card1Slot, switchSpeed);
		yield return new WaitForSeconds(0.1f * switchSpeed);
	}

	public void ShowCardNearBoard(Card card, bool showNearBoard)
	{
		card.GetComponent<Collider>().enabled = !showNearBoard;
		if (showNearBoard)
		{
			Transform parent = Camera.main.transform.Find("CardNearBoardParent");
			card.transform.parent = parent;
			Vector3 vector = new Vector3(-2.6f, -1.7f, 3.7f);
			card.transform.localPosition = vector + Vector3.left * 3f;
			Tween.LocalPosition(card.transform, vector, 0.15f, 0.05f, Tween.EaseOut);
			Tween.LocalRotation(card.transform, Quaternion.Euler(10f, 0f, 0f), 0.1f, 0.1f, Tween.EaseOut);
		}
		else
		{
			PlayerHand.instance.ParentCardToHand(card, Vector3.up * 2f + Vector3.left * 2f);
			PlayerHand.instance.OnCardInspected(card);
		}
	}

	public void AssignCardToSlot(Card card, CardSlot slot, float speed = 1f)
	{
		if (card.Slot != null)
		{
			card.Slot.Card = null;
		}
		card.GetComponent<Collider>().enabled = false;
		slot.Card = card;
		card.Slot = slot;
		card.transform.parent = null;
		Tween.Position(card.transform, slot.transform.position + Vector3.up * 0.025f, 0.1f * speed, 0f, Tween.EaseInOut);
		Tween.Rotation(card.transform, slot.transform.GetChild(0).rotation, 0.1f * speed, 0f, Tween.EaseInOut);
	}

	public void QueueCardForSlot(Card card, CardSlot slot, float speed = 1f, bool doTween = true)
	{
		card.GetComponent<Collider>().enabled = false;
		card.QueuedSlot = slot;
		if (doTween)
		{
			Tween.Position(card.transform, slot.transform.position + Vector3.up * 0.025f + Vector3.forward * 2f, 0.1f * speed, 0f, Tween.EaseInOut);
			Tween.Rotation(card.transform, slot.transform.GetChild(0).rotation, 0.1f * speed, 0f, Tween.EaseInOut);
		}
	}

	public void OnSlotSelected(CardSlot slot)
	{
		if (currentValidSlots != null && currentValidSlots.Contains(slot))
		{
			if (ChoosingSacrifices && slot.Card != null && !currentSacrifices.Contains(slot))
			{
				slot.Card.Anim.SetMarkedForSacrifice(marked: true);
				currentSacrifices.Add(slot);
			}
			else
			{
				LastSelectedSlot = slot;
			}
		}
	}

	public List<CardSlot> GetAdjacentSlots(CardSlot slot)
	{
		List<CardSlot> slotsToCheck = opponentSlots;
		if (playerSlots.Contains(slot))
		{
			slotsToCheck = PlayerSlots;
		}
		return slotsToCheck.FindAll((CardSlot x) => Mathf.Abs(slotsToCheck.IndexOf(x) - slotsToCheck.IndexOf(slot)) < 2 && x != slot);
	}

	public CardSlot GetAdjacent(CardSlot slot, bool adjacentOnLeft)
	{
		bool flag = playerSlots.Contains(slot);
		List<CardSlot> adjacentSlots = GetAdjacentSlots(slot);
		if (adjacentSlots.Count > 0)
		{
			if (flag)
			{
				if (adjacentOnLeft)
				{
					return adjacentSlots.Find((CardSlot x) => SlotIsLeftOfSlot(x, slot, playerSlots));
				}
				return adjacentSlots.Find((CardSlot x) => !SlotIsLeftOfSlot(x, slot, playerSlots));
			}
			if (adjacentOnLeft)
			{
				return adjacentSlots.Find((CardSlot x) => SlotIsLeftOfSlot(x, slot, opponentSlots));
			}
			return adjacentSlots.Find((CardSlot x) => !SlotIsLeftOfSlot(x, slot, opponentSlots));
		}
		return null;
	}

	public bool SlotIsLeftOfSlot(CardSlot slot1, CardSlot slot2, List<CardSlot> row)
	{
		return row.IndexOf(slot1) < row.IndexOf(slot2);
	}

	private bool SacrificesCreateRoomForCard()
	{
		foreach (CardSlot playerSlot in PlayerSlots)
		{
			if (playerSlot.Card == null)
			{
				return true;
			}
			if (CurrentSacrifices.Contains(playerSlot) && playerSlot.Card.Info.ability != SpecialAbility.Sacrificial)
			{
				return true;
			}
		}
		return false;
	}
}
