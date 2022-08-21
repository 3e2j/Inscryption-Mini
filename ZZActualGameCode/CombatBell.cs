public class CombatBell : Interactable
{
	public static CombatBell instance;

	private bool isEnabled;

	public bool Rang { get; set; }

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

	private void Awake()
	{
		instance = this;
	}

	public override void OnCursorSelectStart()
	{
		if (Enabled)
		{
			AudioController.Instance.PlaySoundWithPitch("bell", 0.9f, 0.6f);
			Rang = true;
			Cursor3D.instance.SetCursorType(CursorType.Default);
		}
	}

	public override void OnCursorEnter()
	{
		if (Enabled)
		{
			Cursor3D.instance.SetCursorType(CursorType.Fight);
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
