import { describe, test, expect } from "vitest";
import { render, screen } from '@testing-library/svelte';
import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';
import Header from './Header.svelte';
import logoDark from "$lib/assets/GitGudStats_logo_dark.svg";
import logoLight from "$lib/assets/GitGudStats_logo_light.svg";

// Mock para window.matchMedia, ahora en el propio test
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

describe('Header.svelte', () => {

  test('should render both the dark and light mode logos', () => {
    // Renderiza el componente Header
    render(Header);

    // Usa getAllByRole para obtener ambos logos
    const logos = screen.getAllByRole('img', { name: 'GitGudStats Logo' });

    // Verificamos que se rendericen dos logos.
    expect(logos).toHaveLength(2);

    // Verificamos los atributos de cada logo individualmente.
    expect(logos[0]).toHaveAttribute('src', logoDark);
    expect(logos[1]).toHaveAttribute('src', logoLight);
    
    // Verificamos que ambos estén en el documento.
    expect(logos[0]).toBeInTheDocument();
    expect(logos[1]).toBeInTheDocument();
  });
});