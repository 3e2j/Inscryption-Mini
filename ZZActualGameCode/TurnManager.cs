using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class TurnManager : MonoBehaviour
{
	public static TurnManager instance;

	public OpponentAI opponent { get; set; }

	public bool IsPlayerTurn { get; set; }

	public bool IsCombatPhase { get; set; }

	private void Awake()
	{
		instance = this;
	}

	private void Start()
	{
		StartCoroutine(GameSequence());
	}

	private void Update()
	{
		if (Input.GetKey(KeyCode.LeftShift) && Input.GetKeyDown(KeyCode.R))
		{
			SceneManager.LoadScene(SceneManager.GetActiveScene().name);
		}
	}

	private IEnumerator GameSequence()
	{
		if (GameStats.sceneProgress > 0)
		{
			AudioController.Instance.SetLoop("main_loop");
			AudioController.Instance.SetLoopVolume(0f);
			AudioController.Instance.FadeInLoop(0.2f, 0.75f);
		}
		yield return new WaitForEndOfFrame();
		if (SceneSequencer.instance == null)
		{
			yield break;
		}
		PlayerHand.instance.PlayingLocked = true;
		yield return StartCoroutine(SceneSequencer.instance.Intro());
		yield return new WaitForSeconds(0.5f);
		int startingHandSize = 3;
		for (int i = 0; i < startingHandSize; i++)
		{
			yield return StartCoroutine(PlayerHand.instance.Draw());
		}
		if (opponent.QueueFirstCardBeforePlayer)
		{
			opponent.QueueNewCards();
		}
		while (!GameHasEnded())
		{
			yield return StartCoroutine(PlayerTurn());
			if (GameHasEnded())
			{
				break;
			}
			yield return StartCoroutine(OpponentTurn());
		}
		AudioController.Instance.FadeOutLoop(0.5f);
		yield return StartCoroutine(SceneSequencer.instance.End(PlayerIsWinner()));
	}

	private IEnumerator PlayerTurn()
	{
		IsPlayerTurn = true;
		ViewManager.instance.LockState = ViewLockState.Locked;
		yield return StartCoroutine(DoUpkeepPhase(playerUpkeep: true));
		yield return StartCoroutine(SceneSequencer.instance.PlayerTurnStart());
		ViewManager.instance.SwitchToView(View.Default);
		StartCoroutine(SceneSequencer.instance.PlayerDuringTurn());
		yield return new WaitForSeconds(0.25f);
		if (PlayerHand.instance != null)
		{
			yield return StartCoroutine(PlayerHand.instance.Draw());
		}
		yield return new WaitForSeconds(0.25f);
		CombatBell.instance.Enabled = true;
		if (PlayerHand.instance != null)
		{
			PlayerHand.instance.PlayingLocked = false;
		}
		ViewManager.instance.LockState = ViewLockState.Unlocked;
		while (!CombatBell.instance.Rang)
		{
			if (GameHasEnded())
			{
				yield break;
			}
			yield return new WaitForEndOfFrame();
		}
		CombatBell.instance.Rang = false;
		yield return StartCoroutine(DoCombatPhase(playerIsAttacker: true));
	}

	private IEnumerator OpponentTurn()
	{
		IsPlayerTurn = false;
		if (PlayerHand.instance != null)
		{
			PlayerHand.instance.PlayingLocked = true;
		}
		ViewManager.instance.LockState = ViewLockState.Locked;
		yield return StartCoroutine(DoUpkeepPhase(playerUpkeep: false));
		ViewManager.instance.SwitchToView(View.Default);
		yield return StartCoroutine(SceneSequencer.instance.OpponentTurnStart());
		yield return new WaitForSeconds(0.5f);
		StartCoroutine(opponent.DoPlayPhase());
		yield return new WaitForSeconds(1f);
		yield return StartCoroutine(DoCombatPhase(playerIsAttacker: false));
	}

	private IEnumerator DoUpkeepPhase(bool playerUpkeep)
	{
		List<CardSlot> slots = ((!playerUpkeep) ? BoardManager.instance.OpponentSlots : BoardManager.instance.PlayerSlots);
		foreach (CardSlot slot in slots)
		{
			if (slot.Card != null)
			{
				yield return StartCoroutine(slot.Card.OnUpkeep());
			}
		}
	}

	private IEnumerator DoCombatPhase(bool playerIsAttacker)
	{
		CombatBell.instance.Enabled = false;
		IsCombatPhase = true;
		List<CardSlot> attackingSlots = ((!playerIsAttacker) ? BoardManager.instance.OpponentSlots : BoardManager.instance.PlayerSlots);
		attackingSlots.RemoveAll((CardSlot x) => x.Card == null || x.Card.Attack == 0);
		if (attackingSlots.Count > 0)
		{
			ViewManager.instance.SwitchToView(View.Board);
			ViewManager.instance.LockState = ViewLockState.Locked;
		}
		if (playerIsAttacker)
		{
			yield return StartCoroutine(SceneSequencer.instance.PlayerCombatStart());
		}
		else
		{
			yield return StartCoroutine(SceneSequencer.instance.OpponentCombatStart());
		}
		foreach (CardSlot item in attackingSlots)
		{
			item.Card.AttackedThisTurn = false;
		}
		int pooledAttackDamage = 0;
		foreach (CardSlot slot2 in attackingSlots)
		{
			ViewManager.instance.SwitchToView(View.Board);
			ViewManager.instance.LockState = ViewLockState.Locked;
			if (slot2.Card.AttackedThisTurn)
			{
				continue;
			}
			slot2.Card.AttackedThisTurn = true;
			yield return new WaitForSeconds(0.2f);
			if (slot2.Card.CanAttackDirectly())
			{
				slot2.Card.Anim.PlayAttackAnimation(attackPlayer: true);
				int nextSlotIndex = attackingSlots.IndexOf(slot2) + 1;
				bool nextSlotAlsoAttackingFace = nextSlotIndex < attackingSlots.Count && attackingSlots[nextSlotIndex].Card.CanAttackDirectly();
				pooledAttackDamage += slot2.Card.Attack;
				if (nextSlotAlsoAttackingFace)
				{
					yield return new WaitForSeconds(0.05f);
				}
				else
				{
					yield return new WaitForSeconds(0.3f);
					AudioController.Instance.PlaySound("die");
					yield return StartCoroutine(LifeManager.instance.ShowDamageSequence(pooledAttackDamage, !playerIsAttacker));
					pooledAttackDamage = 0;
				}
				if (GameHasEnded())
				{
					break;
				}
			}
			else
			{
				slot2.Card.Anim.PlayAttackAnimation(attackPlayer: false);
				yield return new WaitForSeconds(0.3f);
				slot2.Card.Anim.SetAnimationPaused(paused: true);
				yield return StartCoroutine(slot2.opposingSlot.Card.OnSlotTargetedForAttack(slot2.Card));
				slot2.Card.Anim.SetAnimationPaused(paused: false);
				yield return new WaitForSeconds(0.3f);
				yield return StartCoroutine(slot2.opposingSlot.Card.TakeDamage(slot2.Card.Attack, slot2.Card));
			}
		}
		foreach (CardSlot slot in attackingSlots)
		{
			if (slot.Card != null)
			{
				yield return StartCoroutine(slot.Card.DoPostAttackActions());
			}
		}
		if (playerIsAttacker)
		{
			yield return StartCoroutine(SceneSequencer.instance.PlayerCombatEnd());
		}
		else
		{
			yield return StartCoroutine(SceneSequencer.instance.OpponentCombatEnd());
		}
		IsCombatPhase = false;
		ViewManager.instance.LockState = ViewLockState.Unlocked;
		yield return new WaitForSeconds(0.5f);
	}

	private bool PlayerIsWinner()
	{
		return LifeManager.instance.Balance >= 5;
	}

	private bool GameHasEnded()
	{
		return Mathf.Abs(LifeManager.instance.Balance) >= 5;
	}
}
