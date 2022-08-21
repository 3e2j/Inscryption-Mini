using UnityEngine;

public class CardSlot : Interactable
{
	public CardSlot opposingSlot;

	private bool choosable;

	[SerializeField]
	private Material defaultMat;

	[SerializeField]
	private Material highlightedMat;

	[SerializeField]
	private Material choosableMat;

	public Card Card { get; set; }

	public bool Chooseable
	{
		get
		{
			return choosable;
		}
		set
		{
			choosable = value;
			if (Cursor3D.instance.CurrentInteractable == this)
			{
				OnCursorEnter();
			}
		}
	}

	public override void OnCursorSelectStart()
	{
		BoardManager.instance.OnSlotSelected(this);
	}

	public override void OnCursorEnter()
	{
		if (Chooseable)
		{
			GetComponentInChildren<Renderer>().material = choosableMat;
		}
		else
		{
			GetComponentInChildren<Renderer>().material = highlightedMat;
		}
	}

	public override void OnCursorExit()
	{
		GetComponentInChildren<Renderer>().material = defaultMat;
	}
}
