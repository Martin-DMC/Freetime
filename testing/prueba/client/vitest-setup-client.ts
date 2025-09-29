import '@testing-library/jest-dom/vitest'
import {vi} from 'vitest';

// required for svelte5 + jsdom as jsdom does not support matchMedia
Object.defineProperty(window, 'matchMedia', {
    writable: true,
    enumerable: true,
    value: vi.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
    })),
})

// add more mocks here if you need them

// Mock global de animate para JSDOM
if (!Element.prototype.animate) {
  Element.prototype.animate = () => ({
    finished: Promise.resolve(),
    cancel: () => {},
    play: () => {},
    pause: () => {},
    reverse: () => {},
    commitStyles: () => {}
  }) as unknown as Animation;
}