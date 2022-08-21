using UnityEngine;
using UnityEngine.SceneManagement;

public class StartScreen : MonoBehaviour
{
	[SerializeField]
	private LerpAlpha fadeMask;

	private void Start()
	{
		AudioController.Instance.SetLoop("main_loop");
		AudioController.Instance.SetLoopVolume(0f);
		AudioController.Instance.FadeInLoop(0.2f, 0.75f);
	}

	private void Update()
	{
		if (Input.anyKeyDown)
		{
			fadeMask.intendedAlpha = 1f;
			CustomCoroutine.WaitThenExecute(3f, Next);
			base.enabled = false;
		}
	}

	private void Next()
	{
		SceneManager.LoadScene("scene1");
	}
}
