using System.Collections.Generic;
using UnityEngine;

public class SequenceSelector : MonoBehaviour
{
	[SerializeField]
	private List<CardInfo> baseDeck = new List<CardInfo>();

	[SerializeField]
	private List<SceneSequencer> sequencers = new List<SceneSequencer>();

	[SerializeField]
	private int debugProgress;

	private void Start()
	{
		InitializePlayerDeck();
		SceneSequencer.instance = null;
		ViewManager.instance.SetColor(Color.black);
		if (GameStats.sceneProgress < sequencers.Count)
		{
			sequencers[GameStats.sceneProgress].gameObject.SetActive(value: true);
			PlayerHand.instance.Deck = sequencers[GameStats.sceneProgress].transform.Find("PlayerDeck").GetComponent<Deck>();
			TurnManager.instance.opponent = sequencers[GameStats.sceneProgress].GetComponentInChildren<OpponentAI>();
		}
	}

	private void InitializePlayerDeck()
	{
		if (GameStats.playerDeck == null)
		{
			GameStats.playerDeck = baseDeck;
		}
	}
}
