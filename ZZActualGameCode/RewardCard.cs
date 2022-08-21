using UnityEngine;

public class RewardCard : Interactable
{
	private CardInfo info;

	private bool flipped = true;

	public CardInfo Info => info;

	public void SetInfo(CardInfo info)
	{
		this.info = info;
		GetComponentInChildren<CardDisplayer>().DisplayInfo(info);
	}

	public override void OnCursorSelectEnd()
	{
		AudioController.Instance.PlaySoundWithPitch("card", 0.9f + Random.value * 0.2f, 0.15f);
		if (flipped)
		{
			flipped = false;
			GetComponent<CardAnimationController>().SetFlipped(flipped: false);
			Cursor3D.instance.SetCursorType(CursorType.Pickup);
			TextDisplayer.instance.ShowMessage(Info.description);
		}
		else
		{
			RewardSelector.instance.OnRewardChosen(this);
		}
	}

	public override void OnCursorEnter()
	{
		if (flipped)
		{
			Cursor3D.instance.SetCursorType(CursorType.Flip);
		}
		else
		{
			Cursor3D.instance.SetCursorType(CursorType.Pickup);
		}
	}

	public override void OnCursorExit()
	{
		Cursor3D.instance.SetCursorType(CursorType.Default);
	}
}
