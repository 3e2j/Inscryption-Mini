using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "CardInfo", menuName = "Cards/CardInfo", order = 1)]
public class CardInfo : ScriptableObject
{
	[Header("Displayed")]
	public string displayedName;

	[TextArea]
	public string description;

	public Texture portraitTex;

	public Texture alternatePortraitTex;

	public Texture abilityTex;

	[Header("Stats")]
	public int cost;

	public int baseAttack;

	public int baseHealth;

	public List<Trait> traits = new List<Trait>();

	[Header("Ability")]
	public SpecialAbility ability;

	public int abilityIntParameter;

	public CardInfo abilityCardParameter;

	[Header("Special")]
	public string specialScriptName;

	public bool HasTrait(Trait trait)
	{
		return traits.Contains(trait);
	}
}
