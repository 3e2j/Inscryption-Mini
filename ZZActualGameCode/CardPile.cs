using System.Collections.Generic;
using Pixelplacement;
using UnityEngine;

public class CardPile : MonoBehaviour
{
	[SerializeField]
	private GameObject cardbackPrefab;

	[SerializeField]
	private GameObject shadow;

	[SerializeField]
	private int fixedPileSize;

	private List<Transform> cards = new List<Transform>();

	private const float ROTATION_VARIANCE = 15f;

	private const float Y_SPACING = 0.01f;

	public Vector3 TopCardPosition => base.transform.position + Vector3.up * cards.Count * 0.01f;

	private void Start()
	{
		if (fixedPileSize > 0)
		{
			SpawnCards(fixedPileSize);
		}
	}

	public void SpawnCards(int numCards)
	{
		for (int i = 0; i < numCards; i++)
		{
			GameObject gameObject = Object.Instantiate(cardbackPrefab);
			gameObject.transform.SetParent(base.transform);
			gameObject.transform.localRotation = Quaternion.Euler(90f, 0f, -7.5f + Random.value * 15f);
			gameObject.transform.localPosition = new Vector3(0f, (float)i * 0.01f, 0f);
			cards.Add(gameObject.transform);
		}
	}

	public void Draw()
	{
		if (cards.Count > 0)
		{
			Transform transform = cards[cards.Count - 1];
			Tween.Position(transform, transform.transform.position + Vector3.up * 1f + Vector3.back * 5f, 0.5f, 0f, Tween.EaseInOut);
			Tween.Rotation(transform, Quaternion.Euler(-180f, 180f, 0f), 0.5f, 0f, Tween.EaseInOut);
			cards.Remove(transform);
			Object.Destroy(transform.gameObject, 2f);
			if (cards.Count == 0)
			{
				shadow.SetActive(value: false);
			}
		}
	}
}
