import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from "vitest/config";
import {svelteTesting} from "@testing-library/svelte/vite";

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		proxy: {
			'/api': {
				target: 'http://localhost/8000',
				changeOrigin: true,
				secure: false
			}
		}
	},
	test: {
        // global test settings that are not workspace dependant
        globals: true,
        coverage:{
            provider:'v8',
            include:['src/**/*.{svelte,js,ts}']
        },
        // workspace settings
        projects:[
            {
                extends: true,
                plugins:[svelteTesting()],
                test:{
                    name:"client",
                    environment:'jsdom',
                    clearMocks: true,
                    include:["src/**/*.svelte.{test,spec}.{js,ts}"],
                    exclude:["src/lib/server/**"],
                    setupFiles:['./vitest-setup-client.ts']
                }
            },
            {
                extends: true,
                test:{
                    name:"server",
                    environment: "node",
                    include:["src/**/*.{test,spec}.{js,ts}"],
                    exclude:["src/**/*.svelte.{test,spec}.{js,ts}"]
                }
            },
        ]
    }
});