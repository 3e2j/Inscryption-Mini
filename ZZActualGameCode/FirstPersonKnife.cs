using System;
using System.Collections;
using UnityEngine;

public class FirstPersonKnife : MonoBehaviour
{
	public static FirstPersonKnife instance;

	[SerializeField]
	private Animator anim;

	private bool madeSelection;

	private BodySacrifice selection;

	private BodySacrifice specificSelectionAllowed;

	private void Awake()
	{
		instance = this;
	}

	private void Start()
	{
		SetActivated(activated: false);
	}

	public IEnumerator ShowKnifeAndWaitForSelection(Action<BodySacrifice> callback, BodySacrifice specificAllowed = BodySacrifice.None)
	{
		SetActivated(activated: true);
		ViewManager.instance.SwitchToView(View.Default);
		madeSelection = false;
		specificSelectionAllowed = specificAllowed;
		yield return new WaitForEndOfFrame();
		yield return new WaitUntil(() => madeSelection);
		callback?.Invoke(selection);
		SetActivated(activated: false);
	}

	private void SetActivated(bool activated)
	{
		anim.gameObject.SetActive(activated);
		base.enabled = activated;
	}

	private void Update()
	{
		BodySacrifice sacrificeForCursorPosition = GetSacrificeForCursorPosition();
		Vector3 euler = Vector3.zero;
		Vector3 b = Vector3.zero;
		Cursor3D.instance.SetCursorType(CursorType.Place);
		switch (GetSacrificeForCursorPosition())
		{
		case BodySacrifice.Hand:
			b = new Vector3(-1.5f, -1f, 1.5f);
			euler = new Vector3(0f, 0f, 20f);
			Cursor3D.instance.SetCursorType(CursorType.Sacrifice);
			break;
		case BodySacrifice.RightEye:
			b = new Vector3(-1.3f, 0f, 1.4f);
			euler = new Vector3(30f, 38f, 3f);
			Cursor3D.instance.SetCursorType(CursorType.Sacrifice);
			break;
		case BodySacrifice.None:
			b = new Vector3(-2.4f, 0f, 2f);
			euler = new Vector3(0f, 0f, 50f);
			break;
		}
		base.transform.localRotation = Quaternion.Lerp(base.transform.localRotation, Quaternion.Euler(euler), Time.deltaTime * 12f);
		base.transform.localPosition = Vector3.Lerp(base.transform.localPosition, b, Time.deltaTime * 12f);
		if (Input.GetButtonDown("Select"))
		{
			selection = sacrificeForCursorPosition;
			madeSelection = true;
			Cursor3D.instance.SetCursorType(CursorType.Default);
		}
	}

	private BodySacrifice GetSacrificeForCursorPosition()
	{
		Vector2 normalizedPosition = Cursor3D.instance.NormalizedPosition;
		if ((normalizedPosition.x > 0f && normalizedPosition.y > 0f && specificSelectionAllowed == BodySacrifice.None) || (specificSelectionAllowed == BodySacrifice.RightEye && normalizedPosition.x > 0f))
		{
			return BodySacrifice.RightEye;
		}
		if (normalizedPosition.y < 0f && (specificSelectionAllowed == BodySacrifice.None || specificSelectionAllowed == BodySacrifice.Hand))
		{
			return BodySacrifice.Hand;
		}
		return BodySacrifice.None;
	}
}
