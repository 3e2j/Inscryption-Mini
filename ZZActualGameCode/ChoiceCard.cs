using UnityEngine;

public class ChoiceCard : Interactable
{
	[SerializeField]
	private bool isChild;

	public override void OnCursorSelectStart()
	{
		(SceneSequencer.instance as Scene4).MakeChoice(isChild);
		GetComponent<Collider>().enabled = false;
	}

	public override void OnCursorEnter()
	{
		Cursor3D.instance.SetCursorType(CursorType.Sacrifice);
	}

	public override void OnCursorExit()
	{
		Cursor3D.instance.SetCursorType(CursorType.Default);
	}
}
