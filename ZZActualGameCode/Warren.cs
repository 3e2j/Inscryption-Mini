using System.Collections;
using UnityEngine;

public class Warren : SpecialCardBehaviour
{
	public override IEnumerator OnSacrifice()
	{
		if (BoardManager.instance.CurrentCardToPlay.Info.HasTrait(Trait.EatsWarrens))
		{
			base.Card.Anim.SetMarkedForSacrifice(marked: false, playSound: false);
			for (int i = 0; i < 3; i++)
			{
				base.Card.Displayer.SetPortrait(Resources.Load<Texture>("Art/Cards/Portraits/portrait_warren_eaten" + (i + 1)));
				GetComponent<Animator>().SetTrigger("sacrifice_selected");
				yield return new WaitForSeconds(0.4f);
			}
		}
	}
}
