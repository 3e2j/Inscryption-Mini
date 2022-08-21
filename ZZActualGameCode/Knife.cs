public class Knife : Interactable
{
	private bool isEnabled;

	public bool Enabled
	{
		get
		{
			return isEnabled;
		}
		set
		{
			isEnabled = value;
			if (Cursor3D.instance.CurrentInteractable != null && Cursor3D.instance.CurrentInteractable == this)
			{
				if (isEnabled)
				{
					OnCursorEnter();
				}
				else
				{
					OnCursorExit();
				}
			}
		}
	}

	private void Update()
	{
		Enabled = TurnManager.instance.IsPlayerTurn && !TurnManager.instance.IsCombatPhase;
	}

	public override void OnCursorSelectEnd()
	{
		if (Enabled)
		{
			SceneSequencer.instance.OnKnifeUsed();
			Cursor3D.instance.SetCursorType(CursorType.Default);
			AudioController.Instance.PlaySound("placeitem");
		}
	}

	public override void OnCursorEnter()
	{
		if (Enabled)
		{
			Cursor3D.instance.SetCursorType(CursorType.Pickup);
		}
	}

	public override void OnCursorExit()
	{
		if (Enabled)
		{
			Cursor3D.instance.SetCursorType(CursorType.Default);
		}
	}
}
