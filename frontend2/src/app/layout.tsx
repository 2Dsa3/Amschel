import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'PymeRisk UI',
  description: 'Evaluación inteligente de riesgo para PYMEs'
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es" className="h-full">
      <body className="min-h-full bg-gray-50 text-gray-900 antialiased">
        <div className="mx-auto max-w-5xl p-6">
          <header className="mb-8 flex items-center justify-between">
            <h1 className="text-2xl font-bold">PymeRisk</h1>
            <span className="text-sm text-gray-500">MVP UI</span>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
