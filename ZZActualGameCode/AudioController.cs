using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;

[RequireComponent(typeof(AudioSource))]
public class AudioController : MonoBehaviour
{
	private List<AudioClip> SFX = new List<AudioClip>();

	private List<AudioClip> Loops = new List<AudioClip>();

	private AudioSource source;

	public string InitialSong;

	public float loopOffset;

	private string currentSong = string.Empty;

	private Dictionary<string, float> limitedFrequencySounds = new Dictionary<string, float>();

	private Dictionary<string, int> lastPlayedSounds = new Dictionary<string, int>();

	private List<AudioMixer> loadedMixers = new List<AudioMixer>();

	private AudioMixerGroup currentSFXMixer;

	private Coroutine skippingCoroutine;

	private const string NULL_INITIAL_SONG = "null";

	public string LoopName
	{
		get
		{
			AudioClip clip = GetComponent<AudioSource>().clip;
			if (clip != null)
			{
				return clip.name;
			}
			return null;
		}
	}

	public float LoopVolume
	{
		get
		{
			if (source.clip != null)
			{
				return source.volume;
			}
			return 0f;
		}
	}

	public float LoopTimeNormalized
	{
		get
		{
			if (source != null && source.clip != null)
			{
				return 1f - (source.clip.length - source.time) / source.clip.length;
			}
			return 0f;
		}
	}

	public static AudioController Instance { get; private set; }

	public bool Fading { get; set; }

	private void Awake()
	{
		if ((bool)Instance)
		{
			if (InitialSong != "null")
			{
				if (!string.IsNullOrEmpty(InitialSong))
				{
					Instance.FadeLoopIfNotPlaying(InitialSong, 1f);
				}
				else
				{
					Instance.currentSong = string.Empty;
				}
			}
			Object.Destroy(base.gameObject);
			return;
		}
		Instance = this;
		base.transform.parent = null;
		Object.DontDestroyOnLoad(base.gameObject);
		source = GetComponent<AudioSource>();
		Object[] array = Resources.LoadAll("Audio/SFX");
		foreach (object obj in array)
		{
			SFX.Add((AudioClip)obj);
		}
		Object[] array2 = Resources.LoadAll("Audio/Loops");
		foreach (object obj2 in array2)
		{
			Loops.Add((AudioClip)obj2);
		}
		if (InitialSong != "null")
		{
			CrossFadeLoop(InitialSong, 1f, 5f, 1f, loopOffset);
		}
	}

	public AudioSource PlayClipAt(AudioClip clip, Vector3 pos)
	{
		GameObject gameObject = new GameObject("TempAudio");
		gameObject.transform.position = pos;
		AudioSource audioSource = gameObject.AddComponent<AudioSource>();
		audioSource.clip = clip;
		audioSource.outputAudioMixerGroup = currentSFXMixer;
		audioSource.Play();
		Object.Destroy(gameObject, clip.length);
		return audioSource;
	}

	public AudioSource PlaySound(string soundName)
	{
		if (string.IsNullOrEmpty(soundName))
		{
			return null;
		}
		AudioClip audioClip = SFX.Find((AudioClip x) => x.name == soundName);
		if (audioClip != null)
		{
			return PlayClipAt(audioClip, Vector3.zero);
		}
		return null;
	}

	public AudioSource PlaySoundAtLimitedFrequency(string soundName, float frequencyMin, float pitch = 1f, float volume = 1f, string entrySuffix = "")
	{
		float unscaledTime = Time.unscaledTime;
		string key = soundName + entrySuffix;
		if (limitedFrequencySounds.ContainsKey(key))
		{
			if (unscaledTime - frequencyMin > limitedFrequencySounds[key])
			{
				limitedFrequencySounds[key] = unscaledTime;
				return PlaySoundWithPitch(soundName, pitch, volume);
			}
			return null;
		}
		limitedFrequencySounds.Add(key, unscaledTime);
		return PlaySoundWithPitch(soundName, pitch, volume);
	}

	public AudioSource PlayRandomSound(string soundPrefix, bool noRepeating = false, bool randomPitch = false)
	{
		List<AudioClip> list = SFX.FindAll((AudioClip x) => x != null && x.name.StartsWith(soundPrefix + " "));
		string empty = string.Empty;
		if (list.Count > 0)
		{
			int num = Random.Range(0, list.Count) + 1;
			if (noRepeating)
			{
				if (!lastPlayedSounds.ContainsKey(soundPrefix))
				{
					lastPlayedSounds.Add(soundPrefix, num);
				}
				else
				{
					int num2 = 0;
					while (lastPlayedSounds[soundPrefix] == num && num2 < 100)
					{
						num = Random.Range(0, list.Count) + 1;
						num2++;
					}
					if (num2 >= 99)
					{
						Debug.Log("Broke out of infinite loop! AudioController.PlayRandomSound");
					}
					lastPlayedSounds[soundPrefix] = num;
				}
			}
			empty = soundPrefix + " " + num;
		}
		else
		{
			empty = soundPrefix;
		}
		AudioSource audioSource = PlaySoundWithPitch(empty, (!randomPitch) ? 1f : Random.Range(0.9f, 1.1f), 1f);
		if (audioSource == null)
		{
			return PlaySoundWithPitch(soundPrefix, 1f, 1f);
		}
		return audioSource;
	}

	public void PlaySoundDelayed(string soundName, float delay, float pitch = 1f, float volume = 1f)
	{
		StartCoroutine(WaitThenPlaySound(soundName, delay, pitch, volume));
	}

	private IEnumerator WaitThenPlaySound(string soundName, float delay, float pitch, float volume)
	{
		yield return new WaitForSeconds(delay);
		PlaySoundWithPitch(soundName, pitch, volume);
	}

	public AudioSource PlaySoundWithPitch(string soundName, float pitch, float volume)
	{
		if (!string.IsNullOrEmpty(soundName))
		{
			AudioSource audioSource = PlaySound(soundName);
			if (audioSource != null)
			{
				audioSource.pitch *= pitch;
				audioSource.volume *= volume;
			}
			return audioSource;
		}
		return null;
	}

	public AudioSource PlaySoundMuffled(string soundName, float cutoff = 300f)
	{
		AudioSource audioSource = PlaySound(soundName);
		AudioLowPassFilter audioLowPassFilter = audioSource.gameObject.AddComponent<AudioLowPassFilter>();
		audioLowPassFilter.cutoffFrequency = cutoff;
		return audioSource;
	}

	public void SetLooping(bool looping)
	{
		source.loop = looping;
	}

	public void PauseLoop()
	{
		source.Pause();
	}

	public void ResumeLoop(float fadeInSpeed = float.MaxValue)
	{
		source.UnPause();
		if (!source.isPlaying)
		{
			source.Play();
		}
		source.volume = 0f;
		FadeInLoop(fadeInSpeed);
	}

	public void RestartLoop()
	{
		source.Stop();
		source.Play();
		Fading = false;
	}

	public void StopLoop()
	{
		source.Stop();
		currentSong = string.Empty;
		Fading = false;
	}

	public AudioClip GetLoop(string loopName)
	{
		return Loops.Find((AudioClip x) => x.name == loopName);
	}

	public void SetLoop(string loopName)
	{
		currentSong = loopName;
		if (source != null)
		{
			AudioClip loop = GetLoop(loopName);
			if (loop != null)
			{
				source.Stop();
				source.time = 0f;
				source.clip = loop;
				source.Play();
			}
		}
	}

	public void ClearLoopMixing()
	{
		source.outputAudioMixerGroup = null;
	}

	public void SetLoopMixing(string mixerId, string groupId)
	{
		source.outputAudioMixerGroup = GetMixerGroup(mixerId, groupId);
	}

	public AudioClip GetSFX(string sfxName)
	{
		return SFX.Find((AudioClip x) => x.name == sfxName);
	}

	public void ClearSFXMixing()
	{
		currentSFXMixer = null;
	}

	public void SetSFXMixing(string mixerId, string groupId)
	{
		currentSFXMixer = GetMixerGroup(mixerId, groupId);
	}

	public void FadeLoopIfNotPlaying(string loopName, float volume)
	{
		if (loopName != currentSong)
		{
			SetLoop(loopName);
			SetLoopVolume(volume);
			FadeInLoop(1f);
		}
	}

	public void CrossFadeLoopIfNotPlaying(string loopName, float volume, float speed = 0.5f, float pitch = 1f)
	{
		if (currentSong != loopName)
		{
			CrossFadeLoop(loopName, volume, speed, pitch);
		}
	}

	public void CrossFadeLoop(string loopName, float volume = 1f, float speed = 5f, float pitch = 1f, float offset = 0f)
	{
		currentSong = loopName;
		for (int i = 0; i < Loops.Count; i++)
		{
			AudioClip audioClip = Loops[i];
			if (audioClip.name == loopName)
			{
				StopAllCoroutines();
				StartCoroutine(Cross(loopName, volume, fadeOut: false, speed, pitch, offset));
				break;
			}
		}
	}

	public void FadeOutLoop(float fadeSpeed = float.MaxValue)
	{
		StopAllCoroutines();
		StartCoroutine(DoFadeToVolume(fadeSpeed, 0f));
	}

	public void FadeInLoop(float fadeSpeed = float.MaxValue, float toVolume = 1f)
	{
		StopAllCoroutines();
		StartCoroutine(DoFadeToVolume(fadeSpeed, toVolume));
	}

	private IEnumerator DoFadeToVolume(float fadeSpeed, float newNormalizedVolume)
	{
		Fading = true;
		if (source.volume > GetAdjustedVolume(newNormalizedVolume))
		{
			while (source.volume >= GetAdjustedVolume(newNormalizedVolume))
			{
				source.volume -= GetAdjustedVolume(Time.deltaTime * fadeSpeed);
				yield return new WaitForEndOfFrame();
			}
		}
		else
		{
			while (source.volume <= GetAdjustedVolume(newNormalizedVolume))
			{
				source.volume += GetAdjustedVolume(Time.deltaTime * fadeSpeed);
				yield return new WaitForEndOfFrame();
			}
		}
		source.volume = GetAdjustedVolume(newNormalizedVolume);
		Fading = false;
	}

	public void FadeOutThenPlayAfterDelay(string bgm, float delay)
	{
		FadeOutLoop();
		StartCoroutine(WaitThenPlay(bgm, delay));
	}

	private IEnumerator WaitThenPlay(string bgm, float waitTime)
	{
		yield return new WaitForSeconds(waitTime);
		CrossFadeLoop(bgm);
	}

	private IEnumerator Cross(string newLoop, float volume, bool fadeOut, float speed = 5f, float pitch = 1f, float offset = 0f)
	{
		Fading = true;
		if ((bool)source.clip && source.isPlaying)
		{
			while (source.volume > 0f)
			{
				source.volume -= speed * Time.deltaTime;
				yield return new WaitForEndOfFrame();
			}
			source.volume = 0f;
		}
		if (!fadeOut)
		{
			SetLoop(newLoop);
			SetLoopVolume(0f);
			source.pitch = pitch;
			source.time = offset;
			while (source.volume < GetAdjustedVolume(volume))
			{
				source.volume += speed * Time.deltaTime;
				yield return new WaitForEndOfFrame();
			}
			source.volume = GetAdjustedVolume(volume);
		}
		Fading = false;
	}

	public void SetLoopCutoff(float cutoff)
	{
		AudioLowPassFilter audioLowPassFilter = GetComponent<AudioLowPassFilter>();
		if (audioLowPassFilter == null)
		{
			audioLowPassFilter = base.gameObject.AddComponent<AudioLowPassFilter>();
		}
		audioLowPassFilter.cutoffFrequency = cutoff;
	}

	public void SetLoopVolume(float volume, bool stopFades = false)
	{
		if (stopFades)
		{
			StopAllCoroutines();
		}
		source.volume = volume;
	}

	public void SetLoopVolume(float volume, float speed)
	{
		StopAllCoroutines();
		StartCoroutine(DoFadeToVolume(speed, volume));
	}

	public void SetLoopTimeNormalized(float time)
	{
		if (source.clip != null)
		{
			float num = source.clip.length * time;
			if (num < source.clip.length)
			{
				source.time = num;
			}
		}
	}

	public void StartLoopSkipping(float skipLength)
	{
		StopLoopSkipping();
		skippingCoroutine = StartCoroutine(DoLoopSkipping(source.time, skipLength));
	}

	public void StopLoopSkipping()
	{
		if (skippingCoroutine != null)
		{
			StopCoroutine(skippingCoroutine);
		}
	}

	public void StopCrossFade()
	{
		StopAllCoroutines();
	}

	public AudioMixerGroup GetMixerGroup(string mixerId, string groupId)
	{
		AudioMixer audioMixer = loadedMixers.Find((AudioMixer x) => x.name == mixerId);
		if (audioMixer == null)
		{
			audioMixer = Resources.Load<AudioMixer>("Audio/Mixing/" + mixerId);
			loadedMixers.Add(audioMixer);
		}
		if (audioMixer != null)
		{
			AudioMixerGroup[] array = audioMixer.FindMatchingGroups(groupId);
			if (array.Length > 0)
			{
				return array[0];
			}
		}
		return null;
	}

	public IEnumerator FadeMixerParameter(string mixer, string channel, string parameter, float fadeTo, float fadeLength)
	{
		AudioMixerGroup mainBGM = GetMixerGroup(mixer, channel);
		mainBGM.audioMixer.GetFloat(parameter, out var startVolume);
		float timer = 0f;
		while (timer < fadeLength)
		{
			timer += Time.deltaTime;
			mainBGM.audioMixer.SetFloat(parameter, Mathf.Lerp(startVolume, fadeTo, timer / fadeLength));
			yield return new WaitForEndOfFrame();
		}
		mainBGM.audioMixer.SetFloat(parameter, fadeTo);
	}

	public IEnumerator FadeOutExternalSource(AudioSource externalSource, float fadeSpeed)
	{
		while (externalSource != null && externalSource.volume > 0f)
		{
			externalSource.volume -= Time.deltaTime * fadeSpeed;
			yield return new WaitForEndOfFrame();
		}
	}

	private IEnumerator DoLoopSkipping(float startTime, float skipLength)
	{
		while (true)
		{
			yield return new WaitForSeconds(skipLength);
			source.time = startTime;
		}
	}

	private float GetAdjustedVolume(float volume)
	{
		return volume;
	}
}
