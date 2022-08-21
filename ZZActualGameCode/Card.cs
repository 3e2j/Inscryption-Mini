using System;
using System.Collections;
using UnityEngine;

public class Card : Interactable
{
	private int attack;

	private int health;

	private int attackBuff;

	private CardInfo info;

	private SpecialCardBehaviour specialBehaviour;

	private bool movingLeft = true;

	public bool AttackedThisTurn { get; set; }

	public int NumTurnsInPlay { get; set; }

	public int Attack => attack;

	public CardInfo Info => info;

	public CardDisplayer Displayer => GetComponentInChildren<CardDisplayer>();

	public CardAnimationController Anim => GetComponent<CardAnimationController>();

	public CardSlot Slot { get; set; }

	public CardSlot QueuedSlot { get; set; }

	public void UpdateHandPosition(Vector3 handPos)
	{
		base.transform.localPosition = Vector3.Lerp(base.transform.localPosition, new Vector3(handPos.x, handPos.y, base.transform.localPosition.z), Time.deltaTime * 8f);
	}

	public void SetInfo(CardInfo info)
	{
		this.info = info;
		attack = info.baseAttack;
		health = info.baseHealth;
		Displayer.DisplayInfo(info);
		if (!string.IsNullOrEmpty(info.specialScriptName))
		{
			Type type = Type.GetType(info.specialScriptName);
			specialBehaviour = base.gameObject.AddComponent(type) as SpecialCardBehaviour;
		}
		else
		{
			specialBehaviour = null;
		}
	}

	public void SwitchToAlternatePortrait()
	{
		Displayer.SetPortrait(info.alternatePortraitTex);
	}

	public void SetIsOpponentCard()
	{
		Anim.FlipCardRenderer();
	}

	public bool CanAttackDirectly()
	{
		return Slot.opposingSlot.Card == null || Info.ability == SpecialAbility.Flying;
	}

	public void AddHealth(int amount)
	{
		health += amount;
		UpdateStatsText();
	}

	public IEnumerator Play()
	{
		if (specialBehaviour != null)
		{
			yield return StartCoroutine(specialBehaviour.OnPlayFromHand());
		}
	}

	public IEnumerator ResolveOnBoard()
	{
		if (specialBehaviour != null)
		{
			yield return StartCoroutine(specialBehaviour.OnResolveOnBoard());
		}
		if (Info.ability == SpecialAbility.DrawRabbits)
		{
			ViewManager.instance.SwitchToView(View.Hand);
			yield return new WaitForSeconds(0.5f);
			yield return StartCoroutine(PlayerHand.instance.Draw(Resources.Load<CardInfo>("Data/Cards/Rabbit")));
			yield return new WaitForSeconds(0.2f);
			yield return StartCoroutine(PlayerHand.instance.Draw(Resources.Load<CardInfo>("Data/Cards/Rabbit")));
		}
	}

	public IEnumerator OtherCardResolve(Card otherCard)
	{
		if (specialBehaviour != null)
		{
			yield return StartCoroutine(specialBehaviour.OnOtherCardResolve(otherCard));
		}
	}

	public IEnumerator OnSlotTargetedForAttack(Card otherCard)
	{
		if (specialBehaviour != null)
		{
			yield return StartCoroutine(specialBehaviour.OnSlotTargetedForAttack());
		}
	}

	public IEnumerator TakeDamage(int damage, Card attacker)
	{
		AudioController.Instance.PlaySound("die");
		health = Mathf.Max(health - damage, 0);
		if (health <= 0 || (attacker != null && attacker.Info.ability == SpecialAbility.Deathtouch))
		{
			Die();
		}
		UpdateStatsText();
		Anim.PlayHitAnimation();
		if (info.ability == SpecialAbility.BeesOnHit)
		{
			yield return new WaitForSeconds(0.25f);
			ViewManager.instance.SwitchToView(View.Hand);
			yield return new WaitForSeconds(0.3f);
			yield return StartCoroutine(PlayerHand.instance.Draw(Resources.Load<CardInfo>("Data/Cards/Bee")));
			yield return new WaitForSeconds(0.6f);
			ViewManager.instance.SwitchToView(View.Board);
			yield return new WaitForSeconds(0.3f);
		}
	}

	public IEnumerator DoPostAttackActions()
	{
		if (Info.ability == SpecialAbility.MoveAfterAttack)
		{
			CardSlot toLeft = BoardManager.instance.GetAdjacent(Slot, adjacentOnLeft: true);
			CardSlot toRight = BoardManager.instance.GetAdjacent(Slot, adjacentOnLeft: false);
			bool toLeftValid = toLeft != null && toLeft.Card == null;
			bool toRightValid = toRight != null && toRight.Card == null;
			if (movingLeft && !toLeftValid)
			{
				movingLeft = false;
			}
			if (!movingLeft && !toRightValid)
			{
				movingLeft = true;
			}
			CardSlot destination = ((!movingLeft) ? toRight : toLeft);
			bool destinationValid = ((!movingLeft) ? toRightValid : toLeftValid);
			Displayer.SetIconFlipped(movingLeft);
			if (destination != null && destinationValid)
			{
				ViewManager.instance.SwitchToView(View.Board);
				yield return new WaitForSeconds(0.25f);
				BoardManager.instance.AssignCardToSlot(this, destination);
				yield return new WaitForSeconds(0.25f);
			}
		}
	}

	public IEnumerator Sacrifice()
	{
		if (info.ability == SpecialAbility.Sacrificial)
		{
			Anim.SetMarkedForSacrifice(marked: false);
			Anim.PlaySacrificeParticles();
			if (specialBehaviour != null)
			{
				yield return StartCoroutine(specialBehaviour.OnSacrifice());
			}
		}
		else
		{
			if (specialBehaviour != null)
			{
				yield return StartCoroutine(specialBehaviour.OnSacrifice());
			}
			Die();
		}
	}

	public IEnumerator OnUpkeep()
	{
		NumTurnsInPlay++;
		if (info.ability == SpecialAbility.Evolve)
		{
			int turnsRemaining = Mathf.Max(1, info.abilityIntParameter - NumTurnsInPlay);
			Displayer.SetAbilityIcon(Resources.Load<Texture>("Art/Cards/AbilityIcons/ability_evolve_" + turnsRemaining));
			if (specialBehaviour != null && NumTurnsInPlay >= info.abilityIntParameter)
			{
				yield return StartCoroutine(TransformIntoCard(info.abilityCardParameter));
				yield return StartCoroutine(SceneSequencer.instance.OnCardTransform(this));
			}
		}
		if (specialBehaviour != null)
		{
			yield return StartCoroutine(specialBehaviour.OnUpkeep());
		}
	}

	public IEnumerator TransformIntoCard(CardInfo evolvedInfo)
	{
		ViewManager.instance.SwitchToView(View.Board);
		yield return new WaitForSeconds(0.15f);
		Anim.PlayTransformAnimation();
		yield return new WaitForSeconds(0.15f);
		SetInfo(evolvedInfo);
		yield return new WaitForSeconds(0.5f);
	}

	public void Die(bool playSound = true)
	{
		if (Slot != null)
		{
			Slot.Card = null;
		}
		Anim.PlayDeathAnimation(playSound);
		UnityEngine.Object.Destroy(base.gameObject, 2f);
	}

	private void UpdateStatsText()
	{
		Displayer.SetStatsText(Attack, health);
	}

	public override void OnCursorSelectStart()
	{
		if (PlayerHand.instance != null)
		{
			PlayerHand.instance.OnCardSelected(this);
		}
	}

	public override void OnCursorEnter()
	{
		if (PlayerHand.instance != null)
		{
			PlayerHand.instance.OnCardInspected(this);
		}
	}
}
