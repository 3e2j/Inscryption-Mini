using System.Collections;
using Pixelplacement;
using UnityEngine;

public class Scales : MonoBehaviour
{
	[SerializeField]
	private GameObject weightPrefab;

	[SerializeField]
	private Transform playerSide;

	[SerializeField]
	private Transform opponentSide;

	[SerializeField]
	private Transform rotator;

	[SerializeField]
	private GameObject eye;

	[SerializeField]
	private GameObject hand;

	private int opponentWeight;

	private int playerWeight;

	private const float MAX_ROTATION = 30f;

	private const float INCREMENT = 5.5f;

	public IEnumerator AddDamage(int damage, bool toPlayer, bool isEye, bool isHand)
	{
		if (isEye)
		{
			eye.SetActive(value: true);
			opponentWeight += damage;
			SetScalesBalance();
			yield return new WaitForSeconds(0.2f);
			yield break;
		}
		if (isHand)
		{
			hand.SetActive(value: true);
			opponentWeight += damage;
			SetScalesBalance();
			yield return new WaitForSeconds(0.2f);
			yield break;
		}
		for (int i = 0; i < damage; i++)
		{
			GameObject weight = Object.Instantiate(weightPrefab);
			weight.transform.parent = base.transform;
			weight.transform.position = ((!toPlayer) ? opponentSide.transform.position : playerSide.transform.position);
			weight.transform.eulerAngles = Random.onUnitSphere * 360f;
			weight.gameObject.SetActive(value: true);
			weight.transform.localScale = Vector3.zero;
			Tween.LocalScale(weight.transform, Vector3.one * 0.2f, 0.1f, 0f, Tween.EaseIn);
			weight.GetComponent<Rigidbody>().useGravity = false;
			yield return new WaitForSeconds(0.12f);
			weight.GetComponent<Rigidbody>().useGravity = true;
			weight.GetComponent<Rigidbody>().AddForce(Random.onUnitSphere * 7f);
			weight.GetComponent<Rigidbody>().AddForce(Vector3.down * 9f);
			yield return new WaitForSeconds(0.12f);
			if (toPlayer)
			{
				playerWeight++;
			}
			else
			{
				opponentWeight++;
			}
			SetScalesBalance();
			AudioController.Instance.PlaySoundWithPitch("weight_drop", 0.9f + Random.value * 0.2f, 0.2f);
			yield return new WaitForSeconds(0.1f);
		}
	}

	private void SetScalesBalance()
	{
		float value = (float)(opponentWeight - playerWeight) * 5.5f;
		value = Mathf.Clamp(value, -27.5f, 27.5f);
		Tween.LocalRotation(rotator, Quaternion.Euler(value, 56f, 0f), 0.3f, 0f, Tween.EaseOut);
	}
}
