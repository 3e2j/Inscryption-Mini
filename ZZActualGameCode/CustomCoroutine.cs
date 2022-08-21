using System;
using System.Collections;
using UnityEngine;

public class CustomCoroutine : MonoBehaviour
{
	private static CustomCoroutine instance;

	private static void TryCreateInstance()
	{
		if (instance == null)
		{
			instance = new GameObject("CustomCoroutineRunner").AddComponent<CustomCoroutine>();
		}
	}

	public static void WaitOnConditionThenExecute(Func<bool> condition, Action action)
	{
		TryCreateInstance();
		instance.StartWaitOnConditionThenExecute(condition, action);
	}

	public void StartWaitOnConditionThenExecute(Func<bool> condition, Action action)
	{
		StartCoroutine(DoWaitOnConditionThenExecute(condition, action));
	}

	private IEnumerator DoWaitOnConditionThenExecute(Func<bool> condition, Action action)
	{
		yield return new WaitUntil(() => condition());
		action();
	}

	public static void WaitThenExecute(float wait, Action action, bool unscaledTime = false)
	{
		TryCreateInstance();
		instance.StartWaitThenExecute(wait, action, unscaledTime);
	}

	public void StartWaitThenExecute(float wait, Action action, bool unscaledTime = false)
	{
		StartCoroutine(DoWaitThenExecute(wait, action, unscaledTime));
	}

	private IEnumerator DoWaitThenExecute(float wait, Action action, bool unscaledTime = false)
	{
		if (wait <= 0f)
		{
			yield return new WaitForEndOfFrame();
		}
		else if (unscaledTime)
		{
			yield return new WaitForSecondsRealtime(wait);
		}
		else
		{
			yield return new WaitForSeconds(wait);
		}
		action();
	}

	public static Coroutine WaitOnCondition(Func<bool> condition)
	{
		TryCreateInstance();
		return instance.StartWaitOnCondition(condition);
	}

	public Coroutine StartWaitOnCondition(Func<bool> condition)
	{
		return StartCoroutine(DoWaitOnCondition(condition));
	}

	private IEnumerator DoWaitOnCondition(Func<bool> condition)
	{
		while (condition())
		{
			yield return new WaitForEndOfFrame();
		}
	}
}
