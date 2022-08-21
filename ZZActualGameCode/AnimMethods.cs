using UnityEngine;

public class AnimMethods : MonoBehaviour
{
	private bool audioMuted;

	public bool AudioMuted
	{
		get
		{
			return audioMuted;
		}
		set
		{
			audioMuted = value;
		}
	}

	private void SendMessageUp(string message)
	{
		base.gameObject.SendMessageUpwards(message, SendMessageOptions.DontRequireReceiver);
	}

	private void Destroy()
	{
		Object.Destroy(base.transform.parent.gameObject);
	}

	private void PlaySound(string soundId)
	{
		if (!audioMuted)
		{
			AudioController.Instance.PlaySound(soundId);
		}
	}

	private void PlaySoundCrossScene(string soundId)
	{
		if (!audioMuted)
		{
			AudioSource audioSource = AudioController.Instance.PlaySound(soundId);
			Object.DontDestroyOnLoad(audioSource.gameObject);
		}
	}

	private void PlaySoundRandomPitch(string soundId)
	{
		if (!audioMuted)
		{
			AudioController.Instance.PlaySoundWithPitch(soundId, Random.Range(0.9f, 1.1f), 1f);
		}
	}

	private void PlaySoundLimited(string soundId)
	{
		if (!audioMuted)
		{
			AudioController.Instance.PlaySoundAtLimitedFrequency(soundId, 0.1f, 1f, 1f, string.Empty);
		}
	}

	private void PlayRandomSound(string soundId)
	{
		if (!audioMuted)
		{
			AudioController.Instance.PlayRandomSound(soundId, noRepeating: true);
		}
	}

	private void PlaySoundMuffled(string soundId)
	{
		if (!audioMuted)
		{
			AudioController.Instance.PlaySoundMuffled(soundId, 600f);
		}
	}
}
