using System.Collections.Generic;
using UnityEngine;

public class Cursor3D : MonoBehaviour
{
	public static Cursor3D instance;

	private Interactable currentInteractable;

	private bool interactionDisabled;

	[SerializeField]
	private Camera rayCamera;

	[SerializeField]
	private List<Sprite> cursorTextures;

	[SerializeField]
	private List<Sprite> cursorDownTextures;

	private CursorType cursorType;

	public Interactable CurrentInteractable => currentInteractable;

	public bool InteractionDisabled
	{
		get
		{
			return interactionDisabled;
		}
		set
		{
			if (!value)
			{
				currentInteractable.OnCursorExit();
				currentInteractable = null;
				SetCursorType(CursorType.Default);
			}
			interactionDisabled = value;
		}
	}

	public Vector2 NormalizedPosition
	{
		get
		{
			float x = Mathf.Clamp(base.transform.localPosition.x / 8.5f, -1f, 1f);
			float y = Mathf.Clamp(base.transform.localPosition.y / 5f, -1f, 1f);
			return new Vector2(x, y);
		}
	}

	private void Awake()
	{
		instance = this;
	}

	private void Start()
	{
		SetCursorType(CursorType.Default);
	}

	public void SetEnabled(bool enabled)
	{
		base.enabled = enabled;
	}

	private void FixedUpdate()
	{
		Vector2 vector = Input.mousePosition;
		Cursor.visible = false;
		Vector2 vector2 = Input.mousePosition / new Vector2(Screen.width, Screen.height);
		Vector2 vector3 = rayCamera.ViewportToWorldPoint(vector2);
		float num = 0.99f;
		base.transform.position = new Vector3(vector3.x * num, vector3.y * num, rayCamera.nearClipPlane);
	}

	private void Update()
	{
		SetCursorDown(Input.GetButton("Select"));
		if (!InteractionDisabled)
		{
			SetCurrentInteractable();
			HandleClicks();
		}
	}

	private void SetCurrentInteractable()
	{
		Interactable interactable = null;
		Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
		if (Physics.Raycast(ray, out var hitInfo, 1000f))
		{
			interactable = hitInfo.transform.GetComponent<Interactable>();
		}
		if (interactable != currentInteractable)
		{
			if (currentInteractable != null)
			{
				currentInteractable.OnCursorExit();
			}
			if (interactable != null)
			{
				interactable.OnCursorEnter();
			}
		}
		currentInteractable = interactable;
	}

	public void SetCursorType(CursorType type)
	{
		cursorType = type;
	}

	private void SetCursorDown(bool down)
	{
		Vector2 vector = new Vector2(60f, 60f);
		if (cursorType == CursorType.Sacrifice)
		{
			vector = new Vector2(60f, 100f);
		}
		GetComponent<SpriteRenderer>().sprite = ((!down) ? cursorTextures[(int)cursorType] : cursorDownTextures[(int)cursorType]);
	}

	private void HandleClicks()
	{
		if (currentInteractable != null)
		{
			if (Input.GetButtonDown("Select"))
			{
				currentInteractable.OnCursorSelectStart();
			}
			else if (Input.GetButtonUp("Select"))
			{
				currentInteractable.OnCursorSelectEnd();
			}
		}
	}
}
