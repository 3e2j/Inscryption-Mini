using TMPro;
using UnityEngine;

public class CardDisplayer : MonoBehaviour
{
	[SerializeField]
	private TextMeshPro nameText;

	[SerializeField]
	private TextMesh healthText;

	[SerializeField]
	private TextMesh attackText;

	[SerializeField]
	private Renderer portraitRenderer;

	[SerializeField]
	private Renderer abilityIconRenderer;

	[SerializeField]
	private Renderer costRenderer;

	[Header("Resources")]
	[SerializeField]
	private Texture2D[] costTextures;

	public void DisplayInfo(CardInfo info)
	{
		SetName(info.displayedName);
		SetPortrait(info.portraitTex);
		abilityIconRenderer.material.mainTexture = info.abilityTex;
		costRenderer.material.mainTexture = costTextures[info.cost];
		SetStatsText(info.baseAttack, info.baseHealth);
	}

	public void SetPortrait(Texture texture)
	{
		portraitRenderer.material.mainTexture = texture;
	}

	public void SetAbilityIcon(Texture texture)
	{
		abilityIconRenderer.material.mainTexture = texture;
	}

	public void SetName(string name)
	{
		nameText.text = name.ToUpper();
	}

	public void SetStatsText(int attack, int health)
	{
		attackText.text = attack.ToString();
		healthText.text = health.ToString();
	}

	public void SetIconFlipped(bool flipped)
	{
		float x = ((!flipped) ? (-0.36f) : 0.36f);
		abilityIconRenderer.transform.localScale = new Vector3(x, abilityIconRenderer.transform.localScale.y, abilityIconRenderer.transform.localScale.z);
	}
}
