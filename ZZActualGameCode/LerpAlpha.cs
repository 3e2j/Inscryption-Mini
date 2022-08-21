using UnityEngine;

public class LerpAlpha : MonoBehaviour
{
	public float speed = 2.5f;

	public float intendedAlpha;

	private SpriteRenderer sR;

	private TextMesh tM;

	private void Awake()
	{
		sR = GetComponent<SpriteRenderer>();
		tM = GetComponent<TextMesh>();
	}

	private void Update()
	{
		Color color = GetColor();
		Color color2 = new Color(color.r, color.g, color.b, Mathf.Lerp(color.a, intendedAlpha, Time.deltaTime * speed));
		SetColor(color2);
	}

	public Color GetColor()
	{
		if ((bool)sR)
		{
			return sR.color;
		}
		if ((bool)tM)
		{
			return tM.color;
		}
		return Color.black;
	}

	public void SetColor(Color c)
	{
		if ((bool)sR)
		{
			sR.color = c;
		}
		else if ((bool)tM)
		{
			tM.color = c;
		}
	}
}
