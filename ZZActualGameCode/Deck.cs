using System.Collections.Generic;
using UnityEngine;

public class Deck : MonoBehaviour
{
	[SerializeField]
	private List<CardInfo> fixedDraws = new List<CardInfo>();

	[SerializeField]
	private List<CardInfo> cards = new List<CardInfo>();

	[SerializeField]
	private bool usePlayerDeck;

	[SerializeField]
	private GameObject cardPrefab;

	public int CardsInDeck => cards.Count;

	private void Awake()
	{
		if (usePlayerDeck)
		{
			cards = new List<CardInfo>();
			cards.AddRange(GameStats.playerDeck);
		}
	}

	public Card DrawSpecificCard(CardInfo info)
	{
		GameObject gameObject = SpawnCard();
		Card component = gameObject.GetComponent<Card>();
		component.SetInfo(info);
		return component;
	}

	public Card DrawCard()
	{
		if (cards.Count == 0)
		{
			return null;
		}
		CardInfo cardInfo = null;
		while (cardInfo == null && fixedDraws.Count > 0)
		{
			if (cards.Contains(fixedDraws[0]))
			{
				cardInfo = fixedDraws[0];
			}
			fixedDraws.RemoveAt(0);
		}
		if (cardInfo == null)
		{
			cardInfo = cards[Random.Range(0, cards.Count)];
		}
		cards.Remove(cardInfo);
		GameObject gameObject = SpawnCard();
		Card component = gameObject.GetComponent<Card>();
		component.SetInfo(cardInfo);
		return component;
	}

	private GameObject SpawnCard()
	{
		return Object.Instantiate(cardPrefab);
	}
}
