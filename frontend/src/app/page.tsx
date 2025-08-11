import SocialInput from '../components/SocialInput';

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section>
        <h2 className="text-xl font-semibold mb-2">Red Social de la Empresa</h2>
  <p className="text-sm text-gray-600 mb-4">Ingresa SOLO la URL completa (https://...) de la red social principal de la empresa.</p>
        <SocialInput />
      </section>
    </div>
  );
}
