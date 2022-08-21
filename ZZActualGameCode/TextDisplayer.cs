using UnityEngine;

public class TextDisplayer : MonoBehaviour
{
	public static TextDisplayer instance;

	[SerializeField]
	private TextMesh textMesh;

	private AudioSource currentAudio;

	private void Awake()
	{
		instance = this;
	}

	public void ShowMessage(string message, Emotion emotion = Emotion.Neutral)
	{
		textMesh.gameObject.SetActive(value: true);
		textMesh.text = message.ToUpper();
		if (currentAudio != null)
		{
			Object.Destroy(currentAudio);
		}
		switch (emotion)
		{
		case Emotion.Neutral:
			currentAudio = AudioController.Instance.PlayRandomSound("spiritvoice", noRepeating: true, randomPitch: true);
			break;
		case Emotion.Anger:
			currentAudio = AudioController.Instance.PlaySound("spiritvoice_impatient");
			break;
		case Emotion.Laughter:
			currentAudio = AudioController.Instance.PlaySound("spiritvoice_laugh");
			break;
		}
	}

	public void Clear()
	{
		textMesh.gameObject.SetActive(value: false);
	}
}
