using System.Collections.Generic;
using UnityEngine;

public class AnimatingSprite : MonoBehaviour
{
	[Header("Frames")]
	public List<Sprite> frames = new List<Sprite>();

	[SerializeField]
	private bool randomizeSprite;

	[Header("Animation")]
	[SerializeField]
	private float animSpeed = 0.033f;

	[SerializeField]
	private float animOffset;

	[SerializeField]
	private bool randomOffset;

	[SerializeField]
	private bool stopAfterSingleIteration;

	[Header("Audio")]
	[SerializeField]
	private string soundId;

	[SerializeField]
	private int soundFrame;

	[Header("Blinking")]
	public List<Sprite> blinkFrames = new List<Sprite>();

	public float blinkRate;

	public float doubleBlinkRate;

	private int blinkFrameIndex;

	private float blinkTimer;

	private float timer;

	private SpriteRenderer sR;

	[HideInInspector]
	public int frameIndex;

	private bool stopOnNextFrame;

	private void Awake()
	{
		sR = GetComponent<SpriteRenderer>();
	}

	private void Start()
	{
		if (randomOffset)
		{
			animOffset = (0f - Random.value) * ((float)frames.Count * animSpeed);
		}
		timer = animOffset;
	}

	public void StartAnimatingWithDecrementedIndex()
	{
		frameIndex--;
		StartAnimating();
	}

	public void StartAnimating()
	{
		base.enabled = true;
		stopOnNextFrame = false;
	}

	public void StopAnimating()
	{
		stopOnNextFrame = true;
	}

	public void StopImmediate()
	{
		Stop();
	}

	public void StartFromBeginning()
	{
		base.enabled = true;
		frameIndex = 0;
	}

	public void IterateFrame()
	{
		if (stopOnNextFrame)
		{
			Stop();
			return;
		}
		timer = 0f;
		if (blinkFrames.Count > 0 && blinkTimer > blinkRate)
		{
			sR.sprite = blinkFrames[blinkFrameIndex];
			if (blinkFrameIndex < blinkFrames.Count - 1)
			{
				blinkFrameIndex++;
				return;
			}
			if (Random.value < doubleBlinkRate)
			{
				blinkTimer = blinkRate - 0.1f;
			}
			else
			{
				blinkTimer = Random.value * -0.5f;
			}
			blinkFrameIndex = 0;
			return;
		}
		if (randomizeSprite)
		{
			int index = (frameIndex = Random.Range(0, frames.Count));
			sR.sprite = frames[index];
			return;
		}
		frameIndex++;
		if (frameIndex >= frames.Count)
		{
			if (stopAfterSingleIteration)
			{
				stopAfterSingleIteration = false;
				base.enabled = false;
				frameIndex--;
			}
			else
			{
				frameIndex = 0;
			}
		}
		sR.sprite = frames[frameIndex];
		if (frameIndex == soundFrame && !string.IsNullOrEmpty(soundId))
		{
			AudioController.Instance.PlaySound(soundId);
		}
	}

	public void Clear()
	{
		base.enabled = false;
		sR.sprite = null;
	}

	private void Stop()
	{
		stopOnNextFrame = false;
		base.enabled = false;
		if (sR != null)
		{
			sR.sprite = frames[0];
		}
	}

	private void Update()
	{
		blinkTimer += Time.deltaTime;
		timer += Time.deltaTime;
		if (timer > animSpeed)
		{
			IterateFrame();
		}
	}
}
