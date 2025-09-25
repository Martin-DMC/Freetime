import {describe,test,expect} from "vitest";
import {render,screen} from '@testing-library/svelte';
import Page from  './+page.svelte';
describe('/+page.svelte',()=>{
    test('should render h1',()=>{
        render(Page);
        expect(screen.getByRole('heading',{level:1})).toBeInTheDocument();
    })
    // Esta es la prueba corregida
    test('should render the h2 and the Counter component', () => {
        // 1. Renderizamos el componente
        render(Page);

        // 2. Verificamos que el h2 con el texto "try editing src/routes/+page.svelte" exista
        expect(screen.getByRole('heading', { level: 2, name: 'try editing src/routes/+page.svelte' })).toBeInTheDocument();
        
        // 3. Verificamos que el texto del contador esté presente, buscándolo por el rol de heading (si lo tuviera), o por texto dentro de un strong.
        // La mejor opción es buscar el texto "0" directamente en cualquier elemento.
        expect(screen.getByText('0')).toBeInTheDocument();

        // También podemos verificar la presencia de los botones de incremento y decremento
        expect(screen.getByRole('button', { name: 'Decrease the counter by one' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Increase the counter by one' })).toBeInTheDocument();
    });
})