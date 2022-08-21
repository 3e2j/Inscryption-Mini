using UnityEngine;

public class CardAnimationController : MonoBehaviour
{
	[SerializeField]
	private Renderer cardRenderer;

	[SerializeField]
	private GameObject sacrificeMarker;

	[SerializeField]
	private GameObject deathParticles;

	private bool flippedOver;

	public void FlipCardRenderer()
	{
		cardRenderer.transform.localRotation = Quaternion.Euler(0f, 0f, 180f);
	}

	public void SetMarkedForSacrifice(bool marked, bool playSound = true)
	{
		sacrificeMarker.SetActive(marked);
		GetComponent<Animator>().SetTrigger("sacrifice_selected");
		if (playSound)
		{
			AudioController.Instance.PlaySoundWithPitch("card", 0.9f + Random.value * 0.2f, 0.2f);
		}
	}

	public void SetFlipped(bool flipped, bool immediate = false)
	{
		if (flippedOver != flipped)
		{
			GetComponent<Animator>().Play((!flipped) ? "card_flip_faceup" : "card_flip_facedown", 0, (!immediate) ? 0f : 1f);
			AudioController.Instance.PlaySoundWithPitch("card", 0.9f + Random.value * 0.2f, 0.2f);
		}
		flippedOver = flipped;
	}

	public void PlayTransformAnimation()
	{
		GetComponent<Animator>().SetTrigger("flip");
	}

	public void PlaySacrificeParticles()
	{
		GameObject gameObject = Object.Instantiate(deathParticles);
		gameObject.SetActive(value: true);
		gameObject.transform.SetParent(base.transform);
		gameObject.transform.position = deathParticles.transform.position;
		gameObject.transform.localScale = deathParticles.transform.localScale;
		gameObject.transform.rotation = deathParticles.transform.rotation;
		Object.Destroy(gameObject, 6f);
	}

	public void PlayHitAnimation()
	{
		GetComponent<Animator>().SetTrigger("take_hit");
	}

	public void PlayDeathAnimation(bool playSound = true)
	{
		GetComponent<Animator>().SetTrigger("death");
		PlayDeathParticles();
	}

	public void PlayAttackAnimation(bool attackPlayer)
	{
		AudioController.Instance.PlaySound("growl");
		GetComponent<Animator>().SetTrigger((!attackPlayer) ? "attack_creature" : "attack_player");
	}

	public void SetAnimationPaused(bool paused)
	{
		GetComponent<Animator>().speed = ((!paused) ? 1f : 0f);
	}

	private void PlayDeathParticles()
	{
		deathParticles.transform.parent = null;
		deathParticles.transform.localScale = Vector3.one;
		deathParticles.gameObject.SetActive(value: true);
		Object.Destroy(deathParticles, 6f);
	}
}
