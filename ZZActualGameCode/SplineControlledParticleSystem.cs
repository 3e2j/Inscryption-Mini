using Pixelplacement;
using UnityEngine;

[ExecuteInEditMode]
[RequireComponent(typeof(Spline))]
public class SplineControlledParticleSystem : MonoBehaviour
{
	public float startRadius;

	public float endRadius;

	[SerializeField]
	private ParticleSystem _particleSystem;

	private Spline _spline;

	private ParticleSystem.Particle[] _particles;

	private const float _prviousDiff = 0.01f;

	private void Awake()
	{
		_spline = GetComponent<Spline>();
	}

	private void LateUpdate()
	{
		if (_particleSystem == null)
		{
			return;
		}
		if (_particles == null)
		{
			_particles = new ParticleSystem.Particle[_particleSystem.main.maxParticles];
		}
		int particles = _particleSystem.GetParticles(_particles);
		for (int i = 0; i < particles; i++)
		{
			float num = Mathf.Pow(10f, _particles[i].randomSeed.ToString().Length);
			float num2 = (float)_particles[i].randomSeed / num;
			float num3 = 1f - _particles[i].remainingLifetime / _particles[i].startLifetime;
			if (!(_spline.GetDirection(num3) == Vector3.zero))
			{
				Vector3 vector = Quaternion.AngleAxis(1080f * num2, -_spline.GetDirection(num3)) * _spline.Up(num3);
				Vector3 vector2 = Quaternion.AngleAxis(1080f * num2, -_spline.GetDirection(num3 - 0.01f)) * _spline.Up(num3 - 0.01f);
				Vector3 position = _spline.GetPosition(num3);
				Vector3 vector3 = position;
				if (num3 - 0.01f >= 0f)
				{
					vector3 = _spline.GetPosition(num3 - 0.01f);
				}
				float num4 = Mathf.Lerp(startRadius, endRadius, num3);
				float num5 = Mathf.Lerp(startRadius, endRadius, num3 - 0.01f);
				Vector3 vector4 = Vector3.zero;
				Vector3 vector5 = Vector3.zero;
				switch (_particleSystem.main.simulationSpace)
				{
				case ParticleSystemSimulationSpace.Local:
					vector4 = _particleSystem.transform.InverseTransformPoint(position + vector * num4);
					vector5 = _particleSystem.transform.InverseTransformPoint(vector3 + vector2 * num5);
					break;
				case ParticleSystemSimulationSpace.World:
				case ParticleSystemSimulationSpace.Custom:
					vector4 = position + vector * num4;
					vector5 = position + vector2 * num5;
					break;
				}
				_particles[i].position = vector4;
				_particles[i].velocity = vector4 - vector5;
			}
		}
		_particleSystem.SetParticles(_particles, _particles.Length);
	}
}
